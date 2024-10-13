import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

# Selenium Setup for Safari
driver = webdriver.Safari()

# Scraping URL
url = 'https://www.bbc.com/news'  # An example of a site for testing

# Open the page using Selenium
driver.get(url)

# Wait for the page to load completely
try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article')))
except TimeoutException:
    print("Час очікування закінчився. Не вдалося знайти елемент з класом 'gs-c-promo'.")


# Collect HTML after loading dynamic content
html = driver.page_source

# Close the browser after receiving the HTML
driver.quit()

# Parsing HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Collect the necessary data from the website
articles = soup.find_all('article')

data = []
print(f"Знайдено статей: {len(articles)}")

for article in articles:
    # Let's try to find the title, link, author and date
    title_tag = article.find('title')
    title = title_tag.text.strip() if title_tag else 'There is no title'
    
    link_tag = article.find('a', href=True)
    link = link_tag['href'] if link_tag else 'There is no link'
    if not link.startswith('http'):  # Add the base URL if the link is relative
        link = f'https://www.bbc.com{link}'
    
    author_tag = article.find('span')
    author = author_tag.text.strip() if author_tag else 'Unknown author'
    
    date_tag = article.find('time')
    date = date_tag['datetime'] if date_tag and 'datetime' in date_tag.attrs else 'There is no date'
    
    print(f"Title: {title}, Link: {link}, Author: {author}, Date: {date}")
    
    data.append({
        'Title': title,
        'Link': link,
        'Author': author,
        'Date': date
    })

# Save the data in a CSV file
if data:
    df = pd.DataFrame(data)
    df.to_csv('articles.csv', index=False)
    print("Parsing is complete! The data is saved in articles.csv.")
else:
    print("No data found to save.")