from opensearchpy import OpenSearch
from opensearch_dsl import Search
import streamlit as st
import requests
import json

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}], http_auth=("admin", "admin")
)


def simple_search(query):
    index_name = "imdb_movie_test"
    search_body = {"query": {"match": {"Series_Title": query}}}
    response = client.search(index=index_name, body=search_body)
    return response


def paginate_search(query, from_index=0, page_size=10):
    index_name = "imdb_movie_test"
    search_body = {
        "query": {"match": {"Series_Title": query}},
        "from": from_index,
        "size": page_size,
    }
    response = client.search(index=index_name, body=search_body)
    return response


def autocomplete_suggestions_Prefix(prefix, field="Series_Title", size=10):
    index_name = "imdb_movie_keyword"
    prefix_query = {"query": {"prefix": {field: prefix}}}
    response = client.search(index=index_name, body=prefix_query)
    suggestions = [hit["_source"][field] for hit in response["hits"]["hits"]]
    return suggestions[:size]


def search_movies_autocomplete_suggestions(query, field="Series_Title"):
    index_name = "imdb_movie_ngram"
    s = Search(using=client, index=index_name).query(
        "match", **{field: {"query": query, "analyzer": "standard"}}
    )
    response = s.execute()
    return response


def autocomplete_suggestions_ngram_matching(prefix, field="Series_Title", size=10):
    index_name = "imdb_movie_ngram"
    if field == "Released_Year":
        try:
            prefix = int(prefix)
        except ValueError:
            return []

        s = Search(using=client, index=index_name).query("term", **{field: prefix})
    else:
        s = Search(using=client, index=index_name).query(
            "match_phrase_prefix", **{field: {"query": prefix}}
        )

    response = s.execute()
    suggestions = [hit["_source"].get(field, "") for hit in response.hits.hits]
    return suggestions[:size]


def miss_spelling_suggestions_terms(term):
    index_name = "imdb_movie_test"
    response = client.search(
        index=index_name,
        body={
            "suggest": {
                "spell-check": {"text": term, "term": {"field": "Series_Title"}}
            }
        },
    )
    suggestions = response["suggest"]["spell-check"][0]["options"]
    return suggestions


def miss_spelling_suggestions_Phrase(term):
    index_name = "imdb_movie_trigram"
    response = client.search(
        index=index_name,
        body={
            "suggest": {
                "phrase-check": {
                    "text": term,
                    "phrase": {
                        "field": "Series_Title.trigram",
                        "gram_size": 3,
                        "highlight": {"pre_tag": "<em>", "post_tag": "</em>"},
                    },
                }
            }
        },
    )
    suggestions = (
        response.get("suggest", {}).get("phrase-check", [{}])[0].get("options", [])
    )
    return suggestions


def Collate_Search(term):
    index_name = "imdb_movie_trigram"
    response = client.search(
        index=index_name,
        body={
            "suggest": {
                "phrase-check": {
                    "text": term,
                    "phrase": {
                        "field": "Series_Title.trigram",
                        "gram_size": 3,
                        "highlight": {"pre_tag": "<em>", "post_tag": "</em>"},
                        "collate": {
                            "query": {
                                "source": {
                                    "match_phrase": {"Series_Title": "{{suggestion}}"}
                                }
                            },
                            "prune": True,
                        },
                        "smoothing": {"laplace": {"alpha": 0.7}},
                    },
                }
            }
        },
    )

    suggestions = (
        response.get("suggest", {}).get("phrase-check", [{}])[0].get("options", [])
    )
    return suggestions


