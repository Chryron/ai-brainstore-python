from config import Config
import openai
import json
from duckduckgo_search import ddg 
from brain import BrainInstance
import requests
from transformers import T5ForConditionalGeneration, T5Tokenizer
import warnings
from bs4 import BeautifulSoup
from parse_text import split_text, create_message
warnings.filterwarnings('ignore')
cfg = Config()
openai.api_key = cfg.openai_api_key


def create_chat_completion(content=None, context=None, messages=None, model=cfg.fast_llm_model, temperature=None, max_tokens=1000)->str:
    """Create a chat completion using the OpenAI API"""
    if not messages:
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": content},
        ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message["content"]



def search(query: str, num_results: int = 8) -> str:
    """Return the results of a Google search

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.

    Returns:
        str: The results of the search.
    """
    search_results = []
    if not query:
        return json.dumps(search_results)

    results = ddg(query, max_results=num_results)
    if not results:
        return json.dumps(search_results)

    for j in results:
        search_results.append(j)

    return search_results

def learn(query: str) -> str:
    search_results = search(query)
    texts = []
    for result in search_results:
        try:
            r = requests.get(result['href'])
            soup = BeautifulSoup(r.content, 'html.parser')
            text = soup.get_text()
            # input(text)
            # summary = summarize_text(text)
            # input(summary)
            texts.append(text)
        except Exception:
            continue
            
    for text in texts:
        summarized = summarize(text, query)
        context = f"""You will be given a query. Your task is to answer this query in a detailed but concise manner ONLY using the following text: {summarized}
        If you are UNABLE to answer the question using the provided text or if there is no infornation in the given text relevant to the query, then ONLY respond with the string "INSUFFICIENT_DATA".
        """
        try:
            result = create_chat_completion(query, context)
        except Exception:
            continue
        if "INSUFFICIENT_DATA" not in result:
            data = [{"document_text": result}]
            BrainInstance.add_data(data)
            break


def summarize_text(text, model_name="t5-small", max_length=150):
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=max_length, num_return_sequences=1, num_beams=4, early_stopping=True)

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize(
    text: str, question: str,
) -> str:
    """Summarize text using the OpenAI API

    Args:
        url (str): The url of the text
        text (str): The text to summarize
        question (str): The question to ask the model
        driver (WebDriver): The webdriver to use to scroll the page

    Returns:
        str: The summary of the text
    """
    if not text:
        return "Error: No text to summarize"

    summaries = []
    chunks = list(split_text(text))
    for i, chunk in enumerate(chunks):

        messages = [create_message(chunk, question)]

        summary = create_chat_completion(
            model=cfg.fast_llm_model,
            messages=messages,
        )
        summaries.append(summary)

    combined_summary = "\n".join(summaries)
    if len(list(split_text(combined_summary, 4000)))>1:
        summarized =  summarize_text(combined_summary, question)
        return summarized
    else:
        return combined_summary