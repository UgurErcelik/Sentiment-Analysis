from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

class TwitterBot:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.bot=webdriver.Chrome()

    def login(self):
        bot=self.bot
        bot.get('https://twitter.com/login')
        bot.implicitly_wait(5)
        
        email=bot.find_element_by_name('session[username_or_email]')
        password=bot.find_element_by_name('session[password]')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)

    def find_tweet(self,hashtag,baslangic_tarih,bitis_tarih,dosya_yolu):
        sayac=0
        time.sleep(4)
        tarih_listesi=[]
        isim_listesi=[]
        tweetin_listesi=[]
        dil_listesi=[]
        link_listesi=[]
        self.dosya_yolu=dosya_yolu
        self.baslangic_tarih=baslangic_tarih
        self.bitis_tarih=bitis_tarih
        bot=self.bot
        tweet_listesi=[]
        #Arama textfieldına tıklayıp hashtag gönderme ve arama yapma
        search=bot.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input')
        search.send_keys(hashtag+","+'lang:en '+"SINCE:"+baslangic_tarih+" UNTIL:"+bitis_tarih)
        search.send_keys(Keys.RETURN)
        bot.implicitly_wait(5)
        #Twitterda hashtag aradıktan sonra latest bölümüne tıklama
        latest=bot.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/span')
        latest.click()
        veri_kumesi=set()

        lenOfPage=bot.execute_script('window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage')
        hata_sayac=1

        match=False
        while(match==False):
            lastcount=lenOfPage
            bot.implicitly_wait(5)

            post=bot.find_elements_by_css_selector('.css-1dbjc4n.r-1loqt21.r-18u37iz.r-1ny4l3l.r-1udh08x.r-1yt7n81.r-ry3cjt.r-o7ynqc.r-6416eg')
            for tweets in post:
                try:
                    tweet=tweets.find_element_by_css_selector('.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0')
                    isim=tweets.find_element_by_css_selector('.css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0').text
                    link=tweets.find_element_by_css_selector('.css-4rbku5.css-18t94o4.css-1dbjc4n.r-sdzlij.r-1loqt21.r-1adg3ll.r-ahm1il.r-1ny4l3l.r-1udh08x.r-o7ynqc.r-6416eg.r-13qz1uu').get_attribute('href')                  
                    dil=tweet.get_attribute('lang')                   
                    tweet_listesi.append(tweet.text)                    
                    print(isim)
                    print(tweet.text)
                    print(link)
                    print(dil)
                    print('**********************')                   
                    tweet_listesi.append(dil)                    
                    veri_kumesi.add((isim,tweet.text,dil,link))
                except:
                    print(hata_sayac,end='')
                    print('.hata')
                    hata_sayac+=1


            lenOfPage=bot.execute_script('window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage')
            if lastcount==lenOfPage:
                match=True
        bot.implicitly_wait(5)
        sayac=1
        for i in veri_kumesi:
            isim=i[0]
            tweet=i[1]
            dil=i[2]
            link=i[3]
            print(tweet)
            tweetin_listesi.append(tweet)
            print(isim)
            isim_listesi.append(isim)
            print(dil)
            dil_listesi.append(dil)
            print(sayac)
            link_listesi.append(link)
            print(link)
            sayac+=1
            print('*********')
        df=pd.DataFrame({
            "isim":isim_listesi,
            "tweet":tweetin_listesi,
            "dil":dil_listesi,
            "link":link_listesi})
        df.to_csv(dosya_yolu,encoding='utf-8')
ed=TwitterBot('username','password')
ed.login()
ed.find_tweet('messi',"2020-12-13","2020-12-15","messi8.csv")