import os

# When you are not using remote drivers uncomment these imports
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from dotenv import load_dotenv
# If you are doing scraping for learning or practice use this but i will give sometime ip ban and captcha
# def scrape_website(website):
#     print("launching chrome")
#     chrome_driver_path="./chromedriver.exe"
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
#     try:
#         driver.get(website)
#         print("page loaded")
#         html = driver.page_source
#         time.sleep(10)
#         return html
#
#
#     finally:
#         driver.quit()


# get sbr_webdriver from bright data or some other platform
load_dotenv(dotenv_path="simple.env")

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")
# AUTH = 'brd-customer-hl_9a6f9e89-zone-ai_scraper:xz8uj56vesbv'
# SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'
def scrape_website(website):
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html
def extract_body_contents(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content=soup.body
    if body_content:
        return str(body_content)
    return ""
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]