import re

def extract_articles(input_text):
    """        
        Params:
            input_text: str - input text from which the article numbers are extracted
        Returns:
            the list of articles numbers from the given input text
            
    """
    pattern = r'Article\s+(\d+)'
    matches = re.findall(pattern, input_text)
    articles = sorted(filter(lambda x: int(x) <= 21, map(int, matches)))
    return articles

def read_content(abs_filepath):
    """
        Returns the content of a file as text
        
        Params:
            abs_filepath: str - absolute path of the articles summaries file
        Returns:
            string content of the input file 
    """
    with open(abs_filepath) as f_summaries:
        return f_summaries.read().replace("\n\n",'\n')

