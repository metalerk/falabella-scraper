#!/usr/bin/env python3

import json
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url = 'https://www.falabella.com.co/falabella-co/category/cat1660941/Celulares-y-Smartphones'

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options, executable_path='./geckodriver')
browser.get(url)

def get_bs_node_with_id(node_id, tag, classes):
    html = browser.find_element_by_id(node_id).get_attribute('innerHTML')
    doc = BeautifulSoup(html, features="lxml")
    return doc.find_all(tag, class_=classes)

def get_bs_node_from_html(html, tag, classes):
    doc = BeautifulSoup(html, features="lxml")
    return doc.find_all(tag, class_=classes)

def save_json(obj, filename):
    print('[+] Saving...')
    json.dump(obj, open(filename, 'w'), indent=4, ensure_ascii=False)
    print('[+] Saved.')

items_list = list()
for i in get_bs_node_with_id(
    node_id='testId-searchResults-products',
    tag='div',
    classes='jsx-1395131234 search-results-list'):
    item = dict()
    node = BeautifulSoup(str(i), features="lxml")
    images = node.find_all('img', class_='jsx-2487856160')
    item['images'] = list()
    for img in images:
        item['images'].append(img['src'])
    title = node.find('b', class_='jsx-287641535 title2 primary jsx-185326735 bold pod-subTitle')
    item['title'] = title.text
    vendor = node.find('b', class_='jsx-287641535 title4 primary jsx-185326735 normal pod-sellerText')
    item['vendor'] = vendor.text.replace('Por ', '')
    features = node.find_all('li', class_='jsx-4018082099')
    item['features'] = list()
    for f in features:
        item['features'].append(f.text)
    discount = node.find_all('div', class_='jsx-1231170568 pod-badges pod-badges-LIST')
    item['discount'] = list()
    for s in discount:
        amount = s.text
        if '%' in amount:
            amount = amount.replace(' ', '').replace('DCTO', '')
        item['discount'].append(amount)
    prices = node.find_all('li', class_='jsx-2556988298')
    item['prices'] = list()
    for p in prices:
        text = p.text.replace(' ', '').replace('$', '').replace('.', '')
        description = ''
        if '(Preciofinal)' in text:
            text = text.replace('(Preciofinal)', '')
            description = 'Final Price'
        obj = {
                'value': float(text),
                'description': description,
            }
            
        item['prices'].append(obj)
    items_list.append(item)
browser.quit()
save_json(items_list, 'falabella.json')