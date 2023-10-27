import requests
import requests as rq
from bs4 import BeautifulSoup as bs
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor


data = {}

# for i in range(1, 100):  # max is 6341
#     url = f'https://memeshappen.com/makeameme/{i}'
#     temp = rq.get(url)
#     soup = bs(temp.text, 'html.parser')
#     scripts = soup.find_all('script')
#     if scripts:
#         im = scripts[3].text.split(',')
#         image_name = im[40][5:-2]
#         data[i] = image_name
#         image = requests.get('https://s3.memeshappen.com/templates/' + image_name).content
#         with open(f'hmeme/{image_name}', 'wb') as handler:
#             handler.write(image)

url = f'https://memeshappen.com/makeameme/1'
temp = rq.get(url)
soup = bs(temp.text, 'html.parser')
scripts = soup.find_all('script')
if scripts:
    im = scripts[3]
    parser = Parser()
    tree = parser.parse(im)
    print(tree)