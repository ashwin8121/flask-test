import os.path
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from glob import glob
# from langchain.embeddings.ollama import OllamaEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.llms import ollama

app = Flask(__name__, template_folder="templates")
app.config["FILESFOLDER"] = "uploadfiles"
app.secret_key = "kerwfvbqkjwehrfvjqehrfvjwkerhvf"

ALLOWED_EXTENSIONS = {"pdf", "txt"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

fileslist = []

@app.route("/", methods=["GET"])
def index():
    global fileslist
    files = enumerate(fileslist, start=1)
    return render_template("index.html", files=files)

@app.route("/uploadfile", methods=["GET", "POST"])
def uploadFile():
    if request.method == "GET":
        return render_template("uploadfile.html")
    if request.method == "POST":
        global fileslist
        if 'file' not in request.files:
            print("No files selected")
            flash("No File selected")
            return redirect(url_for("index"))
        file = request.files['file']
        if file.filename == '':
            return "No File Selected"
        filename = secure_filename(file.filename)
        fileslist.append(filename)
        file.save(os.path.join(app.config["FILESFOLDER"], filename))
        return redirect(url_for("index"))


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)