import os
import re

from fpdf import FPDF
import requests
import markdown
import os
from tqdm import tqdm 

LLM_MODEL="gpt-4-turbo"


# GPT_PROMPT_BOIILER_PLATE_INTRO= "Here are contents from a huge list of files about jetstream. Give me a glossary of items for every single relevant terms in these files. remember \n denotes new line and ~~~~~~~~~~~~~~~~ denotes end of a file "
GPT_PROMPT_BOIILER_PLATE_INTRO= "Here are contents of a file about jetstream. Give me a glossary of as many terms you can find."
output_file="data/jetstream/output.txt"
output_file_pdf="data/jetstream/output.pdf"


llm_url = os.environ.get('LLM_URL')
api_key = os.environ.get('LLM_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')
from chains.llm_proxy import build_llm_proxy

import os
import re

def convert_md_to_txt(md_content):
    """Converts a Markdown file to plain text using the markdown library."""

    # with open(md_file, "r") as f:
    #     md_content = f.read()

    html_content = markdown.markdown(md_content)

    # Extract text from HTML using BeautifulSoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    txt_content = soup.get_text()

    return txt_content

# def collate_md_files(directory):
#     """
#     Collates words from all .md files in the specified directory into a single list.
    
#     Args:
#         directory (str): The path to the directory containing .md files.
    
#     Returns:
#         list: A list of all words from the .md files.
#     """
#     words = []
    
#     print(f"Total no of files : {len(os.listdir(directory))}")

#     # Traverse the directory for .md files
#     for filename in os.listdir(directory):
        
#         if filename.endswith('.md'):
#             file_path = os.path.join(directory, filename)
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 content = file.read()
#                 content_transformed= convert_md_to_txt(content)
#                 # Extract words using regex and convert to lowercase
#                 file_words = re.findall(r'\b\w+\b', content.lower())
#                 words.append(content_transformed)
                
#     return words


def append_to_file(output_path, content):
    """
    Appends the provided content to a file at the given output_path.

    Parameters:
    output_path (str): The file path where content will be appended.
    content (str): The content to append to the file.
    """
    try:
        with open(output_path, 'a') as file:
            file.write(content + '\n')  # Adds content and a newline
        print(f"Content successfully appended to {output_path}")
    except Exception as e:
        print(f"Error appending to file: {e}")



def save_reply_to_pdf(reply_text, output_path):
    """
    Saves the given reply text to a PDF file.

    Args:
        reply_text (str): The text to save in the PDF.
        output_path (str): The path where the PDF will be saved.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add the reply text to the PDF, handling line wrapping
    for line in reply_text.splitlines():
        pdf.multi_cell(0, 10, line)

    # Output the PDF
    pdf.output(output_path)
    print(f"PDF saved successfully to {output_path}")

def collate_md_files_original(directory,llm_model,output_file):
    """
    Collates words from all .md files in the specified directory into a single list.
    
    Args:
        directory (str): The path to the directory containing .md files.
    
    Returns:
        list: A list of all words from the .md files.
    """
    replies_for_all_files_this_llm = []
    all_files=os.listdir(directory)
    # Traverse the directory for .md files
    for filename in  tqdm(all_files, total=len(all_files),desc="reading md files"):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                content= convert_md_to_txt(content)
                # Extract words using regex and convert to lowercase
                # file_words = re.findall(r'\b\w+\b', content.lower())
                content = content.split("\n")
                content_no_new_line=[]
                for each_line in content:
                    if not each_line == "":
                        content_no_new_line.append(each_line)                                                    
                reply = get_response_llm(llm_model," ".join(content_no_new_line))
                replies_for_all_files_this_llm.append(reply)                
                append_to_file(output_file, reply)
    return replies_for_all_files_this_llm

def get_response_llm(llm_model,combined_words):
    llm = build_llm_proxy(
    model=llm_model, 
    url=llm_url,
    engine="OpenAI",
    temperature=0.1,
    api_key=api_key,
    )
    print(f"value of LLm model is: {llm_model}")
    prompt = GPT_PROMPT_BOIILER_PLATE_INTRO + combined_words
    try:        
        output = llm.invoke(prompt)         
        print(output)
        return output.content
    except Exception as ex:
        print(f"\ngot error inside GPT call and the error is {ex}")                                                                                                 

        


# Example usage
if __name__ == "__main__":
    directory = "data/jetstream"  # Update this to the directory containing your .md files
   
    
    out= collate_md_files_original(directory,LLM_MODEL,output_file)
    save_reply_to_pdf("".join(out),output_file_pdf)       
