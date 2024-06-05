import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Function to scrape product data
def scrape_products(url, category):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load
    
    product_data = []
    product_elements = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'productcontainer')]")
    
    for product in product_elements:
        product_id = product.get_attribute("id")
        name = product.find_element(By.CLASS_NAME, "ProductTitle--uka4ue.eGVKEf").text.strip()
        rating = product.find_element(By.CLASS_NAME, "NumberedRatingSpan--z7nb9e.cdLOTT").text.strip()
        price_element = product.find_element(By.CLASS_NAME, "SpecialPriceSpan--1x73s3l.eQcivy")
        price = price_element.find_elements(By.TAG_NAME, "span")[1].text.strip() if price_element else "N/A"
        reviews_element = product.find_elements(By.CLASS_NAME, "NumberedRatingSpan--z7nb9e.eTGwQ")
        reviews = reviews_element[0].text.strip() if reviews_element else "None yet"
        size_style_element = product.find_elements(By.CLASS_NAME, "ProductSize--1xo1j94.rmxph")
        size = size_style_element[0].text.split(": ")[1].strip() if size_style_element else "N/A"
        style = size_style_element[1].text.strip() if len(size_style_element) > 1 else "No additional style"
        
        product_data.append([product_id, name, rating, price, reviews, size, style, category])
    
    return product_data

# URLs for different categories
categories = {
    "Sunglasses": "https://www.lenskart.com/sunglasses.html",
    "Eyeglasses": "https://www.lenskart.com/eyeglasses.html",
    "Computer Glasses": "https://www.lenskart.com/eyeglasses/collections/all-computer-glasses.html",
    "Kids Eyeglasses": "https://www.lenskart.com/eyeglasses/promotions/all-kids-eyeglasses.html",
    "Contact Lenses": "https://www.lenskart.com/contact-lenses.html"
}

# Scrape data for each category
all_product_data = []
for category, url in categories.items():
    print("Scraping", category)
    product_data = scrape_products(url, category)
    all_product_data.extend(product_data)

# Convert data to DataFrame
columns = ["Product ID", "Name", "Rating", "Price", "Reviews", "Size", "Style", "Category"]
df = pd.DataFrame(all_product_data, columns=columns)

# Write data to CSV
df.to_csv("lenskart_products.csv", index=False)

# Close the WebDriver
driver.quit()
