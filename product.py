from bs4 import BeautifulSoup
import requests
import ipdb
import csv

Products = []

with open("./products.csv", 'r', encoding = 'utf8') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        result = requests.get(f'https://www.amazon.in/{row[-1]}')
        Products.append(result)


descriptionPattern = "a-unordered-list a-vertical a-spacing-mini"
featureListId = 'detailBullets_feature_div'
productDescId = 'productDescription'
techListId = 'productDetails_techSpec_section_1'


fields = ['Manufacturer', 'ASIN', 'Description', 'Product Description']

rows = []
rowCount = 0

for bag in Products:
    
    # try:
    doc = BeautifulSoup(bag.text, "html.parser") 
    
    descContent = doc.find_all(["ul"], class_=descriptionPattern, partial = False)
    desc = descContent[0].text if bool(descContent) else ''

    
    productDescContent = doc.find_all(["div"], id=productDescId, partial = False) 
    productDesc = productDescContent[0].text if bool(productDescContent) else ''
    
    featureList = doc.find_all(["div"], id=featureListId, partial = False)
    techList = doc.find_all(["table"], id = techListId, partial = False)
    addList = doc.find_all(["table"], id = "productDetails_detailBullets_sections1", partial = False)
    
    manufacturer = ''
    asin = ''
    
    if (bool(featureList)):
        
        manufacturer = featureList[0].select_one("div ul li:nth-of-type(3) span span:nth-of-type(2)").text
        asin = featureList[0].select_one("div ul li:nth-of-type(4) span span:nth-of-type(2)").text
    
    if (bool(addList)):
        asin = addList[0].find_all('tr')[0].text.split()[1]
    if(len(techList)>11):
        manufacturer = techList[0].find_all('tr')[11].text.split( )[1].strip()
    
    rows.append([manufacturer, asin, desc, productDesc])
    rowCount+=1
    print(rowCount, manufacturer)
    
# print(rows)
# ipdb.set_trace()
print("Products Scarped from link : ", len(rows))

with open('productDetails.csv', 'w', newline='', encoding="utf8") as file:
    writer = csv.writer(file)
     
    writer.writerow(fields)
    writer.writerows(rows)