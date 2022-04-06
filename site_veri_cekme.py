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
    tumkelimeler=[]
    liste=['p','a']
    for liste1 in liste:
        for kelimegruplari in soup.find_all(liste1):
            icerik=kelimegruplari.text
            icerik=icerik.replace("/"," ")
            kelimeler1=icerik.split()
            for kelime in kelimeler1:
                if kelime in tumkelimeler:
                    break
                else:
                    tumkelimeler.append(kelime)
                    dosya.write(kelime+" ")
def icerik(soup,dosyaid):
    uzanti=dosyaid+"icerik.txt"
    dosya = open(uzanti,"a",encoding="utf-8")
    text = soup.find_all(text=True)
    out = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
    ]

    for t in text:
        if t.parent.name not in blacklist:
            out += str('{} '.format(t))
            out.strip()
            dosya.write(str(out))


def gir(soup):
    liste=['a']
    i=0
    j=0
    for kelimegruplari in soup.find_all(liste):
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
            i=i+1
            en="en"
            if(detect(tumkelimeler)==en):
                j=j+1
    if (j==0) or (j/i<0.5):
        return False
    else:
        return True
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
            try:
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
            except IOError:
                print("bir hata oluştu!")
                continue
        else:
            continue
    return liste
def resim_boyut(dosya_ismi): 
    imageFile = dosya_ismi
    imageObj = Image.open(imageFile)
    data = imageObj.size
    imageWidth=data[0]
    imageHeight=data[1]
    print(str(imageWidth) +" "+str(imageHeight) )
    if (imageHeight>=100) and (imageWidth>=100):
        print("kayıt başarılı")
        return False
    else:
        return True
def resim_kontol(dosya_link):
    blacklist = [
        'icon',
        'svg',

    ]
    uzanti=dosya_link.split(".")
    k=uzanti[1]
    if k not in blacklist:
        return True
def resim_sil(liste):
    liste=liste.split(",")
    for i in liste:
        if (len(i)>1):
            if os.path.exists(i):
                os.remove(i)
                print("resim dosyası silindi"+i)
            else:
                 print("Dosya mevcut değil")
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
def a_guncelle(id):
     
    cursor.execute("UPDATE site set aktif = 1 where id=?",id)
 
    con.commit()

for i in data :
    id=str(i[0])
    dosyaid=str(i[0])+"/"
    url=str(i[1])
    url=linkkontrol(url)
    x=True
    y= kontrol (url)
    if(x==y):
        soup=parse(url)
        z=gir(soup)
        if(z):
            a_guncelle(id)
            dosya(dosyaid)
            kelime(soup,dosyaid)
            meta(soup,dosyaid)
            liste=resim(soup,dosyaid,url)
            resim_sil(liste)
    else:
        url=str(i[1])
        url1=linkkontrol2(url)
        x=True
        y= kontrol (url1)
        if(x==y):
            soup=parse(url1)
            z=gir(soup)
            if(z):
                a_guncelle(id)
                dosya(dosyaid)
                kelime(soup,dosyaid)
                meta(soup,dosyaid)
                liste=resim(soup,dosyaid,url1)
                resim_sil(liste)
                
        else:
            print("kazı devam ediyor"+dosyaid)
con.close()