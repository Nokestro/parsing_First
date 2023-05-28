import re

from bs4 import BeautifulSoup
with open('phelp.html', encoding="utf-8") as file:
    src = file.read()

bs = BeautifulSoup(src, "lxml")


# Вывод title
# title = bs.title
# print(title)
# print(title.text)
# print(title.string)

# .find() - первый попавшийся вариант сверху, .find_all() - все совпадения
# soap = bs.find('h1')
# print(soap)
#
# soap_all = bs.find_all('h1')
# print(soap_all)
#
# for item in soap_all:
#     print(item.text)

#Поиск по классу

# soap_class = bs.find('div', class_= 'user__name')
# print(soap_class.text.strip())


# user_name = bs.find('div', class_= 'user__name').find('span').text
# print(user_name)


#Передача словаря

# user_name = bs.find("div", { "class" :"user__name" }).find('span').text


#find_parants() , find_parants() - поиск снизу вверх


#.next_element(), previous_element()

#.find_next_sibling(), .find_prevuous_sibling()

# метод re.complite = ('Одежда') - парсинг по слову

cloth = bs.find(string=re.compile("(Одежда)"))
print(cloth)

cloth = bs.find_all(string=re.compile("([Оо]дежда)"))
print(cloth)