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
from datetime import timedelta
import tkinter
import tkinter.filedialog
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import json

# cd /Users/tsutsumi/Python3/Scraping/idole
# pyinstaller idole.py --onefile

# JSONファイルからデータを読み込む
with open('/Users/tsutsumi/Python3/Scraping/idole/token/token.json') as f:
    data = json.load(f)
f.close()
# 'dev'と'prd'の値を取得する
dev_token = data['dev']
prd_token = data['prd']

LINE_NOTIFY_API = 'https://notify-api.line.me/api/notify'
# テスト用
LINE_NOTIFY_TOKEN = dev_token
# 本番用 
# LINE_NOTIFY_TOKEN = prd_token

login_url = 'https://tiget.net/users/sign_in'
args = sys.argv
# ファイル選択ダイアログの表示
file_path = tkinter.filedialog.askopenfilename(initialdir="/Users/tsutsumi/Python3/Scraping/idole/UserText")
with open(file_path) as f:
    data = json.load(f)
f.close()
mailaddless = data['mailaddless']
password = data['password']
nickname = data['nickname']
oshi = int(data['oshi'])
tel1 = data['tel1']
tel2 = data['tel2']
tel3 = data['tel3']
postcode = data['postcode']
addless = data['addless']
firstName = data['firstName']
lastName = data['lastName']
home_url = data['home_url']
array_index = int(data['array_index'])
yyyy = int(data['yyyy'])
mm = int(data['mm'])
dd = int(data['dd'])
hh = int(data['hh'])
mi = int(data['mi'])
ss = int(data['ss'])
mSeconds = int(data['mSeconds'])
# クレカ決済
iscardstr = data['iscard']
iscard = False
if iscardstr.upper() == 'TRUE':
    iscard = True
# コンビニ決済
isconvstr = data['isconv']
isconv = False
if isconvstr.upper() == 'TRUE':
    isconv = True



#python3.9.6 64bitで実行するとうまくいく
# driver = webdriver.Chrome()
options = Options()
options = webdriver.FirefoxOptions()
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
# 追加----------------------------------------------------------
# ヘッドレス化
# options.add_argument('--headless')
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

driver = webdriver.Firefox(options=options)
driver.maximize_window()
# ログインページ 　   
driver.get(login_url) 
# メールアドレス
driver.find_element(By.ID, "user_email").send_keys(mailaddless)
# パスワード
driver.find_element(By.ID, "user_password").send_keys(password)
# ログインボタン
driver.find_element(By.CSS_SELECTOR,"input[value='ログイン']").submit()
time.sleep(2)
# チケット画面へ
driver.get(home_url) 
time.sleep(3)



# 指定の時間まで待機
# LINE通知する
startDt = datetime.datetime(yyyy,mm,dd,hh,mi,ss,mSeconds)
print(startDt)
diff = startDt - datetime.datetime.now()
def waitprogram():
    # エラーチェック
    if iscard is True and isconv is True:
        send_line_notify('\n' + 'エラーチェック' + '\n' + 'コンビニ決済とクレカ決済が両方Trueのためエラー')
        sys.exit()
    type = ''
    if iscard:
        type = 'クレカ決済💳'
    elif isconv:
        type = 'コンビニ決済🏪'
    else:
        type = '当日支払い🙋‍♀️'

    send_line_notify('\n' + 'プログラムを起動しました。' + '\n' + 'ニックネーム：' + nickname  + '\n' + '決済方法：' + type +'\n' + '販売開始時刻：' + str(startDt) + '\n' + 'URL：' + home_url)
    if diff.seconds < 300 or diff.days < 0:
        return
    # 5分前まで待機
    send_line_notify('\n' + '発売開始まで時間があるので5分前になるまで一時スリープ🛌' + '\n' + 'ニックネーム：' + nickname)
    while True:
        try:
            difftimes = startDt - datetime.datetime.now()
            print('指定時間(5分前)まであと ' + str(difftimes.seconds) + '秒')
            if difftimes.seconds < 300:
                send_line_notify('\n' + '5分前になったので起床🌞' + '\n' + 'ニックネーム：' + nickname)
                break
            sleep(10)
        except:
            send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
            sys.exit()

