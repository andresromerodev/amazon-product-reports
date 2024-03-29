import re
import os
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as condition
from services.email_service import send_report

load_dotenv()

PYTHON_ENV = os.environ.get('PYTHON_ENV')
PATH = './drivers/chromedriver.exe'
LOCATION_COMPONENT_ID = 'nav-global-location-popover-link'
LOCATION_INPUT_ID = 'GLUXZipUpdateInput'
AMAZON_PRODUCT_URL = 'http://www.amazon.com/dp/product/'
AMAZON_US_URL = 'https://www.amazon.com/?ref=icp_country_us&language=en_US'
CATEGORIES_REGEX = '#\d+ in |#\d+\,*\d+ in'


def set_delivery_to_nyc(driver):
    driver.get(AMAZON_US_URL)

    # To ensure the page has fully loaded
    time.sleep(3) 

    location_popover = driver.find_element_by_id(LOCATION_COMPONENT_ID)
    location_popover.click()

    WebDriverWait(driver, 100).until(
        condition.element_to_be_clickable((By.ID, LOCATION_INPUT_ID)))

    location_field = driver.find_element_by_id(LOCATION_INPUT_ID)

    location_field.click()
    location_field.send_keys('10001')
    location_field.send_keys(Keys.RETURN)


def get_product_data(driver, product):
    url = AMAZON_PRODUCT_URL + product.loc['Asin']

    driver.get(url)

    # To ensure the page has fully loaded
    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        # Product Title
        name = soup.find(id='productTitle').get_text().strip()
    except:
        return dog_page(product)

    qa_html = soup.select('#askATFLink')
    qa_number = ''

    try:
        if qa_html:
            qa_content = qa_html[0].find_all('span')
            if qa_content:
                qa_number = qa_content[0].get_text()
                qa_number = int(''.join(filter(str.isdigit, qa_number)))
    except:
        print('Exception occurred with: QA')

    score = soup.select('i[class*="a-icon a-icon-star a-star-"] span')

    try:
        if score:
            review_score_str = score[0].get_text().split(' ')[
                0].replace(",", ".")
            review_score = float(review_score_str)
        else:
            review_score = ''
    except:
        print('Exception occurred with: Score')

    count = soup.select('#acrCustomerReviewText')
    try:
        if count:
            review_count = int(count[0].get_text().split(
                ' ')[0].replace(".", "").replace(',', ""))
        else:
            review_count = ''
    except:
        print('Exception occurred with: Count')

    # Out of Stock
    try:
        stock_html = soup.select('#availability')
        if 'In Stock' in str(stock_html):
            stock = 'Available'
        else:
            stock = 'Unavailable'
    except:
        stock = 'Unavailable'
        print('Exception occurred with: Stock')


    try:
        categories_html = soup.find_all('div', {'id': 'detailBulletsWrapper_feature_div'})

        if categories_html and 'Best Sellers Rank' in str(categories_html):
            categories = re.findall(CATEGORIES_REGEX, str(categories_html))
        else: # Amazon table view
            categories_html = soup.find_all('table', {'id': 'productDetails_detailBullets_sections1'})

            if categories_html and 'Best Sellers Rank' in str(categories_html):
                categories = re.findall(CATEGORIES_REGEX, str(categories_html))
            else:
                categories = []
    except:
        categories = []
        print('Exception occurred with: Categories')

    coupon = ''

    try:
        coupon_html = soup.find_all('div', {'id': 'vpcButton'})
        if coupon_html and 'coupon' in str(coupon_html):
            coupon = re.findall('\d%|\$\d.\d+', str(coupon_html))
    except:
        coupon = ''
        print('Exception occurred with: Coupon')

    try:
        ships_from_html = soup.find_all('span', {'id': 'tabular-buybox-truncate-0'})
        if ships_from_html:
            ships_from = re.findall(r'<span class="tabular-buybox-text">(.*?)</span>', str(ships_from_html))
        else:
            ships_from = ''
    except:
        ships_from = ''
        print('Exception occurred with: ships_from')

    try:
        sold_by_html = soup.find_all('a', {'id': 'sellerProfileTriggerId'})
        if sold_by_html:
            sold_by = re.findall(r'">(.*?)</a>', str(sold_by_html))
        else:
            sold_by = ''
    except:
        sold_by = ''
        print('Exception occurred with: sold_by')

    data = {
        'Account': product.loc['Account'],
        'Type': product.loc['Type'] if product.loc['Type'] else '',
        'Code': product.loc['Code'] if product.loc['Code'] else '',
        'SKU': product.loc['SKU'],
        'Name': name if name else '',
        'Status': 'Active',
        'ASIN': product.loc['Asin'],
        'Customer Reviews': review_count if review_count else '',
        'Q & A': qa_number if qa_number else '',
        'Reviews Rating': review_score if review_score else '',
        'Category': categories[0].replace('#', '').replace(',', '').replace(' in', '').strip() if categories else '',
        'Sub. Cat': categories[1].replace('#', '').replace(',', '').replace(' in', '').strip() if len(categories) >= 2 else '',
        'Sub.Cat2': categories[2].replace('#', '').replace(',', '').replace(' in', '').strip() if len(categories) >= 3 else '',
        'Available/Unavailable': stock,
        'Coupon': coupon[0] if len(coupon) > 0 else '',
        'Ships From': ships_from[0] if len(ships_from) > 0 else '',
        'Sold By': sold_by[0] if len(sold_by) > 0 else ''
    }

    missing = []
    for key, value in data.items():
        if value is None or value == '':
            missing.append(key)

    if missing:
        data['Comments'] = 'No ' + ', '.join(missing)
    else:
        data['Comments'] = ''

    return data


def create_report(on_report_success, on_report_failure):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=PATH)

    df = pd.DataFrame(
        columns=[
            'Account', 'Type', 'Code', '', 'SKU', 'Name', 'Status', 'ASIN',
            'Customer Reviews', 'Q & A', 'Reviews Rating', 'Category', 'Sub. Cat',
            'Sub.Cat2', 'Available/Unavailable', 'Coupon', 'Ships From', 'Sold By', 'Comments'
        ]
    )

    try:
        set_delivery_to_nyc(driver)

        if PYTHON_ENV == 'development':
            db = pd.read_excel('./database/database_development.xlsx')
        elif PYTHON_ENV == 'production':
            db = pd.read_excel('./database/database.xlsx')

        for (idx, row) in db.iterrows():
            print(f'\nProduct # {idx + 1}')
            product_data = get_product_data(driver, row)
            print(json.dumps(product_data, indent=4))
            df = df.append(product_data, ignore_index=True)

        df.to_excel("./reports/asin_report.xlsx", index=False)

        send_report('asin_report.xlsx')

        on_report_success()

    except Exception as e:
        on_report_failure(e)

    finally:
        driver.close()


def dog_page(product):
    return {
        'Account': product.loc['Account'],
        'Type': product.loc['Type'] if product.loc['Type'] else '',
        'Code': product.loc['Code'] if product.loc['Code'] else '',
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
        'Coupon': '',
        'Ships From': '',
        'Sold By': '',
        'Comments': 'Dog Page'
    }
