import streamlit as st
import requests
from transformers import pipeline
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# API keys
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# Initialize the summarization pipeline
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

def fetch_news(query, categories='business,technology,education,science', language='en', size=10):
    try:
        encoded_query = requests.utils.quote(query)
        newsdata_url = f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_API_KEY}&q={encoded_query}&category={categories}&language={language}&size={size}"
        logging.info(f"Newsdata API URL: {newsdata_url}")
        newsdata_response = requests.get(newsdata_url)
        newsdata_response.raise_for_status()
        newsdata_json = newsdata_response.json()
        
        if newsdata_json['status'] == 'success':
            return newsdata_json.get("results", [])
        else:
            logging.error(f"Newsdata API returned an error: {newsdata_json}")
            return []
    except Exception as e:
        logging.exception(f"Unexpected error in Newsdata API request: {e}")
        return []

def summarize_text(text):
    try:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        logging.error(f"Summarization failed: {e}")
        return "Summary unavailable"

def display_articles(articles):
    seen_titles = set()
    for article in articles:
        if article['title'] not in seen_titles:
            seen_titles.add(article['title'])
            st.write(f"**{article['title']}**")
            
            # Safely access the source name
            source_name = article.get('source', {}).get('name', 'Unknown Source')
            st.write(f"Source: {source_name}")
            
            content = article.get('content', article.get('description', ''))
            if content:
                summary = summarize_text(content)
                st.write(f"Summary: {summary}")
            else:
                st.write("No content available for summarization.")
            
            if 'link' in article:
                st.write(f"[Read more]({article['link']})")
            st.write("---")

st.title("Cool News Aggregator")

# User input for query and filters
query = st.text_input("Enter a news topic:")
categories = st.multiselect("Select categories:", 
                            options=['business', 'technology', 'education', 'science'], 
                            default=['business', 'technology'])
language = st.selectbox("Select language:", options=['en', 'de', 'el'], index=0)
size = st.slider("Number of articles to display:", min_value=1, max_value=50, value=10)

if query:
    st.subheader("Recent News Articles")
    with st.spinner('Fetching news articles...'):
        articles = fetch_news(query, ','.join(categories), language, size)
    
    if articles:
        display_articles(articles)
    else:
        st.warning("No articles found for the given query. Try adjusting your search terms or filters.")

st.subheader("Personalized News Feed")
st.info("Based on your interests, here are some additional suggestions:")
# Placeholder for personalized suggestions
st.write("Feature coming soon!")

# Error handling for API key
if not NEWSDATA_API_KEY:
    st.error("Newsdata API key is missing. Please check your .env file.")

# Footer
st.markdown("---")
st.write("Powered by Newsdata.io and Hugging Face Transformers")
