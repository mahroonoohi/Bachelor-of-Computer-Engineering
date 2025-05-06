# import pandas as pd
# from opensearchpy import OpenSearch
# import streamlit as st


# index_name = 'imdb_movie_test'

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin') 
# )

# def search_movies(query):
#     search_body = {
#         "query": {
#         "match": {
#         "Series_Title": query
#             }
#         }
#     }
#     response = client.search(index=index_name, body=search_body)
#     return response

# def main():
#     st.title('IMDb Movie Search')
#     query = st.text_input('Enter your search query:')

#     if st.button('Search'):
#         results = search_movies(query)
#         st.subheader('Search Results:')
#         for hit in results['hits']['hits']: 
#             st.write(f"ID: {hit['_id']}")
#             st.write(f"Title: {hit['_source']['Series_Title']}")
#             st.write(f"Overview: {hit['_source']['Overview']}")
#             st.write(f"IMDB Rating: {hit['_source']['IMDB_Rating']}")
#             st.write(f"Director: {hit['_source']['Director']}")
#             st.write("---")

# if __name__ == '__main__':
#     main()
#----------------------------------------------------------------------------------------------------------
## Configuring BM25 similarity
# import streamlit as st
# from opensearchpy import OpenSearch
# import requests

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin'), 
# )

# index_name = 'shakespeare'

# def create_index_with_custom_similarity():
#     """
#     Creates an OpenSearch index with custom BM25 similarity settings.
#     """
#     custom_similarity_settings = {
#         "settings": {
#             "index": {
#                 "similarity": {
#                     "custom_similarity": {
#                         "type": "BM25",
#                         "k1": 1.25,  
#                         "b": 0.75,  
#                         "discount_overlaps": True
#                     }
#                 }
#             }
#         }
#     }

#     url = f"http://localhost:9200/{index_name}"
#     headers = {
#         "Content-Type": "application/json"
#     }

#     response = requests.put(url, json=custom_similarity_settings, headers=headers)
#     if response.status_code == 200:
#         st.write(f"Index '{index_name}' created successfully with custom BM25 similarity settings.")
#     else:
#         st.write(f"Failed to create index '{index_name}'. Status code: {response.status_code}")
#         st.write(response.text)

# if not client.indices.exists(index=index_name):
#     create_index_with_custom_similarity()
#     documents = [
#         {"text_entry": "Long live the king!", "play_name": "Hamlet", "speaker": "BERNARDO"},
#         {"text_entry": "Long live Richard, Englands royal king!", "play_name": "Richard III", "speaker": "BUCKINGHAM"},
#         {"text_entry": "Live long.", "play_name": "Richard III", "speaker": "GLOUCESTER"},
#         {"text_entry": "Long live our sovereign Richard, Englands king!", "play_name": "Henry VI Part 2", "speaker": "BOTH"}
#     ]

#     for idx, doc in enumerate(documents, start=1):
#         client.index(index=index_name, id=idx, body=doc)

# def perform_keyword_search(query):
#     """
#     Performs a keyword-based search using OpenSearch.

#     Args:
#     - query (str): The search term entered by the user.

#     Returns:
#     - list: List of search results (hits) as dictionaries.
#     """
#     response = client.search(
#         index=index_name,
#         body={
#             "query": {
#                 "match": {
#                     "text_entry": query  
#                 }
#             }
#         }
#     )
#     return response['hits']['hits'] if 'hits' in response else []

# st.title("Keyword Search in Shakespeare's Works")

# def display_search_results(results):
#     """
#     Displays the search results in the Streamlit app.

#     Args:
#     - results (list): List of dictionaries representing search results.
#     """
#     st.write(f"Found {len(results)} result(s):")
#     for result in results:
#         play_name = result['_source']['play_name']
#         speaker = result['_source']['speaker']
#         text_entry = result['_source']['text_entry']
#         score = result['_score']
#         st.write(f"- Play: {play_name}, Speaker: {speaker}, Text: {text_entry} (Score: {score:.2f})")

