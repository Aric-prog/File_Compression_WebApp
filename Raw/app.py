from flask import Flask, request, redirect, send_file, render_template, url_for
from werkzeug.utils import secure_filename
from os.path import join
from LZ77_Final import LZ77

UPLOAD_FOLDER = "uploads/"
LZ77 = LZ77()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/compress", methods=["GET", "POST"])
def compress_upload(done = False):
    if request.method == "POST":
        if "file" not in request.files:
            print("No file")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == '':
            print("No filename")
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(join(app.config["UPLOAD_FOLDER"], filename))
            print("Saved file successfully")
            print("Processing")
            # Check algorithm here  
            output_name = LZ77.run_compress(UPLOAD_FOLDER + filename)
            # Block here
            return render_template("compress.html", done = True, output_name=output_name)
    return render_template("compress.html", done=done)

@app.route("/decompress", methods=["GET", "POST"])
def decompress_upload():
    if request.method == "POST":
        if "file" not in request.files:
            print("no file")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == '':
            print("No filename")
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(join(app.config["UPLOAD_FOLDER"], filename))

            print("Saved file successfully")
            return render_template("decompress.html", done = True)
    return render_template("decompress.html",done = False)

@app.route("/return-files/<filename>")
def return_files(filename):
    file_path = filename
    return send_file(file_path, as_attachment = True, attachment_filename='')

if __name__ == "__main__":
    app.run(debug=True)