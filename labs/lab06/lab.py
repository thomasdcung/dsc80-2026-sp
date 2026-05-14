# lab.py


import os
import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')
import requests
import bs4
import lxml


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def question1():
    """
    NOTE: You do NOT need to do anything with this function.
    The function for this question makes sure you
    have a correctly named HTML file in the right
    place. Note: This does NOT check if the supplementary files
    needed for your page are there!
    """
    # Don't change this function body!
    # No Python required; create the HTML file.
    return


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------
 
def extract_book_links(page_html):

    soup = bs4.BeautifulSoup(page_html, features='lxml')
    links = []
 
    for article in soup.find_all('article', class_='product_pod'):
        
        rating_tag = article.find('p', class_='star-rating')
        rating_word = rating_tag['class'][1]
        rating = RATING_MAP.get(rating_word, 0)
        if rating < 4:
            continue
 
        price_text = article.find('p', class_='price_color').get_text(strip=True)
        price_str = ''.join(c for c in price_text if c.isdigit() or c == '.')
        price = float(price_str)
        if price >= 50:
            continue
 
        a_tag = article.find('h3').find('a')
        href = a_tag['href']
        links.append(href)
 
    return links
 
 
def get_product_info(page_html, categories):

    soup = bs4.BeautifulSoup(page_html, features='lxml')
 
    breadcrumbs = soup.find('ul', class_='breadcrumb').find_all('li')
    category = breadcrumbs[-2].get_text(strip=True)
 
    if category not in categories:
        return None
 
    rating_tag = soup.find('p', class_='star-rating')
    rating = rating_tag['class'][1]

    title = soup.find('div', class_='product_main').find('h1').get_text(strip=True)
 
    desc_div = soup.find('div', id='product_description')
    if desc_div:
        description = desc_div.find_next_sibling('p').get_text(strip=True)
    else:
        description = ''
 
    table = soup.find('table', class_='table table-striped')
    info = {}
    for row in table.find_all('tr'):
        key = row.find('th').get_text(strip=True)
        val = row.find('td').get_text(strip=True)
        info[key] = val
 
    result = {
        'UPC': info.get('UPC', ''),
        'Product Type': info.get('Product Type', ''),
        'Price (excl. tax)': info.get('Price (excl. tax)', ''),
        'Price (incl. tax)': info.get('Price (incl. tax)', ''),
        'Tax': info.get('Tax', ''),
        'Availability': info.get('Availability', ''),
        'Number of reviews': info.get('Number of reviews', ''),
        'Category': category,
        'Rating': rating,
        'Description': description,
        'Title': title,
    }
    return result
 
 
def scrape_books(k, categories):
    """
    Scrape the first k pages of books.toscrape.com and return a DataFrame of
    books that have ≥4-star rating, price < £50, and category in `categories`.
    """
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    book_base = 'http://books.toscrape.com/catalogue/'
 
    rows = []
    for page_num in range(1, k + 1):
        page_url = base_url.format(page_num)
        resp = requests.get(page_url)
        page_html = resp.text
 
        links = extract_book_links(page_html)
        for link in links:
            book_url = book_base + link
            book_resp = requests.get(book_url)
            info = get_product_info(book_resp.text, categories)
            if info is not None:
                rows.append(info)
 
    if rows:
        return pd.DataFrame(rows)
    else:
        return pd.DataFrame(columns=[
            'UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)',
            'Tax', 'Availability', 'Number of reviews', 'Category',
            'Rating', 'Description', 'Title'
        ])



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------
 
def stock_history(symbol, year, month):

    start = pd.Timestamp(year=year, month=month, day=1)
    end = start + pd.offsets.MonthEnd(1)
    from_date = start.strftime('%Y-%m-%d')
    to_date = end.strftime('%Y-%m-%d')
 
    url = (
        f'https://financialmodelingprep.com/stable/historical-price-eod/full'
        f'?symbol={symbol}&from={from_date}&to={to_date}&apikey={FMP_API_KEY}'
    )
    resp = requests.get(url)
    data = resp.json()
 
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict) and 'historical' in data:
        df = pd.DataFrame(data['historical'])
    else:
        raise KeyError(f"Unexpected API response: {data}")
 
    return df
 
 
def stock_stats(df):

    df = df.sort_values('date', ascending=True).reset_index(drop=True)
 
    start_price = df.iloc[0]['open']
    end_price = df.iloc[-1]['close']
    pct_change = (end_price - start_price) / start_price * 100
 
    sign = '+' if pct_change >= 0 else ''
    pct_str = f'{sign}{pct_change:.2f}%'
 
    df['avg_price'] = (df['high'] + df['low']) / 2
    df['daily_volume_dollars'] = df['volume'] * df['avg_price']
    total_volume_billions = df['daily_volume_dollars'].sum() / 1e9
    vol_str = f'{total_volume_billions:.2f}B'
 
    return (pct_str, vol_str)



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------
 
def _fetch_item(item_id):

    resp = requests.get(HN_URL.format(item_id))
    return resp.json()
 
 
def _collect_comments(item_id, rows):

    item = _fetch_item(item_id)
    if item is None:
        return
    if item.get('dead', False):
        return
    if item.get('deleted', False):
        return
 
    row = {
        'id': item.get('id'),
        'by': item.get('by', ''),
        'text': item.get('text', ''),
        'parent': item.get('parent'),
        'time': pd.Timestamp(item.get('time', 0), unit='s'),
    }
    rows.append(row)
 
    for child_id in item.get('kids', []):
        _collect_comments(child_id, rows)
 
 
def get_comments(storyid):

    story = _fetch_item(storyid)
    rows = []
    for kid_id in story.get('kids', []):
        _collect_comments(kid_id, rows)
 
    df = pd.DataFrame(rows, columns=['id', 'by', 'text', 'parent', 'time'])
    return df.reset_index(drop=True)