# user_input = st.text_input("Enter search term:")

# if user_input:
#     results = perform_keyword_search(user_input)
#     display_search_results(results)

#----------------------------------------------------------------------------------------------------------
##	Paginate results(The from and size parameters)
# import pandas as pd
# from opensearchpy import OpenSearch
# import streamlit as st

# index_name = 'imdb_movie_test'

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin') 
# )

# def search_movies(query, from_index=0, page_size=10):
#     search_body = {
#         "query": {
#             "match": {
#                 "Series_Title": query
#             }
#         },
#         "from": from_index,
#         "size": page_size
#     }
#     response = client.search(index=index_name, body=search_body)
#     return response

# def main():
#     st.title('IMDb Movie Search')
#     query = st.text_input('Enter your search query:')
#     from_index = st.number_input('Enter starting index (from)', min_value=0, step=1, value=0)
#     page_size = st.number_input('Enter number of results per page (size)', min_value=1, step=1, value=10)

#     if st.button('Search'):
#         results = search_movies(query, from_index=from_index, page_size=page_size)
#         st.subheader('Search Results:')
#         for hit in results['hits']['hits']: 
#             st.write(f"ID: {hit['_id']}")
#             st.write(f"Title: {hit['_source']['Series_Title']}")
#             st.write(f"Overview: {hit['_source']['Overview']}")
#             st.write(f"IMDB Rating: {hit['_source']['IMDB_Rating']}")
#             st.write(f"Director: {hit['_source']['Director']}")
#             st.write("---")

#         # Display pagination if there are more than one page
#         total_hits = results['hits']['total']['value']
#         if total_hits > page_size:
#             num_pages = total_hits // page_size + 1 if total_hits % page_size != 0 else total_hits // page_size
#             st.markdown(f"Total Pages: {num_pages}")
            
#             # Display pagination buttons
#             st.markdown("<div class='pagination'>", unsafe_allow_html=True)
#             for page in range(num_pages):
#                 from_param = page * page_size
#                 st.markdown(f"""
#                 <button class="pagination-button" onclick="window.location.href='/streamlit?search_input={query}&from={from_param}&size={page_size}'">{page + 1}</button>
#                 """, unsafe_allow_html=True)
#             st.markdown("</div>", unsafe_allow_html=True)

# if __name__ == '__main__':
#     main()
#----------------------------------------------------------------------------------------------------------
## Autocomplete functionality(Prefix matching)
# import pandas as pd
# from opensearchpy import OpenSearch
# import streamlit as st


# index_name = 'imdb_movie_keyword'

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin')
# )

# def search_movies(query):
#     search_body = {
#         "query": {
#             "match": {
#                 "Series_Title": query
#             }
#         }
#     }
#     response = client.search(index=index_name, body=search_body)
#     return response

# def autocomplete_suggestions(prefix, field='Series_Title', size=10):
#     prefix_query = {
#         "query": {
#             "prefix": {
#                 field: prefix
#             }
#         }
#     }
#     response = client.search(index=index_name, body=prefix_query)
#     suggestions = [hit['_source'][field] for hit in response['hits']['hits']]
#     return suggestions[:size]
# def main():
#     st.title('IMDb Movie Search and Autocomplete')
#     query = st.text_input('Enter your search query:')

#     if st.button('Search'):
#         results = search_movies(query)
#         st.subheader('Search Results:')
#         for hit in results['hits']['hits']:
#             st.write(f"ID: {hit['_id']}")
#             st.write(f"Title: {hit['_source']['Series_Title']}")
#             st.write(f"Overview: {hit['_source']['Overview']}")
#             st.write(f"IMDB Rating: {hit['_source']['IMDB_Rating']}")
#             st.write(f"Director: {hit['_source']['Director']}")
#             st.write("---")
    
   
#     prefix = st.text_input('Enter a prefix for autocomplete suggestions:')
#     if prefix:
#         suggestions = autocomplete_suggestions(prefix)
#         st.write(f"Autocomplete suggestions for prefix '{prefix}':")
#         st.write(suggestions)

