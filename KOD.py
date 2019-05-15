import sqlite3 as sql
import imaplib
import email
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
veri2=[]

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
        sayac = 0
        gecici=i[0]
        gecici_fiyat=i[3]
        im.execute("SELECT * FROM gelen_veri")
        for veri in im.fetchall():
            if gecici==veri[0] and gecici_fiyat==veri[3] and ad==veri[4]:
                sayi=str(int(i[2])+int(veri[2]))
                im.execute("UPDATE gelen_veri SET adet=? WHERE barkod=?", (sayi, gecici,))
                vt.commit()
                sayac=1
                print("1")
                break
            elif gecici==veri[0] and gecici_fiyat==veri[6] and ad==veri[7]:
                sayi=str(int(i[2])+int(veri[5]))
                im.execute("UPDATE gelen_veri SET adet=? WHERE barkod=?", (sayi, gecici,))
                vt.commit()
                sayac=1
                print("2")
                break
            elif gecici==veri[0] and gecici_fiyat==veri[9] and ad==veri[10]:
                sayi=str(int(i[2])+int(veri[8]))
                im.execute("UPDATE gelen_veri SET adet=? WHERE barkod=?", (sayi, gecici,))
                vt.commit()
                sayac=1
                print("3")
                break
            elif gecici==veri[0] and veri[6]=='0' and veri[9]=='0':
                im.execute("UPDATE gelen_veri SET adet2=? WHERE barkod=?", (i[2], gecici,))
                im.execute("UPDATE gelen_veri SET fiyat2=? WHERE barkod=?", (gecici_fiyat,gecici,))
                im.execute("UPDATE gelen_veri SET market2=? WHERE barkod=?", (ad,gecici,))
                vt.commit()
                print("4")
                sayac=1
                break
            elif gecici==veri[0] and veri[9]=='0' and veri[6]!='0':
                im.execute("UPDATE gelen_veri SET adet3=? WHERE barkod=?", (i[2], gecici,))
                im.execute("UPDATE gelen_veri SET fiyat3=? WHERE barkod=?", (gecici_fiyat,gecici,))
                im.execute("UPDATE gelen_veri SET market3=? WHERE barkod=?", (ad,gecici,))
                vt.commit()
                print("5")
                sayac=1
                break
                
        if sayac==0:
            i=list(i)+[0]
            im.execute("""INSERT INTO gelen_veri VALUES
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",i)
            vt.commit()
            im.execute("UPDATE gelen_veri SET market=? WHERE barkod=?", (ad,gecici,))
            vt.commit()
    vt.close()
    veri2.clear()
def kullanici_karsilastir():
    vt = sql.connect('utp_proje.db')
    im = vt.cursor()
    sorgu = """CREATE TABLE IF NOT EXISTS gelen_veri
                (barkod, isim, adet, fiyat, market, adet2, fiyat2, market2, adet3, fiyat3, market3, bitis)"""
    im.execute(sorgu)
    genel_toplam=0.0
    genel=[]
    im.execute("SELECT market FROM gelen_veri")
    adlar=[]
    gönder=""
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
            adlar.append(veri[0])
            break
    for i in adlar:
        sayı=0
        sayac=0

        im.execute("SELECT * FROM gelen_veri WHERE market=?",(i,))
        gönder=gönder+i+" marketinden alınan ürünler :\n"+"-"*(len(i)+29)+"\n\n"+"isim"+" "*44+"adet"+"  "+"fiyat\n"+"\n"+"-"*4+" "*44+"-"*4+"  "+"-"*5+"\n"
        for k in im.fetchall():
            if(len(k)>3):
                gönder=gönder+k[1]+" "*(50-len(k[1]))+k[2]+"    "+k[3]+"\n"
                sayı=sayı+(float(k[2])*float(k[3]))
                sayac=1

        
        im.execute("SELECT * FROM gelen_veri WHERE market2=?",(i,))
        for k in im.fetchall():
            if(len(k)>3):
                gönder=gönder+k[1]+" "*(50-len(k[1]))+k[5]+"    "+k[6]+"\n"
                sayı=sayı+(float(k[5])*float(k[6]))
                sayac=1

        im.execute("SELECT * FROM gelen_veri WHERE market3=?",(i,))
        for k in im.fetchall():
            if(len(k)>3):
                gönder=gönder+k[1]+" "*(50-len(k[1]))+k[8]+"    "+k[9]+"\n"
                sayı=sayı+(float(k[8])*float(k[9]))
                sayac=1
        if sayac==1:
            gönder=gönder+"\nToplam = "+str(round(sayı,2))+"\n\n\n\n"
            genel.append(sayı)
            sayac=0
    
    for v in genel:
        genel_toplam+=v
    gönder=gönder+"Genel Toplam = "+str(genel_toplam)
    vt.close()
    L=os.listdir()
    if(L.count("yol")==0):
        os.mkdir("yol")
    with open("yol/yollanacak.txt","w") as dosya:
        
        dosya.write(gönder)
    return gönder
             
def dosya_gönder():
    smtp_server = "smtp.gmail.com"                   # Giden posta sunucusu
    port = 587                            # Sunucu port ayarı
    user = "utpproje@gmail.com"                          # Kullanıcı adı
    pwd  = "1q2w3e4rk."                          # Parola
    name  = "utp"                         # Alias ID
    alias = "" + name                          # Nickname
    path = "yol/"                          # Split edilmiş dosyaların bulunduğu klasör
    destination = "bkagan0737@gmail.com"                   # Dosyaların gönderileceği e-posta adresi
    text = "alışveriş listesi"                          # E-postanın mesajın gövdesi
     
    # Mecbur kalmadıkça bu noktadan sonra değişiklik yapmayın.
    class mail_sender:
        def __init__(self):
            self.liste = os.listdir(path)
     
        def login(self):
            print("Sunucuya giris yapiliyor...")
            self.mailServer = smtplib.SMTP(smtp_server, port)
            self.mailServer.set_debuglevel(1)
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
            mail['Subject'] = self.dosya      # E-postanın konu kısmı = gönderilen dosyanın ismi
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
            # winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            print('E-posta yollandi. Dosya = ' + self.dosya)
            os.remove(path + os.sep + self.dosya)
            print(self.dosya + ' silindi.')
            print('\n')
     
    a = mail_sender()
    a.begin()             
def mail_yolla(gönder):
    kullanıcı="utpproje@gmail.com"
    kullanıcı_sifresi = '1q2w3e4rk.'
    alıcı = 'bkagan0737@gmail.com'            
    konu = 'Alışveriş listesi'
    email_text = """
    From: {}
    To: {}
    Subject: {}
    {}
    """ .format(kullanıcı,alıcı, konu, gönder)
    server = smtplib.SMTP('smtp.gmail.com:587')   
    server.starttls() 
    server.login(kullanıcı, kullanıcı_sifresi)
    server.sendmail(kullanıcı, alıcı, email_text) 
    server.close()
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
                        market=data2
                        isim=veri[1]
        L=os.listdir()
        if L.count("karsi")==0:
            os.mkdir("karsi")
        with open("karsi/"+market+".txt","a") as dosya:
            dosya.write(barkod2+" "*(15-len(barkod2))+isim+" "*(50-len(isim))+str(max_deger)+"\n")
            max_deger=100000

def veri_silme(bar):
    vt = sql.connect('utp_proje.db')
    im = vt.cursor()
    im.execute("SELECT * FROM gelen_veri WHERE barkod= ?",(bar,))
    silinecek=im.fetchall()
    print(silinecek)
    for i in silinecek:
        i=list(i)
        if int(i[2]) > 1 :
            deger=str(int(i[2])-1)
            im.execute("UPDATE gelen_veri SET adet=? WHERE barkod=?",(deger,bar))
            vt.commit()
        elif i[2] == "1" :
            im.execute("UPDATE gelen_veri SET bitis=? WHERE barkod=?",("1",bar))
            vt.commit()
    vt.close()


def dosya_okuma():
    with open("gecici.txt", "r") as dosya:
        veri = dosya.readlines()
        for i in veri :
            if i == "\n":
                continue
            else :
                i=i.replace("\n","")
                i=i.split("  ")
                i=i+['0','0','0','0','0','0','0']
                print(i)
                i=tuple(i)
                if len(i)==11 or len(i)==8:                
                    veri2.append(i)
    with open("gecici.txt","w") as dosya:
        dosya.write("")

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
            else:
                with open("gecici.txt","a") as dosya:
                    dosya.write(veri2[1]+"\n")
                    

karsilastir()

