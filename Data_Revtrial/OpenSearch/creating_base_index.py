# import pandas as pd
# from opensearchpy import OpenSearch
# import streamlit as st


# index_name = 'imdb_movie_test'

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin') 
# )

# def create_index_with_knn_vector(client, index_name):
#     if client.indices.exists(index=index_name):
#         return
#     index_body = {
#         "settings": {
#             "index.knn": True 
#         },
#         "mappings": {
#             "properties": {
#                 "Series_Title": {
#                     "type": "text"
#                 },
#                 "Released_Year": {
#                     "type": "text"
#                 },
#                 "Runtime": {
#                     "type": "keyword"
#                 },
#                 "Genre": {
#                     "type": "text"
#                 },
#                 "IMDB_Rating": {
#                     "type": "float"
#                 },
#                 "Overview": {
#                     "type": "text"
#                 },
#                 "Director": {
#                     "type": "text"
#                 },
#                 "Star1": {
#                     "type": "text"
#                 },
#                 "Star2": {
#                     "type": "text"
#                 },
#                 "Star3": {
#                     "type": "text"
#                 },
#                 "Star4": {
#                     "type": "text"
#                 },
#                 "No_of_Votes": {
#                     "type": "integer"
#                 }
#             }
#         }
#     }
#     response = client.indices.create(index=index_name, body=index_body)

# def index_documents():
#     df = pd.read_csv('imdb_top_1000.csv')
#     for idx, row in df.iterrows():
#         document = {
#             'Series_Title': row['Series_Title'],
#             'Released_Year': row['Released_Year'],
#             'Runtime': row['Runtime'],
#             'Genre': row['Genre'],
#             'IMDB_Rating': row['IMDB_Rating'],
#             'Overview': row['Overview'],
#             'Director': row['Director'],
#             'Star1': row['Star1'],
#             'Star2': row['Star2'],
#             'Star3': row['Star3'],
#             'Star4': row['Star4'],
#             'No_of_Votes': row['No_of_Votes']
#         }
#         response = client.index(index=index_name, body=document)  


# create_index_with_knn_vector(client, index_name)
# index_documents()
    
#--------------------------------------------------------------------------------------------------------------
# import pandas as pd
# from opensearchpy import OpenSearch
# import streamlit as st

# index_name = 'imdb_movie_keyword'

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin') 
# )

# def create_index_with_knn_vector(client, index_name):
#     if client.indices.exists(index=index_name):
#         return
#     index_body = {
#         "settings": {
#             "index.knn": True 
#         },
#         "mappings": {
#             "properties": {
#                 "Series_Title": {
#                     "type": "keyword"
#                 },
#                 "Released_Year": {
#                     "type": "keyword"
#                 },
#                 "Runtime": {
#                     "type": "keyword"
#                 },
#                 "Genre": {
#                     "type": "keyword"
#                 },
#                 "IMDB_Rating": {
#                     "type": "keyword"
#                 },
#                 "Overview": {
#                     "type": "keyword"
#                 },
#                 "Director": {
#                     "type": "keyword"
#                 },
#                 "Star1": {
#                     "type": "keyword"
#                 },
#                 "Star2": {
#                     "type": "keyword"
#                 },
#                 "Star3": {
#                     "type": "keyword"
#                 },
#                 "Star4": {
#                     "type": "keyword"
#                 },
#                 "No_of_Votes": {
#                     "type": "keyword"
#                 }
#             }
#         }
#     }
#     response = client.indices.create(index=index_name, body=index_body)

# def index_documents():
#     df = pd.read_csv('imdb_top_1000.csv')
#     for idx, row in df.iterrows():
#         document = {
#             'Series_Title': row['Series_Title'],
#             'Released_Year': row['Released_Year'],
#             'Runtime': row['Runtime'],
#             'Genre': row['Genre'],
#             'IMDB_Rating': row['IMDB_Rating'],
#             'Overview': row['Overview'],
#             'Director': row['Director'],
#             'Star1': row['Star1'],
#             'Star2': row['Star2'],
#             'Star3': row['Star3'],
#             'Star4': row['Star4'],
#             'No_of_Votes': row['No_of_Votes']
#         }
#         response = client.index(index=index_name, body=document)  


# create_index_with_knn_vector(client, index_name)
# index_documents()
#--------------------------------------------------------------------------------------------------------------
# import pandas as pd
# from opensearchpy import OpenSearch
# import streamlit as st
# from opensearch_dsl import Search

# host = 'localhost'
# port = 9200

# client = OpenSearch(
#     hosts=[{'host': host, 'port': port}],
#     http_compress=True,
#     use_ssl=False,
#     verify_certs=False,
#     ssl_assert_hostname=False,
#     ssl_show_warn=False,
# )

# index_name = 'imdb_movie_ngram'   

# def create_index(client, index_name):
#     index_body = {
#         'settings': {
#             'index': {
#                 'number_of_shards': 4
#             },
#             'analysis': {
#                 'filter': {
#                     'edge_ngram_filter': {
#                         'type': 'edge_ngram',
#                         'min_gram': 1,
#                         'max_gram': 20
#                     }
#                 },
#                 'analyzer': {
#                     'autocomplete': {
#                         'type': 'custom',
#                         'tokenizer': 'standard',
#                         'filter': [
#                             'lowercase',
#                             'edge_ngram_filter'
#                         ]
#                     }
#                 }
#             }
#         },
#         'mappings': {
#             'properties': {
#                 'Series_Title': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Director': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Released_Year': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Runtime': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Genre': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'IMDB_Rating': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Overview': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Star1': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Star2': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Star3': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Star4': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'No_of_Votes': {
#                     'type': 'text',
#                     'analyzer': 'autocomplete',
#                     'search_analyzer': 'standard',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 }
#             }
#         }
#     }
#     client.indices.create(index=index_name, body=index_body)


