import re
import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_product_data(product):
    url = 'http://www.amazon.com/dp/product/' + product['asin']

    HEADERS = (
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }
    )

    html = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(html.content, features="lxml")

    # Product information
    name = soup.find(id='productTitle').get_text().strip()

    asin = soup.select(".askAsin")[0].get('value')

    qaHtml = soup.select('#askATFLink')

    if qaHtml:
        qa = qaHtml[0].find_all('span')[0].get_text()
        qa = int(''.join(filter(str.isdigit, qa)))
    else:
        qa = ''

    score = soup.select('i[class*="a-icon a-icon-star a-star-"]')

    if score:
        review_score = float(
            score[0].get_text().split(' ')[0].replace(",", ".")
        )
    else:
        review_score = ''

    count = soup.select('#acrCustomerReviewText')

    if count:
        review_count = int(count[0].get_text().split(
            ' ')[0].replace(".", "").replace(',', ""))
    else:
        review_count = ''

    # checking if there is "Out of stock"
    try:
        soup.select('#exportAlternativeContentTitle')[0].get_text().strip()
        stock = 'Available'
    except:
        # if there is any error in the previous try statements, it means the product is available
        stock = 'Out of Stock'

    regex = re.compile('.*/bestsellers/.*')
    categoriesHtml = soup.find_all("a", {"href": regex})

    if "Best Sellers Rank" not in str(categoriesHtml[0].parent):
        categories = re.findall('#\d+\,*\d+', str(categoriesHtml[1].parent))
    else:
        categories = re.findall('#\d+\,*\d+', str(categoriesHtml[0].parent))

    print(f'Name = {name}')
    print(f'ASIN = {asin}')
    print(f'Review_Score = {review_score}')
    print(f'Review_Count = {review_count}')
    print(f'QA = {qa}')
    print(f'Stock = {stock}')
    print(f'Categories = {categories}')
    print(f'Size categories = {len(categories)}')

    data = {
        'Account': product['account'],
        'SKU': product['sku'],
        'Name': name if name is not None else '',
        'Status': 'Active',
        'ASIN': product['asin'],
        'Customer Reviews': review_count if review_count is not None else '',
        'Q & A': qa if qa is not None else '',
        'Reviews Rating': review_score if review_score is not None else '',
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

    # 'https://towardsdatascience.com/scraping-multiple-amazon-stores-with-python-5eab811453a8'
    # 'https://www.youtube.com/watch?v=Bg9r_yLk7VY&feature=youtu.be'


def create_report():
    df = pd.DataFrame(
        columns=[
            'Account', 'SKU', 'Name', 'Status', 'ASIN', 'Customer Reviews',
            'Q & A', 'Reviews Rating', 'Category', 'Sub. Cat', 'Sub.Cat2',
            'Available/Unavailable', 'Comments'
        ]
    )
    data = {}
    try:

        with open('./reports/products2.json') as json_file:
            data = json.load(json_file)
        for product in data['products']:
            df = df.append(get_product_data(product), ignore_index=True)
            time.sleep(0.5)

        df.to_excel("./reports/asin2.xlsx", index=False)

    except Exception as e:
        print("except")
        print(e)
