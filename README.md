# GDPR RAG 

## STEP 1 - Install the requirements
Create a new environment either by using conda or pythone venv tool

The system uses ChromaDB as vector store which uses Rust programming language under the hood.
If you don't have Rust installed yet, open a terminal and run `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` as recommended here[https://rustup.rs/]
`pip install requirements.txt`

## STEP 2 - Load and extract the articles and their content
The input files we are working with are the actual GDPR articles pdf file and and a summaries.txt file that contains metadata (article number, title and summary) about each article 

Provide the absolute path for both the GDPR articles pdf

## STEP 3 - Split and vectorize the content
Split each article into smaller chunks and then vectorize each chunk

## STEP 4 - Run the RAG system


## STEP 5 - 