# def index_documents():
#     df = pd.read_csv('imdb_top_1000.csv')
#     for idx, row in df.iterrows():
#         document = {
#             'Series_Title': row['Series_Title'],
#             'Released_Year': row['Released_Year'],
#             'Runtime': row['Runtime'],
#             'Genre': row['Genre'],
#             'IMDB_Rating': row['IMDB_Rating'],
#             'Overview': row['Overview'],
#             'Director': row['Director'],
#             'Star1': row['Star1'],
#             'Star2': row['Star2'],
#             'Star3': row['Star3'],
#             'Star4': row['Star4'],
#             'No_of_Votes': row['No_of_Votes']
#         }
#         response = client.index(index=index_name, body=document)  


# create_index(client, index_name)
# index_documents()
#------------------------------------------------------------------------------------------------------------------------
# import pandas as pd
# from opensearchpy import OpenSearch
# import streamlit as st
# from opensearch_dsl import Search

# host = 'localhost'
# port = 9200

# client = OpenSearch(
#     hosts=[{'host': host, 'port': port}],
#     http_compress=True,
#     use_ssl=False,
#     verify_certs=False,
#     ssl_assert_hostname=False,
#     ssl_show_warn=False,
# )

# index_name = 'imdb_movie_trigram'  

# def create_index(client, index_name): 
#     index_body = {
#         "settings": {
#             "index": {
#                 "analysis": {
#                     "analyzer": {
#                         "trigram": {
#                             "type": "custom",
#                             "tokenizer": "standard",
#                             "filter": [
#                                 "lowercase",
#                                 "shingle"
#                             ]
#                         }
#                     },
#                     "filter": {
#                         "shingle": {
#                             "type": "shingle",
#                             "min_shingle_size": 2,
#                             "max_shingle_size": 3
#                         }
#                     }
#                 }
#             }
#         },
#         "mappings": {
#             "properties": {
#                 "Series_Title": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "Director": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "Released_Year": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "Runtime": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "Genre": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "IMDB_Rating": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "Overview": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "Star1": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "Star2": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "Star3": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "Star4": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 },
#                 "No_of_Votes": {
#                     "type": "text",
#                     "fields": {
#                         "trigram": {
#                             "type": "text",
#                             "analyzer": "trigram"
#                         }
#                     }
#                 }
#             }
#         }
#     }
#     client.indices.create(index=index_name, body=index_body)


# def index_documents():
#     df = pd.read_csv('imdb_top_1000.csv')
#     for idx, row in df.iterrows():
#         document = {
#             'Series_Title': row['Series_Title'],
#             'Released_Year': row['Released_Year'],
#             'Runtime': row['Runtime'],
#             'Genre': row['Genre'],
#             'IMDB_Rating': row['IMDB_Rating'],
#             'Overview': row['Overview'],
#             'Director': row['Director'],
#             'Star1': row['Star1'],
#             'Star2': row['Star2'],
#             'Star3': row['Star3'],
#             'Star4': row['Star4'],
#             'No_of_Votes': row['No_of_Votes']
#         }
#         response = client.index(index=index_name, body=document)  


# create_index(client, index_name)
# index_documents()
#------------------------------------------------------------------------------------------------------------------------
## Sort in Search
# import pandas as pd
# from opensearchpy import OpenSearch

# host = 'localhost'
# port = 9200

# client = OpenSearch(
#     hosts=[{'host': host, 'port': port}],
#     http_compress=True,
#     use_ssl=False,
#     verify_certs=False,
#     ssl_assert_hostname=False,
#     ssl_show_warn=False,
# )

# index_name = 'imdb_movie_sort'

# def create_index(client, index_name):
#     index_body = {
#         'settings': {
#             'index': {
#                 'number_of_shards': 4
#             }
#         },
#         'mappings': {
#             'properties': {
#                 'Series_Title': {
#                     'type': 'text',
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Director': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Released_Year': {
#                     'type': 'keyword'
#                 },
#                 'Runtime': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Genre': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'IMDB_Rating': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Overview': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Star1': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Star2': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Star3': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'Star4': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#                 'No_of_Votes': {
#                     'type': 'text', 
#                     'fields': {
#                         'raw': {
#                             'type': 'keyword'
#                         }
#                     }
#                 },
#             }
#         }
#     }
#     client.indices.create(index=index_name, body=index_body)

# def index_documents():
#     df = pd.read_csv('imdb_top_1000.csv')
#     for idx, row in df.iterrows():
#         document = {
#             'Series_Title': row['Series_Title'],
#             'Released_Year': row['Released_Year'],
#             'Runtime': row['Runtime'],
#             'Genre': row['Genre'],
#             'IMDB_Rating': row['IMDB_Rating'],
#             'Overview': row['Overview'],
#             'Director': row['Director'],
#             'Star1': row['Star1'],
#             'Star2': row['Star2'],
#             'Star3': row['Star3'],
#             'Star4': row['Star4'],
#             'No_of_Votes': row['No_of_Votes']
#         }
#         response = client.index(index=index_name, body=document)  


# create_index(client, index_name)
# index_documents()