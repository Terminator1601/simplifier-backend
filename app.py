




# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import fitz  # PyMuPDF

# app = Flask(__name__)
# CORS(app)  # Enable CORS for the frontend to communicate with Flask

# @app.route('/upload', methods=['POST'])
# def upload_pdf():
#     if 'pdf' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     pdf_file = request.files['pdf']
#     if pdf_file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     # Save the file temporarily
#     pdf_path = './uploads/' + pdf_file.filename
#     pdf_file.save(pdf_path)

#     # Extract text from PDF using PyMuPDF
#     doc = fitz.open(pdf_path)
#     extracted_text = ""

#     # Loop through each page and extract text
#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
#         page_text = page.get_text("text")  # Extract text as-is
#         extracted_text += page_text + "\n"  # Ensure newlines between pages

#     return jsonify({"text": extracted_text})

# if __name__ == '__main__':
#     app.run(debug=True)








from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)  # Enable CORS for the frontend to communicate with Flask

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file temporarily
    pdf_path = './uploads/' + pdf_file.filename
    pdf_file.save(pdf_path)

    # Extract text from PDF using PyMuPDF
    doc = fitz.open(pdf_path)
    pages_text = []

    # Loop through each page and extract text
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text("text")  # Extract text as-is
        pages_text.append(page_text)  # Store text for each page

    return jsonify({"pages": pages_text})

if __name__ == '__main__':
    app.run(debug=True)
