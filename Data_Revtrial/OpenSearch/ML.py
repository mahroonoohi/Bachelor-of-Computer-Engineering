# ##ML(k-NNSearch)
# import streamlit as st
# from opensearchpy import OpenSearch
# import requests
# import json

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin'),  
# )

# index_name = 'my-knn-index-1'


# def create_index_with_knn_vector():
#     """
#     Creates an OpenSearch index with knn_vector fields.
#     """
#     index_body = {
#         "settings": {
#             "index": {
#                 "knn": True
#             }
#         },
#         "mappings": {
#             "properties": {
#                 "my_vector1": {
#                     "type": "knn_vector",
#                     "dimension": 2  
#                 },
#                 "my_vector2": {
#                     "type": "knn_vector",
#                     "dimension": 4  
#                 }
#             }
#         }
#     }

#     url = f"http://localhost:9200/{index_name}"
#     headers = {
#         "Content-Type": "application/json"
#     }

#     response = requests.put(url, json=index_body, headers=headers)

#     if response.status_code == 200:
#         st.write(f"Index '{index_name}' created successfully with knn_vector fields.")
#     else:
#         st.write(f"Failed to create index '{index_name}'. Status code: {response.status_code}")
#         st.write(response.text)


# def index_example_documents():
#     """
#     Indexes example documents into the OpenSearch index.
#     """
#     bulk_data = [
#         {"index": {"_index": index_name, "_id": "1"}},
#         {"my_vector1": [1.5, 2.5], "price": 12.2},
#         {"index": {"_index": index_name, "_id": "2"}},
#         {"my_vector1": [2.5, 3.5], "price": 7.1},
#         {"index": {"_index": index_name, "_id": "3"}},
#         {"my_vector1": [3.5, 4.5], "price": 12.9},
#         {"index": {"_index": index_name, "_id": "4"}},
#         {"my_vector1": [5.5, 6.5], "price": 1.2},
#         {"index": {"_index": index_name, "_id": "5"}},
#         {"my_vector1": [4.5, 5.5], "price": 3.7},
#         {"index": {"_index": index_name, "_id": "6"}},
#         {"my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 10.3},
#         {"index": {"_index": index_name, "_id": "7"}},
#         {"my_vector2": [2.5, 3.5, 5.6, 6.7], "price": 5.5},
#         {"index": {"_index": index_name, "_id": "8"}},
#         {"my_vector2": [4.5, 5.5, 6.7, 3.7], "price": 4.4},
#         {"index": {"_index": index_name, "_id": "9"}},
#         {"my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 8.9}
#     ]

#     bulk_body = ''
#     for i in range(0, len(bulk_data), 2):
#         bulk_body += json.dumps(bulk_data[i]) + '\n' + json.dumps(bulk_data[i+1]) + '\n'

#     url = f"http://localhost:9200/_bulk"
#     headers = {
#         "Content-Type": "application/json"
#     }

#     response = requests.post(url, data=bulk_body, headers=headers)

#     if response.status_code in [200, 201]:
#         st.write("Example documents indexed successfully.")
#     else:
#         st.write("Failed to index example documents.")
#         st.write(response.text)


# def perform_vector_search(query_vector, space_type):
#     """
#     Performs a vector-based search using the knn_score script.

#     Args:
#     - query_vector (list): The vector representing the query point.
#     - space_type (str): The space type for similarity calculation (e.g., "cosinesimil").

#     Returns:
#     - list: List of search results (hits) as dictionaries.
#     """
#     response = client.search(
#         index=index_name,
#         body={
#             "size": 4,  
#             "query": {
#                 "script_score": {
#                     "query": {"match_all": {}},
#                     "script": {
#                         "source": "knn_score",
#                         "lang": "knn",
#                         "params": {
#                             "field": "my_vector2",
#                             "query_value": query_vector,
#                             "space_type": space_type
#                         }
#                     }
#                 }
#             }
#         }
#     )
#     return response['hits']['hits'] if 'hits' in response else []

# st.title("Vector Search in OpenSearch")

# if not client.indices.exists(index=index_name):
#     create_index_with_knn_vector()
#     index_example_documents()

# user_input_vector = st.text_input("Enter vector search query for my_vector2 (comma-separated floats):")

