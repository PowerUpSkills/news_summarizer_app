import streamlit as st
import requests
from transformers import pipeline
import os
from dotenv import load_dotenv
import wikipedia

# Load environment variables
load_dotenv()

# API keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def fetch_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&language=en&sortBy=publishedAt"
    response = requests.get(url)
    return response.json()["articles"]

def summarize_text(text):
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

def get_wikipedia_info(query):
    try:
        # Search for the page
        search_results = wikipedia.search(query)
        if search_results:
            # Get the full page content of the first result
            page = wikipedia.page(search_results[0])
            # Return a summary of the page
            return page.summary[:500] + "..."
        else:
            return "No information found."
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation pages
        return f"Multiple results found. Did you mean: {', '.join(e.options[:5])}?"
    except wikipedia.exceptions.PageError:
        return "No information found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

st.title("News Summarizer and Topic Explorer")

query = st.text_input("Enter a news topic:")

if query:
    st.subheader("Recent News Articles")
    articles = fetch_news(query)
    
    for article in articles[:5]:
        st.write(f"**{article['title']}**")
        st.write(f"Source: {article['source']['name']}")
        
        summary = summarize_text(article['description'])
        st.write(f"Summary: {summary}")
        
        st.write("---")
    
    st.subheader("Topic Information")
    wiki_info = get_wikipedia_info(query)
    st.write(wiki_info)
