import argparse
import os
from tqdm import tqdm
import PyPDF2
import openai
import pypandoc
from docx import Document

from pytesseract_ocr import path2txt

class PDFChat(object):

    def __init__(self, OPENAI_API_KEY, doc_dir, 
                        model_name, system_prompts, 
                                    max_tokens=1000):

        self.doc_dir = doc_dir
        self.model_name = model_name
        self.system_prompts = system_prompts
        self.max_tokens = max_tokens

        openai.api_key = OPENAI_API_KEY

    def ingest_pdf(self, doc_path, messages):

        try:

            pdf_file_obj = open(doc_path, "rb")
            pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
            num_pages = pdf_reader.numPages

            for page in tqdm(range(num_pages), desc='Analyzing '+doc_path.split('/')[-1]):

                page_obj = pdf_reader.getPage(page)
                page_text = page_obj.extractText() 

                messages = self.summarize_page_text(messages, page_text, doc_path, page)

            pdf_file_obj.close()

        except:

            messages = self.ingest_doc_ocr(doc_path, messages)

        return messages

    def ingest_txt_file(self, doc_path, messages):

        for _ in tqdm(range(1), desc='Analyzing '+doc_path.split('/')[-1]):

            with open(doc_path, 'r') as f:
                doc_text = f.read()

        return self.summarize_page_text(messages, doc_text, doc_path, 0)

    def ingest_doc_ocr(self, doc_path, messages):
        
        page_texts = path2txt(doc_path)
        page = 0

        for page_text in tqdm(page_texts, desc='Analyzing '+doc_path.split('/')[-1]):

            messages = self.summarize_page_text(messages, page_text, doc_path, page)

            page += 1

        return messages

    def ingest_word_doc(self, doc_path, messages):

        doc = Document(doc_path)

        page = 0

        for paragraph in tqdm(doc.paragraphs, desc='Analyzing '+doc_path.split('/')[-1]):

            messages = self.summarize_page_text(messages, paragraph.text, doc_path, page)
            page += 1

        return messages

    def summarize_page_text(self, messages, page_text, doc_path, page):

        user_dict = {"role": "user", "content": page_text}
        messages.append(user_dict)
        
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            max_tokens=self.max_tokens
        ).choices[0].message['content']
        
        messages.pop()
        user_dict = {"role": "user", "content": "Summarize "+doc_path.split('/')[-1].split('.')[0]+" page {}".format(page)}
        assistant_dict = {"role": "assistant", "content": response}
        messages.append(user_dict)
        messages.append(assistant_dict)

        return messages

    def ingest_docs(self):

        messages = [{"role":"system", "content": self.system_prompts[0]}]

        fns = os.listdir(self.doc_dir)

        for fn in fns:

            if fn == '.DS_Store':
                continue

            ingested_f_ext = os.path.splitext(fn)[1].lower()

            if ingested_f_ext == '.pdf':

                messages = self.ingest_pdf(os.path.join(self.doc_dir,fn), messages)

            elif ingested_f_ext in ['.doc','.docx']:
                
                docx_fp = os.path.join(self.doc_dir,fn)

                if ingested_f_ext == '.doc':

                    docx_fp = os.path.join(self.doc_dir,os.path.splitext(file_path)[0]+'.docx')
                    pypandoc.convert_file(os.path.join(self.doc_dir,fn), 'docx', outputfile=docx_fp)
                
                messages = self.ingest_word_doc(docx_fp, messages)

            elif ingested_f_ext == '.txt':

                messages = self.ingest_txt_file(os.path.join(self.doc_dir,fn), messages)

            else:

                messages = self.ingest_doc_ocr(os.path.join(self.doc_dir,fn), messages)

        return messages

    def initiate_chatgpt(self, messages):

        system_dict = {"role": "system", "content": self.system_prompts[1]}
        messages.append(system_dict)

        while True:

            query = input('Question: ')

            if query in 'QqQUITQuitquitESCEscesc':

                break

            user_dict = {"role": "user", "content": query}
            messages.append(user_dict)
            
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens
            ).choices[0].message['content']

            print(self.model_name+': '+response)
            assistant_dict = {"role": "assistant", "content": response}
        
            messages.append(assistant_dict)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--OPENAI_API_KEY', type=str)
    parser.add_argument('--doc_dir', type=str)
    parser.add_argument('--model_name', type=str, default='gpt-3.5-turbo-0125')
    parser.add_argument('--summary_system_prompt', type=str, default='You are a helpful assistant who will be fed pages of documents. You will generate a summary of each query that you can reference later for user queries.')
    parser.add_argument('--user_query_system_prompt', type=str, default='You are a helpful assistant. You will be asked questions by users about documents that have been summarized prior.')
    args = parser.parse_args()

    system_prompts = [args.summary_system_prompt,args.user_query_system_prompt]
    
    pdfChat = PDFChat(args.OPENAI_API_KEY,args.doc_dir,args.model_name,system_prompts)
    
    chat_history = pdfChat.ingest_docs()
    pdfChat.initiate_chatgpt(chat_history)
    
    


