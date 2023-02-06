import requests
from lxml import html

url = 'https://ivypanda.com/essays/customer-loyalty-in-the-gas-manufacturing-industry/'
response = requests.get(url, headers={'User-Agent':''})
print(response.content)


# Parsing the response as an HTML document
#tree = html.fromstring(cont)

# Extracting the elements using the specified xpath
#elements = tree.xpath('//*[contains(@class,"article__content")]/*[self::h2 or self::h3 or self::p]')

# Printing the extracted elements
#for element in elements:
#    print(element.text)