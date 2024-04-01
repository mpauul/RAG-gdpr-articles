## GDPR RAG 

This repository holds the **Retrieval Augmented Generation (RAG)** system collection of code dedicated to efficiently handling the extraction, vectorization, and retrieval of data pertinent to GDPR articles from PDF documents. 

### Technology stack used:
1. Python
2. ChromaDB
3. Numpy
4. Langchain
5. Replicate

## STEP 1 - Install the requirements

1. Create a new python virtual environment either by:
- using conda: `conda create -n rag_env python=3.10`and then `conda activate rag_env` 
- python venv: `python3 -m venv rag_env` and then `source ./python_env/bin/activate`

2. In the newly created virtual environment, run `pip install requirements.txt`

**NOTE:** The rag app uses ChromaDB as vector store which in turn uses Rust programming language under the hood.

If you don't have Rust installed yet run the following command in the terminal:

`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` as suggested [here](https://rustup.rs/)


## STEP 2 - Load and extract the articles and their content

1. The two input files that contain the GDPR articles content are:
- the **actual GDPR articles pdf file**
- a **summaries.txt file** that contains the metadata (article number, title and summary) for each article 

Both of these 2 files can be found in the data directory from this repository

2. Before we run the python script for parsing and extracting the content for each article, we must first add the absolute path of the repository directory.

`if __name__ == '__main__':`
    `## modify the root dir path with the absolut path of the repository directory`
    `root_dir_path = '' # <- modify here`
    `root_dir_path = '/Users/mihai.paul/Desktop/work/rag-app' ## Example`
    
Provide the absolute path for both the GDPR articles pdf

## STEP 3 - Split and vectorize the content
Split each article into smaller chunks and then vectorize each chunk

## STEP 4 - Run the RAG system


## STEP 5 - 
