from bs4 import BeautifulSoup
import requests
import ipdb
import csv



# print(result)
# doc = BeautifulSoup(result.text, "html.parser") 

Requests = []

page = 1
while page<=20:
    url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1&page={page}'
    result = requests.get(url)
    Requests.append(result)
    page+=1

print(len(Requests))

# with open("./scraper.html", encoding="utf8") as fp:
#     doc = BeautifulSoup(fp, 'html.parser')




classToFind = 'a-section a-spacing-small a-spacing-top-small'
namePattern = 'a-size-medium a-color-base a-text-normal'
pricePattern = 'a-price-whole'
ratingValuePattern = 'a-size-base'
ratingCountPattern = 'a-size-base s-underline-text'
targetLinkPattern = 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'

fields = ['Name', 'Price', 'Rating', 'RatingCount', 'ProductLink']

rows = []

reqCount = 1
error = ()

for req in Requests:
    doc = BeautifulSoup(req.text, "html.parser") 

    bagCount = 0
    
    bags = doc.find_all(["div"], class_=classToFind, partial = False)
    # print(bags)
    for bag in bags[1:]:
        try:
            List = bag.children
            # Name, Price, Rating
            NameTag = next(List)
            RatingTag = next(List)
            PriceTag = next(List)
            
            Name = NameTag.find_all(["span"], class_ = namePattern, partial = False)[0].text
            # print(Name)
            
            Price = PriceTag.find_all(["span"], class_= pricePattern, partial = False)[0].text
            Rating = RatingTag.find_all(["span"], class_ = ratingValuePattern, partial = False)[0].text
            RatingCount = RatingTag.find_all(["span"], class_ = ratingCountPattern, partial = False)[0].text
            ProductLink = NameTag.find_all(["a"], class_ = targetLinkPattern, partial = False)[0]['href']
            
            rows.append([Name, Price, Rating, RatingCount, ProductLink])

            bagCount +=1
        except:
            error = (bagCount, reqCount)
            
    reqCount +=1
# print(rows)
# ipdb.set_trace()
print("Products Scarped from link : ", len(rows))

with open('products.csv', 'w', newline='', encoding="utf8") as file:
    writer = csv.writer(file)
     
    # writer.writerow(fields)
    writer.writerows(rows)