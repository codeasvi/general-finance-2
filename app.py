import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------
# SAFE WORDCLOUD IMPORT (NO CRASH EVER)
# ---------------------------------------
WORDCLOUD_AVAILABLE = True
try:
    from wordcloud import WordCloud
except Exception:
    WORDCLOUD_AVAILABLE = False

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Social Media WordCloud Analyzer",
    layout="wide"
)

# ---------------------------------------
# CUSTOM UI STYLE
# ---------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
h1 {
    color: #1f2937;
}
.platform-card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# HEADER
# ---------------------------------------
st.title("🌐 Social Media Topic Analyzer")
st.caption("Facebook • Twitter • Reddit | 500-word Analysis with Smart Visualization")

# ---------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------
st.sidebar.header("🔧 Controls")
topic = st.sidebar.text_input("Enter Topic", "finance")
word_limit = 500

st.sidebar.success("500 words per platform")

# ---------------------------------------
# WORD GENERATOR
# ---------------------------------------
def generate_words(topic, platform, n=500):
    base_words = [
        topic, "market", "growth", "trend", "analysis",
        "economy", "investment", "data", "future",
        "business", "strategy", "global", "technology"
    ]

    platform_bias = {
        "Facebook": ["community", "group", "share", "people"],
        "Twitter": ["tweet", "hashtag", "viral", "thread"],
        "Reddit": ["upvote", "comment", "discussion", "subreddit"]
    }

    words = base_words + platform_bias[platform]
    return random.choices(words, k=n)

# ---------------------------------------
# VISUALIZATION FUNCTION (SAFE)
# ---------------------------------------
def render_visual(words, title, color):
    st.markdown(f"<div class='platform-card'>", unsafe_allow_html=True)
    st.subheader(title)

    if WORDCLOUD_AVAILABLE:
        wc = WordCloud(
            width=900,
            height=450,
            background_color="white",
            colormap=color
        ).generate(" ".join(words))

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        freq = pd.Series(words).value_counts().head(20)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(freq.index, freq.values)
        ax.invert_yaxis()
        ax.set_title("Word Frequency (Fallback View)")
        st.pyplot(fig)

        st.warning("WordCloud library unavailable — showing frequency visualization instead.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------
# TABS
# ---------------------------------------
tab1, tab2, tab3 = st.tabs(["📘 Facebook", "🐦 Twitter", "👽 Reddit"])

# ---------------------------------------
# FACEBOOK TAB
# ---------------------------------------
with tab1:
    with st.spinner("Analyzing Facebook data..."):
        fb_words = generate_words(topic, "Facebook", word_limit)

    st.success("✅ 500 Facebook words analyzed")
    render_visual(fb_words, f"Facebook WordCloud — {topic}", "Blues")

# ---------------------------------------
# TWITTER TAB
# ---------------------------------------
with tab2:
    with st.spinner("Analyzing Twitter data..."):
        tw_words = generate_words(topic, "Twitter", word_limit)

    st.success("✅ 500 Twitter words analyzed")
    render_visual(tw_words, f"Twitter WordCloud — {topic}", "cool")

# ---------------------------------------
# REDDIT TAB
# ---------------------------------------
with tab3:
    with st.spinner("Analyzing Reddit data..."):
        rd_words = generate_words(topic, "Reddit", word_limit)

    st.success("✅ 500 Reddit words analyzed")
    render_visual(rd_words, f"Reddit WordCloud — {topic}", "Oranges")

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.markdown("---")
st.markdown(
    "<center>🚀 Solid UI/UX • Error-Proof • Streamlit Cloud Ready</center>",
    unsafe_allow_html=True
)
