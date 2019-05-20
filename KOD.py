import sqlite3 as sql
import imaplib
import email
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time
veri2=[]
tutucu=[]
def veri_tabanı_olusturma():
    vt = sql.connect('utp_proje.db')
    im = vt.cursor()
    sorgu = """CREATE TABLE IF NOT EXISTS gelen_veri
                (barkod, isim, adet, fiyat, market, adet2, fiyat2, market2, adet3, fiyat3, market3, bitis)"""
    im.execute(sorgu)
    for_sayac=0    
    for i in veri2:
        if for_sayac==0:
            ad=i[0]
            for_sayac=1
            print(ad)
            continue
        if tutucu.count(i[0]):
            tutucu.remove(i[0])
        sayac = 0
        gecici=i[0]
        gecici_fiyat=i[3]
        im.execute("SELECT * FROM gelen_veri")
        for veri in im.fetchall():
            if gecici==veri[0] and gecici_fiyat==veri[3] and ad==veri[4]:
                sayi=str(int(i[2])+int(veri[2]))
                sayi2=str(int(i[2])+int(veri[11]))
                im.execute("UPDATE gelen_veri SET adet=? WHERE barkod=?", (sayi, gecici,))
                im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
                vt.commit()
                sayac=1
                print("1")
                break
            elif gecici==veri[0] and gecici_fiyat==veri[6] and ad==veri[7]:
                sayi=str(int(i[2])+int(veri[5]))
                sayi2=str(int(i[2])+int(veri[11]))
                im.execute("UPDATE gelen_veri SET adet2=? WHERE barkod=?", (sayi, gecici,))
                im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
                vt.commit()
                sayac=1
                print("2")
                break
            elif gecici==veri[0] and gecici_fiyat==veri[9] and ad==veri[10]:
                sayi=str(int(i[2])+int(veri[8]))
                sayi2=str(int(i[2])+int(veri[11]))
                im.execute("UPDATE gelen_veri SET adet3=? WHERE barkod=?", (sayi, gecici,))
                im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
                vt.commit()
                sayac=1
                print("3")
                break
            elif gecici==veri[0] and veri[6]=='0' and veri[9]=='0':
                sayi2=str(int(veri[11])+int(i[2]))
                im.execute("UPDATE gelen_veri SET adet2=? WHERE barkod=?", (i[2], gecici,))
                im.execute("UPDATE gelen_veri SET fiyat2=? WHERE barkod=?", (gecici_fiyat,gecici,))
                im.execute("UPDATE gelen_veri SET market2=? WHERE barkod=?", (ad,gecici,))
                im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
                vt.commit()
                print("4")
                sayac=1
                break
            elif gecici==veri[0] and veri[9]=='0' and veri[6]!='0':
                sayi2=str(int(veri[11])+int(i[2]))
                im.execute("UPDATE gelen_veri SET adet3=? WHERE barkod=?", (i[2], gecici,))
                im.execute("UPDATE gelen_veri SET fiyat3=? WHERE barkod=?", (gecici_fiyat,gecici,))
                im.execute("UPDATE gelen_veri SET market3=? WHERE barkod=?", (ad,gecici,))
                im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
                vt.commit()
                print("5")
                sayac=1
                break
                
        if sayac==0:
            im.execute("""INSERT INTO gelen_veri VALUES
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",i)
            im.execute("UPDATE gelen_veri SET market=? WHERE barkod=?", (ad,gecici,))
            im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (i[2],gecici,))
            vt.commit()
    vt.close()
    veri2.clear()
def kullanici_karsilastir(tarih):
    vt = sql.connect('utp_proje2.db')
    im = vt.cursor()
    sorgu = """CREATE TABLE IF NOT EXISTS gelen_veri
                (barkod, isim, adet, fiyat, market, adet2, fiyat2, market2, adet3, fiyat3, market3, bitis)"""
    im.execute(sorgu)
    genel_toplam=0.0
    genel=[]
    im.execute("SELECT market FROM gelen_veri")
    adlar=[]
    adlar2=[]
    gönder="Seçilen {} tarihleri arası yapılan alışveris listesi".format(tarih)+"\n"+"-"*71+"\n\n\n"
    for veri in im.fetchall():
        if veri!= '0':
            adlar.append(veri[0])
            break
    im.execute("SELECT market2 FROM gelen_veri")
    for veri in im.fetchall():
        if veri!='0':
            adlar.append(veri[0])
            break
    im.execute("SELECT market3 FROM gelen_veri")
    for veri in im.fetchall():
        if veri!= '0':
            adlar.append(veri[0])
            break
    for i in adlar:
        if i!='0':
            adlar2.append(i)
    print(adlar2)
    for i in adlar2:
        sayı=0
        sayac=0

        im.execute("SELECT * FROM gelen_veri WHERE market=?",(i,))
        gönder=gönder+i+" marketinden alınan ürünler :\n"+"-"*(len(i)+29)+"\n\n"+"isim"+" "*54+"adet"+"  "+"fiyat\n"+"\n"+"-"*4+" "*54+"-"*4+"  "+"-"*5+"\n"
        for k in im.fetchall():
            if(len(k)>3):
                gönder=gönder+k[1]+" "*(60-len(k[1]))+k[2]+" "*(4-len(k[2]))+k[3]+"\n"
                sayı=sayı+(float(k[2])*float(k[3]))
                sayac=1

        
        im.execute("SELECT * FROM gelen_veri WHERE market2=?",(i,))
        for k in im.fetchall():
            if(len(k)>3):
                gönder=gönder+k[1]+" "*(60-len(k[1]))+k[5]+" "*(4-len(k[5]))+k[6]+"\n"
                sayı=sayı+(float(k[5])*float(k[6]))
                sayac=1

        im.execute("SELECT * FROM gelen_veri WHERE market3=?",(i,))
        for k in im.fetchall():
            if(len(k)>3):
                gönder=gönder+k[1]+" "*(60-len(k[1]))+k[8]+" "*(4-len(k[8]))+k[9]+"\n"
                sayı=sayı+(float(k[8])*float(k[9]))
                sayac=1
        if sayac==1:
            gönder=gönder+"\nToplam = "+str(round(sayı,2))+"\n\n\n\n"
            genel.append(sayı)
            sayac=0
    
    for v in genel:
        genel_toplam+=v
    gönder=gönder+"Genel Toplam = "+str(round(genel_toplam,2))
    vt.close()
    L=os.listdir()
    if(L.count("yol")==0):
        os.mkdir("yol")
    with open("yol/karsilastirma_listesi.txt","w") as dosya:
        os.chmod("yol/karsilastirma_listesi.txt",777)
        dosya.write(gönder)
    dosya_gönder()
    os.remove("utp_proje2.db")
             
def dosya_gönder():
    smtp_server = "smtp.gmail.com"                   
    port = 587                            
    user = "utpproje@gmail.com"                          
    pwd  = "1q2w3e4rk."                          
    name  = "utp"                         
    alias = "" + name                          
    path = "yol/"                          
    destination = "bkagan0737@gmail.com"                   
    text = "alışveriş listesi"                          
     
    class mail_sender:
        def __init__(self):
            self.liste = os.listdir(path)
     
        def login(self):
            print("Sunucuya giris yapiliyor...")
            self.mailServer = smtplib.SMTP(smtp_server, port)
            self.mailServer.set_debuglevel(0)
            self.mailServer.ehlo()
            self.mailServer.starttls()
            self.mailServer.ehlo()
            self.mailServer.login(user, pwd)
            print("Sunucuya basariyla giris yapildi.\n")
     
        def logout(self):
            self.mailServer.close()
        def begin(self):
            self.login()
            while(self.liste):
                self.liste = os.listdir(path)
                self.dosya = self.dosyasec()
                print(self.dosya + ' secildi.')
                self.send()
            self.logout()
     
        def dosyasec(self):
            return self.liste.pop(0)
        def mailprep(self):
            mail = MIMEMultipart()
            mail['From'] = alias
            mail['To'] = destination
            mail['Subject'] = self.dosya      
            mail.attach(MIMEText(text))
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(path + os.sep + self.dosya, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition','attachment; filename="%s"' % self.dosya)
            mail.attach(part)
            return mail
        def send(self):
            newmail = self.mailprep()
            self.mailServer.sendmail(user, destination, newmail.as_string())
            print('E-posta yollandi. Dosya = ' + self.dosya)
            os.remove(path + os.sep + self.dosya)
            print(self.dosya + ' silindi.')
            print('\n')
     
    a = mail_sender()
    a.begin()             

def mail_atmak_icin_okuma(data):
    for i in data:
        gönder=i+" marketindeki en ucuz ürünler :\n"
        with open(i+".txt","r"):
            oku=dosya.read()
            gönder=gönder+oku
            gönder=gönder+"\r\n\r\n"
def karsilastir():
    adlar=[]
    barkodlar=[]
    isim=""
    vt = sql.connect('utp_proje.db')
    im = vt.cursor()
    sorgu = """CREATE TABLE IF NOT EXISTS gelen_veri
                (barkod, isim, adet, fiyat, market, adet2, fiyat2, market2, adet3, fiyat3, market3, bitis)"""
    im.execute(sorgu)
    im.execute("SELECT market FROM gelen_veri")
    for veri in im.fetchall():
        if veri!='0':
            adlar.append(veri[0])
            break
    im.execute("SELECT market2 FROM gelen_veri")
    for veri in im.fetchall():
        if veri!='0':
            adlar.append(veri[0])
            break
    im.execute("SELECT market3 FROM gelen_veri")
    for veri in im.fetchall():
        if veri!='0':
            veri=veri[0].replace("=C5=9Eok","Şok")
            adlar.append(veri)
            break
    im.execute("SELECT barkod FROM gelen_veri")
    for veri in im.fetchall():
        barkodlar.append(veri[0])
    max_deger=100000.0
    for barkod2 in barkodlar:
        for data2 in adlar:    
            vt = sql.connect(data2+".db")
            im = vt.cursor()
            sorgu = """CREATE TABLE IF NOT EXISTS gelen_veri
            (barkod, isim, fiyat)"""
            im.execute(sorgu)
            im.execute("SELECT * FROM gelen_veri")
            for veri in im.fetchall():
                
                if veri[0]==barkod2:
                    if max_deger>float(veri[2]):
                        max_deger=float(veri[2])
                        market=data2.replace("Ş","S")
                        isim=veri[1]

        with open("yol/"+market+".txt","a") as dosya:
            dosya.write(barkod2+" "*(15-len(barkod2))+isim+" "*(50-len(isim))+str(max_deger)+"\n")
            max_deger=100000
    for i in adlar :
        with open("yol/"+i.replace("Ş","S")+".txt","r") as dosya:
            veri3=dosya.read()
            with open("yol/ucuz_urun.txt","a") as dosya2:
                data="\n\n{} marketindeki en ucuz ürünler :".format(i)+"\n"+"-"*len(i)+"-"*31+"\n"+"barkod"+" "*15+"isim"+" "*40+"fiyat(TL)"+"\n"+"-"*6+" "*15+"-"*4+" "*40+"-"*9+"\n\n"
                dosya2.write(data)
                dosya2.write(veri3)
        os.remove("yol/"+i.replace("Ş","S")+".txt")            
    dosya_gönder()        

def veri_silme(bar):
    vt = sql.connect('utp_proje.db')
    im = vt.cursor()
    im.execute("SELECT * FROM gelen_veri WHERE barkod= ?",(bar,))
    silinecek=im.fetchall()
    for i in silinecek:
        i=list(i)
        if int(i[11]) > 1 :
            deger=str(int(i[11])-1)
            im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?",(deger,bar))
            vt.commit()
        elif i[11] == "1" :
            i[11]=0
            im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?",("0",bar))
            data="\n\n{} barkodlu {} ürün bitti.\n".format(i[0],i[1])
            mail_yolla(data)
            vt.commit()
        data=int(i[2])+int(i[5])+int(i[8])
        data=int(data/5)
        if int(i[11])<=data and tutucu.count(i[0])==0:
            data="\n\n{} barkodlu {} ürün bitmek üzere {} ürününden sadece {} kaldı.\n".format(i[0],i[1],i[1],i[11])
            mail_yolla(data)
            tutucu.append(i[0])
        print(tutucu)
    vt.close()


def dosya_okuma():
    dosya2=open("karsilastirma/"+str(int(time.strftime('%d')))+":"+str(int(time.strftime('%m')))+":"+str(int(time.strftime('%Y')))+".txt","a")
    with open("gecici.txt", "r") as dosya:
        veri = dosya.readlines()
        for i in veri :
            print(i)
            if i == "\n":
                continue
            elif i=="":
                continue
            else :
                i=i.replace("\n","")
                if i=="=C5=9Eok":
                    i="Şok"
                i=i.split("-")
                i=i+['0','0','0','0','0','0','0','0']
                i=tuple(i)
                
                if len(i)==12 or len(i)==9:                
                    veri2.append(i)
                    for k in i:
                        print(k)
                        k=k+" "
                        dosya2.write(k)
                    dosya2.write("\n")
                    
    
    with open("gecici.txt","w") as dosya:
        os.chmod("gecici.txt",777)
        dosya2.write("")
    veri_tabanı_olusturma()
    dosya.close()


def karsilastirma_icin_okuma(gun=1,ay=1,yıl=2019,gun2=1,ay2=1,yıl2=2019):
    ad2=""
    L=os.listdir("karsilastirma/")
    if yıl==yıl2 and ay==ay2:
        print("11")
        for k in range(gun,gun2+1):
            try:
                with open("karsilastirma/"+str(k)+":"+str(ay)+":"+str(yıl)+".txt","r") as dosya:
                    verii=dosya.readlines()
                    
                    for i in verii:
                        i=i.split(" ")
                        if i[-1]=="\n":
                            i.pop(-1)
                        print(i)
                        if len(i)==9:
                            ad2=i[0]
                        else:
                            ekleme(i,ad2)
            except:
                continue
    elif yıl==yıl2 and ay!=ay2:
        print("22")
        sayac=0
        for k in range(gun,31):
            try:
                with open("karsilastirma/"+str(k)+":"+str(ay)+":"+str(yıl)+".txt","r") as dosya:
                    verii=dosya.readlines()
                    
                    for i in verii:
                        i=i.split(" ")
                        if i[-1]=="\n":
                            i.pop(-1)
                        print(i)
                        if len(i)==9:
                            ad2=i[0]
                        else:
                            ekleme(i,ad2)
            except:
                continue
        while 1:
            ay+=1
            if ay==ay2:
                break
            for k in range(gun,31):
                try:
                    with open("karsilastirma/"+str(k)+":"+str(ay)+":"+str(yıl)+".txt","r") as dosya:
                        verii=dosya.readlines()
                        
                    for i in verii:
                        i=i.split(" ")
                        if i[-1]=="\n":
                            i.pop(-1)
                        print(i)
                        if len(i)==9:
                            ad2=i[0]
                        else:
                            ekleme(i,ad2)
                except:
                    continue
                        
        for k in range(gun,gun2+1):
            try:
                with open("karsilastirma/"+str(k)+":"+str(ay)+":"+str(yıl)+".txt","r") as dosya:
                    verii=dosya.readlines()
                    for i in verii:
                        i=i.split(" ")
                        if i[-1]=="\n":
                            i.pop(-1)
                        print(i)
                        if len(i)==9:
                            ad2=i[0]
                        else:
                            ekleme(i,ad2)
            except:
                continue

    elif yıl!=yıl2:
        print("33")
        sayac=0
        for k in range(gun,31):
            try:
                with open("karsilastirma/"+str(k)+":"+str(ay)+":"+str(yıl)+".txt","r") as dosya:
                    verii=dosya.readlines()
                    
                    for i in verii:
                        i=i.split(" ")
                        if i[-1]=="\n":
                            i.pop(-1)
                        print(i)
                        if len(i)==9:
                            ad2=i[0]
                        else:
                            ekleme(i,ad2)
            except:
                continue

        while 1:
            ay+=1
            if ay==13:
                ay=1
                yıl+=1
            if yıl==yıl2 and ay==ay2:
                break
            for k in range(1,31):
                try:
                    with open("karsilastirma/"+str(k)+":"+str(ay)+":"+str(yıl)+".txt","r") as dosya:
                        verii=dosya.readlines()
                        
                    for i in verii:
                        i=i.split(" ")
                        if i[-1]=="\n":
                            i.pop(-1)
                        print(i)
                        if len(i)==9:
                            ad2=i[0]
                        else:
                            ekleme(i,ad2)
                except:
                    continue
                        
        for k in range(gun,gun2+1):
            try:
                with open("karsilastirma/"+str(k)+":"+str(ay)+":"+str(yıl)+".txt","r") as dosya:
                    verii=dosya.readlines()
                    
                    for i in verii:
                        i=i.split(" ")
                        if i[-1]=="\n":
                            i.pop(-1)
                        print(i)
                        if len(i)==9:
                            ad2=i[0]
                        else:
                            ekleme(i,ad2)
            except:
                continue
                        
    kullanici_karsilastir("{}.{}.{}-{}.{}.{}".format(str(gun),str(ay),str(yıl),str(gun2),str(ay2),str(yıl2)))
            
        
            
def ekleme(i,ad2):
    vt = sql.connect('utp_proje2.db')
    im = vt.cursor()
    sorgu = """CREATE TABLE IF NOT EXISTS gelen_veri
                (barkod, isim, adet, fiyat, market, adet2, fiyat2, market2, adet3, fiyat3, market3, bitis)"""
    im.execute(sorgu)
    im = vt.cursor()       

    sayac = 0
    gecici=i[0]
    gecici_fiyat=i[3]
    im.execute("SELECT * FROM gelen_veri")
    for veri in im.fetchall():
        if gecici==veri[0] and gecici_fiyat==veri[3] and ad2==veri[4]:
            sayi=str(int(i[2])+int(veri[2]))
            sayi2=str(int(i[2])+int(veri[11]))
            im.execute("UPDATE gelen_veri SET adet=? WHERE barkod=?", (sayi, gecici,))
            im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
            vt.commit()
            sayac=1
            print("1")
            break
        elif gecici==veri[0] and gecici_fiyat==veri[6] and ad2==veri[7]:
            sayi=str(int(i[2])+int(veri[5]))
            sayi2=str(int(i[2])+int(veri[11]))
            im.execute("UPDATE gelen_veri SET adet2=? WHERE barkod=?", (sayi, gecici,))
            im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
            vt.commit()
            sayac=1
            print("2")
            break
        elif gecici==veri[0] and gecici_fiyat==veri[9] and ad2==veri[10]:
            sayi=str(int(i[2])+int(veri[8]))
            sayi2=str(int(i[2])+int(veri[11]))
            im.execute("UPDATE gelen_veri SET adet3=? WHERE barkod=?", (sayi, gecici,))
            im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
            vt.commit()
            sayac=1
            print("3")
            break
        elif gecici==veri[0] and veri[6]=='0' and veri[9]=='0':
            sayi2=str(int(veri[11])+int(i[2]))
            im.execute("UPDATE gelen_veri SET adet2=? WHERE barkod=?", (i[2], gecici,))
            im.execute("UPDATE gelen_veri SET fiyat2=? WHERE barkod=?", (gecici_fiyat,gecici,))
            im.execute("UPDATE gelen_veri SET market2=? WHERE barkod=?", (ad2,gecici,))
            im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
            vt.commit()
            print("4")
            sayac=1
            break
        elif gecici==veri[0] and veri[9]=='0' and veri[6]!='0':
            sayi2=str(int(veri[11])+int(i[2]))
            im.execute("UPDATE gelen_veri SET adet3=? WHERE barkod=?", (i[2], gecici,))
            im.execute("UPDATE gelen_veri SET fiyat3=? WHERE barkod=?", (gecici_fiyat,gecici,))
            im.execute("UPDATE gelen_veri SET market3=? WHERE barkod=?", (ad2,gecici,))
            im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (sayi2, gecici,))
            vt.commit()
            print("5")
            sayac=1
            break
            
    if sayac==0:
        im.execute("""INSERT INTO gelen_veri VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",i)
        im.execute("UPDATE gelen_veri SET market=? WHERE barkod=?", (ad2,gecici,))
        im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?", (i[2],gecici,))
        vt.commit()
    vt.close()
                        
                        
            
    
def mail_alma():
    gecici_veri=""
    with open("gecici_veri.txt","r") as dosya:
        gecici_veri=str(dosya.read())
    msrvr=imaplib.IMAP4_SSL('imap.gmail.com',993)
    unm="utpproje@gmail.com"
    psw="1q2w3e4rk."
    msrvr.login(unm,psw)
    stat,cnt=msrvr.select('Inbox')
    stat,dta=msrvr.fetch(cnt[0],"(UID BODY[TEXT])")
    typ, data = msrvr.fetch(cnt[0], '(RFC822)' )
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1].decode('UTF-8'))
            email_from = msg['from']
            email_from = email_from.split("<")
            email_from=str(email_from[1]).replace(">","")
    if email_from == "bkagan0737@gmail.com":
        veri=dta[0][1].split()
        if gecici_veri==str(veri[0].decode('UTF-8')):
            pass
        elif gecici_veri != str(veri[0].decode('UTF-8')):
            with open("gecici_veri.txt","w") as dosya:
                dosya.write(veri[0].decode('UTF-8'))
            veri2=(dta[0][1].decode('UTF-8')).split("\r\n\r\n")
            if veri2[1]=="karsilastir":
                karsilastir()
            elif veri2[1][2]=="." and veri2[1][5]=="." and veri2[1][2]=="." and veri2[1][13]=="." and veri2[1][16]=="." and len(veri2[1])==21:
                print(int(veri2[1][0:2]),int(veri2[1][3:5]),int(veri2[1][6:10]),int(veri2[1][11:13]),int(veri2[1][14:16]),int(veri2[1][17:21]))
                karsilastirma_icin_okuma(int(veri2[1][0:2]),int(veri2[1][3:5]),int(veri2[1][6:10]),int(veri2[1][11:13]),int(veri2[1][14:16]),int(veri2[1][17:21]))
                
            else:
                with open("gecici.txt","a") as dosya:
                    os.chmod("gecici.txt",777)
                    dosya.write(veri2[1]+"\n")
                dosya_okuma()
                    
while 1:
    mail_alma()