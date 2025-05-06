import os
import PyPDF2
import string
import math
from collections import Counter, defaultdict

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
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

def read_pdfs_from_directory(pdf_directory):
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
    tf_dict = {}
    for doc_name, tokens in all_texts.items():
        tf_counter = Counter(tokens)
        total_tokens = len(tokens)
        tf = {term: tf_counter[term] / total_tokens for term in tf_counter}
        for term, tf_value in tf.items():
            if term not in tf_dict:
                tf_dict[term] = []
            tf_dict[term].append((doc_name, tf_value))
    return tf_dict

def calculate_idf(all_texts):
    total_documents = len(all_texts)
    doc_frequency = {}
    for doc_tokens in all_texts.values():
        unique_tokens = set(doc_tokens)
        for term in unique_tokens:
            if term not in doc_frequency:
                doc_frequency[term] = 0
            doc_frequency[term] += 1
    
    idf_dict = {}
    for term, document_frequency in doc_frequency.items():
        if(document_frequency==0):
             idf = math.log10(total_documents / (1 + document_frequency)) 
        else:    
             idf = math.log10(total_documents / (document_frequency))
        idf_dict[term] = idf
    
    return idf_dict

def save_dictionary_to_file(dictionary, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for term, values in dictionary.items():
                f.write(f"{term}: {values}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def calculate_tf_idf(tf_dict, idf_dict):
    tf_idf_dict = defaultdict(lambda: defaultdict(float))
    for term, doc_tf_list in tf_dict.items():
        if term in idf_dict:
            idf = idf_dict[term]
            for doc_name, tf in doc_tf_list:
                tf_idf_dict[doc_name][term] = tf * idf
    return tf_idf_dict

def calculate_cosine_similarity(query_vector, doc_vector):
    intersection = set(query_vector.keys()) & set(doc_vector.keys())
    numerator = sum(query_vector[term] * doc_vector[term] for term in intersection)
    
    sum_query = sum(value**2 for value in query_vector.values())
    sum_doc = sum(value**2 for value in doc_vector.values())
    
    denominator = math.sqrt(sum_query) * math.sqrt(sum_doc)
    
    if not denominator:
        return 0.0
    else:
        return numerator / denominator

def main():
    pdf_directory = "arxiv_orgs_pdfs"
    all_texts = read_pdfs_from_directory(pdf_directory)
    tf_dict = build_tf_dictionary(all_texts)

    save_dictionary_to_file(tf_dict, "term_document_tf_dictionary.txt")

    idf_dict = calculate_idf(all_texts)
    save_dictionary_to_file(idf_dict, "idf_dictionary.txt")

    tf_idf_dict = calculate_tf_idf(tf_dict, idf_dict)
    
    while True:
        query = input("Enter your query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break

        query_tokens = tokenize_text(query)
        query_tf = Counter(query_tokens)
        query_vector = {term: (query_tf[term] / len(query_tokens)) * idf_dict.get(term, 0) for term in query_tf}
        
        cosine_scores = {}
        for doc_name, doc_vector in tf_idf_dict.items():
            cosine_scores[doc_name] = calculate_cosine_similarity(query_vector, doc_vector)
        
        sorted_cosine_scores = sorted(cosine_scores.items(), key=lambda item: item[1], reverse=True)
        
        for doc, score in sorted_cosine_scores:
            print(f"{doc}: {score:.6f}")

if __name__ == "__main__":
    main()
