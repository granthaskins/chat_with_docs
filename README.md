# Chat with PDF

This project allows you to interact with PDF documents using GPT 3.5 Turbo (or another model of your choice). The script extracts text from PDF files and uses OpenAI's GPT 3.5 Turbo (or another model of your choice) to generate summaries or interact with the content. 

## Features

- Extract text from PDF files.
- Use GPT 3.5 Turbo (or another model of your choice) to generate summaries or interact with the extracted text.
- Handle encrypted PDFs (requires `PyCryptodome`).

## Requirements

- Python 3.8 or higher
- PyPDF2
- OpenAI
- PyCryptodome (for handling encrypted PDFs)
- OCR functionality (requires installation of both poppler and tesseract)

## Installation

1. Clone the repository or download the script:

    ```sh
    git clone https://github.com/granthaskins/chat_with_docs.git
    cd chat_with_docs
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Place your files in the same directory as the script or specify the path to the PDF file.

2. Run the script with your OpenAI API key as an argument:

    ```sh
    python chat_with_pdf.py --api_key <your-api-key> --pdf_path <path-to-dir>
    ```

3. The script will extract text from the PDF, interact with GPT 3.5 Turbo (or another model of your choice), and print the summary or response.

