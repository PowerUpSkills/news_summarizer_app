# News Summarizer and Topic Explorer

This application combines news article fetching with text summarization and Wikipedia information retrieval to provide a comprehensive overview of news topics.

## Functionality

1. **News Article Fetching:** The app fetches recent news articles from the Newsdata.io API based on a user-provided query. It displays the titles and sources of the top five unique articles.  Note that there are currently unresolved issues with filtering by category and language, and some irrelevant or duplicate articles may be returned.

2. **Text Summarization:** Using a pre-trained transformer model (`facebook/bart-large-cnn`), the app generates concise summaries of the fetched news articles. This allows users to quickly grasp the main points of each article.

3. **Wikipedia Integration:** The app retrieves relevant information from a locally cached Wikipedia dataset (downloaded on first run). This provides additional context and background information on the news topic.

## Setup

1. **Install Dependencies:** Make sure you have Python 3.9 or higher installed. Then, install the required packages listed in `requirements.txt` using:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables:** Create a `.env` file in the project root directory and add your Newsdata.io API token:

   ```
   NEWSDATA_API_KEY=YOUR_NEWSDATA_API_KEY
   HUGGINGFACE_API_TOKEN=YOUR_HUGGINGFACE_API_TOKEN
   ```

3. **Run the App:** Start the application using Streamlit:

   ```bash
   streamlit run app.py
   ```

   This will open the app in your web browser.

## Note

The Newsdata.io API integration is currently incomplete. Filtering by category and language, and the removal of duplicate articles, are not fully functional.
