import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as condition
from services.email_service import send_report

PATH = './drivers/chromedriver.exe'


def set_delivery_to_nyc(driver):
    driver.get('https://www.amazon.com/?ref=icp_country_us')
    location_popover = driver.find_element_by_id(
        'nav-global-location-popover-link')
    location_popover.click()
    WebDriverWait(driver, 100).until(
        condition.element_to_be_clickable((By.ID, 'GLUXZipUpdateInput')))
    location_input = driver.find_element_by_id('GLUXZipUpdateInput')
    location_input.click()
    location_input.send_keys('10001')  # NYC General ZIP code
    location_input.send_keys(Keys.RETURN)  # RETURN == ENTER


def get_product_data(driver, product):
    url = 'http://www.amazon.com/dp/product/' + product.loc['Asin']

    driver.get(url)

    # this renders the JS code and stores all
    # of the information in static HTML code.
    html = driver.page_source

    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, 'html.parser')

    try:
        # Product information
        name = soup.find(id='productTitle').get_text().strip()
    except:
        # Dog Page
        return {
            'Account': product.loc['Account'],
            'SKU': product.loc['SKU'],
            'Name': '',
            'Status': 'Active',
            'ASIN': product.loc['Asin'],
            'Customer Reviews': '',
            'Q & A': '',
            'Reviews Rating': '',
            'Category': '',
            'Sub. Cat': '',
            'Sub.Cat2': '',
            'Available/Unavailable': '',
            'Comments': 'Dog Page'
        }

    qa_html = soup.select('#askATFLink')

    try:
        if qa_html:
            qa = ''
            qa_content = qa_html[0].find_all('span')
            if qa_content:
                qa = qa_content[0].get_text()
                qa = int(''.join(filter(str.isdigit, qa)))
        else:
            qa = ''
    except:
        print('qa')

    score = soup.select('i[class*="a-icon a-icon-star a-star-"] span')

    try:
        if score:
            review_score_str = score[0].get_text().split(' ')[
                0].replace(",", ".")
            review_score = float(review_score_str)
        else:
            review_score = ''
    except:
        print('score')

    count = soup.select('#acrCustomerReviewText')
    try:
        if count:
            review_count = int(count[0].get_text().split(
                ' ')[0].replace(".", "").replace(',', ""))
        else:
            review_count = ''
    except:
        print('count')

    # checking if there is "Out of stock"
    try:
        soup.select('#availability .a-color-success')
        stock = 'Available'
    except:
        stock = 'Unavailable'
        print('stock')

    try:
        regex = re.compile('.*/bestsellers/.*')
        categories_html = soup.find_all("a", {"href": regex})

        if categories_html:
            if "Best Sellers Rank" not in str(categories_html[0].parent):
                categories = re.findall(
                    '#\d+\,*\d+', str(categories_html[1].parent))
            else:
                categories = re.findall(
                    '#\d+\,*\d+', str(categories_html[0].parent))
        else:
            categories = []
    except:
        categories = []
        print('categories')

    print(f'Name = {name}')
    print(f'ASIN = {product.loc["Asin"]}')
    print(f'Review_Score = {review_score}')
    print(f'Review_Count = {review_count}')
    print(f'QA = {qa}')
    print(f'Stock = {stock}')
    print(f'Categories = {categories}')
    print(f'Size categories = {len(categories)}')

    data = {
        'Account': product.loc['Account'],
        'SKU': product.loc['SKU'],
        'Name': name if name else '',
        'Status': 'Active',
        'ASIN': product.loc['Asin'],
        'Customer Reviews': review_count if review_count else '',
        'Q & A': qa if qa else '',
        'Reviews Rating': review_score if review_score else '',
        'Category': categories[0].replace('#', '') if categories else '',
        'Sub. Cat': categories[1].replace('#', '') if len(categories) >= 2 else '',
        'Sub.Cat2': categories[2].replace('#', '') if len(categories) >= 3 else '',
        'Available/Unavailable': stock,
    }

    missing = []
    for key, value in data.items():
        if value is None or value == '':
            missing.append(key)

    if missing:
        data['Comments'] = 'Lose ' + ', '.join(missing)
    else:
        data['Comments'] = ''

    return data


def create_report(callback):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=PATH, options=options)

    df = pd.DataFrame(
        columns=[
            'Account', 'SKU', 'Name', 'Status', 'ASIN', 'Customer Reviews',
            'Q & A', 'Reviews Rating', 'Category', 'Sub. Cat', 'Sub.Cat2',
            'Available/Unavailable', 'Comments'
        ]
    )

    data = {}

    try:
        set_delivery_to_nyc(driver)
        db = pd.read_excel('./reports/db2.xlsx')
        for (idx, row) in db.iterrows():
            df = df.append(get_product_data(
                driver, row), ignore_index=True)

        df.to_excel("./reports/asin_report.xlsx", index=False)

        send_report('asin_report')

    except Exception as e:
        print("except")
        print(e)

    finally:
        driver.close()
        callback()
