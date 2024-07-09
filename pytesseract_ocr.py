import os
import argparse
import pytesseract
from pdf2image import convert_from_path

def path2txt(fp):
    f_ext = os.path.splitext(fp)[1].lower()
    
    if f_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        return image_to_text(fp)
    elif f_ext == '.pdf':
        return pdf_to_text(fp)
    else:
        raise ValueError(f"Unsupported file type: {f_ext}")

def image_to_text(fp):
    try:
        img = Image.open(fp)
        text = pytesseract.image_to_string(img)
        return [text]
    except Exception as e:
        raise ValueError(f"Error processing image file '{fp}': {e}")

def pdf_to_text(fp):
    try:
        imgs = convert_from_path(fp)
        texts = [pytesseract.image_to_string(img) for img in imgs]
        return texts
    except Exception as e:
        raise ValueError(f"Error processing PDF file '{fp}': {e}")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str)

    txt = path2txt(args.file_path)

    with open(os.path.splitext(args.file_path)[0]+'.txt', 'w') as f:
        f.write(txt)





