# парсинг ОКРБ
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pandas
html_doc = "https://inform.best/page/OKPby.html"
# Выгрузка с страницы сайта блока <div> с перечнем всех значений ОКРБ
soup = BeautifulSoup(urlopen(html_doc), 'html.parser')
item = soup.find_all('div', class_="main")
rezult: list = []
#Вставка в список кода и значения каждого значения
for elem in item:
      #print(elem.find_all('span'))
      test = str(elem.find_all('span'))
      start = 0
      finish = 0
      #print(type(test))
      for i in range(len(test)):
            #print(i)
            #print(type(str(i)))
            if test[i] == '>':

                  start = i+1
                  #print(start)
            elif test[i] == '/':
                  finish = i-1
                  #print(type(finish))
                  rezult.append(str(test[start:finish]))

#Создание словоря где клю = коду ОКРБ, параметр = наименование ОКРБ
dict_OKRB = {}
for elem in rezult:
      dict_OKRB[elem[0:elem.index(' ')-1]] = elem[elem.index(' ') + 1:]

list_rezult = [[key, value] for key, value in dict_OKRB.items()]
print(list_rezult[0:4])
# Определение и Добавление вышестоящего уровня к наименованию
alfa = []
for index in range(len(list_rezult)-1):
      print(list_rezult[index][0])
      if list_rezult[index][0].isalpha():
            #list_rezult[index+1].append(list_rezult[index][0])
            alfa = list_rezult[index][0]
            count = 1
            try:
                  while not list_rezult[index + count][0].isalpha():
                        if len(list_rezult[index + count][0]) == 2:
                              print(1)

                              print(len(list_rezult[index + count]))
                              list_rezult[index + count].append(alfa[0])
                        count += 1
            except TypeError:
                  print("Конец списка")

            except IndexError:
                  print('Конец списка')
      else:
            count = 1
            try:
                  while not list_rezult[index + count][0].isalpha():

                        if len(list_rezult[index][0]) + 1 == len(list_rezult[index+count][0]) and \
                           len(list_rezult[index+count]) == 2 and list_rezult[index][0] in list_rezult[index+count][0]:
                              list_rezult[index + count].append(list_rezult[index][0])

                        elif len(list_rezult[index][0]) + 2 == len(list_rezult[index+count][0]) and \
                             len(list_rezult[index+count]) == 2 and list_rezult[index][0] in list_rezult[index+count][0]:
                              list_rezult[index + count].append(list_rezult[index][0])

                        elif len(list_rezult[index][0]) == 8 and \
                             len(list_rezult[index+count]) == 2 and list_rezult[index][0] in list_rezult[index+count][0]:
                              list_rezult[index + count].append(list_rezult[index][0])

                        count += 1
            except TypeError:
                  print("Конец списка")

            except IndexError:
                  print('Конец списка')


dict_list_rezult = {}
#выгрузка из списка
for elem in list_rezult:
      dict_list_rezult[elem[0]] = elem[1:]
print('печать')
data_to_excel_OKRB = pandas.DataFrame.from_dict(dict_list_rezult, orient='index')
data_to_excel_OKRB.to_excel('testOKRB.xlsx')
print('конец')