# if user_input_vector:
#     try:
#         query_vector = [float(x.strip()) for x in user_input_vector.split(',')]

#         results_vector = perform_vector_search(query_vector, "cosinesimil")

#         st.write(f"Vector Search Results for Query Vector {query_vector}:")
#         for result in results_vector:
#             st.write(result) 

#     except ValueError:
#         st.error("Invalid input for vector search. Please enter comma-separated floats.")
#---------------------------------------------------------------------------------------------------------------
##pre-filter approach to k-NN search with the score script approach
# import streamlit as st
# from opensearchpy import OpenSearch
# import requests

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin'),  
# )

# index_name = 'my-knn-index-2'


# def create_index_with_knn_vector():
#     """
#     Creates an OpenSearch index with knn_vector fields.
#     """
#     index_body = {
#         "mappings": {
#             "properties": {
#                 "my_vector": {
#                     "type": "knn_vector",
#                     "dimension": 2 
#                 },
#                 "color": {
#                     "type": "keyword"
#                 }
#             }
#         }
#     }
#     url = f"http://localhost:9200/{index_name}"
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = requests.put(url, json=index_body, headers=headers)

#     if response.status_code == 200:
#         st.write(f"Index '{index_name}' created successfully with knn_vector field.")
#     else:
#         st.write(f"Failed to create index '{index_name}'. Status code: {response.status_code}")
#         st.write(response.text)


# def index_documents():
#     """
#     Indexes example documents into the OpenSearch index.
#     """
#     documents = [
#         {"my_vector": [1, 1], "color": "RED"},
#         {"my_vector": [2, 2], "color": "RED"},
#         {"my_vector": [3, 3], "color": "RED"},
#         {"my_vector": [10, 10], "color": "BLUE"},
#         {"my_vector": [20, 20], "color": "BLUE"},
#         {"my_vector": [30, 30], "color": "BLUE"}
#     ]

#     for idx, doc in enumerate(documents, start=1):
#         client.index(index=index_name, id=idx, body=doc)


# def perform_vector_search(query_vector, space_type):
#     """
#     Performs a vector-based search using the knn_score script with a pre-filter.

#     Args:
#     - query_vector (list): The vector representing the query point.
#     - space_type (str): The space type for similarity calculation (e.g., "l2").

#     Returns:
#     - list: List of search results (hits) as dictionaries.
#     """
#     response = client.search(
#         index=index_name,
#         body={
#             "size": 1,  
#             "query": {
#                 "script_score": {
#                     "query": {
#                         "bool": {
#                             "filter": {
#                                 "term": {
#                                     "color": "BLUE"
#                                 }
#                             }
#                         }
#                     },
#                     "script": {
#                         "source": "knn_score",
#                         "lang": "knn",
#                         "params": {
#                             "field": "my_vector",
#                             "query_value": query_vector,
#                             "space_type": space_type
#                         }
#                     }
#                 }
#             }
#         }
#     )
#     return response['hits']['hits'] if 'hits' in response else []

# st.title("k-NN Search with Pre-filtering in OpenSearch")

# if not client.indices.exists(index=index_name):
#     create_index_with_knn_vector()
#     index_documents()

# user_input_vector = st.text_input("Enter vector search query (comma-separated floats):")

# if user_input_vector:
#     try:
#         query_vector = [float(x.strip()) for x in user_input_vector.split(',')]
#         results_vector = perform_vector_search(query_vector, "l2")
#         st.write(f"Vector Search Results for Query Vector {query_vector}:")
#         for result in results_vector:
#             my_vector = result['_source']['my_vector']
#             color = result['_source']['color']
#             st.write(f"- Vector: {my_vector}, Color: {color}")
    
#     except ValueError:
#         st.error("Invalid input for vector search. Please enter comma-separated floats.")
#--------------------------------------------------------------------------------------------------------------
## Getting started with the score script for binary data
# import streamlit as st
# from opensearchpy import OpenSearch
# import requests
# import base64

# # Initialize OpenSearch client
# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin'),  # Replace with your credentials if needed
# )

# # OpenSearch index name
# index_name = 'my-index'


