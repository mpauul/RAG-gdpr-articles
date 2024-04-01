# GDPR RAG 

This repository holds the **Retrieval Augmented Generation (RAG)** system collection of code dedicated to efficiently handling the extraction, vectorization, and retrieval of data pertinent to GDPR articles from PDF documents. 

## STEP 1 - Install the requirements
Create a new python virtual environment either by:
- using conda: `conda create -n rag_env python=3.10`and then `conda activate rag_env` 
- python venv: `python3 -m venv rag_env` and then `source ./python_env/bin/activate`

In the newly created virtual environment, run `pip install requirements.txt`
**NOTE:** The rag app uses ChromaDB as vector store which in turn uses Rust programming language under the hood.

If you don't have Rust installed yet run this command in the terminal `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` as suggested [here](https://rustup.rs/)


## STEP 2 - Load and extract the articles and their content
The input files we are working with are the actual GDPR articles pdf file and and a summaries.txt file that contains metadata (article number, title and summary) about each article 

Provide the absolute path for both the GDPR articles pdf

## STEP 3 - Split and vectorize the content
Split each article into smaller chunks and then vectorize each chunk

## STEP 4 - Run the RAG system


## STEP 5 - 
