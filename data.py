

import pandas
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier

trips_data_girl=pandas.read_excel("table/data-6269-2020-10-16.xlsx", index_col=0)

x=trips_data_girl.Name
pol=[]
last=[]
for i in trips_data_girl.Name:
  pol.append("Woman")
  last.append(i[-2:])
trips_data_girl['POL']=pol
trips_data_girl['LAST']=last

trips_data_man=pandas.read_excel("table/Boys.xlsx", index_col=0)

x=trips_data_man.Name
pol=[]
last=[]
for i in trips_data_man.Name:
  pol.append("Man")
  last.append(i[-2:])

trips_data_man['POL']=pol
trips_data_man['LAST']=last
s=trips_data_man.append(trips_data_girl)

trips_data_girl.LAST.value_counts()

trip=trips_data_girl[['NumberOfPersons', 'LAST']]
k1=trips_data_girl.LAST.sort_values().to_list()
k1=set(k1)
k1=sorted(list(k1))
k=trip.groupby('LAST')['NumberOfPersons'].sum().to_list()

tripm=trips_data_man[['NumberOfPersons', 'LAST']]
km1=trips_data_man.LAST.sort_values().to_list()
km1=set(km1)
km1=sorted(list(km1))
km=tripm.groupby('LAST')['NumberOfPersons'].sum().to_list()
#______________________________________________________________________________



# Построение графиков
#_______________________________________________________________________________

def GrWoman():
  plt.figure(figsize=(20, 20))
  plt.subplot(2, 1, 1)
  plt.plot(k1, k)          # построение графика
  plt.title("Зовисимость окончание имени от пола (женщины)") # заголовок
  plt.grid(True)
  plt.savefig('Графики/График женщины')              # включение отображение сетки

def GrMan():
  plt.figure(figsize=(20, 20))
  plt.subplot(2, 1, 2)
  plt.plot(km1, km)
  plt.title("Зовисимость окончание имени от пола (Мужчины)")
  plt.grid(True)
  plt.savefig('Графики/График мужчины')

#_____________________________________________________________________________

GrMan()

#Объеденение данных
s=pandas.get_dummies(s, columns=['LAST'])

model=RandomForestClassifier()
X=s.drop(['Name','Year', 'NumberOfPersons','global_id', 'Month','POL', ], axis=1)
Y=s.POL

model.fit(X,Y)

def ask (Name, example):# функция для уважительного ответа
  name=Name[-2:]
  example['LAST_'+name]=[1]
  table=pandas.DataFrame(example)
  if model.predict(table)=='Man':
    return 'Уважаемый '+Name
  else:
    return 'Уважаемая '+Name


for i in range(3):
  print(ask(input("Введите имя: "), {col:[0] for col in X.columns}))
