import requests as rq
from bs4 import BeautifulSoup as bs

for i in range(1, 6341):  # max is 6341
    url = f'https://memeshappen.com/makeameme/{i}'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    temp = rq.get(url, headers=headers)
    soup = bs(temp.text, 'html.parser')
    scripts = soup.find_all('meta')
    if len(scripts) > 9:
        image_url = scripts[9]['content']
        image = rq.get(image_url).content
        try:
            with open(f'hmeme/{i} - {image_url[37:]}', 'wb') as handler:
                handler.write(image)
        except OSError:
            print("Ahmed is retarded")
        else:
            print(f'ID: {i} found!')