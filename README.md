# Belgian Gazette Document Processor

## Description
This Python application processes Belgian Official Gazette documents (PDFs) using Claude 3.5 Sonnet API to extract business information and provide translations. The solution converts PDFs to high-quality images, processes them through Claude's vision capabilities, and outputs structured data in JSON format, including both original language content and English translations.

## Prerequisites
- Python 3.8 or higher
- Anthropic API key
- PDF files from Belgian Gazette

## Installation and Setup

### Setting up Virtual Environment

#### Windows
```batch
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Deactivating Virtual Environment
When you're done:
- Windows: `deactivate`
- macOS/Linux: `deactivate`

### Configuration
Open the script and modify these variables:

#### Windows Path Format
```python
ANTHROPIC_API_KEY = "your-api-key-here"
PDF_DIR = r"C:\path\to\your\pdf\directory"
```

#### macOS/Linux Path Format
```python
ANTHROPIC_API_KEY = "your-api-key-here"
PDF_DIR = "/path/to/your/pdf/directory"
```

## How to Run

### Windows
```batch
# Activate virtual environment if not already activated
venv\Scripts\activate

# Run the script
python gazette_processor.py
```

### macOS/Linux
```bash
# Activate virtual environment if not already activated
source venv/bin/activate

# Run the script
python3 gazette_processor.py
```

## Output
Results are saved in `extracted_gazette_info.json` with this structure:
```json
{
    "results": [
        {
            "filename": "document.pdf",
            "extracted_data": {
                "original": {
                    "Language": "...",
                    "Company Name": "...",
                    "Company Identifier": "...",
                    "Document Purpose": {
                        "Key terms": "...",
                        "Additional Information": {}
                    }
                },
                "english": {
                    "Company Name": "...",
                    "Company Identifier": "...",
                    "Document Purpose": {
                        "Key terms": "...",
                        "Additional Information": {}
                    }
                }
            }
        }
    ]
}
```

## Project Structure
```
.
├── venv/                  # Virtual environment directory
├── gazette_processor.py   # Main script
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## Troubleshooting

### Common Issues
1. API Key Issues:
   - Verify API key is valid
   - Check API key permissions

2. PDF Processing Issues:
   - Ensure PDFs are not corrupted
   - Check file permissions
   - Verify PDF is readable

3. Output Issues:
   - Check disk space
   - Verify write permissions in output directory

## Environment-Specific Notes

### Windows
- Use backslashes (\) or raw strings (r"path") for file paths
- May require administrator privileges for certain directories
- Check Windows Defender if facing file access issues

### macOS/Linux
- Use forward slashes (/) for file paths
- May require `sudo` for certain directories
- Check file permissions with `ls -la`

## Limitations
- Requires valid Anthropic API key
- PDF quality affects extraction accuracy
- API rate limits may apply
- Maximum token limits for large documents
