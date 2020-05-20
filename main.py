import requests
from pyquery import PyQuery as pq
import time
import random
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

inn = list(set(['7813341546', '7810245940']))

base_url = 'https://www.list-org.com'


def get_link(index, element):
    return element.attrib['href']


output_data = {}

start_time = time.time()

for inn_ in inn:
    time.sleep(random.randint(0, 5000) / 1000)
    html = requests.get('https://www.list-org.com/search?type=inn&val={}'.format(inn_), headers=headers).text
    doc = pq(html)
    links = list(doc('.org_list a').map(get_link))
    output_data.update({
        inn_: {}
    })
    for link in links:
        company_html = requests.get(base_url + link, headers=headers).text
        company_doc = pq(company_html)
        company_name = company_doc('a.upper:first').text()
        data = {r.split(':')[0]: r.split(':')[1][1:] for r in
                list(company_doc('.tt:first tr').map(lambda i, e: pq(e).text()))}

        output_data[inn_].update({
            company_name: data
        })

        print('{}: {}'.format(inn_, company_name))

print('{} secs elapsed!'.format(time.time() - start_time))

with open('output_data.json', 'w', encoding='utf-8') as file:
    json.dump(output_data, file, ensure_ascii=False)
