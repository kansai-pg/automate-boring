from aws_tools_class import aws_tools
import time
import selenium 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tempfile import mkdtemp
import os

#http://holiday-programmer.net/selenium-teams1/
id  = os.getenv('email') #ログイン用のメアド
pw  = aws_tools.get_pass() #ログイン用のパス

def handler(event=None, context=None):
    options = selenium.webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
#     options.add_argument(f"--user-data-dir={mkdtemp()}")
#     options.add_argument(f"--data-path={mkdtemp()}")
#     options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    options.binary_location = "./chrome-linux/chrome"

    driver = selenium.webdriver.Chrome('./chromedriver', options=options)
   #URL
    driver.get(os.getenv('url',"https://teams.microsoft.com/_#/conversations/48:notes?ctx=chat"))

    #メアド入力
    time.sleep(3)
    driver.find_element(By.NAME,"loginfmt").send_keys(id)
    driver.find_element(By.ID,"idSIButton9").click()

    #パスワード入力
    time.sleep(3)
    driver.find_element(By.NAME,"passwd").send_keys(pw)
    driver.find_element(By.ID,"idSIButton9").click()

    #サインインの状態を維持しますか？   →   いいえ
    time.sleep(3)
    driver.find_element(By.ID,"idBtn_Back").click()

    # Teamsチャット画面
    time.sleep(60)
    
    try:
        driver.find_element(By.XPATH,'/html/body/promote-desktop/div/div/div/div[1]/div[2]/div/a').click()
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR, ".action-button:nth-child(2) > .text").click()
    except:
        pass
    
    send_text = aws_tools.get_cost()
    driver.switch_to.frame(0)
    driver.find_element(By.CLASS_NAME, "cke_textarea_inline").send_keys("自動通知")
    driver.find_element(By.CLASS_NAME, "cke_textarea_inline").send_keys(Keys.SHIFT,"\n")
    driver.find_element(By.CLASS_NAME, "cke_textarea_inline").send_keys(send_text['time'])
    driver.find_element(By.CLASS_NAME, "cke_textarea_inline").send_keys(Keys.SHIFT,"\n")
    driver.find_element(By.CLASS_NAME, "cke_textarea_inline").send_keys(send_text['cost'])
    driver.find_element(By.XPATH, "//button[@data-tid='newMessageCommands-send']").click()

    time.sleep(30)
    
    driver.quit()
    return
