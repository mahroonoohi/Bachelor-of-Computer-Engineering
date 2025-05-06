import os
import PyPDF2
import string
import math
from collections import Counter

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page_number in range(len(pdf_reader.pages)):
                extracted_text = pdf_reader.pages[page_number].extract_text()
                if extracted_text:
                    text += extracted_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def tokenize_text(text):
    text = text.lower()
    text = ''.join([char if char not in string.punctuation else ' ' for char in text])
    tokens = text.split()
    return tokens

def read_pdf(pdf_directory):
    all_texts = {}
    try:
        pdf_files = [filename for filename in os.listdir(pdf_directory) if filename.endswith(".pdf")]
        pdf_files.sort(key=lambda x: int(os.path.splitext(x)[0]))
        for filename in pdf_files:
            pdf_path = os.path.join(pdf_directory, filename)
            text = extract_text_from_pdf(pdf_path)
            tokens = tokenize_text(text)
            filename_without_extension = os.path.splitext(filename)[0]
            all_texts[filename_without_extension] = tokens
    except Exception as e:
        print(f"Error reading PDFs: {e}")
    return all_texts

def build_tf_dictionary(all_texts):
    term_document_tf_dict = {}
    for doc_name, tokens in all_texts.items():
        tf_counter = Counter(tokens)
        total_tokens = len(tokens)
        tf = {term: tf_counter[term] for term in tf_counter}
        for term, tf_value in tf.items():
            if term not in term_document_tf_dict:
                term_document_tf_dict[term] = []
            term_document_tf_dict[term].append((doc_name, tf_value, total_tokens))
    return term_document_tf_dict

def calculate_idf(all_texts):
    total_documents = len(all_texts)
    term_document_frequency = {}
    for doc_tokens in all_texts.values():
        unique_tokens = set(doc_tokens)
        for term in unique_tokens:
            if term not in term_document_frequency:
                term_document_frequency[term] = 0
            term_document_frequency[term] += 1

    idf_dict = {}
    for term, document_frequency in term_document_frequency.items():
        #idf = math.log10((total_documents - document_frequency + 0.5) / (document_frequency + 0.5) + 1)
        if(document_frequency==0):
             idf = math.log10(total_documents / (1 + document_frequency)) 
        else:    
             idf = math.log10(total_documents / (document_frequency))
        idf_dict[term] = idf

    return idf_dict

def save_tf_dictionary_to_file(term_document_tf_dict, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for term, doc_tf_list in term_document_tf_dict.items():
                f.write(f"{term}: {doc_tf_list}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def save_idf_dictionary_to_file(idf_dict, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for term, idf in idf_dict.items():
                f.write(f"{term}: {idf}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def bm25_score(idf_dict, term_document_tf_dict, query_tokens, doc_name, k1=1.8, b=1, avgdl=0):
    score = 0.0
    for term in query_tokens:
        if term in idf_dict and term in term_document_tf_dict:
            idf = idf_dict[term]
            for doc, tf, doc_length in term_document_tf_dict[term]:
                if doc == doc_name:
                    tf_component = ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_length / avgdl))))
                    score += idf * tf_component
                    break
    return score

def main():
    pdf_directory = "arxiv_orgs_pdfs"
    all_texts = read_pdf(pdf_directory)
    term_document_tf_dict = build_tf_dictionary(all_texts)
    total_doc_length = sum(len(tokens) for tokens in all_texts.values())
    avgdl = total_doc_length / len(all_texts)

    output_file = "term_document_tf_dictionary.txt"
    save_tf_dictionary_to_file(term_document_tf_dict, output_file)

    idf_dict = calculate_idf(all_texts)
    output_file = "idf_dictionary.txt"
    save_idf_dictionary_to_file(idf_dict, output_file)

    while True:
        total_score = {}
        query = input("Enter your Query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break

        query_tokens = list(set(query.lower().split()))

        for doc_name, tokens in all_texts.items():
            score = bm25_score(idf_dict, term_document_tf_dict, query_tokens, doc_name, avgdl=avgdl)
            total_score[doc_name] = score

        sorted_total_score = sorted(total_score.items(), key=lambda item: item[1], reverse=True)

        for doc, score in sorted_total_score:
            print(f"{doc}: {score}")

if __name__ == "__main__":
    main()
