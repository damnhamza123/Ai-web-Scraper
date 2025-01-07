import streamlit as st
from scrape import scrape_website
st.title("AI Web Scraper")
url = st.text_input("Enter the URL")
if st.button("Scrape"):
    st.write("Scraping the website")
    scrape_website(url)
    result = scrape_website(url)
    print(result)