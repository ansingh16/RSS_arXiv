import streamlit as st
import feedparser
import re
import datetime

# Function to fetch and filter RSS feed
def fetch_filtered_feed(rss_url, keywords, filter_logic, days):
    feed = feedparser.parse(rss_url)
    filtered_entries = []

    # Create a regex pattern for each keyword to match whole words only
    keyword_patterns = [re.compile(r'\b' + re.escape(keyword.lower()) + r'\b') for keyword in keywords]

    for entry in feed.entries:
        title = entry.title
        summary = entry.summary

        # Check if keywords match based on filter logic
        if filter_logic == "OR":
            if any(pattern.search(title.lower()) or pattern.search(summary.lower()) for pattern in keyword_patterns):
                filtered_entries.append(entry)
        elif filter_logic == "AND":
            if all(pattern.search(title.lower()) or pattern.search(summary.lower()) for pattern in keyword_patterns):
                filtered_entries.append(entry)

    return filtered_entries



# Function to highlight keywords in text
def highlight_keywords(text, keywords, highlight_color="yellow"):
    for keyword in keywords:
        # Use word boundaries to ensure whole word matches
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        text = pattern.sub(f"<span style='color:{highlight_color}; font-weight:bold;'>{keyword}</span>", text)
    return text

# Streamlit app setup
st.set_page_config(page_title="RSS Feed Filter", layout="wide")
st.title("RSS Feed Filter")

# RSS Feed Source
st.subheader("Choose Source")
preloaded_feeds = {
    "astro-ph": "https://arxiv.org/rss/astro-ph",
    "astro-ph.GA": "https://arxiv.org/rss/astro-ph.GA",
    "astro-ph.CO": "https://arxiv.org/rss/astro-ph.CO",
    "astro-ph.EP": "https://arxiv.org/rss/astro-ph.EP",
    "astro-ph.HE": "https://arxiv.org/rss/astro-ph.HE",
    "astro-ph.IM": "https://arxiv.org/rss/astro-ph.IM",
    "astro-ph.SR": "https://arxiv.org/rss/astro-ph.SR",
    "cond-mat": "https://arxiv.org/rss/cond-mat",
    "cond-mat.mtrl-sci": "https://arxiv.org/rss/cond-mat.mtrl-sci",
    "cond-mat.stat-mech": "https://arxiv.org/rss/cond-mat.stat-mech",
    "cond-mat.mes-hall": "https://arxiv.org/rss/cond-mat.mes-hall",
    "gr-qc": "https://arxiv.org/rss/gr-qc",
    "hep-ex": "https://arxiv.org/rss/hep-ex",
    "hep-lat": "https://arxiv.org/rss/hep-lat",
    "hep-ph": "https://arxiv.org/rss/hep-ph",
    "hep-th": "https://arxiv.org/rss/hep-th",
    "math-ph": "https://arxiv.org/rss/math-ph",
    "nlin": "https://arxiv.org/rss/nlin",
    "nlin.CD": "https://arxiv.org/rss/nlin.CD",
    "math": "https://arxiv.org/rss/math",
    "math.AG": "https://arxiv.org/rss/math.AG",
    "math.DG": "https://arxiv.org/rss/math.DG",
    "math.PR": "https://arxiv.org/rss/math.PR",
    "math.ST": "https://arxiv.org/rss/math.ST",
    "cs.AI": "https://arxiv.org/rss/cs.AI",
    "cs.CL": "https://arxiv.org/rss/cs.CL",
    "cs.CV": "https://arxiv.org/rss/cs.CV",
    "cs.LG": "https://arxiv.org/rss/cs.LG",
    "cs.NI": "https://arxiv.org/rss/cs.NI",
    "q-bio.BM": "https://arxiv.org/rss/q-bio.BM",
    "q-bio.GN": "https://arxiv.org/rss/q-bio.GN",
    "q-bio.NC": "https://arxiv.org/rss/q-bio.NC",
    "q-bio.PE": "https://arxiv.org/rss/q-bio.PE",
    "q-fin.CP": "https://arxiv.org/rss/q-fin.CP",
    "q-fin.RM": "https://arxiv.org/rss/q-fin.RM",
    "q-fin.PM": "https://arxiv.org/rss/q-fin.PM",
    "q-fin.ST": "https://arxiv.org/rss/q-fin.ST",
    "stat.AP": "https://arxiv.org/rss/stat.AP",
    "stat.ME": "https://arxiv.org/rss/stat.ME",
    "stat.TH": "https://arxiv.org/rss/stat.TH",
    "eess": "https://arxiv.org/rss/eess",
    "eess.SP": "https://arxiv.org/rss/eess.SP",
    "econ": "https://arxiv.org/rss/econ",
    "econ.GN": "https://arxiv.org/rss/econ.GN",
    "econ.EM": "https://arxiv.org/rss/econ.EM"
}

col1, col2 = st.columns(2)
with col1:
        
    selected_feed = st.selectbox("RSS Feed", list(preloaded_feeds.keys()))
    custom_feed = st.text_input("Or enter a custom RSS feed URL:")
    rss_url = custom_feed if custom_feed else preloaded_feeds[selected_feed]

with col2:


    # Keywords input
    keywords = st.text_area(
        "Enter keywords (comma-separated):",
        placeholder="e.g., metallicity, galaxy cluster, AGN"
    ).split(",")
    keywords = [keyword.strip() for keyword in keywords if keyword.strip()]

    # Display entered keywords
    if keywords:
        st.subheader("Keywords")
        st.write(", ".join(keywords))

    # logic
    filter_logic = st.radio("Keyword Logic", ["OR", "AND"], help="OR: Match any keyword. AND: Match all keywords.")

        
    # Pagination setup
    page_size = 5
    current_page = st.selectbox("Page", range(1, 100 // page_size + 1))


# Fetch and filter the feed
st.subheader("Filtered Articles")

# Fetch and filter articles
if st.button("Fetch Articles"):
    if not keywords:
        st.warning("Please enter at least one keyword to filter articles.")
    else:
        with st.spinner("Fetching and filtering articles..."):
            filtered_articles = fetch_filtered_feed(rss_url, keywords, filter_logic, 1)

        if filtered_articles:
            # Display paged articles
            for article in filtered_articles:
                    highlighted_title = highlight_keywords(article.title, keywords)
                    highlighted_summary = highlight_keywords(article.summary, keywords)

                    highlighted_title = highlight_keywords(article.title, keywords)
                    highlighted_summary = highlight_keywords(article.summary, keywords)

                    authors = article.get("authors", ["N/A"])

                    # Format authors and categories as comma-separated values
                    author_names = ", ".join([author.name for author in authors if hasattr(author, 'name')]) or "N/A"

                    
                    # Display the article based on view option
                    st.markdown(f"### [{highlighted_title}]({article.link})", unsafe_allow_html=True)
                    st.markdown(f'Authors: {author_names}')
                    st.markdown(f"{highlighted_summary}...", unsafe_allow_html=True)  # Reduced summary
                    st.write("---")

                
        else:
            st.info("No articles matched the specified keywords.")
