# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import requests
import sys
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import tkinter
import tkinter.filedialog
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


# /Users/userName/Python3/Scraping/idole
# pyinstaller idole.py --onefile                   
login_url = 'https://tiget.net/users/sign_in'

# ファイル選択ダイアログの表示
file_path = tkinter.filedialog.askopenfilename(initialdir="/Users/tsutsumi/Python3/Scraping/idole")
# ファイルを開いて読み込んでdataに格納
f = open(file_path,'r')
datalist = f.readlines()
mail = datalist[0].rstrip('\n')
password = datalist[1].rstrip('\n')
nickname = datalist[2].rstrip('\n')
oshi = int(datalist[3].rstrip('\n'))
tel1 = datalist[4].rstrip('\n')
tel2 = datalist[5].rstrip('\n')
tel3 = datalist[6].rstrip('\n')
yuubin = datalist[7].rstrip('\n')
addless = datalist[8].rstrip('\n')
name1 = datalist[9].rstrip('\n')
name2 = datalist[10].rstrip('\n')
home_url = datalist[11].rstrip('\n')
array_index = int(datalist[12].rstrip('\n'))
yyyy = int(datalist[13].rstrip('\n'))
mm = int(datalist[14].rstrip('\n'))
dd = int(datalist[15].rstrip('\n'))
hh = int(datalist[16].rstrip('\n'))
mi = int(datalist[17].rstrip('\n'))
ss = int(datalist[18].rstrip('\n'))
miriss = int(datalist[19].rstrip('\n'))
f.close()


#python3.9.6 64bitで実行するとうまくいく
# driver = webdriver.Chrome()
# options = Options()
options = webdriver.FirefoxOptions()
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
# 追加----------------------------------------------------------
# ヘッドレス化
options.headless = True
# 必須
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
# エラーの許容
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
# headless では不要そうな機能を除外
options.add_argument('--disable-desktop-notifications')
options.add_argument("--disable-extensions")
# UA設定 （なくてもいい）
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0')
# 言語 (なくてもいいが言語によって表示されるページが変わる可能性があるので念のため)
options.add_argument('--lang=ja')
# 画像を読み込まないで軽くする
options.add_argument('--blink-settings=imagesEnabled=false')
# 追加----------------------------------------------------------

options.set_preference('--permissions.default.image',2)
options.page_load_strategy = 'eager' # eager ページの完全読み込みを待たない
options.set_preference('--browser.cache.disk.enable',False)
options.set_preference('--browser.cache.memory.enable',True)
options.set_preference('--network.http.pipelining',True)
options.set_preference('--network.http.proxy.pipelining',True)
options.set_preference('--network.http.pipelining.ssl',True)
options.set_preference('--browser.tabs.animate',False)
options.set_preference('--browser.panorama.animate_zoom',False)
options.set_preference('--browser.cache.memory.max_entry_size',1000000)

options.set_preference('--services.sync.prefs.sync.permissions.default.image',False)

driver = webdriver.Firefox(firefox_profile=firefox_profile,options=options)
# driver = webdriver.Firefox()
driver.maximize_window()
# ログインページ    
driver.get(login_url) 
# メールアドレス
driver.find_element(By.ID, "user_email").send_keys(mail)
# パスワード
driver.find_element(By.ID, "user_password").send_keys(password)
# ログインボタン
driver.find_element(By.CSS_SELECTOR,"input[value='ログイン']").submit()
time.sleep(2)
# チケット画面へ
driver.get(home_url) 
time.sleep(3)

# 指定の時間まで待機
startDt = datetime.datetime(yyyy,mm,dd,hh,mi,ss,miriss)
print(startDt)
diff = startDt - datetime.datetime.now()

if diff.seconds < 600 and diff.seconds > 3:
    print("until specified time " + str(int(diff.seconds) - 5) + " seconds Sleep")
    sleep(int(diff.seconds - 5))
while True:
    dt_now = datetime.datetime.now()
    print(dt_now)
    if dt_now > startDt:
        # driver.refresh()
        # 時間計測開始
        time_sta = time.time()
        driver.get(home_url) 
        print("Startーーーーーーーーーーーー")
        dt_now = datetime.datetime.now()
        print(dt_now)
        break
    print("untilStartーーーーーーーーーーーー")

# 女性エリアボタン　
girlsBtn = driver.find_elements(By.CLASS_NAME,"c-ordering-btn__content__status")
girlsBtn[array_index].click()

# # 女性エリアボタン押せるまでぶん回す
# while True:
#     # 女性エリアボタン　
#     girlsBtn = driver.find_elements(By.CLASS_NAME,"c-ordering-btn__content__status")
#     girlsBtn[array_index].click()
#     cur_url = driver.current_url
#     if cur_url != home_url:
#         # 時間計測開始
#         time_sta = time.time()
#         print("発売開始！ーーーーーーーーーーーー")
#         dt_now = datetime.datetime.now()
#         print(dt_now)
#         break
#     print("発売開始前")
#     driver.refresh()


# チケット情報入力画面
# 推しメン
if len(driver.find_elements(By.ID,"audience_introducer")) > 0 :
    dropdown = driver.find_element(By.ID,"audience_introducer")
    select = Select(dropdown).select_by_index(oshi)
# 備考
# チェックボックス
driver.find_element(By.ID, "checke").click()
# 次へボタン
driver.find_element(By.ID,"submitBtn").submit()

# 予約確定
while True:
    submitBtn = driver.find_elements(By.ID,"submitBtn-nonagree")
    if len(submitBtn) > 0 :
        # driver.find_element(By.ID,"submitBtn-nonagree").submit()
        # 時間計測終了
        time_end = time.time()
        # 経過時間（秒）
        tim = time_end- time_sta
        print("Successーーーーーーーーーーーー")
        print('チケット取得所要時間：' + str(tim))
        dt_now = datetime.datetime.now()
        print('チケット予約完了日時：' + str(dt_now))
        # チケ番号を取得
        sleep(5)
        num = driver.find_element(By.ID,"show-modal-number")
        print('ticket Number：' + num.text)
        break
    # print("submitボタン見つからないためループ")

time.sleep(10)
# ブラウザを終了する。
driver.close()