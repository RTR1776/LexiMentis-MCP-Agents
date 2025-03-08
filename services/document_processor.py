class DocumentProcessor:
    def __init__(self, openai_service, ocr_service):
        self.openai_service = openai_service
        self.ocr_service = ocr_service
    
    def process(self, file):
        """
        Process document through OCR and generate summary
        """
        # Step 1: Extract text using OCR
        ocr_result = self.ocr_service.extract_text(file)
        
        if not ocr_result["success"]:
            return {
                "error": f"OCR processing failed: {ocr_result.get('error', 'Unknown error')}",
                "success": False
            }
        
        extracted_text = ocr_result["text"]
        
        # Step 2: Generate summary using OpenAI
        summary_result = self.openai_service.generate_summary(extracted_text)
        
        if not summary_result["success"]:
            return {
                "error": f"Summary generation failed: {summary_result.get('error', 'Unknown error')}",
                "success": False
            }
        
        # Return both the extracted text and the summary
        return {
            "extracted_text": extracted_text,
            "summary": summary_result["summary"],
            "success": True
        }
