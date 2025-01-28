import streamlit as st
import feedparser
from markdown import markdown
import re

# Function to fetch and filter RSS feed
def fetch_filtered_feed(rss_url, keywords):
    feed = feedparser.parse(rss_url)
    filtered_entries = []

    for entry in feed.entries:
        title = entry.title
        summary = entry.summary
        if any(keyword.lower() in title.lower() or keyword.lower() in summary.lower() for keyword in keywords):
            filtered_entries.append(entry)

    return filtered_entries

# Function to highlight keywords in text
def highlight_keywords(text, keywords):
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub(f"<span style='color:red; font-weight:bold;'>{keyword}</span>", text)
    return text

# Streamlit app setup
st.set_page_config(page_title="RSS Feed Filter", layout="wide")
st.title("RSS Feed Filter")

# Sidebar for keyword input
st.sidebar.header("Filter Settings")
rss_url = "https://arxiv.org/rss/astro-ph.GA"  # Default RSS feed
keywords = st.sidebar.text_area(
    "Enter keywords (comma-separated):",
    placeholder="e.g., metallicity, galaxy cluster, AGN"
).split(",")
keywords = [keyword.strip() for keyword in keywords if keyword.strip()]

# Display entered keywords below the search bar
if keywords:
    st.subheader("Keywords")
    st.write(", ".join(keywords))

# Fetch and filter the feed
st.subheader("Filtered Articles")
if st.button("Fetch Articles"):
    if not keywords:
        st.warning("Please enter at least one keyword to filter articles.")
    else:
        with st.spinner("Fetching and filtering articles..."):
            filtered_articles = fetch_filtered_feed(rss_url, keywords)

        if filtered_articles:
            for article in filtered_articles:
                highlighted_title = highlight_keywords(article.title, keywords)
                highlighted_summary = highlight_keywords(article.summary, keywords)

                st.markdown(f"### [{markdown(highlighted_title)}]({article.link})", unsafe_allow_html=True)
                st.markdown(f"{markdown(highlighted_summary)}", unsafe_allow_html=True)
                st.write("---")
        else:
            st.info("No articles matched the specified keywords.")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed with ❤️ using Streamlit")
