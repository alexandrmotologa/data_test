from pyquery import PyQuery as pq
import json
from time import sleep

from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent': str(ua.random)}
ua.update()

cat_target = 'https://www.luxuryestate.com/france/ile-de-france/paris/paris'


def estatePage(target_url):
    try:
        document = pq(url=target_url, headers = headers)
        print(headers, 'pagina')
        heading = document('.item-max-width').find('h1').text()
        price = document('.hallmarks').find('.text-right').text()
        currency = document('.hallmarks').find('.selected').text()[2:5]
        specs = document('.hallmarks').find('.specs').text()[:6]
        specs = specs[:5] + '2'
        image = document('.small-gallery').find('#smallgallerypic1').attr('data-src')[2:]
        phone = document('.agency__contact').find('a').attr('data-track-phone-value')[::-1]
        return {
            'title': heading,
            'specs': specs,
            'image': image,
            'phone': phone,
            'price': price,
            'currency': currency,
        }
    except :
        pass


def estateCategory(target_url):

    document = pq(url=target_url, headers = headers)
    print(headers, 'category')
    adds = []
    links_to_ads = document('.details').find('.details_title')

    for link in links_to_ads:
        try:
            url = pq(link).find('a').attr('href')
            adds.append(estatePage(url))
            sleep(10)
        except :
            print('attribute error')

    return adds


with open('data.json', 'a', encoding='utf-8') as json_file:
    adds = estateCategory(cat_target)
    print(adds)
    json.dump(adds, json_file, indent=2, ensure_ascii=False)
