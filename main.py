import requests
import bs4
from fake_headers import Headers
import re
import json

def get_headers():
    return Headers(browser='firefox', os='win').generate()

def get_vacancy(page):
    url = 'https://spb.hh.ru/search/vacancy'
    params = {
        'area': (1, 2),
        'text': 'python',
        'page': page,
        'items_on_page': 20
    }

    hh_html = requests.get(url=url, params=params, headers=get_headers()).text
    hh_soup = bs4.BeautifulSoup(hh_html, features="html.parser")


    vacancys = hh_soup.find_all(class_='vacancy-serp-item-body__main-info')
    parsed_data = []
    for vacancy in vacancys:
        name_vacancy = vacancy.find('h3').text
        word = name_vacancy.split()
        words = ', '.join(word)
        words_list = re.findall(r"\w+-?w*", words)
        if ('Django' or 'Flask') in words_list:
            link_vacancy = vacancy.find('h3').find('span').find('a').attrs['href']
            company = vacancy.find_all(class_="bloko-text")[0].text
            city = vacancy.find_all(class_="bloko-text")[1].text
            try:
                salary = vacancy.find_all(class_="bloko-header-section-3")[1].text
            except:
                salary = 'Не указана'
            print(name_vacancy, link_vacancy, salary, company)
            parsed_data.append(
                {"вакансия": name_vacancy, "ссылка": link_vacancy,
                 "зарплата": salary.replace(' ', ''), "название компании": company.replace('NBSP', ''),
                 "город": city})
    with open('vacancys.json', 'a', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=5)

for page in range(0,3):
    get_vacancy(page)



