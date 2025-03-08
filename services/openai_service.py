import openai

class OpenAIService:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
        
    def generate_summary(self, text):
        """
        Generate a medical record summary using OpenAI
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a medical professional assistant. Summarize the following medical record information concisely and accurately. Include key diagnoses, treatments, medications, and important clinical findings."},
                    {"role": "user", "content": text}
                ],
                max_tokens=500,
                temperature=0.3
            )
            return {
                "summary": response.choices[0].message["content"],
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
