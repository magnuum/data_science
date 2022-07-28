# -*- coding: utf-8 -*-
"""corona_science.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uwxaSdhyK6SjyGjU_WvyLf89VV5rnbp4
"""

#Wczytanie potrzebnych bibliotek
import pandas as pd
import plotly.express as px
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

#Pobranie danych z wybranego pliku csv, zawierającego dane o koronawirusie na świecie
url= f"https://covid.ourworldindata.org/data/ecdc/full_data.csv"
df = pd.read_csv(url, error_bad_lines=False)

#Funkcja służąca do ustawienia odpowiedniego formatu daty
#Przykładowe wywołanie: format_data(datetime.date(2020,3,26))
def format_data(date: datetime.date):
  return date.strftime('%Y-%#m-%#d')

#Funkcja pokazująca na mapie świata przyrost śmierci w poszczególnych krajach na skutek COVID-19
#Przykładowe wywołanie: new_deaths(datetime.date(2020,3,26))
def new_deaths(date: datetime.date):

  #Ustawienie daty w odpowiednim formacie 
  data = format_data(date)

  #Wybranie danych z tabeli o odpowiedniej dacie i pogrupowanie ich pod wzgędam krajów, oraz wyrzucenie wiersza z danymi o świecie
  formated_gdf = df.loc[df["date"]==data].groupby("location").max().drop("World")
  formated_gdf = formated_gdf.reset_index()

  #Stworzenie definicji figury mapy świata z danymi o nowych śmierciach
  fig = px.choropleth(formated_gdf, locations="location", locationmode='country names', 
                     color="new_deaths", hover_name="location", 
                     range_color= [0, max(formated_gdf['new_deaths'])], 
                     projection="natural earth", color_continuous_scale=px.colors.sequential.Cividis_r,  
                     title='Przyrost przypadków śmierci na skutek COVID-19 na swiecie')
  
  #Wyświetlenie mapy
  fig.show()

#Wywołanie funkcji new_deaths
new_deaths(datetime.date(2020,3,26))

#Funkcja pokazująca na mapie świata przyrost przypadków zachorowań na COVID-19 w poszczególnych krajach
#Przykładowe wywołanie: new_cases(datetime.date(2020,3,26))
def new_cases(date: datetime.date):

  #Ustawienie daty w odpowiednim formacie 
  data = format_data(date)

  #Wybranie danych z tabeli o odpowiedniej dacie i pogrupowanie ich pod wzgędam krajów, oraz wyrzucenie wiersza z danymi o świecie
  formated_gdf = df.loc[df["date"]==data].groupby("location").max().drop("World")
  formated_gdf = formated_gdf.reset_index()

  #Stworzenie definicji figury mapy świata z danymi o nowych przypadkach zarażenia
  fig = px.choropleth(formated_gdf, locations="location", locationmode='country names', 
                     color="new_cases", hover_name="location", 
                     range_color= [0, max(formated_gdf['new_cases'])], 
                     projection="natural earth", color_continuous_scale=px.colors.sequential.Cividis_r,  
                     title='Przyrost przypadków zachorowań na COVID-19 na swiecie')
  
  #Wyświetlenie mapy
  fig.show()

#Wywołanie funkcji new_cases
new_cases(datetime.date(2020,3,26))

