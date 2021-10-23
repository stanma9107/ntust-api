from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def loadCookie(cookies):
    loginPageURL = "https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection"
    setCookieURL = "https://courseselection.ntust.edu.tw/test"
    checkSessionURL = "https://courseselection.ntust.edu.tw/"

    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get(setCookieURL)

    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(checkSessionURL)
    if driver.current_url == loginPageURL:
        return {
            "success": False
        }
    else:
        return {
            "success": True,
            "driver": driver,
        }