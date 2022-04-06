from sqlite3.dbapi2 import Cursor
from bs4.element import SoupStrainer
import requests
import sqlite3
import os
from bs4 import BeautifulSoup
from langdetect import detect
from PIL import Image
con=sqlite3.connect("bl.db")
cursor=con.cursor()
cursor.execute("SELECT * FROM site")
data=cursor.fetchall()
def dosya(dosyaid):
    if(os.path.isdir(dosyaid)):
         print("dosya var")
    else:
        os.makedirs(dosyaid) 
def resim_boyut(dosya_ismi): 
    imagefile = dosya_ismi
    imageobj = Image.open(imagefile)
    data = imageobj.size
    imagewidth=data[0]
    imageheight=data[1]
    print(str(imagewidth) +" "+str(imageheight) )
    if (imageheight>100) and (imagewidth>100):
        print("kayıt başarılı")
        return False
    else:
        return True
def meta(soup,dosyaid):
    uzanti=dosyaid+"meta.txt"
    dosya = open(uzanti,"a",encoding="utf-8")
    liste=['meta']
    for liste1 in liste:
        for kelimegruplari in soup.find_all(liste1):
            dosya.write(str(kelimegruplari)+" ")
def kelime(soup,dosyaid):
    uzanti=dosyaid+"bilgiler.txt"
    dosya = open(uzanti,"a",encoding="utf-8")
    liste=['a']
    for liste1 in liste:
        for kelimegruplari in soup.find_all(liste1):
            icerik=kelimegruplari.text
            icerik=icerik.replace("/"," ")
            kelimeler1=icerik.split()
            y=kelime_kontrol(kelimeler1)
            if(y):
                tumkelimeler=""
                for kelime in kelimeler1:
                    kelime=kirp(kelime)
                    y=kelime_kontrol(kelime)
                    if(y):
                        kelime=kelime.lower() 
                        tumkelimeler=tumkelimeler+kelime+" "
                        dosya.write(kelime+" ")
                print(str(detect(tumkelimeler))+"==>"+tumkelimeler)
def kirp(icerik):
    punc = '''!()-[]{};:'"“”\,<>./?@#$%^&*_~'''
    for ele in icerik:   
        if ele in punc:
            icerik = icerik.replace(ele, "")
    return icerik
def kelime_kontrol(kelime):
    if(len(kelime)>2):
        sayi="1,2,3,4,5,6,7,8,9,0"   
        for k in kelime:
            if k in sayi:
                return False
            else:
                return True
    else:
        return False
def parse(url):
    r = requests.get(url)
    soup=BeautifulSoup(r.content,"html.parser")
    return soup
def kontrol(url):
    try:
        response = requests.head(url)

        if response.status_code == 200: 
            return True
        else:
            return False
    except requests.ConnectionError as e:
        return e
def resim(soup,dosyaid,url):
    liste=""
    for link in soup.find_all('img'):
        dosya_linki=link.get('src')
        if (dosya_linki==None):
            break  
        dosya_linki=resimurl(url,dosya_linki)
        print(dosya_linki)
        x=True
        y= kontrol (dosya_linki)
        if(x==y):
                dosya_ismi=dosya_linki.split('/')[-1]
                print(dosya_ismi)
                y=resim_kontol(dosya_ismi)
                if(y):
                    dosya_ismi=dosyaid+dosya_ismi
                    with open(dosya_ismi,'wb') as dosya:
                        cevap=requests.get(dosya_linki)
                        dosya.write(cevap.content)
                    z=resim_boyut(dosya_ismi)
                    if(z):
                        liste=liste + dosya_ismi+","
        else:
            continue
    return liste
def resim_kontol(dosya_link):
    blacklist = [
        'icon',
        'jpg',
        'svg',

    ]
    uzantı=dosya_link.split(".")
    k=uzantı[1]
    if k not in blacklist:
        return True

def linkkontrol(url):
    ekle="http://"
    x="http"
    i = 0
    parca=""
    while i < 4:
        parca=parca+url[i]
        i += 1   
    if(x==parca):
        return url
    else:
        url=ekle+url
        print(url)
        return url
def linkkontrol2(url):
    ekle="https://"
    x="https"
    i = 0
    parca=""
    while i < 5:
        parca=parca+url[i]
        i += 1   
    if(x==parca):
        return url
    else:
        url=ekle+url
        print(url)
        return url
def resimurl(url,dosya_linki):
    ekle="https://"
    for link in dosya_linki:
        if (link=="h"): 
             
            return dosya_linki
        else:
            dosya_linki=dosya_linki.replace("..","")
            dosya_linki=ekle+url+"/"+dosya_linki
            return dosya_linki
def resim_sil(liste):
    liste=liste.split(",")
    for i in liste:
        if (len(i)>1):
            if os.path.exists(i):
                os.remove(i)
                print("resim dosyası silindi"+i)
            else:
                 print("Dosya mevcut değil")

for i in data :
    dosyaid=str(i[0])+"/"
    url=str(i[1])
    url=linkkontrol(url)
    x=True
    y= kontrol (url)
    if(x==y):
        soup=parse(url)
        dosya(dosyaid)
        kelime(soup,dosyaid)
        meta(soup,dosyaid)
        liste=resim(soup,dosyaid,url)
        resim_sil(liste)
    else:
        url1=url=str(i[1])
        url1=linkkontrol2(url)
        x=True
        y= kontrol (url1)
        if(x==y):
            soup=parse(url1)
            dosya(dosyaid)
            kelime(soup,dosyaid)
            meta(soup,dosyaid)
            liste=resim(soup,dosyaid,url1)
            resim_sil(liste)
            
        else:
            print("kazı devam ediyor"+dosyaid)