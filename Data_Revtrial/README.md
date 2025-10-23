### **Information Retrieval**   
*May 2025*  
**Advanced Search & Recommendation System with OpenSearch (ML & DL-based)**  
*Supervisor: Dr. Rezapour*

#### 🧠 Overview
Developed an advanced **Information Retrieval (IR) and Recommendation System** that integrates **traditional search algorithms** with **deep learning–based semantic retrieval**.  
The system leverages **OpenSearch** for indexing, querying, and ranking while incorporating **machine learning (ML)** and **transformer-based embeddings** for intelligent and context-aware search.

---

#### ⚙️ Core Functionalities
- Implemented **keyword**, **vector**, and **semantic search pipelines** within OpenSearch.  
- Designed **custom analyzers** for stemming, tokenization, and stopword removal to improve retrieval accuracy.  
- Integrated **autocomplete**, **did-you-mean**, and **search-as-you-type** features for enhanced UX.  
- Deployed **BM25 ranking** as a baseline and extended it with **ML-based re-ranking** using user behavior data.  
- Connected **Sentence-BERT** and **transformer embeddings** for **semantic similarity** and **contextual understanding**.  
- Used **k-NN vector search** (approximate nearest neighbor) for fast high-dimensional retrieval.  
- Implemented **relevance feedback** and **query expansion** to dynamically improve results over time.  

---

#### 🧩 Architecture & Workflow
1. **Data Preprocessing:**  
   - Cleaned and normalized a large-scale dataset (IMDB-scale corpus).  
   - Generated embeddings using **Sentence-BERT**, **MiniLM**, and **OpenAI embedding APIs**.  
2. **Indexing Layer (OpenSearch):**  
   - Created hybrid indexes combining **text** and **vector** fields.  
   - Used **custom analyzers**, **synonym filters**, and **n-gram tokenizers**.  
3. **Query Processing:**  
   - Combined keyword scoring (BM25) with **cosine similarity** from vector search.  
   - Implemented **weighted scoring functions** for hybrid relevance.  
4. **Ranking & Recommendation:**  
   - Trained ML models for **learning-to-rank (LTR)** using user interactions.  
   - Generated **personalized recommendations** with **semantic matching** and **content embeddings**.  
5. **Evaluation:**  
   - Used **Precision@k**, **nDCG**, and **MAP** metrics to assess retrieval quality.  
   - Conducted experiments comparing **BM25**, **Dense Retrieval**, and **Hybrid Search** models.

---

#### 🧰 Tech Stack
| Category | Tools / Technologies |
|-----------|----------------------|
| **Search Engine** | OpenSearch, Elasticsearch-compatible APIs |
| **Machine Learning** | scikit-learn, PyTorch, Sentence-BERT |
| **Vector Search** | OpenSearch k-NN plugin |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Plotly |
| **Deployment** | Docker, REST API integration |

---

#### 🚀 Highlights
- Achieved **up to 42% improvement in semantic recall** compared to BM25-only baseline.  
- Indexed **over 1 million documents** with efficient hybrid retrieval structures.  
- Built a **real-time search dashboard** showing ranked results, embeddings, and score breakdowns.  
- Deployed **interactive API endpoints** for search, ranking, and recommendation tasks.  
- Designed **modular pipeline architecture** supporting plug-and-play ML models for retrieval.

---

#### 📈 Future Enhancements
- Integrate **RAG (Retrieval-Augmented Generation)** using LLMs like GPT or Llama.  
- Add **user intent classification** and **context-aware query rewriting**.  
- Explore **cross-lingual retrieval** using multilingual embeddings.  
- Extend system to support **streaming data** and **real-time re-indexing**.

---

✨ *This project bridges classical IR techniques with modern deep learning, creating a scalable, intelligent, and user-centric retrieval engine.*
