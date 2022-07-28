from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import os
import pandas as pd
import datetime

class updatePrice(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def komunikat_blad(self,plik):
        odp = QMessageBox.critical(
            self, 'Błąd',
            "Nie ma pliku "+plik,
            QMessageBox.Ok)

    def uruchom(self):
        dost = (str(self.listaDost.currentText()))

        if os.path.isfile('mytable.csv') == False:
            self.komunikat_blad("mytable.csv")
        if os.path.exists("cena_cennikowa.csv") == False:
            self.komunikat_blad("cena_cennikowa.csv")
        if os.path.exists("dostawcy/"+dost+"/cennik_dostawcy_"+dost+".csv") == False:
            self.komunikat_blad("dostawcy/"+dost+"/cennik_dostawcy_"+dost+".csv")
        if os.path.exists("dostawcy/"+dost+"/odrzucone_"+dost+".txt") == False:
            self.komunikat_blad("dostawcy/"+dost+"/odrzucone_"+dost+".txt")

        old_prices = pd.read_csv('cena_cennikowa.csv', sep=';')
        print("Wczytano cena_cennikowa.csv")
        baza_to = pd.read_csv("mytable.csv", sep=';')
        print("Wczytano mytable.csv")
        cennik_dostawcy = pd.read_csv("dostawcy/" + dost + "/cennik_dostawcy_" + dost + ".csv", sep=';',
                                      dtype={'kod dostawcy': str})
        print("Wczytano cennik_dostawcy_"+dost+".csv")
        baza_to.rename(columns={'4 KOD': 'kod skos'}, inplace=True)
        print("Zamiana mytable.csv 4 KOD na kod skos")
        odrzucone = pd.read_csv("dostawcy/" + dost + "/odrzucone_" + dost + '.txt')
        print("Wczytano odrzucone.txt")

        old_prices = pd.merge(old_prices, baza_to, on='kod skos', how='left')
        print("Złączenie cena_cennikowa.csv i mytable.csv")
        old_prices = pd.merge(old_prices, cennik_dostawcy, on='kod dostawcy', how='left')
        print("Złączenie cena_cennikowa.csv i cennik_dostawcy_"+dost+".csv")
        print(old_prices.columns)
        print(old_prices.iloc[1, 6])

        rest = cennik_dostawcy[~cennik_dostawcy["kod dostawcy"].isin(old_prices["kod dostawcy"])]
        rest = rest[~rest["kod dostawcy"].isin(odrzucone["kod dostawcy"])]
        rest.to_csv('dostawcy/' + dost + "/rest_" + dost + ".csv", index=False, sep=';')
        print("Stworznie rest_"+dost+".csv")

        not_match = baza_to.loc[baza_to["29 ust. dostawca"] == dost]
        not_match = not_match[~not_match["5 kod dostawcy"].isin(cennik_dostawcy["kod dostawcy"])]
        not_match['dopasowanie'] = ""
        for i in range(len(not_match)):
            for j in range(len(cennik_dostawcy)):
                if str(not_match.iloc[i, 1]) in str(cennik_dostawcy.iloc[j, 0]):
                    not_match.iloc[i, 3] = cennik_dostawcy.iloc[j, 0]
        not_match.to_csv('dostawcy/' + dost + "/not_match_" + dost + ".csv", index=False, sep=';')
        print("Stworznie not_match_"+dost+".csv")

        old_prices.rename(columns={'Column4': 'dostawca'}, inplace=True)

        old_prices.rename(columns={'cena po rabacie': 'cennik dostawcy'}, inplace=True)

        old_prices['cennik dostawcy'] = pd.to_numeric(old_prices['cennik dostawcy'], downcast="float")
        print("breakpoint0")
        print(old_prices['cena cennikowa'])
        #old_prices['cena cennikowa'] = pd.to_numeric(old_prices['cena cennikowa'], downcast="float")
        print("breakpoint1")
        old_prices['cena cennik wg jedn, dostawcy'] = pd.to_numeric(old_prices['cena cennik wg jedn, dostawcy'],
                                                                    errors='coerce')
        print("breakpoint2")
        old_prices['werfikacja'] = round(
            abs(old_prices['cennik dostawcy'] - old_prices['cena cennik wg jedn, dostawcy']), 2)
        print("breakpoint3")
        old_prices['nowa cena cennik wg jend, dostawcy'] = ""
        old_prices['nowe skonto-puste'] = old_prices['skonto-puste']
        old_prices['nowy mnoznik'] = old_prices['mnoznik']
        old_prices['nowa cena cenikowa'] = ""
        old_prices['nowa data'] = old_prices['data']
        old_prices['werf w %'] = ""

        date_now = datetime.datetime.now()
        for i in range(len(old_prices)):
            if pd.notna(old_prices.iloc[i, 10]) and old_prices.iloc[i, 9] == dost:
                print('nowa cena '+str(old_prices.iloc[i, 3])+" "+str(old_prices.iloc[i, 10]))
                old_prices.iloc[i, 12] = old_prices.iloc[i, 10]
                old_prices.iloc[i, 15] = round(old_prices.iloc[i, 10] * old_prices.iloc[i, 5], 2)
                old_prices.iloc[i, 16] = date_now.strftime("%Y-%m-%d")
                old_prices.iloc[i, 17] = float(round((float(old_prices.iloc[i, 15]) - float(old_prices.iloc[i, 6])) / float(old_prices.iloc[i, 6]) * 100, 2))
            else:
                old_prices.iloc[i, 12] = old_prices.iloc[i, 3]
                old_prices.iloc[i, 15] = old_prices.iloc[i, 6]

        print(old_prices.head())

        old_prices.to_csv('export.csv', index=False, sep=';')

        odp = QMessageBox.information(
            self, 'Komunikat',
            "Program wygenerował pliki.",
            QMessageBox.Ok)
        if odp == QMessageBox.Ok:
                self.close()


    def interfejs(self):

        self.setWindowIcon(QtGui.QIcon('logo.jpg'))
        etykieta1 = QLabel("Wymagane aktualne pliki przed uruchomieniem:\n1.cena_cennikowa.csv\n"
                           "2.mytable.csv - baza TO kolumny:4,5,29\n3.dostawcy/nazwa dostawcy/cennik_dostawcy.csv\n"
                           "4.dostawcy/nazwa dostawcy/odrzucone.txt\n\nPliki wygenerowane przez program:\n"
                           "1.export.csv - główny plik z aktualizacją\n2.dostawcy/nazwa dostawcy/not_match.csv - "
                           "nie dopasowane kody z naszej bazy\n3.dostawcy/nazwa dostawcy/rest.csv - "
                           "nie dopasowane kody z cennika dostawcy\n\nWybierz dostawcę:", self)
        etykieta1.setFont(QFont('Arial', 10))

        ukladT = QGridLayout()
        ukladT.addWidget(etykieta1, 0, 0)

        self.listaDost  =QComboBox(self)
        l = list(os.listdir("dostawcy"))
        l.remove("desktop.ini")
        l.sort()
        for v in l:
            self.listaDost.addItem(v)
        self.listaDost.setEnabled(True)

        uruchomBtn = QPushButton("&Uruchom", self)

        ukladH = QHBoxLayout()
        ukladH.addWidget(self.listaDost)
        ukladH.addWidget(uruchomBtn)
        ukladT.addLayout(ukladH, 2, 0, 1, 3)

        uruchomBtn.clicked.connect(self.uruchom)

        self.setLayout(ukladT)
        self.resize(350, 100)
        self.setWindowTitle("Aktualizator cenników")
        self.show()



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = updatePrice()

    sys.exit(app.exec_())