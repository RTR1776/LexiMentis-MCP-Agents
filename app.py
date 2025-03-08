from flask import Flask, request, jsonify
from services.openai_service import OpenAIService
from services.ocr_service import OCRService
from services.document_processor import DocumentProcessor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize services
openai_service = OpenAIService(api_key=os.getenv('OPENAI_API_KEY'))
ocr_service = OCRService()
document_processor = DocumentProcessor(openai_service, ocr_service)

@app.route('/api/process_document', methods=['POST'])
def process_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    result = document_processor.process(file)
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True)
