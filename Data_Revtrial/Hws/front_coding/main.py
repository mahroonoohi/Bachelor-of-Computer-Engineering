def read_inverted_index_from_file(input_file):
    inverted_index = {}
    try:
        with open(input_file, 'r', encoding="utf-8") as file:  
            for line in file:
                parts = line.strip().split(':')
                word, docs_str = parts[0], parts[1]
                docs = docs_str.strip().strip('[]').split(', ')
                inverted_index[word] = docs
    except Exception as e:
        print(f"Error reading inverted index from file: {e}")
    return inverted_index
def compress_inverted_index(inverted_index, prefix_size):
    common_prefixes = {}

    for word, document_ids in inverted_index.items():
        prefix_key = word[:prefix_size]  
        if prefix_key not in common_prefixes:
            common_prefixes[prefix_key] = {}
        suffix = word[prefix_size:]
        if suffix not in common_prefixes[prefix_key]: 
            common_prefixes[prefix_key][suffix] = document_ids

    return common_prefixes

def print_compressed_index_to_file(compressed_index, output_file):
    try:
        with open(output_file, "w", encoding="utf-8") as f: 
            for prefix, suffixes in compressed_index.items():
                f.write(f"{prefix}{{")
                for suffix, docs in suffixes.items():
                    # Remove double quotes from document IDs
                    docs_str = ', '.join(doc.strip("'\"") for doc in docs)
                    f.write(f"'{suffix}':[{docs_str}],")
                f.write("}\n")
        print(f"Compressed inverted index saved to {output_file}")
    except Exception as e:
        print(f"Error printing compressed index to file: {e}")

def process_boolean_query(query, compress_inverted_index, prefix_size):
    terms = query.lower().split()
    result = None  
    i = 0
    while i < len(terms):
        term = terms[i]
        prefix = term[:prefix_size]
        suffix = term[prefix_size:]
        docs = search_in_compressed_index(compress_inverted_index, prefix, suffix)
        if result is None:
            result = set(docs)
        else:
            if i + 1 < len(terms):
                next_operator = terms[i + 1]
                next_term = terms[i + 2] if i + 2 < len(terms) else None
                if next_operator == "and":
                    if next_term:
                        result.intersection_update(search_in_compressed_index(compress_inverted_index, next_term[:prefix_size], next_term[prefix_size:]))
                    else:
                        break
                elif next_operator == "or":
                    if next_term:
                        result.update(search_in_compressed_index(compress_inverted_index, next_term[:prefix_size], next_term[prefix_size:]))
                    else:
                        break
                elif next_operator == "not":
                    if next_term:
                        result.difference_update(search_in_compressed_index(compress_inverted_index, next_term[:prefix_size], next_term[prefix_size:]))
                    else:
                        break
            i += 2 

    return result

        
def search_in_compressed_index(compressed_index, prefix, suffix):
    if prefix in compressed_index and suffix in compressed_index[prefix]:
        return compressed_index[prefix][suffix]
    else:
        return []


def main():
    input_file = "inverted_index.txt"  
    output_file = "compressed_inverted_index.txt"  
    prefix_size = int(input("Enter the prefix size: "))  
    inverted_index = read_inverted_index_from_file(input_file)
    compressed_index = compress_inverted_index(inverted_index, prefix_size)
    print_compressed_index_to_file(compressed_index, output_file)
    print("1. Search Inverted Index")
    print("2. Exit")
    while True:
        choice = input("Enter your choice (1-2): ")
        if choice == "1":
            Query = input("Enter your Query: ")
            boolean_operators = ["and", "or", "not"]
            if any(op in Query.lower() for op in boolean_operators):
                results=process_boolean_query(Query, compressed_index,prefix_size)
            else:
                prefix = Query[:prefix_size]
                suffix = Query[prefix_size:]
                results = search_in_compressed_index(compressed_index, prefix, suffix)
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