# if __name__ == '__main__':
#     main()
#--------------------------------------------------------------------------------------------------------------
## Autocomplete functionality(Edge n-gram matching)
# from opensearch_dsl import Search
# import pandas as pd
# from opensearchpy import OpenSearch
# import streamlit as st

# index_name = 'imdb_movie_ngram'

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin') 
# )

# def search_movies(query, field='Series_Title'):
#     s = Search(using=client, index=index_name).query('match', **{field: {'query': query, 'analyzer': 'standard'}})
#     response = s.execute()
#     return response

# def autocomplete_suggestions(prefix, field='Series_Title', size=10):
#     if field == 'Released_Year':
#         try:
#             prefix = int(prefix)
#         except ValueError:
#             return []  

#         s = Search(using=client, index=index_name).query('term', **{field: prefix})
#     else:
#         s = Search(using=client, index=index_name).query('match_phrase_prefix', **{field: {'query': prefix}})

#     response = s.execute()
#     suggestions = [hit['_source'].get(field, '') for hit in response.hits.hits]
#     return suggestions[:size]

# st.markdown("""
# <style>
# .search-container {
#     display: flex;
#     justify-content: center;
#     margin-top: 20px;
# }
# .search-bar {
#     width: 300px;
#     padding: 10px;
#     border: 2px solid #ccc;
#     border-radius: 5px;
#     font-size: 16px;
# }
# .search-button {
#     padding: 10px 20px;
#     background-color: #4CAF50;
#     color: white;
#     border: none;
#     border-radius: 5px;
#     cursor: pointer;
#     font-size: 16px;
#     margin-left: 10px;
# }
# .search-button:hover {
#     background-color: #45a049;
# }
# .card {
#     background-color: #f9f9f9;
#     border: 1px solid #ddd;
#     border-radius: 5px;
#     padding: 20px;
#     margin: 10px 0;
#     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
# }
# </style>
# """, unsafe_allow_html=True)

# st.title("Movie Search App")

# query = st.text_input("Search for a movie")

# search_field = st.selectbox("Search by", ['Series_Title', 'Director', 'Released_Year'])

# if st.button("Search"):
#     results = search_movies(query, field=search_field)
#     st.write(f"Search results for: **{query}** by **{search_field}**")
#     for hit in results:
#         st.markdown(f"""
#         <div class="card">
#             <p>Title: {hit.Series_Title}</p>
#             <p>Director: {hit.Director}</p>
#             <p>Released Year: {hit.Released_Year}</p>
#         </div>
#         """, unsafe_allow_html=True)

# prefix = st.text_input("Enter a prefix for autocomplete suggestions")
# autocomplete_field = st.selectbox("Autocomplete by", ['Series_Title', 'Director', 'Released_Year'])
# if prefix:
#     suggestions = autocomplete_suggestions(prefix, field=autocomplete_field)
#     st.write(f"Autocomplete suggestions for prefix '{prefix}' by **{autocomplete_field}**:")
#     st.write(suggestions)
#---------------------------------------------------------------------------------------------------------------------
## Autocomplete functionality(Completion suggester&& Search as you type)
# import streamlit as st
# from opensearchpy import OpenSearch
# from opensearch_dsl import Search, Document, Text, Keyword

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

# index_name = 'test'

# def create_index():
#     index_body = {
#         'mappings': {
#             'properties': {
#                 'title': {
#                     'type': 'search_as_you_type'
#                 },
#                 'director': {
#                     'type': 'search_as_you_type'
#                 },
#                 'year': {
#                     'type': 'keyword'
#                 }
#             }
#         }
#     }
#     client.indices.create(index=index_name, body=index_body)

