from sqlite3.dbapi2 import Cursor
import requests
import sqlite3
import os
from bs4 import BeautifulSoup
import shutil
con=sqlite3.connect("bl1.db")
cursor=con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS site(    "id"INTEGER,"link"TEXT,"kategori"TEXT,"aktif"BLOB,PRIMARY KEY("id" AUTOINCREMENT))')
yer="C:/Users/osman/python/Workspace/ornekler/proje1/vproject/BL"
os.chdir(yer)
liste=os.listdir()
def veri_ekle(yer):
    os.chdir(yer)
    yer=yer.split("/")
    x=yer.index("BL")
    x=x+1
    kategori=yer[x]
    with open("domains.txt", "r") as dosya:
        vliste=dosya.read()
    vliste=vliste.split()
    for veri in vliste:
        aktif="0"
        sql = "INSERT INTO site  (link,kategori,aktif) VALUES (?,?,?)"
        val = (veri,kategori,aktif,)
        cursor.execute(sql,val)
    con.commit()
def arama(yer):
    sabit="C:/Users/osman/python/Workspace/ornekler/proje1/vproject/BL"
    liste=os.listdir()
    print(liste)
    print("çalışma vaaaaar")
    k="domains.txt"
    if(len(liste)>0): 
            if k in liste:
                veri_ekle(yer)
                print("forun içinde!!!!!!!!")
                os.chdir(sabit)
                print(yer)
                print("silme işlemi yapılıyor!!!!!!!")
                shutil.rmtree(yer) 
                liste=os.listdir()
                if(len(liste)==0):
                    print("program bitti1")
                else:
                        arama(sabit)
            else:
                print("else çalıştı")
                a=liste[0]
                print(a)
                yol=yer+"/"+a
                x=os.path.exists(yol)
                if(x):
                    print("else sonrası if çalıştı")
                    os.chdir(yol)   
                    liste=os.listdir()
                    if(len(liste)==0) and yol==sabit:
                        print("program bitti2")
                    else:
                        arama(yol)
    else:
            print("son else çalıştı")
            os.chdir(sabit)
            os.rmdir(yer)
            liste=os.listdir()
            if(len(liste)==0):
                print("son else if ")
            else:
                arama(sabit) 
arama(yer)
con.close()