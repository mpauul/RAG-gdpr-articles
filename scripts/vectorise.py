from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import numpy as np
import chromadb
import json

if __name__ == '__main__':
    root_dir_path = '/Users/mihai.paul/Desktop/work/rag-app' ## Example
    # root_dir_path = '' # <- modify here
    article_output_filepath = "{}/data/articles.json".format(root_dir_path)
    vectordb_dir_path = '{}/data/vector_db'.format(root_dir_path)
    models_base_dir_path = '{}/base_models'.format(root_dir_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=120, 
        chunk_overlap=30,  # number of tokens overlap between chunks
        separators=['.\n']
    )

    articles_lst = []
    with open(article_output_filepath) as json_file:
        articles_lst = json.load(json_file)

    ## initiate Chroma vectorDB locally
    chroma_client = chromadb.PersistentClient(path=vectordb_dir_path)
    collection = chroma_client.get_or_create_collection(name="gdpr-articles")

    ## initiate embedding model
    embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder = models_base_dir_path)

    ## iterate over all the articles dicts
    articles_chunks = []
    articles_chunks_embeddings = []
    articles_metadata = []

    for article in tqdm(articles_lst):
        ## split the article content into chunks
        article_chunks = text_splitter.split_text(article['article_content'])

        ## embbed the extracted chunks
        article_chunks_embeddings = embedding_model.encode(article_chunks)

        ## create the metadata 
        article_metadata = [{'article_number':article['article_number'], 'article_summary':article['article_summary']} for i in range(len(article_chunks))]
        
        articles_chunks.extend(article_chunks)
        articles_metadata.extend(article_metadata)
        articles_chunks_embeddings.append(article_chunks_embeddings)


    stacked_articles_chunks_embeddings = np.vstack(tuple(articles_chunks_embeddings))

    ## persist the chunks and their embeddings in the vectorDB        
    collection.add(
        embeddings=stacked_articles_chunks_embeddings,
        documents=articles_chunks,
        metadatas=articles_metadata,
        ids=[str(chunk_index) for chunk_index in range(len(articles_chunks))]
    )






