def load_inverted_index(file_path):
    inverted_index = {}
    with open(file_path, 'r') as file:
        for line in file:
            word, filenames = line.strip().split(' ', 1)  
            inverted_index[word] = set(filenames.split()) 
    return inverted_index

def query(inverted_index, query_string):
    if any(op in query_string for op in ['and', 'or', 'not']):
        return boolean_query(inverted_index, query_string)
    else:
        return simple_query(inverted_index, query_string)

def simple_query(inverted_index, term):
    return list(inverted_index.get(term, set()))

def boolean_query(inverted_index, query_string):
    terms = query_string.split()
    print(terms)
    results = set()
    operation = None
    for term in terms:
        if term.lower() == 'and':
            operation = 'and'
        elif term.lower() == 'or':
            operation = 'or'
        elif term.lower() == 'not':
            operation = 'not'
        else:
            if operation == 'and':
                results = results.intersection(inverted_index.get(term, set()))
            elif operation == 'or':
                results = results.union(inverted_index.get(term, set()))
            elif operation == 'not':
                results = results.difference(inverted_index.get(term, set()))
            else:
                results = inverted_index.get(term, set())

    return list(results)

def main():
    inverted_index = load_inverted_index('inverted_index.txt')
    query_string = input("Enter a query: ")
    result = query(inverted_index, query_string)
    if result:
        print(f"Documents satisfying the query '{query_string}': {result}")
    else:
        print(f"No documents found for the query '{query_string}'")

if __name__ == "__main__":
    main()