# class Movie(Document):
#     title = Text(fields={'raw': Keyword()})
#     director = Text(fields={'raw': Keyword()})
#     year = Text(fields={'raw': Keyword()})

#     class Index:
#         name = index_name

#     def save(self, **kwargs):
#         return super(Movie, self).save(**kwargs)


# def initialize_index():
#     if not client.indices.exists(index=index_name):
#         create_index()
#         add_documents()


# def delete_all_documents():
#     client.delete_by_query(index=index_name, body={"query": {"match_all": {}}})


# def add_documents():
#     delete_all_documents() 

#     movies_bulk = [
#         { "index" : { "_index" : index_name, "_id" : "1" } },
#         { "title" : "Interstellar", "director" : "Christopher Nolan", "year" : "2014"},
#         { "index" : { "_index" : index_name, "_id" : "2" } },
#         { "title" : "Inception and Interstellar", "director" : "Christopher Nolan", "year" : "2010"},
#         { "index" : { "_index" : index_name, "_id" : "3" } },
#         { "title" : "The Dark Knight", "director" : "Christopher Nolan", "year" : "2008"},
#     ]

#     client.bulk(movies_bulk)

# def search_movies(query, field='title'):
#     s = Search(using=client, index=index_name).query('match', **{field: {'query': query}})
#     response = s.execute()
#     return response

# def autocomplete_suggestions(prefix, field='title', size=5):
#     suggestions = []

#     if field == 'year':
#         s = Search(using=client, index=index_name).query('prefix', **{field: prefix})
#     else:
#         s = Search(using=client, index=index_name).query('match_phrase_prefix', **{field: prefix})
    
#     response = s.execute()
#     field_suggestions = [hit['_source'].get(field.split('.')[0], '') for hit in response.hits.hits]
#     suggestions.extend(field_suggestions)

#     return list(set(suggestions))[:size]


# st.markdown("""
# <style>
# .search-container {
#     display: flex;
#     justify-content: center;
#     margin-top: 20px;
# }
# .search-bar {
#     width: 300px;
#     padding: 10px;
#     border: 2px solid #ccc;
#     border-radius: 5px;
#     font-size: 16px;
# }
# .search-button {
#     padding: 10px 20px;
#     background-color: #4CAF50;
#     color: white;
#     border: none;
#     border-radius: 5px;
#     cursor: pointer;
#     font-size: 16px;
#     margin-left: 10px;
# }
# .search-button:hover {
#     background-color: #45a049;
# }
# .card {
#     background-color: #f9f9f9;
#     border: 1px solid #ddd;
#     border-radius: 5px;
#     padding: 20px;
#     margin: 10px 0;
#     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
# }
# </style>
# """, unsafe_allow_html=True)

# st.title("Movie Search App")

# initialize_index()

# query = st.text_input("Search for a movie")

# search_field = st.selectbox("Search by", ['title', 'director', 'year'])

# if st.button("Search"):
#     results = search_movies(query, field=search_field)
#     st.write(f"Search results for: **{query}** by **{search_field}**")

#     for hit in results:
#         st.markdown(f"""
#         <div class="card">
#             <p>Title: {hit.title}</p>
#             <p>Director: {hit.director}</p>
#             <p>Year: {hit.year}</p>
#         </div>
#         """, unsafe_allow_html=True)

# prefix = st.text_input("Enter a prefix for autocomplete suggestions")
# autocomplete_field = st.selectbox("Autocomplete by", ['title', 'director', 'year'])
# if prefix:
#     suggestions = autocomplete_suggestions(prefix, field=autocomplete_field)
#     st.write(f"Autocomplete suggestions for prefix '{prefix}' by **{autocomplete_field}**:")
#     st.write(suggestions)
#-----------------------------------------------------------------------------------------------------------------
## Miss_Spelling (Term suggester)
# import streamlit as st
# from opensearchpy import OpenSearch

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin'), 
# )
# index_name = 'imdb_movie_test'

