import pandas as pd
from opensearchpy import OpenSearch
import streamlit as st

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('intfloat/multilingual-e5-large')

index_name = 'imdb_movie'
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_auth=('admin', 'admin') 
)

def search_movies(query):
    query_vector = list(model.encode(query))   
    query = {
            "size": 5, 
            "query": {
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": "knn_score",
                            "lang": "knn",
                            "params": {
                                "field": "vector",
                                "query_value": query_vector,
                                "space_type": "cosinesimil"
                            }
                        }
                    }
                }
            }
    response = client.search(index=index_name, body=query)
    return response

def main():
    st.title('IMDb Movie Search')
    query = st.text_input('Enter your search query:')

    if st.button('Search'):
        results = search_movies(query)
        st.subheader('Search Results:')
        
        st.markdown("""
        <style>
        .card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        for hit in results['hits']['hits']:
            st.markdown(f"""
            <div class="card">
                <p><b>ID:</b> {hit['_id']}</p>
                <p><b>Title:</b> {hit['_source']['Series_Title']}</p>
                <p><b>Overview:</b> {hit['_source']['Overview']}</p>
                <p><b>IMDB Rating:</b> {hit['_source']['IMDB_Rating']}</p>
                <p><b>Director:</b> {hit['_source']['Director']}</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()