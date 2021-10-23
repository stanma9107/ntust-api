import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from recaptcha import recaptchaSolver

def login(username, password):
    load_dotenv()
    antiCaptchaKey = os.environ["ANTI_CAPTCHA_API_KEY"]
    loginPageURL = "https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection?ReturnUrl=CourseSelection"
    correctURL = "https://courseselection.ntust.edu.tw/"

    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    
    driver.get(loginPageURL)

    # Get siteKey
    siteKeyElement = driver.find_element(By.CSS_SELECTOR, "div.g-recaptcha")
    siteKey = siteKeyElement.get_attribute("data-sitekey")

    # Get Verify Token Field
    verifyTokenField = driver.find_element(By.NAME, "__RequestVerificationToken")
    verifyToken = verifyTokenField.get_attribute("value")

    # Set Username Field
    usernameField = driver.find_element(By.NAME, "UserName")
    usernameField.send_keys(username)

    # Set Password Field
    passwordField = driver.find_element(By.NAME, "Password")
    passwordField.send_keys(password)

    # Slove Recaptcha
    recaptcha = recaptchaSolver(
        apiKey=antiCaptchaKey,
        url=loginPageURL,
        siteKey=siteKey
    )

    if recaptcha["success"] == True:
        # Set g-recaptcha-response Field with JS
        driver.execute_script("$('.g-recaptcha-response').html('{0}')".format(recaptcha["result"]))

        # Submit Form
        driver.execute_script("$('form.login-form-container')[0].submit()")

        cookies = driver.get_cookies()

        if driver.current_url == correctURL:
            return {
                "success": True,
                "cookies": cookies
            }
        else:
            return {
                "success": False
            }
    else:
        return {
            "success": False
        }