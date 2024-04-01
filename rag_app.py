import os
import chromadb
import replicate
from sentence_transformers import SentenceTransformer
from langchain_community.llms import Replicate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

## API keys
os.environ["REPLICATE_API_TOKEN"] = ''


from scripts.utils import extract_articles,read_content

def retrieve_vector_db(db_collection, embdeding_model, query, articles_in =[range(0,21)],n_results=3):
    return db_collection.query(
        query_embeddings = embdeding_model.encode(query).tolist(),
        n_results = n_results,
        where={"article_number": {"$in": articles_in}} ## only look for retrieval in the relevant articles
    )['documents']


def get_relevant_articles(summaries_content, query):
    """
        Returns the list of articles numbers that are relevant for the given query
        
        Params:
            summaries_content: str - text that contains all articles number, title and their respective summary
            query: str - given query
        Returns:
            List of article numbers for which the query is relevant
    """
    retrieval_prompt = f"""
        This is the context you will be working with: {summaries_content}
        You are provided with the above context. The above context contains a list of 21 GDPR articles. 
        Give answer for the question strictly based on the context provided. NEVER provide answers from your own knowledge. Keep answers short and to the point.
        An article is in text format and it contains the article number and a short summary that describes what article is all about.
        Your task is to take this query {query} and chose from this list which articles are the most relevant for the given query.
        DO NOT PROVIDE explanations about why you chose the relevant artilces.
        Do not forget that some query may retrieve only one single relevant article and other prompts may retrieve multiple articles.
    """
    input_replicate = {
        "top_k": 50,
        "top_p": 0.9,
        "prompt":retrieval_prompt,
        "temperature": 0,
        "max_new_tokens": 512,
        "prompt_template": "<s>[INST] {prompt} [/INST] "
    }

    output = replicate.run(
        "mistralai/mistral-7b-instruct-v0.2",
        input=input_replicate
    )
    
    return extract_articles(''.join(output))

if __name__ == '__main__':
    root_dir_path = '/Users/mihai.paul/Desktop/work/rag-app' ## Example
    # root_dir_path = '' # <- modify here
    articles_summaries_filepath = '{}/data/summaries.txt'.format(root_dir_path)
    vectordb_dir_path = '{}/data/vector_db'.format(root_dir_path)
    models_base_dir_path = '{}/base_models'.format(root_dir_path)

    ## load summaries content
    summaries_content = read_content(articles_summaries_filepath)

    ## load vectordb
    client = chromadb.PersistentClient(path=vectordb_dir_path)
    print("Chroma DB articles collection: ",client.list_collections())
    articles_collection = client.get_collection("gdpr-articles")

    ## load embedding model
    embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder = models_base_dir_path)
    
    ## initiate the llm chat model
    llm = Replicate(
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
        model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
        model_kwargs={"temperature": 0.75, "max_length": 4096,"max_new_tokens":2048, "top_p": 1},
    )


    while(True): ## infinite loop for continuous prompting

        ## get the user prompt
        user_query = input("\nYour prompt: ")
        print('Processing the prompt...(please wait)')

        ## stop whenever the letter q is enterd
        if user_query == 'q':
            print("STOP looping")
            break
        
        ## get the relevant articles numbers for context
        relevant_articles = get_relevant_articles(summaries_content,user_query)
        retrieved_chunks = retrieve_vector_db(articles_collection, embedding_model, user_query, relevant_articles, n_results=3)        
        context = '\n\n\n'.join(retrieved_chunks[0])

        ## create the llm prompt and run it through llm
        prompt = f'''
            [INST]
            Give answer for the question strictly based on the context provided. Keep answers short and to the point.

            Question: {user_query}

            Context : {context}
            [/INST]
        '''
        print('Answer: ')
        print('**'*2**7)
        llm(prompt)
        print('\n')
        print('**'*2**7)
        print('\n')