# def create_index_with_binary_field():
#     """
#     Creates an OpenSearch index with a binary field for storing base64-encoded data.
#     """
#     index_body = {
#         "mappings": {
#             "properties": {
#                 "my_binary": {
#                     "type": "binary",
#                     "doc_values": True
#                 },
#                 "color": {
#                     "type": "keyword"
#                 }
#             }
#         }
#     }

#     # URL for the index creation API endpoint
#     url = f"http://localhost:9200/{index_name}"
#     headers = {
#         "Content-Type": "application/json"
#     }

#     # Send the PUT request to create the index with binary field
#     response = requests.put(url, json=index_body, headers=headers)

#     # Check the response
#     if response.status_code == 200:
#         st.write(f"Index '{index_name}' created successfully with binary field.")
#     else:
#         st.write(f"Failed to create index '{index_name}'. Status code: {response.status_code}")
#         st.write(response.text)


# def index_binary_documents():
#     """
#     Indexes example binary documents into the OpenSearch index.
#     """
#     documents = [
#         {"my_binary": "SGVsbG8gV29ybGQh", "color": "RED"},
#         {"my_binary": "ay1OTiBjdXN0b20gc2NvcmluZyE=", "color": "RED"},
#         {"my_binary": "V2VsY29tZSB0byBrLU5O", "color": "RED"},
#         {"my_binary": "SSBob3BlIHRoaXMgaXMgaGVscGZ1bA==", "color": "BLUE"},
#         {"my_binary": "QSBjb3VwbGUgbW9yZSBkb2NzLi4u", "color": "BLUE"},
#         {"my_binary": "TGFzdCBvbmUh", "color": "BLUE"}
#     ]

#     for idx, doc in enumerate(documents, start=1):
#         client.index(index=index_name, id=idx, body=doc)


# def perform_binary_search(query_value, space_type):
#     """
#     Performs a binary-based search using the knn_score script with a pre-filter.

#     Args:
#     - query_value (str): The base64-encoded binary data representing the query point.
#     - space_type (str): The space type for similarity calculation (e.g., "hammingbit").

#     Returns:
#     - list: List of search results (hits) as dictionaries.
#     """
#     response = client.search(
#         index=index_name,
#         body={
#             "size": 2,  # Number of nearest neighbors to retrieve
#             "query": {
#                 "script_score": {
#                     "query": {
#                         "bool": {
#                             "filter": {
#                                 "term": {
#                                     "color": "BLUE"
#                                 }
#                             }
#                         }
#                     },
#                     "script": {
#                         "source": "knn_score",
#                         "lang": "knn",
#                         "params": {
#                             "field": "my_binary",
#                             "query_value": query_value,
#                             "space_type": space_type
#                         }
#                     }
#                 }
#             }
#         }
#     )
#     return response['hits']['hits'] if 'hits' in response else []


# # Streamlit interface
# st.title("k-NN Search with Binary Data and Hamming Distance in OpenSearch")

# # Check if the index exists, create it if not
# if not client.indices.exists(index=index_name):
#     create_index_with_binary_field()
#     index_binary_documents()

# # User input for binary search
# user_input_binary = st.text_input("Enter base64-encoded binary data:")

# if user_input_binary:
#     try:
#         # Perform binary search (example with Hamming distance)
#         results_binary = perform_binary_search(user_input_binary, "hammingbit")
        
#         # Display binary search results
#         st.write(f"Binary Search Results for Query Binary Data {user_input_binary}:")
#         for result in results_binary:
#             my_binary = result['_source']['my_binary']
#             color = result['_source']['color']
#             st.write(f"- Binary Data: {my_binary}, Color: {color}")
    
#     except ValueError:
#         st.error("Invalid input for binary search. Please enter a valid base64-encoded string.")
#-----------------------------------------------------------------------------------------------------------
## Get started with approximate k-NN
# import streamlit as st
# from opensearchpy import OpenSearch
# import requests

# # Initialize OpenSearch client
# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin'),  # Replace with your credentials if needed
# )

# # OpenSearch index name
# index_name = 'my-knn-index-1'