def candidate_generators(term):
    index_name = "imdb_movie_trigram"
    response = client.search(
        index=index_name,
        body={
            "suggest": {
                "phrase-check": {
                    "text": term,
                    "phrase": {
                        "field": "Series_Title.trigram",
                        "size": 3,  # Adjust size to get top 3 suggestions
                        "direct_generator": [
                            {
                                "field": "Series_Title.trigram",
                                "suggest_mode": "always",
                                "min_word_length": 2,  # Adjust min_word_length
                                "max_edits": 2,  # Adjust max_edits
                            }
                        ],
                        "collate": {
                            "query": {
                                "source": {
                                    "match_phrase": {"Series_Title": "{{suggestion}}"}
                                }
                            },
                            "prune": True,
                        },
                        "smoothing": {"laplace": {"alpha": 0.7}},
                    },
                }
            }
        },
    )

    suggestions = (
        response.get("suggest", {}).get("phrase-check", [{}])[0].get("options", [])
    )
    return suggestions


def sort_based_year(released_year=2020):
    index_name = "imdb_movie_sort"

    s = Search(using=client, index=index_name)

    s = s.query("match", Released_Year=str(released_year))
    s = s.sort({"Series_Title.raw": {"order": "asc"}})

    try:
        response = s.execute()
        return response
    except Exception as e:
        st.error(f"Error executing search query: {e}")
        return None


def index_example_documents(index_name):
    bulk_data = [
        {"index": {"_index": index_name, "_id": "1"}},
        {"my_vector1": [1.5, 2.5], "price": 12.2},
        {"index": {"_index": index_name, "_id": "2"}},
        {"my_vector1": [2.5, 3.5], "price": 7.1},
        {"index": {"_index": index_name, "_id": "3"}},
        {"my_vector1": [3.5, 4.5], "price": 12.9},
        {"index": {"_index": index_name, "_id": "4"}},
        {"my_vector1": [5.5, 6.5], "price": 1.2},
        {"index": {"_index": index_name, "_id": "5"}},
        {"my_vector1": [4.5, 5.5], "price": 3.7},
        {"index": {"_index": index_name, "_id": "6"}},
        {"my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 10.3},
        {"index": {"_index": index_name, "_id": "7"}},
        {"my_vector2": [2.5, 3.5, 5.6, 6.7], "price": 5.5},
        {"index": {"_index": index_name, "_id": "8"}},
        {"my_vector2": [4.5, 5.5, 6.7, 3.7], "price": 4.4},
        {"index": {"_index": index_name, "_id": "9"}},
        {"my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 8.9},
    ]

    bulk_body = ""
    for i in range(0, len(bulk_data), 2):
        bulk_body += (
            json.dumps(bulk_data[i]) + "\n" + json.dumps(bulk_data[i + 1]) + "\n"
        )

    url = f"http://localhost:9200/_bulk"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=bulk_body, headers=headers)

    if response.status_code in [200, 201]:
        st.write("Example documents indexed successfully.")
    else:
        st.write("Failed to index example documents.")
        st.write(response.text)


def create_index_with_knn_vector():
    index_name = "my-knn-index-1"
    index_body = {
        "settings": {"index": {"knn": True}},
        "mappings": {
            "properties": {
                "my_vector1": {"type": "knn_vector", "dimension": 2},
                "my_vector2": {"type": "knn_vector", "dimension": 4},
            }
        },
    }

    url = f"http://localhost:9200/{index_name}"
    headers = {"Content-Type": "application/json"}

    response = requests.put(url, json=index_body, headers=headers)

    if response.status_code == 200:
        st.write(f"Index '{index_name}' created successfully with knn_vector fields.")
    else:
        st.write(
            f"Failed to create index '{index_name}'. Status code: {response.status_code}"
        )
        st.write(response.text)


def perform_vector_search(query_vector, space_type, index_name):
    response = client.search(
        index=index_name,
        body={
            "size": 4,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "knn_score",
                        "lang": "knn",
                        "params": {
                            "field": "my_vector2",
                            "query_value": query_vector,
                            "space_type": space_type,
                        },
                    },
                }
            },
        },
    )
    return response["hits"]["hits"] if "hits" in response else []


