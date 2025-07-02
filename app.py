from models import predict
from io import BytesIO
from PIL import Image
import base64
from flask import Flask, render_template, request
app = Flask(__name__)


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
            if image:
                image_data = image.read()
            elif camera and camera.startswith("data:image"):
                header, encoded = camera.split(",", 1)
                camera = base64.b64decode(encoded)
                camera = BytesIO(camera)
                image_data = Image.open(camera).convert('RGB')
                print(f"Image type: {type(image)}")
            category, percentages, model_name = predict(
                model_name, image_data)
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