# def create_index_with_knn_vectors():
#     """
#     Creates an OpenSearch index with knn_vector fields and appropriate settings for approximate k-NN.
#     """
#     index_body = {
#         "settings": {
#             "index": {
#                 "knn": True,
#                 "knn.algo_param.ef_search": 100  # Adjust as per your requirements
#             }
#         },
#         "mappings": {
#             "properties": {
#                 "my_vector1": {
#                     "type": "knn_vector",
#                     "dimension": 2,
#                     "method": {
#                         "name": "hnsw",
#                         "space_type": "l2",
#                         "engine": "nmslib",
#                         "parameters": {
#                             "ef_construction": 128,
#                             "m": 24
#                         }
#                     }
#                 },
#                 "my_vector2": {
#                     "type": "knn_vector",
#                     "dimension": 4,
#                     "method": {
#                         "name": "hnsw",
#                         "space_type": "innerproduct",
#                         "engine": "faiss",
#                         "parameters": {
#                             "ef_construction": 256,
#                             "m": 48
#                         }
#                     }
#                 }
#             }
#         }
#     }

#     # URL for the index creation API endpoint
#     url = f"http://localhost:9200/{index_name}"
#     headers = {
#         "Content-Type": "application/json"
#     }

#     # Send the PUT request to create the index with knn_vector fields
#     response = requests.put(url, json=index_body, headers=headers)

#     # Check the response
#     if response.status_code == 200:
#         st.write(f"Index '{index_name}' created successfully with knn_vector fields.")
#     else:
#         st.write(f"Failed to create index '{index_name}'. Status code: {response.status_code}")
#         st.write(response.text)


# def index_documents():
#     """
#     Indexes example documents into the OpenSearch index.
#     """
#     documents = [
#         {"my_vector1": [1.5, 2.5], "price": 12.2},
#         {"my_vector1": [2.5, 3.5], "price": 7.1},
#         {"my_vector1": [3.5, 4.5], "price": 12.9},
#         {"my_vector1": [5.5, 6.5], "price": 1.2},
#         {"my_vector1": [4.5, 5.5], "price": 3.7},
#         {"my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 10.3},
#         {"my_vector2": [2.5, 3.5, 5.6, 6.7], "price": 5.5},
#         {"my_vector2": [4.5, 5.5, 6.7, 3.7], "price": 4.4},
#         {"my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 8.9}
#     ]

#     for idx, doc in enumerate(documents, start=1):
#         client.index(index=index_name, id=idx, body=doc)


# def perform_approximate_knn_search(query_vector, field_name, k):
#     """
#     Performs an approximate k-NN search using the knn query type.

#     Args:
#     - query_vector (list): The vector representing the query point.
#     - field_name (str): The name of the knn_vector field to search against (e.g., "my_vector1", "my_vector2").
#     - k (int): The number of nearest neighbors to retrieve.

#     Returns:
#     - list: List of search results (hits) as dictionaries.
#     """
#     response = client.search(
#         index=index_name,
#         body={
#             "size": k,
#             "query": {
#                 "knn": {
#                     field_name: {
#                         "vector": query_vector,
#                         "k": k
#                     }
#                 }
#             }
#         }
#     )
#     return response['hits']['hits'] if 'hits' in response else []


# # Streamlit interface
# st.title("Approximate k-NN Search in OpenSearch")

# # Check if the index exists, create it if not
# if not client.indices.exists(index=index_name):
#     create_index_with_knn_vectors()
#     index_documents()

# # User input for approximate k-NN search
# user_input_vector = st.text_input("Enter query vector (comma-separated floats):")
# user_input_field = st.selectbox("Select knn_vector field:", ["my_vector1", "my_vector2"])
# user_input_k = st.number_input("Enter number of nearest neighbors to retrieve:", min_value=1, value=2, step=1)

# if user_input_vector:
#     try:
#         query_vector = [float(x.strip()) for x in user_input_vector.split(',')]
        
#         # Perform approximate k-NN search
#         results = perform_approximate_knn_search(query_vector, user_input_field, user_input_k)
        
#         # Display search results
#         st.write(f"Approximate k-NN Search Results for Query Vector {query_vector} in Field '{user_input_field}':")
#         for result in results:
#             vector_field = result['_source'][user_input_field]
#             price = result['_source']['price']
#             st.write(f"- Vector Field: {vector_field}, Price: {price}")
    
#     except ValueError:
#         st.error("Invalid input for query vector. Please enter comma-separated floats.")
