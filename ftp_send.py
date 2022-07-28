import pandas as pd
import datetime
import xml.etree.cElementTree as ET
from xml.dom import minidom

table = pd.read_csv("mytable.csv", sep=';')
table['10 cena netto'] = table['10 cena netto'].str.replace(',','.')
table['12 vat'] = table['12 vat'].str.replace(',','.')

root = ET.Element("Document-ProductCatalogue")
header = ET.SubElement(root, "ProductCatalogue-Header")
lines = ET.SubElement(root, "ProductCatalogue-Lines")
summary = ET.SubElement(root, "ProductCatalogue-Summary")

ET.SubElement(header, "ProductCatalogueNumber").text = "00001"
ET.SubElement(header, "ProductCatalogueDate").text = datetime.datetime.now().strftime("%Y-%m-%d")
ET.SubElement(header, "DocumentFunctionCode").text = "N"
ET.SubElement(header, "DocumentTest").text = "0"
parties = ET.SubElement(header, "ProductCatalogue-Parties")
buyer = ET.SubElement(parties, "Buyer")
ET.SubElement(buyer, "ILN").text = "5901819002184"
seller = ET.SubElement(parties, "Seller")
ET.SubElement(seller, "ILN").text = "5901503600108"

for i in range(len(table)):
    line = ET.SubElement(lines, "Line")
    line_item = ET.SubElement(line, "Line-Item")
    ET.SubElement(line_item, "LineNumber").text = str(i+1)
    ET.SubElement(line_item, "LineType").text = "1"
    ET.SubElement(line_item, "SupplierItemCode").text = str(table.iloc[i,1])
    ET.SubElement(line_item, "UnitNetPrice").text = str(table.iloc[i,4])
    ET.SubElement(line_item, "TaxRate").text = str(table.iloc[i,5])
    ET.SubElement(line_item, "ItemDescription").text = "<![CDATA["+table.iloc[i,2]+"]]>"
    ET.SubElement(line_item, "BuyerItemLink").text = "<![CDATA[index.php?kod1="+table.iloc[i,0]+"]]>"

ET.SubElement(summary, "TotalLines").text = str(len(table))

xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml()
with open("catalogue.xml", "wb") as f:
    f.write(xmlstr.encode('utf-8'))
f.close()

with open('catalogue.xml', 'r') as file :
  filedata = file.read()

filedata = filedata.replace('version="1.0"', 'version="1.0" encoding="UTF-8"')
filedata = filedata.replace('&lt;', '<')
filedata = filedata.replace('&gt;', '>')

with open('catalogue.xml', 'w') as file:
  file.write(filedata)

file.close()

import ftplib
session = ftplib.FTP('priv','priv','priv')
file = open('catalogue.xml','rb')                  # file to send
session.storbinary('STOR catalogue.xml', file)     # send the file
file.close()                                    # close file and FTP
session.quit()