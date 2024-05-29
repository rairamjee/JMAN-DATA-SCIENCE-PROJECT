from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

driver = webdriver.Edge()

url = "https://www.lenskart.com/eyeglasses.html"
driver.get(url)



# Function to scroll to the bottom of the page
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    last_height = last_height
    print(f"Height : {last_height}")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 2500);")
        # Wait for some time for the content to load
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll to the bottom of the page
scroll_to_bottom()

# Get the HTML content of the page
html = driver.page_source

# Parse the HTML using Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')
products = soup.find_all('div', class_=re.compile('ProductContainer'))
# print(len(products))

name_list = []
rating_list = []
price_list = []
no_of_reviews = []
sizes = []

for product_container in products:
    # rating = product_container.find('div', class_=re.compile('RatingStarContainer')).span.text
    name = product_container.find('p', class_=re.compile('ProductTitle')).text
    span_elements = product_container.find_all('span')
    price = span_elements[-1].text
    # print(span_elements)

    try:
        review_container = product_container.find_all('span', class_=re.compile('NumberedRatingSpan'))
        no_of_review = review_container[1].text
        rating = review_container[0].text
    except:
        rating = 0
        no_of_review = 0

    try:
        size = product_container.find('span', class_=re.compile('ProductSize')).text
    except:
        size = 'none'



    name_list.append(name)
    rating_list.append(rating)
    price_list.append(price)
    no_of_reviews.append(no_of_review)
    sizes.append(size)
    

data = {"Name" : name_list, "Rating": rating_list, "No. of reviews": no_of_reviews, "Size and Color": sizes,  "Price": price_list}
df = pd.DataFrame(data)
# print(df)
df.to_csv('extracted_data/Product.csv', index=False)

# Close the webdriver
driver.quit()
