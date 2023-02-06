import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import json

def get_headers():
    headers = Headers(browser='firefox', os='win')
    return headers.generate()

HOST = 'https://spb.hh.ru/search/vacancy?text=python+django+flask&salary=&area=1&area=2&ored_clusters=true&enable_snippets=true'
response = requests.get(HOST, headers=get_headers())
response_text = response.text
soup = BeautifulSoup(response_text, features='lxml')
vacancy_list = soup.find('div', class_='vacancy-serp-content')
vacancies = vacancy_list.find_all('div', class_='vacancy-serp-item-body')
names = []
links = []
company_names = []
city_names = []
salaries = []
for vacancy in vacancies:
    hrefs = vacancy.find('a', class_='serp-item__title')
    for vacancy_name in hrefs:
        vacancy_name = vacancy_name.text
        names.append((vacancy_name))
    for link in hrefs:
        link = hrefs['href']
        links.append(link)

companies = vacancy_list.find_all('div', class_='vacancy-serp-item-company')
for company in companies:
    company = company.find('a', class_='bloko-link bloko-link_kind-tertiary')
    company_name = company.text
    company_names.append(company_name)


for city in companies:
    city = city.find(attrs={'class': 'bloko-text', 'data-qa': 'vacancy-serp__vacancy-address'})
    city_name = city.text.split(",")[0]
    city_names.append(city_name)


vacancies = vacancy_list.find_all('div', class_='vacancy-serp-item-body')
for salary in vacancies:
    salary = salary.find(attrs={'class': 'bloko-header-section-3', 'data-qa': 'vacancy-serp__vacancy-compensation'})
    if salary != None:
        salary_list = salary.contents
        salary_str = ",".join(salary_list)
        salary_amount = salary_str.replace(',', '').replace('  ', ' ')
    else:
        salary_amount = 'Зарплата не указана'
    salaries.append(salary_amount)

parsed = {names[i]: [links[i], company_names[i], city_names[i], salaries[i]] for i in range(len(names))}
pprint(parsed)
# json_data = json.load(parsed)
# json.dump(json_data, parsed, ensure_ascii=False, indent=4)
with open("hh.json", "w") as outfile:
    json.dump(parsed, outfile)





