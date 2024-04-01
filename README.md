## GDPR RAG 

This repository holds the **Retrieval Augmented Generation (RAG)** system collection of code dedicated to efficiently handling the extraction, vectorization, and retrieval of data pertinent to GDPR articles from PDF documents. 

### Technology stack used:
1. Python
2. ChromaDB
3. Numpy
4. Langchain
5. Replicate
6. Sentence Transformer

## STEP 1 - Install the requirements

1. Create a new python virtual environment either by:
- using conda: `conda create -n rag_env python=3.10`and then `conda activate rag_env` 
- python venv: `python3 -m venv rag_env` and then `source ./python_env/bin/activate`

2. In the newly created virtual environment, run `pip install requirements.txt`

**NOTE:** The rag app uses ChromaDB as vector store which in turn uses Rust programming language under the hood.

If you don't have Rust installed yet run the following command in the terminal:

`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` as suggested [here](https://rustup.rs/)


## STEP 2 - Load and extract the articles and their content

1. Clone this repository
2. The two input files that contain the GDPR articles content are:
- the **actual GDPR articles pdf file**
- a **summaries.txt file** that contains the metadata (article number, title and summary) for each article 

Both of these 2 files can be found in the data directory from this repository
 
3. Before we run the python script for parsing and extracting the content for each article, we must first modify the root_dir_path with the absolute path of the repository directory.

In `extract_articles.py :`

```
if __name__ == '__main__':
    ## modify the root dir path with the absolut path of the repository directory
    root_dir_path = '' # <- modify here
    ## EXAMPLE: root_dir_path = '/Users/mihai.paul/Desktop/work/rag-app' 
```

4. Run in the terminal `python scripts/extract_articles.py`. This command will:
- start parsing each page of the GDPR articles pdf file
- while parsing, it will extract the content for each article and it will create an custom object called Document which holds the content as well as metadata for the article
- add each created article in a list 
- save the created list of articles as JSON in the **data** directory of the repository in a file called `articles.json`

## STEP 3 - Split and vectorise each article's content

Now that we have the content for each article extracted and stored, we can now split each article into smaller chunks and then vectorise each chunk

1. Before we run the python script for chunking and embedding each article, we must first modify the root_dir_path with the absolute path of the repository directory.


In `vectorise.py :`

```
if __name__ == '__main__':
    ## modify the root dir path with the absolut path of the repository directory
    root_dir_path = '' # <- modify here
    ## EXAMPLE: root_dir_path = '/Users/mihai.paul/Desktop/work/rag-app' 
```

2. In the terminal, run `python scripts/vectorise.py`. This command will (for each article):
- split the content into smaller chunks. The chunking strategy is to treat each line of the content as an individual chunk, thus keeping each line short in order to embbed a smaller chunk into a vector (for better semantics embedding) 
- vectorise each chunk and add it into the vectorDB for retrieval. The vectorisation is done using the `sentence-transformers/all-mpnet-base-v2` model.
- persist the VectorDB in a in the **data/vector_db** directory`

## STEP 4 - Run the RAG system

Now that we have the entire GDPR content vectorized, we can now use it for contextualized text generation.

1. Before we run the python app for for prompt-based text generation, we must first modify the root_dir_path with the absolute path of the repository directory.


In `rag_app.py :`

```
os.environ["REPLICATE_API_TOKEN"] = '' <-write your Replicate token here

```

```
if __name__ == '__main__':
    ## modify the root dir path with the absolut path of the repository directory
    root_dir_path = '' # <- modify here
    ## EXAMPLE: root_dir_path = '/Users/mihai.paul/Desktop/work/rag-app' 
```

2. In the terminal, run `python rag_app.py`. This command will:
- Prompt the user to provide a prompt/query/question that (ideally) is concerning any of the topics found in the GDPR articles.
- the user query it's them analysed by an LLM `(Mistral-7B)` in order to determine the most relevant GDPR Article(s) for the query. This LLM is  able to direct the RAG system to search within the context of the selected Article(s), improving the relevance and accuracy of the responses. 
- In order to achieve this, the LLM takes the articles summaries and the user query and determines the most relevant articles wherein the context for the final answer should be retrieved.
- The context is filtered during the retrieval from Chroma VectorDB based on the relevant articles extracted
- After the context is fully extracted, it's then provided as input context to the Llama2-13B chat model, that is responsable for generating the final output to the user.
- After the output is generated, the system will prompt the user again for a query until `q` is provided to it

