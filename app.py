import streamlit as st
from transformers import pipeline
from bs4 import BeautifulSoup
import requests

st.title("Blog Post Summarizer")

summarizer = pipeline("summarization")

# Get user input
url = st.text_input("Enter the Blog Post URL to summarize:")

# Process user input and display output
if url:
    # Get the content of the URL
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all(['h1','p'])
    text = [results.text for results in results]
    ARTICLE = ' '.join(text)


    # Summarize the content using Transformers
    ARTICLE = ARTICLE.replace('.', '.<eos>')
    ARTICLE = ARTICLE.replace('?', '?<eos>')
    ARTICLE = ARTICLE.replace('!', '!<eos>')

    sentences = ARTICLE.split('<eos>')
    max_chunk = 500
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))

            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])

    res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)

    summary = ' '.join([summ['summary_text'].capitalize() for summ in res])


    # Display the summary
    st.subheader("Summary:")
    st.write(summary)