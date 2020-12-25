from flask import Flask, request, redirect, send_file, render_template, url_for
from Algorithm import Compress_Wrapper as comp
from werkzeug.utils import secure_filename
from pathlib import Path
from os.path import join

UPLOAD_FOLDER = "uploads/"
OUTPUT_FOLDER = "output/"
SUPPORTED_EXTENSIONS = {'lz77','lzw'}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

@app.route("/")
@app.route("/compress", methods=["GET", "POST"])
def compress_upload():
    if request.method == "POST":
        file = request.files["file"]
        if "file" not in request.files:
            print("No file")
            return redirect(request.url)
        if file.filename == '':
            print("No filename")
            return redirect(request.url)
        else:
            output_name = ""
            filename = secure_filename(file.filename)
            file.save(join(app.config["UPLOAD_FOLDER"], filename))
            old_file_size = Path(join(app.config["UPLOAD_FOLDER"], filename)).stat().st_size
            print("Saved file successfully")
            print("Processing")
            
            algorithm = str(request.form.get("algorithms"))
            print(algorithm)
            # TODO : Get compress_wrapper to raw and implement algorithm selects
            if(algorithm == "LZ77"):
                output_name = comp.LZ77_compress(UPLOAD_FOLDER + filename)
            elif(algorithm == "LZW"):
                output_name = comp.LZW_compress(UPLOAD_FOLDER + filename)
            else:
                print("Algorithm not found")
            # Check algorithm here  
            # output_name = LZ77.run_compress(UPLOAD_FOLDER + filename)
            # Block here
            print(output_name)
            new_file_size = Path(join(app.config["OUTPUT_FOLDER"], output_name)).stat().st_size
            compression_rate = 100 - round(((new_file_size / old_file_size) * 100), 2)
            return render_template("compress.html", output_name=output_name, old_file_size = old_file_size, new_file_size = new_file_size, compression_rate = compression_rate)
    return render_template("compress.html")

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
            output_name = ""
            filename = secure_filename(file.filename)
            extension = filename.split('.')[1]
            alert_message = ""

            file.save(join(app.config["UPLOAD_FOLDER"], filename))
            old_file_size = Path(join(app.config["UPLOAD_FOLDER"], filename)).stat().st_size
    
            # TODO : check extension and do appropriate function
            if extension in SUPPORTED_EXTENSIONS:
                if(extension == "lz77"):
                    output_name = comp.LZ77_decompress(UPLOAD_FOLDER + filename)
                elif(extension == "lzw"):
                    output_name = comp.LZW_decompress(UPLOAD_FOLDER + filename)
            else:
                pass
            output_name = output_name
            new_file_size = Path(join(app.config["OUTPUT_FOLDER"], output_name)).stat().st_size
            decompression_rate = 100 - round(((old_file_size / new_file_size) * 100), 2)
    
            print("Saved file successfully")
            return render_template("Decompress2.html" , output_name = output_name, new_file_size = new_file_size, old_file_size = old_file_size, decompression_rate = decompression_rate)
    return render_template("Decompress2.html")

@app.route("/return-files/<filename>")
def return_files(filename):
    file_path = Path(join(app.config["OUTPUT_FOLDER"], filename))
    return send_file(file_path, as_attachment = True, attachment_filename='')

if __name__ == "__main__":
    app.run(debug=True)