def create_index_with_knn_vector_prefilter(index_name):
    index_body = {
        "mappings": {
            "properties": {
                "my_vector": {"type": "knn_vector", "dimension": 2},
                "color": {"type": "keyword"},
            }
        }
    }
    url = f"http://localhost:9200/{index_name}"
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=index_body, headers=headers)

    if response.status_code == 200:
        st.write(f"Index '{index_name}' created successfully with knn_vector field.")
    else:
        st.write(
            f"Failed to create index '{index_name}'. Status code: {response.status_code}"
        )
        st.write(response.text)


def index_documents_prefilter(index_name):
    documents = [
        {"my_vector": [1, 1], "color": "RED"},
        {"my_vector": [2, 2], "color": "RED"},
        {"my_vector": [3, 3], "color": "RED"},
        {"my_vector": [10, 10], "color": "BLUE"},
        {"my_vector": [20, 20], "color": "BLUE"},
        {"my_vector": [30, 30], "color": "BLUE"},
    ]

    for idx, doc in enumerate(documents, start=1):
        client.index(index=index_name, id=idx, body=doc)


def perform_prefilter_vector_search(query_vector, space_type, index_name):
    response = client.search(
        index=index_name,
        body={
            "size": 1,
            "query": {
                "script_score": {
                    "query": {"bool": {"filter": {"term": {"color": "BLUE"}}}},
                    "script": {
                        "source": "knn_score",
                        "lang": "knn",
                        "params": {
                            "field": "my_vector",
                            "query_value": query_vector,
                            "space_type": space_type,
                        },
                    },
                }
            },
        },
    )
    return response["hits"]["hits"] if "hits" in response else []


def create_index_with_binary_field(index_name):
    index_body = {
        "mappings": {
            "properties": {
                "my_binary": {"type": "binary", "doc_values": True},
                "color": {"type": "keyword"},
            }
        }
    }

    url = f"http://localhost:9200/{index_name}"
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=index_body, headers=headers)

    if response.status_code == 200:
        st.write(f"Index '{index_name}' created successfully with binary field.")
    else:
        st.write(
            f"Failed to create index '{index_name}'. Status code: {response.status_code}"
        )
        st.write(response.text)


def index_binary_documents(index_name):
    documents = [
        {"my_binary": "SGVsbG8gV29ybGQh", "color": "RED"},
        {"my_binary": "ay1OTiBjdXN0b20gc2NvcmluZyE=", "color": "RED"},
        {"my_binary": "V2VsY29tZSB0byBrLU5O", "color": "RED"},
        {"my_binary": "SSBob3BlIHRoaXMgaXMgaGVscGZ1bA==", "color": "BLUE"},
        {"my_binary": "QSBjb3VwbGUgbW9yZSBkb2NzLi4u", "color": "BLUE"},
        {"my_binary": "TGFzdCBvbmUh", "color": "BLUE"},
    ]

    for idx, doc in enumerate(documents, start=1):
        client.index(index=index_name, id=idx, body=doc)


def perform_binary_search(query_value, space_type, index_name):
    response = client.search(
        index=index_name,
        body={
            "size": 2,  # Number of nearest neighbors to retrieve
            "query": {
                "script_score": {
                    "query": {"bool": {"filter": {"term": {"color": "BLUE"}}}},
                    "script": {
                        "source": "knn_score",
                        "lang": "knn",
                        "params": {
                            "field": "my_binary",
                            "query_value": query_value,
                            "space_type": space_type,
                        },
                    },
                }
            },
        },
    )
    return response["hits"]["hits"] if "hits" in response else []


