import streamlit as st
import feedparser
from markdown import markdown
import re

# Function to fetch and filter RSS feed
def fetch_filtered_feed(rss_url, keywords):
    feed = feedparser.parse(rss_url)
    filtered_entries = []
    # Create a regex pattern for each keyword to match whole words only
    keyword_patterns = [re.compile(r'\b' + re.escape(keyword.lower()) + r'\b') for keyword in keywords]

    for entry in feed.entries:
        title = entry.title
        summary = entry.summary
        # Check if any keyword matches whole words in title or summary
        if any(pattern.search(title.lower()) or pattern.search(summary.lower()) for pattern in keyword_patterns):
            filtered_entries.append(entry)

    return filtered_entries

# Function to highlight keywords in text
# Function to highlight keywords in text
def highlight_keywords(text, keywords):
    for keyword in keywords:
        # Use word boundaries to ensure whole word matches
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        text = pattern.sub(f"<span style='color:red; font-weight:bold;'>{keyword}</span>", text)
    return text

# Streamlit app setup
st.set_page_config(page_title="RSS Feed Filter", layout="wide")
st.title("RSS Feed Filter")



st.subheader("Choose source")

rss_url = st.selectbox("RSS Feed", ("https://arxiv.org/rss/astro-ph.GA", "https://arxiv.org/rss/hep-th.GA"), key="rss_feed")

keywords = st.text_area(
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

# Create side-by-side buttons for display options
col1, col2, col3,_,_ = st.columns(5)

with col1:
    card_button = st.button("📇 Card View ")
with col2:
    list_button = st.button("📝 List View (Just Titles)")
with col3:
    full_text_button = st.button("📖 Full Text View")

# Define a variable to track which button was clicked
if card_button:
    st.session_state.display_option = "Card View (Reduced Summary)"
elif list_button:
    st.session_state.display_option = "List View (Just Titles)"
elif full_text_button:
    st.session_state.display_option = "Full Text View"


if st.button("Fetch Articles"):

    
    if not keywords:
        st.warning("Please enter at least one keyword to filter articles.")
    else:

        with st.spinner("Fetching and filtering articles..."):
            filtered_articles = fetch_filtered_feed(rss_url, keywords)

        print(st.session_state.display_option)
        
        if filtered_articles:
            for article in filtered_articles:

                highlighted_title = highlight_keywords(article.title, keywords)
                highlighted_summary = highlight_keywords(article.summary, keywords)

                if st.session_state.display_option == "Card View (Reduced Summary)":
                    
                    # Show the title and a reduced version of the summary as a card
                    st.markdown(f"### [{highlighted_title}]({article.link})", unsafe_allow_html=True)
                    st.markdown(f"{highlighted_summary[:300]}...", unsafe_allow_html=True)  # Reduced summary
                    st.write("---")

                elif st.session_state.display_option == "List View (Just Titles)":
                    # Show only the title as a list
                    st.markdown(f"### [{highlighted_title}]({article.link})", unsafe_allow_html=True)
                    st.write("---")

                elif st.session_state.display_option == "Full Text View":
                    # Show the title and full text of the summary
                    st.markdown(f"### [{highlighted_title}]({article.link})", unsafe_allow_html=True)
                    st.markdown(f"{highlighted_summary}", unsafe_allow_html=True)
                    st.write("---")
        else:
            st.info("No articles matched the specified keywords.")

        st.write("---")