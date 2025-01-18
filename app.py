


import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai  # OpenAI Python SDK
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for the frontend to communicate with Flask

# Set up the OpenAI client with the local server and API key
openai.api_base = "http://localhost:1234/v1"  # Your local server URL
openai.api_key = "lm-studio"  # Your API key for LM Studio

# Ensure the upload directory exists
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    print("Starting PDF upload process...")

    if 'pdf' not in request.files:
        print("No 'pdf' key in uploaded files.")
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        print("No file selected for upload.")
        return jsonify({"error": "No selected file"}), 400

    # Save the file temporarily
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    print(f"Saving uploaded file to: {pdf_path}")
    pdf_file.save(pdf_path)

    # Extract text from PDF using PyMuPDF
    try:
        print(f"Opening PDF file: {pdf_path}")
        doc = fitz.open(pdf_path)
        pages_text = []

        # Loop through each page and extract text
        for page_num in range(len(doc)):
            print(f"Processing page {page_num + 1}/{len(doc)}...")
            page = doc.load_page(page_num)
            page_text = page.get_text("text")  # Extract text as-is
            pages_text.append(page_text)  # Store text for each page

        print("PDF text extraction completed successfully.")
        return jsonify({"pages": pages_text})

    except Exception as e:
        print(f"Error during PDF processing: {e}")
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

@app.route('/saveSelectedText', methods=['POST'])
def save_selected_text():
    print("Starting text processing with LM Studio...")
    selected_text = request.json.get('text')
    print(f"Received text for processing: {selected_text}")
    
    if not selected_text:
        print("No text provided in the request.")
        return jsonify({"error": "No selected text provided"}), 400

    try:
        print("Sending text to LM Studio for processing...")
        completion = openai.ChatCompletion.create(
            model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",  # Verify this with LM Studio
            messages=[
                {"role": "system", "content": "Explain in 20 words."},
                {"role": "user", "content": selected_text}
            ],
            temperature=0.7,
        )
        print("Received response from LM Studio.")

        # Extract and return the response from the model
        response_message = completion.choices[0].message['content']
        print(f"Model response: {response_message}")
        return jsonify({"message": "Selected text processed successfully", "response": response_message})
    
    except Exception as e:
        print(f"Error during LM Studio processing: {e}")
        return jsonify({"error": f"Error processing the text: {str(e)}"}), 500


if __name__ == '__main__':
    print("Starting Flask app in debug mode...")
    app.run(debug=True)