def create_index_with_knn_vectors_approximate(index_name):
    index_body = {
        "settings": {"index": {"knn": True, "knn.algo_param.ef_search": 100}},
        "mappings": {
            "properties": {
                "my_vector1": {
                    "type": "knn_vector",
                    "dimension": 2,
                    "method": {
                        "name": "hnsw",
                        "space_type": "l2",
                        "engine": "nmslib",
                        "parameters": {"ef_construction": 128, "m": 24},
                    },
                },
                "my_vector2": {
                    "type": "knn_vector",
                    "dimension": 4,
                    "method": {
                        "name": "hnsw",
                        "space_type": "innerproduct",
                        "engine": "faiss",
                        "parameters": {"ef_construction": 256, "m": 48},
                    },
                },
            }
        },
    }

    url = f"http://localhost:9200/{index_name}"
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=index_body, headers=headers)
    if response.status_code == 200:
        st.write(f"Index '{index_name}' created successfully with knn_vector fields.")
    else:
        st.write(
            f"Failed to create index '{index_name}'. Status code: {response.status_code}"
        )
        st.write(response.text)


def approximate_index_documents(index_name):
    """
    Indexes example documents into the OpenSearch index.
    """
    documents = [
        {"my_vector1": [1.5, 2.5], "price": 12.2},
        {"my_vector1": [2.5, 3.5], "price": 7.1},
        {"my_vector1": [3.5, 4.5], "price": 12.9},
        {"my_vector1": [5.5, 6.5], "price": 1.2},
        {"my_vector1": [4.5, 5.5], "price": 3.7},
        {"my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 10.3},
        {"my_vector2": [2.5, 3.5, 5.6, 6.7], "price": 5.5},
        {"my_vector2": [4.5, 5.5, 6.7, 3.7], "price": 4.4},
        {"my_vector2": [1.5, 5.5, 4.5, 6.4], "price": 8.9},
    ]

    for idx, doc in enumerate(documents, start=1):
        client.index(index=index_name, id=idx, body=doc)


def perform_approximate_knn_search(query_vector, field_name, k, index_name):
    response = client.search(
        index=index_name,
        body={
            "size": k,
            "query": {"knn": {field_name: {"vector": query_vector, "k": k}}},
        },
    )
    return response["hits"]["hits"] if "hits" in response else []


def semantic_search(query):
    index_name = "imdb_movie"
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("intfloat/multilingual-e5-large")
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
                        "space_type": "cosinesimil",
                    },
                },
            }
        },
    }
    response = client.search(index=index_name, body=query)
    return response