# def get_spelling_suggestions(term):
#     response = client.search(
#         index=index_name,
#         body={
#             "suggest": {
#                 "spell-check": {
#                     "text": term,
#                     "term": {
#                         "field": "Series_Title"
#                     }
#                 }
#             }
#         }
#     )
#     suggestions = response['suggest']['spell-check'][0]['options']
#     return suggestions


# st.title("Did-You-Mean Suggester")
# search_term = st.text_input("Enter search term:")

# if search_term:
#     suggestions = get_spelling_suggestions(search_term)
#     if suggestions:
#         st.write("Did you mean:")
#         for suggestion in suggestions:
#             st.write(f"- {suggestion['text']} (score: {suggestion['score']})")
#     else:
#         st.write("No suggestions found.")
#------------------------------------------------------------------------------------------------------------------
## Miss_Spelling (phrase suggester)
# import streamlit as st
# from opensearchpy import OpenSearch

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin'),  
# )

# index_name = 'imdb_movie_trigram'

# def get_phrase_suggestions(term):
#     response = client.search(
#         index=index_name,
#         body={
#             "suggest": {
#                 "phrase-check": {
#                     "text": term,
#                     "phrase": {
#                         "field": "Series_Title.trigram",
#                         "gram_size": 3,
#                         "highlight": {
#                             "pre_tag": "<em>",
#                             "post_tag": "</em>"
#                         }
#                     }
#                 }
#             }
#         }
#     )
#     suggestions = response.get('suggest', {}).get('phrase-check', [{}])[0].get('options', [])
#     return suggestions

# st.title("Did-You-Mean Suggester")

# user_input = st.text_input("Enter a search term:")

# if user_input:
#     suggestions = get_phrase_suggestions(user_input)
#     if suggestions:
#         st.write("Did you mean:")
#         for suggestion in suggestions:
#             st.write(f"{suggestion['highlighted']} (score: {suggestion['score']})")
#     else:
#         st.write("No suggestions found.")
#---------------------------------------------------------------------------------------------------------------------------------
## Collate field
# import streamlit as st
# from opensearchpy import OpenSearch

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin'),  
# )

# index_name = 'imdb_movie_trigram'

# def get_phrase_suggestions(term):
#     response = client.search(
#         index=index_name,
#         body={
#             "suggest": {
#                 "phrase-check": {
#                     "text": term,
#                     "phrase": {
#                         "field": "Series_Title.trigram",
#                         "gram_size": 3,
#                         "highlight": {
#                             "pre_tag": "<em>",
#                             "post_tag": "</em>"
#                         },
#                         "collate": {
#                             "query": {
#                                 "source": {
#                                     "match_phrase": {
#                                         "Series_Title": "{{suggestion}}"
#                                     }
#                                 }
#                             },
#                             "prune": True
#                         },
#                         "smoothing": {
#                             "laplace": {
#                                 "alpha": 0.7
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     )
  
#     suggestions = response.get('suggest', {}).get('phrase-check', [{}])[0].get('options', [])
#     return suggestions


# st.title("Did-You-Mean Suggester")

# user_input = st.text_input("Enter a search term:")

# if user_input:
#     suggestions = get_phrase_suggestions(user_input)
#     if suggestions:
#         st.write("Did you mean:")
#         for suggestion in suggestions:
#             highlighted_text = suggestion['highlighted'].replace('<em>', '**').replace('</em>', '**')
#             collate_status = "Matches found" if suggestion.get('collate_match', False) else "No matches found"
#             st.write(f"- {highlighted_text} (score: {suggestion['score']:.2f}) - {collate_status}")
#     else:
#         st.write("No suggestions found.")
#----------------------------------------------------------------------------------------------------------------------------
## Candidate generators
# import streamlit as st
# from opensearchpy import OpenSearch