def main():
    diff = startDt - datetime.datetime.now()
    if diff.seconds < 600 and diff.seconds > 3 and diff.days >= 0:
        print("until specified time " + str(int(diff.seconds) - 10) + " seconds Sleep")
        sleep(int(diff.seconds - 10))
    while True:
        try:
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
        except:
            send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
            sys.exit()

    # 女性エリアボタン　
    while True:
        try:
            girlsBtn = driver.find_elements(By.CLASS_NAME,"c-ordering-btn__content__status")
            if len(girlsBtn) > 0 :
                girlsBtn[array_index].click()
                print('女性エリボタンクリック')
                break
            print('女性エリボタン表示前')
        except:
            send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
            sys.exit()

    # コンビニ決済の場合
    if isconv:
        while True:
            try:
                radio = driver.find_elements(By.CLASS_NAME,"pay_method-label")
                if len(radio) > 0 :
                    # コンビニ決済
                    radio[1].click()
                    print('コンビニ決済選択')
                    break
                print('コンビニ決済表示前')
            except:
                send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
                sys.exit()

    # チケット情報入力画面
    # 推しメン
    while True:
        try:
            if len(driver.find_elements(By.ID, "checke")) > 0 :
                if len(driver.find_elements(By.ID,"audience_introducer")) > 0 :
                    dropdown = driver.find_element(By.ID,"audience_introducer")
                    select = Select(dropdown).select_by_index(oshi)
                break
            print('推しメン表示前')
        except:
            send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
            sys.exit()

    # 備考
    try:
        # チェックボックス
        driver.find_element(By.ID, "checke").click()
        # 次へボタン
        driver.find_element(By.ID,"submitBtn").submit()
        print('次へボタンクリック')
    except:
        send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
        sys.exit()

    # コンビニ決済の場合
    if isconv:
        while True:
            try:
                radio = driver.find_elements(By.CLASS_NAME,"cvs-payment-name")
                if len(radio) > 0 :
                    # ファミマ
                    radio[0].click()
                    # 次へボタン
                    driver.find_element(By.ID,"ticket_cvs_submit").submit()
                    print('支払いコンビニ選択し、次へボタンクリック')
                    break
                print('支払いコンビニ表示前のためループ')
            except:
                send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
                sys.exit()

    # カード決済の場合
    if iscard:
        # クレカ画面で次へボタン
        try:
            while True:
                if len(driver.find_elements(By.CSS_SELECTOR,".btn.button-green.center-button.card-page-btn")) > 0 :
                    # クレカ選択（2枚目に）
                    card = driver.find_elements(By.CSS_SELECTOR,".card-image-box.card-image-box-registed")
                    # card[1].click()
                    card[0].click()
                    driver.find_element(By.CSS_SELECTOR,".btn.button-green.center-button.card-page-btn").click()
                    print('クレカ画面次へボタンクリック')
                    break
                print('クレカ画面次へボタン非活性のためループ')
        except:
            send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
            sys.exit()

       
        count = 0
        try:
            while True:
                submitBtn = driver.find_elements(By.ID,"submitBtn-nonagree")
                if len(submitBtn) > 0 :
                    driver.find_element(By.ID,"submitBtn-nonagree").submit()
                    break

            while True:
                 # VISA認証画面(表示されない可能性もあり)
                time.sleep(20)
                if len(driver.find_elements(By.ID,"password")) > 0 :
                    driver.find_element(By.ID,"password").send_keys('Aa223036222')
                    driver.find_element(By.ID,"submitBtn").submit()
                    break

                # チケット確定している可能性を考慮
                if len(driver.find_elements(By.ID,"show-modal-number")) > 0:
                    num = driver.find_element(By.ID,"show-modal-number")
                    print('ticket Number：' + num.text)
                    if len(num.text) == 0:
                        send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
                        sys.exit()
                        
                    send_line_notify('\n' + 'チケット取得完了しました❗️' + '\n' + 'ニックネーム：' + nickname + '\n' + 'チケット番号：' + num.text )
                    sys.exit()
                # count = count + 1
                # print('count：' + str(count))
                # if count > 30 :
                #     break
        except:
            send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
            sys.exit()
        
        count = 0
            
    # 予約確定
    while True:
        try:
            submitBtn = driver.find_elements(By.ID,"submitBtn-nonagree")
            if len(submitBtn) > 0 :
                driver.find_element(By.ID,"submitBtn-nonagree").submit()
                # 時間計測終了
                time_end = time.time()
                # 経過時間（秒）
                tim = time_end- time_sta
                print("Successーーーーーーーーーーーー")
                print('チケット取得所要時間：' + str(tim))
                dt_now = datetime.datetime.now()
                print('チケット予約完了日時：' + str(dt_now))
                send_line_notify('\n' + 'ニックネーム：' + nickname + '\n' + '取れたっぽい')
                # チケ番号を取得
                sleep(5)
                if len(driver.find_elements(By.ID,"show-modal-number")) > 0:
                    num = driver.find_element(By.ID,"show-modal-number")
                    print('ticket Number：' + num.text)
                    send_line_notify('\n' + 'チケット取得完了しました❗️' + '\n' + 'ニックネーム：' + nickname + '\n' + 'チケット番号：' + num.text )
                break
            print("submitボタン見つからないためループ")
        except:
            send_line_notify('\n' + '処理失敗しました😭手動で取得してください')
            sys.exit()
    
    # お片付け
    time.sleep(10)
    # ブラウザを終了する。
    driver.close()

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    headers = {'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'}
    data = {'message': f'{notification_message}'}
    requests.post(LINE_NOTIFY_API, headers = headers, data = data)

if __name__ == "__main__":
    waitprogram()
    main()
    sys.exit()