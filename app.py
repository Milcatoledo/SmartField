import os
import uuid
from models import predict
import base64
from flask import Flask, render_template, request
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Base directory: {BASE_DIR}")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"Upload folder created at: {UPLOAD_FOLDER}")


def save_image_file(image_file, upload_folder=UPLOAD_FOLDER):
    filename = image_file.filename
    save_path = os.path.join(upload_folder, filename)
    image_file.save(save_path)
    return save_path


def save_base64_image(base64_string, upload_folder=UPLOAD_FOLDER):
    if not base64_string.startswith("data:image/"):
        raise ValueError("Invalid base64 image string")

    header, encoded = base64_string.split(",", 1)
    file_extension = header.split(";")[0].split("/")[1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    save_path = os.path.join(upload_folder, filename)

    with open(save_path, "wb") as f:
        f.write(base64.b64decode(encoded))

    return save_path


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/selectSource")
def source():
    return render_template("selectSource.html")


@app.route("/analysis", defaults={"source": "gallery"})
@app.route("/analysis/<string:source>", methods=["GET", "POST"])
def analysis(source):
    if request.method == "POST":
        model_name = request.form.get("model")
        image = request.files.get("photo")
        camera = request.form.get("camera")
        if not model_name or (not image and not camera):
            return render_template("analysis.html",
                                   error="Model and photo are required."
                                   )
        try:
            if image and image.filename:
                save_path = save_image_file(image)
            else:
                save_path = save_base64_image(camera)
                # NOTE: el nuevo funcionamiento de camara no esta probado
            category, percentages, model_name = predict(model_name, save_path)

            return render_template("analysis.html",
                                   source="gallery",
                                   category=category,
                                   percentages=percentages,
                                   model_name=model_name
                                   )

        except Exception as e:
            print(f"Error processing image: {e}")
            return render_template("analysis.html", error=f"error: {e}")
    else:
        source = request.view_args.get("source") if hasattr(
            request, 'view_args') else None
        if source:
            return render_template("analysis.html", source=source)
        return render_template("analysis.html")


if __name__ == "__main__":
    app.run(debug=True)
