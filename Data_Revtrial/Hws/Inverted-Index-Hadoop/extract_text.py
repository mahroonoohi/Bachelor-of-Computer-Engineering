import PyPDF2
import os

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
        return text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    pdf_folder = 'pdfs/'  
    txt_folder = 'txts/'  
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)
    pdf_files = [file for file in os.listdir(pdf_folder) if file.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        txt_filename = os.path.splitext(pdf_file)[0] + '.txt'
        txt_path = os.path.join(txt_folder, txt_filename)

        save_text_to_file(text, txt_path)
        print(f'Text extracted from {pdf_file} and saved to {txt_filename}')

if __name__ == "__main__":
    main()
