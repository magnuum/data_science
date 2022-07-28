import pandas as pd

warzywa_owoce = []
mleka = []
herbaty_kawy = []
ciastka = []
wody = []
napoje = []
chemia = []
pozostale = []

listaZakup = pd.read_csv('makro.csv', sep=';');
slownik = pd.read_csv('slownik_sort_makro.csv', sep=';')

print(listaZakup.head())

print(listaZakup.iloc[0])

for i in range(len(listaZakup)):
    for j in range(len(slownik)):
        if listaZakup.iloc[i, 4].startswith(slownik.iloc[j,0]):
            if slownik.iloc[j,1] == 1:
                warzywa_owoce.append(listaZakup.iloc[i])
            elif slownik.iloc[j,1] == 2:
                mleka.append(listaZakup.iloc[i])
            elif slownik.iloc[j,1] == 3:
                herbaty_kawy.append(listaZakup.iloc[i])
            elif slownik.iloc[j,1] == 4:
                ciastka.append(listaZakup.iloc[i])
            elif slownik.iloc[j,1] == 5:
                wody.append(listaZakup.iloc[i])
            elif slownik.iloc[j,1] == 6:
                napoje.append(listaZakup.iloc[i])
            elif slownik.iloc[j,1] == 7:
                chemia.append(listaZakup.iloc[i])
            elif slownik.iloc[j,1] == 0:
                pozostale.append(listaZakup.iloc[i])
        else:
            pozostale.append(listaZakup.iloc[i])

df1 = pd.DataFrame(warzywa_owoce)
df2 = pd.DataFrame(mleka)
df3 = pd.DataFrame(herbaty_kawy)
df4 = pd.DataFrame(ciastka)
df5 = pd.DataFrame(wody)
df6 = pd.DataFrame(napoje)
df7 = pd.DataFrame(chemia)
df0 = pd.DataFrame(pozostale)

sortMakro = df1.append(df2).append(df3).append(df4).append(df5).append(df6).append(df7).append(df0)
sortMakro = sortMakro.drop(columns=['lp']).drop_duplicates()

sortMakro = sortMakro[['kod','ilosc','jednostka','kod abis']]
sortMakro.rename(columns={'ilosc':'jm','jednostka':'nazwa','kod abis':'ilosc'},inplace=True)

sortMakro.to_csv('posortwane_makro.csv', index=True, sep=';', encoding='utf-8')

print(sortMakro)