#Funkcja pokazująca na mapie świata stosunek śmierci do zachorowań na skutek COVID-19 
#Przykładowe wywołanie: deaths_to_cases(datetime.date(2020,3,26))
def deaths_to_cases(date: datetime.date):

  #Ustawienie daty w odpowiednim formacie
  data = format_data(date)

  #Wybranie danych z tabeli o odpowiedniej dacie i pogrupowanie ich pod wzgędam krajów, oraz wyrzucenie wiersza z danymi o świecie
  formated_gdf = df.loc[df["date"]==data].groupby("location").max().drop("World")
  formated_gdf = formated_gdf.reset_index()

  #Dodanie do DataFramu nowej kolumny z danymi stosunku śmierci do przypadków
  formated_gdf["proportion"] = formated_gdf["total_cases"]/formated_gdf["total_deaths"]

  #Stworzenie definicji figury mapy świata z danymi o stosunku śmierci do przypadków
  fig = px.choropleth(formated_gdf, locations="location", locationmode='country names', 
                     color="proportion", hover_name="location", 
                     range_color= [0, max(formated_gdf['proportion'])], 
                     projection="natural earth", color_continuous_scale=px.colors.sequential.Cividis_r,  
                     title='Stosunek śmierci do przypadków COVID19 na swiecie')
  
  #Wyświetlenie mapy
  fig.show()

#Wywołanie funkcji new_cases
deaths_to_cases(datetime.date(2020,3,26))

#Funkcja zwracająca tabelę z oszacowanymi danymi na temat śmierci i zarażonych na COVID-19 na najbliższe 5 dni w danym kraju 
#Przykładowe wywołanie: predict_cases("Italy")
def predict_cases(country):

  #Utworznie DataFramu z danymi z ostatnich 10 dni w danym kraju
  frame = df.loc[df["location"]==country].tail(10).drop("location", axis=1).reset_index(drop=True)

  #Utworzenie danych treningowych potrzebnych do modelu regresji liniowej
  x = []
  for i,row in frame.iterrows():
    x.append(i)
  y_t_cases = frame["total_cases"]
  y_t_deaths = frame["total_deaths"]
  y_n_cases = frame["new_cases"]
  y_n_deaths = frame["new_deaths"]
  x, y_t_cases, y_t_deaths, y_n_cases, y_n_deaths = np.array(x), np.array(y_t_cases), np.array(y_t_deaths), np.array(y_n_cases), np.array(y_n_deaths)
  x = x.reshape((-1, 1))

  #Stworzenie modelu regresji linowej dla poszczególnych danych
  model_t_cases = LinearRegression().fit(x, y_t_cases)
  model_t_deaths = LinearRegression().fit(x, y_t_deaths)
  model_n_cases = LinearRegression().fit(x, y_n_cases)
  model_n_deaths = LinearRegression().fit(x, y_n_deaths)

  #Kolejne 5 dni
  x_new = [10, 11, 12, 13, 14]
  x_new = np.array(x_new)
  x_new = x_new.reshape((-1, 1))

  #Wczytanie ostatniej daty z DataFramu
  dzien = frame["date"].values[9]
  date_time_obj = datetime.datetime.strptime(dzien, '%Y-%m-%d')

  #Stworzenie serii danych z datą kolejnych 5 dni
  data_new = []
  for i in range(1,6):
    di = date_time_obj+datetime.timedelta(days=i)
    di = format_data(di)
    data_new.append(di)

  #Stworzenie spodziewanych danych na kolejne 5 dni przy pomocy modelu liniowej regresji  
  y_pred_new_t_cases = model_t_cases.predict(x_new).round()
  y_pred_new_t_deaths = model_t_deaths.predict(x_new).round()
  y_pred_new_n_cases = model_n_cases.predict(x_new).round()
  y_pred_new_n_deaths = model_n_deaths.predict(x_new).round()

  #Stworzenie nowego DataFramu z spodziewanymi danymi na kolejne 5 dni
  d = {"date":data_new, "new_cases":y_pred_new_n_cases, "new_deaths": y_pred_new_n_deaths, "total_cases":y_pred_new_t_cases,
       "total_deaths":y_pred_new_t_deaths}
  frame_pred = pd.DataFrame(data=d)  

  #Dodanie DataFramu z spodziewanymi danymi na kolejne 5 dni do DatFramu z danymi z poprzednich dni
  new_frame = frame.append(frame_pred).reset_index(drop=True)   

  return new_frame

predict_cases("Italy")