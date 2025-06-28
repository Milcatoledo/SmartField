from models import predict
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
        photo = request.files.get("photo")
        if not model_name or not photo:
            return render_template("analysis.html", error="Model and photo are required.")
        try:
            category, percentages, model_name = predict(model_name, photo.read())
            return render_template("analysis.html", source="gallery", category=category, percentages=percentages, model_name=model_name)

        except Exception as e:
            print(f"Error processing image: {e}")
            return render_template("analysis.html", error=f"{e}")
    else:
        # GET request: solo muestra la página sin resultados
        source = request.view_args.get("source") if hasattr(request, 'view_args') else None
        if source:
            return render_template("analysis.html", source=source)
        return render_template("analysis.html")


if __name__ == "__main__":
    app.run(debug=True)
