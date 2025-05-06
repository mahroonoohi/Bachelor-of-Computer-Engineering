import os
import PyPDF2
import string

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page_number in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_number].extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def tokenize_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = ''.join([char if char not in string.punctuation else ' ' for char in text])
    # Split text into words
    tokens = text.split()
    return tokens

def read_pdf(pdf_directory):
    all_texts = []
    try:
        pdf_files = [filename for filename in os.listdir(pdf_directory) if filename.endswith(".pdf")]
        pdf_files.sort(key=lambda x: int(os.path.splitext(x)[0]))
        for filename in pdf_files:
            pdf_path = os.path.join(pdf_directory, filename)
            text = extract_text_from_pdf(pdf_path)
            filename_without_extension = os.path.splitext(filename)[0]
            all_texts.append((filename_without_extension, text))  # Store filename without extension and text
    except Exception as e:
        print(f"Error reading PDFs: {e}")
    return all_texts

def create_inverted_index(all_texts):
    inverted_index = {}
    try:
        for filename, text in all_texts:
            tokens = tokenize_text(text)
            for token in tokens:
                if token not in inverted_index:
                    inverted_index[token] = []
                if filename not in inverted_index[token]: 
                    inverted_index[token].append(filename)
    except Exception as e:
        print(f"Error creating inverted index: {e}")
    return inverted_index


def print_inverted_index_to_file(inverted_index, output_file):
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for word, docs in inverted_index.items():
                f.write(f"{word}: {docs}\n")
        print(f"Inverted index saved to {output_file}")
    except Exception as e:
        print(f"Error printing inverted index to file: {e}")


def search_inverted_index(inverted_index, query):
    terms = query.lower().split()
    result = set()
    if terms[0] in inverted_index:
        result.update(inverted_index[terms[0]])

    for i in range(1, len(terms), 2):
        operator = terms[i]
        next_term = terms[i + 1] if i + 1 < len(terms) else None

        if operator == "and" and next_term:
            if next_term in inverted_index:
                result.intersection_update(inverted_index[next_term])

        elif operator == "or" and next_term:
            if next_term in inverted_index:
                result.update(inverted_index[next_term])

        elif operator == "not" and next_term:
            if next_term in inverted_index:
                result.difference_update(inverted_index[next_term])

    return result

def main():
    pdf_directory = "arxiv_orgs_pdfs"
    output_file = "inverted_index.txt"  
    all_texts = read_pdf(pdf_directory)
    inverted_index = create_inverted_index(all_texts)
    print_inverted_index_to_file(inverted_index, output_file)
    
    print("1. Search Inverted Index")
    print("2. Exit")
    while True:
        choice = input("Enter your choice (1-2): ")
        if choice == "1":
            Query = input("Enter your Query: ")
            results = search_inverted_index(inverted_index, Query)
            if results:
                for filename in results:
                    print(filename)
            else:
                print("No documents found.")
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
