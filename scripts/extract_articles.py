import PyPDF2
import json 
from tqdm import tqdm

class Document:
    def __init__(self, article_number=-1, article_summary='', article_content=''):
        self.article_number = article_number
        self.article_summary = article_summary
        self.article_content = article_content
    
    def get_article_content(self):
        return self.article_content
        
    def set_article_content(self, new_content):
        self.article_content = new_content

    def to_json(self):
        return self.__dict__
    


def extract_article_number(page_content):
    """
        function that extracts the article number from a title page
        page_content: str -> represents the page content text as it is extracted from the pdf
    """
    page_content_lines = page_content.split('\n')
    article_nb_line = page_content_lines[1]
    if 'Article' in article_nb_line:
        return int(article_nb_line.split()[-1].strip('.'))
    return -1

def is_title_page(page_content):
    """
        function that checks if the given page content is the title page of an article
        page_content: str -> represents the page content text as it is extracted from the pdf
    """    
    page_content_lines = page_content.split('\n')
    return (all([
        'EN' == page_content_lines[0],
        'Article' in page_content_lines[1],
        "www.gdpr-text.cominfo@data-privacy-" in page_content_lines,
        "office.eu" in page_content_lines[-1]
    ]))

def extract_articles(pdf_reader, a_summaries_lst):
    """
        function that parses
        reader: PdfReader class -> ssa
        a_summaries_lst: List[str]  
    """
    articles = []
    pages_count = len(pdf_reader.pages)

    # extract the first page content for initialization
    first_article_index = 0
    page_content = pdf_reader.pages[first_article_index].extract_text()

    article_obj = Document()
    if is_title_page(page_content):
        article_number = extract_article_number(page_content)
        article_obj = Document(article_number,a_summaries_lst[first_article_index],'')
        # print("Processing Article ",article_number)

    for page_index in tqdm(range(1,pages_count),desc="Processing pages: "):
        page_content = pdf_reader.pages[page_index].extract_text()
        if is_title_page(page_content):
            articles.append(article_obj)
            article_number = extract_article_number(page_content)
            article_obj = Document(article_number,a_summaries_lst[article_number-1],'')
            # print("Processing Article ",article_number)
        else:
            article_obj.set_article_content(
                article_obj.get_article_content()+'\n'+
                page_content
            )
    articles.append(article_obj)

    return articles

if __name__ == '__main__':
    ## modify the root dir path with the absolut path of the repository directory
    root_dir_path = '/Users/mihai.paul/Desktop/work/rag-app' ## Example
    # root_dir_path = '' # <- modify here
    articles_filepath = '{root_dir_path}/data/GDPR Art 1-21.pdf'
    articles_summaries_filepath = '{root_dir_path}/data/summaries.txt'
    article_output_filepath = "{root_dir_path}/data/articles.json"
    
    article_summaries = []
    with open(articles_summaries_filepath,'r') as file:
        article_summaries = [line for line in file.readlines() if line!='\n']
              
    reader = PyPDF2.PdfReader(articles_filepath)

    articles_jsons = [article.to_json() for article in extract_articles(reader, article_summaries)] 

    with open(article_output_filepath, "w+") as file_write:
        json.dump(articles_jsons, file_write)
