import os
from requests.models import Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time, json
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, sys
import time,requests
from bs4 import BeautifulSoup
MAIN_URL = "https://share-w.in/34t7um-33632"
# KEY_PROXY = "TLQZIEPVTevvW7wdoarIkBDwg7AUy8Qvotgsy5"
# KEY_RECAPCHA = "ca86c30ad357b0b4907b0b57622c0030"
KEY_PROXY = "TLVTygcxIf9UBU9kNCTxUWL68FdtyPlwdU2ywJ"
KEY_RECAPCHA = "7a56c6888d71d93c7b636a1ac22ebb10"
data = open("account.txt", "r").read().split("\n")
executable_path = "/usr/lib/chromium-browser/chromedriver"

from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
#display.start()

os.environ["webdriver.chrome.driver"] = executable_path
Folder_run = "/home/asdcxsd/Documents/Code/"
chrome_options = Options()
#chrome_options.add_extension('/home/asdcxsd/Documents/Code/buster_captcha.zip')
#chrome_options.add_extension(Folder_run + 'proxy.zip')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.132 Safari/537.36")
from selenium.webdriver.common.proxy import Proxy, ProxyType

index_data = 0


def get_proxy():
    #return "171.224.233.222:44620"
    time.sleep(5)
    data = requests.get("https://proxy.tinsoftsv.com/api/changeProxy.php?key=" + KEY_PROXY)
    ans = data.content
    print(ans)
    ans = json.loads(ans)
    if (ans['success'] == False):
        timesleep = ans['next_change']
        time.sleep(timesleep)
        
        res = get_proxy();
        time.sleep(5)
        return res
    print(ans['proxy'])
    time.sleep(5)
    return ans['proxy']
#chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--proxy-bypass-list=localhost')
# chrome_options.add_argument('--proxy-server=http://' + ip_port_proxy)



chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

global driver
global PROXY
def init():
    print("Start init")
    global driver
    global PROXY
    PROXY = get_proxy()
    chrome_options.add_argument('--proxy-server=socks5://' + PROXY)
    chrome_options.add_argument('--proxy-server=http://' + PROXY)
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options, desired_capabilities=capa)
    wait = WebDriverWait(driver, 20)
    #driver.set_window_position(-10000,0)
    #driver.set_page_load_timeout(30)
    driver.get(MAIN_URL)
    time.sleep(20)
    driver.execute_script("window.stop();")

    #get first child window
    time.sleep(1)

    robot_add_browser()
    time.sleep(5)
    print("Init success")

def robot_crack(websiteKey):
    global PROXY
    clientKey = KEY_RECAPCHA
    header = {
        "Content-Type" : "application/json"
    }
    data_post = {
        "clientKey":clientKey,
        "task":
        {
            "type":"NoCaptchaTaskProxyless",
            "websiteURL":MAIN_URL,
            "websiteKey":websiteKey,
            "proxyType":"http",
            "proxyAddress":PROXY.split(":")[0],
            "proxyPort":int(PROXY.split(":")[1]),
            "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.132 Safari/537.36"
        }
    }
    data_post = json.dumps(data_post)
    #print(data_post)
    req = requests.post(url="https://api.capmonster.cloud/createTask",headers=header, data=data_post)
    print(req.content)
    data_json = json.loads(req.content)
    if data_json['errorId'] != 0: 
        print("Error")
        raise Exception("Error make request robot")
    else:
        taskId = data_json["taskId"]
    print("taskId:", taskId)
    data_post = {
        "clientKey":clientKey,
        "taskId": int(taskId)
    }
    data_post = json.dumps(data_post)
    #print(data_post)
    while(True):
        time.sleep(1)
        
        req = requests.post("https://api.capmonster.cloud/getTaskResult",headers=header,  data=data_post)

        #print(req.content)
        data_json = json.loads(req.content)
        if (data_json["errorId"] != 0):
            return ""
        if data_json['status'] == "ready":
            response = data_json['solution']
            break
        else:
            if data_json['status'] != "processing": 
                break
        time.sleep(5)
    print("Received solution", response['gRecaptchaResponse'])
    return response['gRecaptchaResponse']

def robot_add_browser():
    global driver
    key_site_driver = driver.find_element_by_class_name('g-recaptcha')
    key_site = key_site_driver.get_attribute("data-sitekey")
    print("Key-site:", key_site)
    response = robot_crack(key_site)
    driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)
    time.sleep(2)

def send_account():
    global driver
    print("Start send account")
    driver.switch_to.default_content()
    #allIframesLen = driver.find_elements_by_tag_name('iframe')

    buttonsubmit = driver.find_element_by_id('security_check_submit')
    buttonsubmit.click()
    time.sleep(20)
    #print(len(allIframesLen))
    # global index_data
    # email_login = data[index_data]
    # index_data+= 1
    while True:
        email_login =random.choice(data).split(":")[0]
        if "gmail" in email_login :
            break
    user_login =  email_login.split("@")[0]
    print("Find username:",email_login)
    #print("OK robot")
    #driver.switch_to.default_content()
    element = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.NAME, "sw_login_name")))
    element.send_keys(user_login)
    time.sleep(1)
    nameaccount = driver.find_element_by_name("sw_login_email")
    nameaccount.send_keys(email_login)
    time.sleep(1)
    nameaccount = driver.find_element_by_name("sw_text_input_11_1")
    nameaccount.send_keys(user_login.replace('.', ''))
    time.sleep(1)
    nameaccount = driver.find_element_by_name("sw_text_input_12_1")
   
    import string
    lst = "0x" + "".join([random.choice(string.ascii_uppercase + string.digits) for n in range(40)])
    lst = "0xCD1b4571C679e15d9C7F6AAc3Dde224f20Dd483C"
    nameaccount.send_keys(lst)
    time.sleep(1)
    button = driver.find_element_by_id("sw_login_button")
    button.click()
    time.sleep(20)

def bypass_filer(start_time):
    global driver
    driver.refresh()
    status = 1
    try:
        time.sleep(20)
        ans = driver.find_element_by_id('sw_entry_method_result_text')
    except Exception as e:
        status = 0
        pass

    while True:
        if (time.time() - start_time) <= 120:
            time.sleep(10)
        else:
            break
    return status

if __name__ == "__main__":
    #global driver

    count = 0
    success = 0
    firewall = 0
    checkbot = 0
    start_time_global = time.time()
    try:
        while (True):
            start_time = time.time()
            count += 1
            try:
                init()
                firewall += 1
                #robot_bypass()
                checkbot += 1
                send_account()
                success += bypass_filer(start_time)
               
            except Exception as e:
                print(e)
                pass
            finally:
                driver.quit()
            print("Lan: ", count ,",Thanh cong: ", success, ",Firewall: ", firewall, ",RobotCheck: ", checkbot,  ",Thoi gian: ", (time.time() - start_time), ",Tong: ", time.time() - start_time_global) 
    except Exception as e:
        print(e)
        pass
    display.stop()
