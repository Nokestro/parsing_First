import random
from time import sleep

from bs4 import BeautifulSoup
import requests
import json
import  csv

# url = 'https://health-diet.ru/table_calorie'
headers = {
    'Accept': '*/*',
    'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0"
}
#
# req = requests.get(url, headers=headers)
# src = req.text
# # print(src)
#
# with open('index.html', 'w', encoding='utf-8') as file:
#     file.write(src)
#
# with open('index.html', encoding='utf-8') as file:
#     src = file.read()
#
# all_categories_dict = {}
# soap = BeautifulSoup (src, 'lxml')
# all_products_href = soap.find_all(class_='mzr-tc-group-item-href')
# for item in all_products_href:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     # print(f"{item_text} : {item_href}")
#
#     all_categories_dict[item_text] = item_href
#
# # indent - отступы в json,  ensure_ascii - не экранирует символы, помогает при работе с кирилицей----------------------------------------------
#
# with open ('all_categories_dict.json', 'w', encoding='utf-8') as file:
#     json.dump(all_categories_dict, file, indent= 4, ensure_ascii= False)

with open("all_categories_dict.json", encoding='utf-8') as file:
    all_categories = json.load(file)


iterations_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iterations_count}")
for category_name, category_href in all_categories.items():

    rep = [' ', '-', ',' , "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')

    req = requests.get(url = category_href, headers=headers)
    src = req.text

    with open(f'data/{count}_{category_name}.html', 'w' , encoding='utf-8') as file:
        file.write(src)

    with open(f'data/{count}_{category_name}.html', encoding='utf-8') as file:
        src = file.read()

    soap = BeautifulSoup(src, 'lxml')

#Проверка страницы на наличие ссылок
    alert_block = soap.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

#Собираем заголовки таблимцы
    table_head = soap.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    cardohydrates = table_head[4].text

    with open(f"data/{count}_{category_name}.csv", 'w', encoding='utf-8') as file:
        writer =  csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                cardohydrates
            )
        )


    # Собираем данные таблимцы
    product_data = soap.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    product_info = []

    for item in product_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find('a').text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        cardohydrates = product_tds[4].text

        product_info.append(
            {
                "Title" : title,
                "Calories" : calories,
                "Proteins": proteins,
                "Fats": fats,
                "Cardohydrates": cardohydrates
            }
        )

        with open(f"data/{count}_{category_name}.csv", 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    cardohydrates
                )
            )

    with open(f"data/{count}_{category_name}.json", 'a', encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"# Итерация {count}. {category_name} записан...")
    iterations_count = iterations_count - 1

    if iterations_count == 0:
        print('Работа окончена')
        break

    print(f"Осталось итераций: {iterations_count}")
    sleep(random.randrange(2, 4))