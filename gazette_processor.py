import anthropic
import base64
from pathlib import Path
import json
from typing import List, Dict
import fitz  # PyMuPDF
from PIL import Image
import io
import os

class GazetteProcessor:
    def __init__(self, api_key: str):
        """Initialize the processor with Anthropic API key"""
        self.client = anthropic.Anthropic(api_key=api_key)
        
        #Create Prompt
        self.extraction_prompt = """
        Analyze this Belgian Official Gazette document ("Bijlagen bij het Belgisch Staatsblad - Annexes du Moniteur belge").
        Extract information and provide BOTH original language and English translation.
        Return ONLY a JSON object with this structure:

        {
            "original": {
                "Language": "Language which the document is in"
                "Company Name": "full legal company name (keep in original language)",
                "Company Identifier": "business registration number",
                "Document Purpose": {
                    "Key terms": "main purpose of document in original language",
                    "Additional Information": {
                        // All relevant details in original language
                    }
                }
            },
            "english": {
                "Company Name": "same as original - do not translate proper names",
                "Company Identifier": "same as original - do not translate identifiers",
                "Document Purpose": {
                    "Key terms": "main purpose translated to English",
                    "Additional Information": {
                        // All relevant details translated to English
                    }
                }
            }
        }

        Important Notes:
        1. Keep company names, identifiers, and reference numbers IDENTICAL in both versions
        2. For the original version, maintain text in document's language (FR/NL/DE)
        3. Translate all descriptive content to English in the 'english' version
        4. Include all relevant information based on document type:
           - For appointments: position, dates, person names
           - For modifications: type of change, effective date
           - For other purposes: all relevant context and details
        5. Ensure professional and accurate translations
        """

    def pdf_to_images(self, pdf_path: str) -> List[Dict]:
        """Convert PDF pages to images and return list of base64 encoded images"""
        images_data = []
        #Open File
        pdf_document = fitz.open(pdf_path)
        
        #Convert each PDF to images with fitz
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr = img_byte_arr.getvalue()
            base64_encoded = base64.b64encode(img_byte_arr).decode('utf-8')
            
            #Add Encoded data for each page in preparation for LLM
            images_data.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_encoded
                }
            })
        
        pdf_document.close()
        return images_data

    def process_document(self, pdf_path: str) -> Dict:
        """Process entire PDF document with all pages in single API call"""
        try:
            #Convert PDF to images
            images_data = self.pdf_to_images(pdf_path)
            
            # Add image data and prompt to the Sonnet API call
            content = images_data + [
                {
                    "type": "text",
                    "text": self.extraction_prompt
                }
            ]
            
            #Create Sonnet Message using latest model
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )
            
            try:
                # converts this text string into a Python dictionary
                extracted_info = json.loads(message.content[0].text) 
                # Create the JSON structure
                result = {
                    "filename": Path(pdf_path).name,
                    "extracted_data": extracted_info
                }               
                return result
                
            except json.JSONDecodeError:
                return {
                    "filename": Path(pdf_path).name,
                    "status": "error",
                    "error": "Failed to parse JSON response",
                    "raw_response": message.content[0].text
                }
            
        except Exception as e:
            return {
                "filename": Path(pdf_path).name,
                "status": "error",
                "error": str(e)
            }

    def process_directory(self, directory_path: str) -> List[Dict]:
        """Process all PDF files in a directory"""
        results = []
        #Finds pdf in directory and converts them to a list
        pdf_files = list(Path(directory_path).glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {directory_path}")
            return results
        
        print(f"Found {len(pdf_files)} PDF files to process")
        
        #Process each file and add it to 'result'
        for pdf_path in pdf_files:
            print(f"Processing {pdf_path.name}...")
            result = self.process_document(str(pdf_path))
            results.append(result)
            print(f"Completed processing {pdf_path.name}")
        
        return results

def main():
    #Replace with your Anthropic API key
    ANTHROPIC_API_KEY = "your-api-key-here"
    
    # Directory containing your PDF files (Replace with your directory and keep format i.e. r"Path")
    PDF_DIR = r"C:\Users\Nabil\Downloads\BE_GAZETTE_PDFS"
    
    # Output file paths
    OUTPUT_FILE  = f"{PDF_DIR}\extracted_gazette_info.json"
    
    # Initialize processor
    processor = GazetteProcessor(ANTHROPIC_API_KEY)
    
    # Process all documents
    results = processor.process_directory(PDF_DIR)
    
    # Save results directly to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"results": results}, f, indent=2, ensure_ascii=False)
    
    # Print simple completion message
    print(f"Processing complete. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