def main():
    st.sidebar.header("IMDb Movie Search")
    search_methods = ["BM25Search", "VectorSearch", "SemanticSearch"]
    selected_search_method = st.sidebar.selectbox(
        "Choose a search method:", search_methods
    )
    if selected_search_method == "BM25Search":
        st.header("BM25 Search Options")
        options = [
            "Simple Search",
            "Paginate Search",
            "Autocomplete functionality (Prefix matching)",
            "Autocomplete functionality (Edge n-gram matching)",
            "Miss Spelling (Term suggester)",
            "Miss Spelling (Phrase suggester)",
            "Collate field",
            "Candidate generators",
            "Sorting",
        ]
        selected_option = st.selectbox("Choose an option:", options)

        if selected_option:
            if selected_option == "Simple Search":
                query = st.text_input("Enter your search query:")
                if st.button("Search"):
                    results = simple_search(query)
                    st.subheader("Search Results:")
                    for hit in results["hits"]["hits"]:
                        st.write(f"ID: {hit['_id']}")
                        st.write(f"Title: {hit['_source']['Series_Title']}")
                        st.write(f"Overview: {hit['_source']['Overview']}")
                        st.write(f"IMDB Rating: {hit['_source']['IMDB_Rating']}")
                        st.write(f"Director: {hit['_source']['Director']}")
                        st.write("---")

            elif selected_option == "Paginate Search":
                query = st.text_input("Enter your search query:")
                from_index = st.number_input(
                    "Enter starting index (from)", min_value=0, step=1, value=0
                )
                page_size = st.number_input(
                    "Enter number of results per page (size)",
                    min_value=1,
                    step=1,
                    value=10,
                )

                if st.button("Search"):
                    results = paginate_search(
                        query, from_index=from_index, page_size=page_size
                    )
                    st.subheader("Paginated Search Results:")
                    for hit in results["hits"]["hits"]:
                        st.write(f"ID: {hit['_id']}")
                        st.write(f"Title: {hit['_source']['Series_Title']}")
                        st.write(f"Overview: {hit['_source']['Overview']}")
                        st.write(f"IMDB Rating: {hit['_source']['IMDB_Rating']}")
                        st.write(f"Director: {hit['_source']['Director']}")
                        st.write("---")

            elif selected_option == "Autocomplete functionality (Prefix matching)":
                prefix = st.text_input("Enter a prefix for autocomplete suggestions:")
                if prefix:
                    suggestions = autocomplete_suggestions_Prefix(prefix)
                    st.write(f"Autocomplete suggestions for prefix '{prefix}':")
                    if suggestions:
                        st.write(suggestions)
                    else:
                        st.write("No suggestions found.")

            elif selected_option == "Autocomplete functionality (Edge n-gram matching)":

                st.markdown(
                    """
                <style>
                .search-container {
                    display: flex;
                    justify-content: center;
                    margin-top: 20px;
                }
                .search-bar {
                    width: 300px;
                    padding: 10px;
                    border: 2px solid #ccc;
                    border-radius: 5px;
                    font-size: 16px;
                }
                .search-button {
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    margin-left: 10px;
                }
                .search-button:hover {
                    background-color: #45a049;
                }
                .card {
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 20px;
                    margin: 10px 0;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                </style>
                """,
                    unsafe_allow_html=True,
                )

                st.title("Autocomplete(n-gram matching)")

                query = st.text_input("Search for a movie")

                search_field = st.selectbox(
                    "Search by", ["Series_Title", "Director", "Released_Year"]
                )

                if st.button("Search"):
                    results = search_movies_autocomplete_suggestions(
                        query, field=search_field
                    )
                    st.write(f"Search results for: **{query}** by **{search_field}**")
                    for hit in results:
                        st.markdown(
                            f"""
                        <div class="card">
                            <p>Title: {hit.Series_Title}</p>
                            <p>Director: {hit.Director}</p>
                            <p>Released Year: {hit.Released_Year}</p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                prefix = st.text_input(
                    "Enter a Autocomplete functionality (Edge n-gram matching)"
                )
                autocomplete_field = st.selectbox(
                    "Autocomplete by", ["Series_Title", "Director", "Released_Year"]
                )
                if prefix:
                    suggestions = autocomplete_suggestions_ngram_matching(
                        prefix, field=autocomplete_field
                    )
                    st.write(
                        f"Autocomplete suggestions for prefix '{prefix}' by **{autocomplete_field}**:"
                    )
                    st.write(suggestions)

            elif selected_option == "Miss Spelling (Term suggester)":
                st.title("Miss Spelling (Term suggester)")
                search_term = st.text_input("Enter search term:")

                if search_term:
                    suggestions = miss_spelling_suggestions_terms(search_term)
                    if suggestions:
                        st.write("Miss Spelling:")
                        for suggestion in suggestions:
                            st.write(
                                f"- {suggestion['text']} (score: {suggestion['score']})"
                            )
                    else:
                        st.write("No suggestions found.")
            elif selected_option == "Miss Spelling (Phrase suggester)":

                st.title("Miss Spelling (Phrase suggester)")

                user_input = st.text_input("Enter a search term:")

                if user_input:
                    suggestions = miss_spelling_suggestions_Phrase(user_input)
                    if suggestions:
                        st.write("Miss Spelling Phrase suggester:")
                        for suggestion in suggestions:
                            st.write(
                                f"{suggestion['highlighted']} (score: {suggestion['score']})"
                            )
                    else:
                        st.write("No suggestions found.")
            elif selected_option == "Collate field":

                st.title("Collate Search")

                user_input = st.text_input("Enter a search term:")

                if user_input:
                    suggestions = Collate_Search(user_input)
                    if suggestions:
                        st.write("Collate :")
                        for suggestion in suggestions:
                            highlighted_text = (
                                suggestion["highlighted"]
                                .replace("<em>", "**")
                                .replace("</em>", "**")
                            )
                            collate_status = (
                                "Matches found"
                                if suggestion.get("collate_match", False)
                                else "No matches found"
                            )
                            st.write(
                                f"- {highlighted_text} (score: {suggestion['score']:.2f}) - {collate_status}"
                            )
                    else:
                        st.write("No suggestions found.")
            elif selected_option == "Candidate generators":

                st.title("Did-You-Mean Suggester: Candidate generators")

                def display_suggestions(term):
                    suggestions = candidate_generators(term)
                    if suggestions:
                        st.write(f"Top {len(suggestions)} suggestions for '{term}':")
                        for suggestion in suggestions:
                            highlighted_text = suggestion.get("text", "")
                            st.write(f"- {highlighted_text}")
                    else:
                        st.write("No suggestions found.")

                user_input = st.text_input("Enter a search term:")

                if user_input:
                    display_suggestions(user_input)
            elif selected_option == "Sorting":

                st.markdown(
                    """
                    <style>
                    .search-container {
                        display: flex;
                        justify-content: center;
                        margin-top: 20px;
                    }
                    .search-bar {
                        width: 300px;
                        padding: 10px;
                        border: 2px solid #ccc;
                        border-radius: 5px;
                        font-size: 16px;
                    }
                    .search-button {
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                        margin-left: 10px;
                    }
                    .search-button:hover {
                        background-color: #45a049;
                    }
                    .card {
                        background-color: #f9f9f9;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        padding: 20px;
                        margin: 10px 0;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                st.title("Movie Search App")

                st.sidebar.title("Search Options")
                released_year = st.sidebar.number_input(
                    "Enter a year to search for movies released",
                    min_value=1900,
                    max_value=2023,
                    value=2020,
                )

                if st.sidebar.button("Search"):
                    results = sort_based_year(released_year=released_year)
                    if results:
                        st.write(
                            f"Search results for movies released in {released_year}"
                        )
                        for hit in results:
                            st.markdown(
                                f"""
                                <div class="card">
                                    <p>Title: {hit.Series_Title}</p>
                                    <p>Director: {hit.Director}</p>
                                    <p>Year: {hit.Released_Year}</p>
                                    <p>IMDB Rating: {hit.IMDB_Rating}</p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    else:
                        st.warning(
                            f"No results found for movies released in {released_year}"
                        )
        else:
            st.write("Please choose an option from the dropdown.")
    elif selected_search_method == "VectorSearch":
        st.header("Vector Search Options")
        options = [
            "K-NN Search",
            "Pre-filter k-NN search",
            "Binary Data Search",
            "Approximate k-NN",
        ]
        selected_option = st.selectbox("Choose an option:", options)

        if selected_option:
            if selected_option == "K-NN Search":
                index_name = "my-knn-index-1"
                if not client.indices.exists(index=index_name):
                    create_index_with_knn_vector()
                    index_example_documents(index_name=index_name)

                user_input_vector = st.text_input(
                    "Enter vector search query for my_vector2 in(4 dimension) (comma-separated floats):"
                )
                if user_input_vector:
                    try:
                        query_vector = [
                            float(x.strip()) for x in user_input_vector.split(",")
                        ]

                        results_vector = perform_vector_search(
                            query_vector, "cosinesimil", index_name=index_name
                        )

                        st.write(
                            f"Vector Search Results for Query Vector {query_vector}:"
                        )
                        for result in results_vector:
                            st.write(result)
                    except ValueError:
                        st.error(
                            "Invalid input for vector search. Please enter comma-separated floats."
                        )
            elif selected_option == "Pre-filter k-NN search":
                index_name = "my-knn-index-2"
                if not client.indices.exists(index=index_name):
                    index_documents_prefilter(index_name=index_name)
                    index_documents_prefilter(index_name=index_name)
                user_input_vector = st.text_input(
                    "Enter vector search query  in 2 dimention (comma-separated floats):"
                )

                if user_input_vector:
                    try:
                        query_vector = [
                            float(x.strip()) for x in user_input_vector.split(",")
                        ]
                        results_vector = perform_prefilter_vector_search(
                            query_vector, "l2", index_name=index_name
                        )
                        st.write(
                            f"Vector Search Results for Query Vector {query_vector}:"
                        )
                        for result in results_vector:
                            my_vector = result["_source"]["my_vector"]
                            color = result["_source"]["color"]
                            st.write(f"- Vector: {my_vector}, Color: {color}")

                    except ValueError:
                        st.error(
                            "Invalid input for vector search. Please enter comma-separated floats."
                        )
            elif selected_option == "Binary Data Search":
                index_name = "my-index"
                if not client.indices.exists(index=index_name):
                    create_index_with_binary_field(index_name=index_name)
                    index_binary_documents(index_name=index_name)
                user_input_binary = st.text_input(
                    "Enter base64-encoded(Decimal number like 23) binary data :"
                )
                if user_input_binary:
                    try:
                        results_binary = perform_binary_search(
                            user_input_binary, "hammingbit", index_name=index_name
                        )
                        st.write(
                            f"Binary Search Results for Query Binary Data {user_input_binary}:"
                        )
                        for result in results_binary:
                            my_binary = result["_source"]["my_binary"]
                            color = result["_source"]["color"]
                            st.write(f"- Binary Data: {my_binary}, Color: {color}")
                    except ValueError:
                        st.error(
                            "Invalid input for binary search. Please enter a valid base64-encoded string."
                        )
            elif selected_option == "Approximate k-NN":
                index_name = "my-knn-index-1"
                if not client.indices.exists(index=index_name):
                    create_index_with_knn_vectors_approximate(index_name=index_name)
                    approximate_index_documents(index_name=index_name)
                user_input_vector = st.text_input(
                    "Enter query vector (comma-separated floats) if my_vector1 is choosed Enter 2 dimention else 4 dimention:"
                )
                user_input_field = st.selectbox(
                    "Select knn_vector field:", ["my_vector1", "my_vector2"]
                )
                user_input_k = st.number_input(
                    "Enter number of nearest neighbors to retrieve:",
                    min_value=1,
                    value=2,
                    step=1,
                )
                if user_input_vector:
                    try:
                        query_vector = [
                            float(x.strip()) for x in user_input_vector.split(",")
                        ]
                        results = perform_approximate_knn_search(
                            query_vector,
                            user_input_field,
                            user_input_k,
                            index_name=index_name,
                        )
                        st.write(
                            f"Approximate k-NN Search Results for Query Vector {query_vector} in Field '{user_input_field}':"
                        )
                        for result in results:
                            vector_field = result["_source"][user_input_field]
                            price = result["_source"]["price"]
                            st.write(f"- Vector Field: {vector_field}, Price: {price}")
                    except ValueError:
                        st.error(
                            "Invalid input for query vector. Please enter comma-separated floats."
                        )
        else:
            st.write("Please choose an option from the dropdown.")

    elif selected_search_method == "SemanticSearch":
        st.header("Semantic Search Options")
        query = st.text_input("Enter your search query:")

        if st.button("Search"):
            results = semantic_search(query)
            st.subheader("Search Results:")

            st.markdown(
                """
            <style>
            .card {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0;
            }
            </style>
            """,
                unsafe_allow_html=True,
            )

            for hit in results["hits"]["hits"]:
                st.markdown(
                    f"""
                <div class="card">
                    <p><b>ID:</b> {hit['_id']}</p>
                    <p><b>Title:</b> {hit['_source']['Series_Title']}</p>
                    <p><b>Overview:</b> {hit['_source']['Overview']}</p>
                    <p><b>IMDB Rating:</b> {hit['_source']['IMDB_Rating']}</p>
                    <p><b>Director:</b> {hit['_source']['Director']}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    else:
        st.write("Please choose a search method from the sidebar.")


if __name__ == "__main__":
    main()