# client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_auth=('admin', 'admin'),  
# )

# index_name = 'imdb_movie_trigram'

# def get_phrase_suggestions(term):
#     response = client.search(
#         index=index_name,
#         body={
#             "suggest": {
#                 "phrase-check": {
#                     "text": term,
#                     "phrase": {
#                         "field": "Series_Title.trigram",
#                         "size": 3,  # Adjust size to get top 3 suggestions
#                         "direct_generator": [
#                             {
#                                 "field": "Series_Title.trigram",
#                                 "suggest_mode": "always",
#                                 "min_word_length": 2,  # Adjust min_word_length
#                                 "max_edits": 2  # Adjust max_edits
#                             }
#                         ],
#                         "collate": {
#                             "query": {
#                                 "source": {
#                                     "match_phrase": {
#                                         "Series_Title": "{{suggestion}}"
#                                     }
#                                 }
#                             },
#                             "prune": True
#                         },
#                         "smoothing": {
#                             "laplace": {
#                                 "alpha": 0.7
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     )
    
#     suggestions = response.get('suggest', {}).get('phrase-check', [{}])[0].get('options', [])
#     return suggestions

# st.title("Did-You-Mean Suggester")

# def display_suggestions(term):
#     suggestions = get_phrase_suggestions(term)
#     if suggestions:
#         st.write(f"Top {len(suggestions)} suggestions for '{term}':")
#         for suggestion in suggestions:
#             highlighted_text = suggestion.get('text', '')
#             st.write(f"- {highlighted_text}")
#     else:
#         st.write("No suggestions found.")

# user_input = st.text_input("Enter a search term:")

# if user_input:
#     display_suggestions(user_input)
#--------------------------------------------------------------------------------------------------------------------------
## Sortng based year
# import streamlit as st
# from opensearchpy import OpenSearch
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

# index_name = 'imdb_movie_sort'

# def search_movies(released_year=2020):
#     s = Search(using=client, index=index_name)

#     s = s.query('match', Released_Year=str(released_year))
#     s = s.sort({'Series_Title.raw': {'order': 'asc'}})

#     try:
#         response = s.execute()
#         return response
#     except Exception as e:
#         st.error(f"Error executing search query: {e}")
#         return None

# st.markdown("""
# <style>
# .search-container {
#     display: flex;
#     justify-content: center;
#     margin-top: 20px;
# }
# .search-bar {
#     width: 300px;
#     padding: 10px;
#     border: 2px solid #ccc;
#     border-radius: 5px;
#     font-size: 16px;
# }
# .search-button {
#     padding: 10px 20px;
#     background-color: #4CAF50;
#     color: white;
#     border: none;
#     border-radius: 5px;
#     cursor: pointer;
#     font-size: 16px;
#     margin-left: 10px;
# }
# .search-button:hover {
#     background-color: #45a049;
# }
# .card {
#     background-color: #f9f9f9;
#     border: 1px solid #ddd;
#     border-radius: 5px;
#     padding: 20px;
#     margin: 10px 0;
#     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
# }
# </style>
# """, unsafe_allow_html=True)

# st.title("Movie Search App")

# st.sidebar.title("Search Options")
# released_year = st.sidebar.number_input("Enter a year to search for movies released", min_value=1900, max_value=2023, value=2020)

# if st.sidebar.button("Search"):
#     results = search_movies(released_year=released_year)
#     if results:
#         st.write(f"Search results for movies released in {released_year}")
#         for hit in results:
#             st.markdown(f"""
#             <div class="card">
#                 <p>Title: {hit.Series_Title}</p>
#                 <p>Director: {hit.Director}</p>
#                 <p>Year: {hit.Released_Year}</p>
#                 <p>IMDB Rating: {hit.IMDB_Rating}</p>
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.warning(f"No results found for movies released in {released_year}")
#---------------------------------------------------------------------------------------------------------------