import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from fake_useragent import UserAgent
from datetime import datetime

search_query="brooklyn+soap+company"


base_url="https://www.amazon.de/s?k="


url=base_url+search_query
url



headers = {
    'authority': 'www.amazon.de',
    'cache-control': 'max-age=0',
    'rtt': '50',
    'downlink': '10',
    'ect': '4g',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': UserAgent().random,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.amazon.de/',
    'accept-language': 'en-DE,en;q=0.9,de-DE;q=0.8,de;q=0.7,en-US;q=0.6',
    'cookie': 'ubid-acbde=262-7631081-6877614; amznacsleftnav-46ad9bae-2ee0-30ee-8ad1-44d02e45d1ed=1,12,11,15; session-id=258-1332037-6744063; x-acbde=R7qNAWtB8Rcqj3pzpXMxVdUiFxG3Lssq; at-acbde=Atza^|IwEBIGNzF70URnoMqLEJDAPec_CHeyoiA2f_E9uJByCWfDEaZl9egoQQp8EYs9Xbk3BD37GdYI_s3CMATmTT95wf2zEZoH4FYAn6e8GcGPQYd7Pp1PjXimAWyk-rS61FRUMpWOPKHK3yXRcgW9EkhElLkXmwKwCzROXb0NsgbOfrBGk3yQHp0aIqY5M2xgEzOPvnTkhrXxNwVucuuhXVqdYuIiUl; sess-at-acbde=^\\^PlR8cPO3JcczBHpUR+7WQ88TH5cHfAwNU15nLeCJxCk=^\\^; sst-acbde=Sst1^|PQGeoXc6nNKDzmPrciYvh711CXyN6O7p_Bq1jylxSTVhwX8665Atsub6qRsypQJS-4vZE6S7vrIsv-4sS6o90vJBRRDpxYGWouWR5D2RWyUuuO0BAEzh0vdCCNuPISZQVQN1u2phawj9-0fzFZaFImrMGIsiZnijis1SWKsnVgpOH0TpjjDJVvsuDNnwSUgxUQkNrBwJuvwLYfLCCZxUiNkQR_OcN5C8oa5WvClyIAFysOKIzIM59lKg3a4Oa6m2yiUg8tCJ7WTmR3rEIANt9Bvu1t6WrWdIMH7-UGvztpzmVyw; s_vnum=2027427679216^%^26vn^%^3D4; s_nr=1617036605322-Repeat; s_dslv=1617036605324; lc-acbde=en_GB; i18n-prefs=EUR; session-token=^\\^4xs0d0ZcmVD23j2vMKhu2i9WRSV2Zsj7YZzps+OC2OqKzM5UNEPKVfwVIVH82Bt8JEdbq1NtWqJeDKPcz7h4Ny9QD52HYFssc5kJVH+g9ivVM25uEcwEW+nGzCHCXG6mQ4eZApz2Hjv1iyM+jfHv1rP63RnoghXYKfv8/QGOVriAkUN2e4vkopgfIczo4CmXxw18azpzHdj1MO6PgmqQaQ==^\\^; session-id-time=2082754801l; csm-hit=tb:49MQEX0NZFRK85PNKTNN+s-GAYYH66JWZG1704B4NTP^|1628633522318&adb:adblk_yes&t:1628633522318',
}


search_response=requests.get(url,headers=headers)


search_response.status_code



search_response.text



search_response.cookies



cookie={}
def getAmazonSearch(search_query):
    url="https://www.amazon.de/s?k="+search_query
    print(url)
    page=requests.get(url,headers=headers)
    if page.status_code==200:
        return page
    else:
        return "Error"


def Searchasin(asin):
    url="https://www.amazon.de/dp/"+asin
    print(url)
    page=requests.get(url,cookies=cookie,headers=headers)
    if page.status_code==200:
        return page
    else:
        return "Error"


def Searchreviews(review_link):
    url="https://www.amazon.de"+review_link
    print(url)
    page=requests.get(url,cookies=cookie,headers=headers)
    if page.status_code==200:
        return page
    else:
        return "Error"


product_names=[]
response=getAmazonSearch('brooklyn+soap+company')
soup=BeautifulSoup(response.content, 'html.parser')
for i in soup.findAll("span",{'class':'a-size-base-plus a-color-base a-text-normal'}): # the tag which is common for all the names of products
    product_names.append(i.text)


product_names

print(len(product_names))

data_asin=[]
response=getAmazonSearch('brooklyn+soap+company')
soup=BeautifulSoup(response.content, 'html.parser')
for i in soup.findAll("div",{'class':'sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'}):
    data_asin.append(i['data-asin'])
    #print(soup)


print(response.status_code)

#data_asin

print(len(data_asin))


link=[]
for i in range(len(data_asin)):
    response=Searchasin(data_asin[i])
    soup=BeautifulSoup(response.content, 'html.parser')
    for i in soup.findAll("a",{'data-hook':'see-all-reviews-link-foot'}):
        link.append(i['href'])



len(link)


link

reviewlist=[]
reviewsraw=[]

for j in range(len(link)):
    for k in range(1, 3):
        response = Searchreviews(link[j]+'&pageNumber='+str(k))
        soup = BeautifulSoup(response.content, 'html.parser')
        reviewsraw = soup.findAll("div",{'class':'a-section review aok-relative'})
        try:
            for item in reviewsraw:
                review_country = item.find("span", {'class': 'a-size-base a-color-secondary review-date'}).text.strip().split(" ")
                date = item.find("span", {'class': 'a-size-base a-color-secondary review-date'}).text.replace("Reviewed in Germany on ", "").strip()
                review_date = datetime.datetime.strptime(date, '%d %B %Y')
                review = {
                    'Produkt': soup.title.text.replace("Amazon.de:Customer Reviews: ", "").strip(),
                    'ASIN': data_asin[j],
                    'Rezensent': item.find("span", {'class': 'a-profile-name'}).text.strip(),
                    'Datum': review_date,
                    #'Datum': item.find("span", {'class': "a-size-base a-color-secondary review-date"}).text.replace("Reviewed in Germany on ", "").strip(),
                    'Land': review_country[2],
                    'Rezensionstitel': item.find("a", {'class': 'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'}).text.strip(),
                    'Bewertung': float(item.find("a", {'class': 'a-link-normal'}).text.replace(" out of 5 stars", "").strip()),
                    'Rezensionstext': item.find("span", {'class': 'a-size-base review-text review-text-content'}).text.strip(),
                }
                reviewlist.append(review)
        except:
            pass

print(reviewlist)
print(reviewsraw)


len(reviewlist)



review_data = pd.DataFrame.from_dict(reviewlist)
review_data.to_excel('20211221_scrape.xlsx', index = False)
print("Done.")

'''
review_data.head(5)


review_data.shape

review_data.to_csv('Scraping reviewstitle.csv')
'''