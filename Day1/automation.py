import os
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://scholar.parvam.in"
LOGIN_ENDPOINT = "/student/login"
SUCCESS_ENDPOINT = "/student/dashboard"
LOGIN_URL = f"{BASE_URL}{LOGIN_ENDPOINT}"
SUCCESS_URL = f"{BASE_URL}{SUCCESS_ENDPOINT}"
EMAIL = os.getenv("PARVAM_EMAIL", "ankitha@gmail.com")
PASSWORD = os.getenv("PARVAM_PASSWORD", "ankitha005")
SHOW_BROWSER = os.getenv("SHOW_BROWSER", "true").lower() == "true"


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-features=Translate,OptimizationHints,MediaRouter")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")

    if not SHOW_BROWSER:
        chrome_options.add_argument("--headless=new")

    service = Service(log_output=os.devnull)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def wait_for_success(driver, wait):
    try:
        wait.until(lambda current_driver: current_driver.current_url != LOGIN_URL)
    except TimeoutException:
        print("Login page did not redirect in time.")
        return False

    current_url = driver.current_url
    print(f"Current URL: {current_url}")

    if current_url == SUCCESS_URL or SUCCESS_ENDPOINT in current_url:
        print("Success URL reached.")
        return True

    if LOGIN_ENDPOINT in current_url:
        print("Still on the login page.")
        return False

    print("Page redirected, but not to the expected success URL.")
    return False


def login():
    driver = None

    try:
        print("Opening Chrome browser...")
        driver = create_driver()
        wait = WebDriverWait(driver, 20)
        driver.get(LOGIN_URL)
        print("Login page opened.")

        email_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email' or contains(@placeholder, 'Email')]"))
        )
        password_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        sign_in_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sign in') or contains(., 'Login')]"))
        )

        email_field.clear()
        email_field.send_keys(EMAIL)
        password_field.clear()
        password_field.send_keys(PASSWORD)
        print("Credentials entered.")
        sign_in_button.click()
        print("Login button clicked.")

        if wait_for_success(driver, wait):
            print("Login submitted successfully.")
        else:
            print("Login attempt finished, but success URL was not confirmed.")

        input("Press Enter to close the browser...")
    except SessionNotCreatedException:
        print("Chrome could not start. Please check that Chrome and ChromeDriver versions match.")
        input("Press Enter to close the browser...")
    except WebDriverException as error:
        print(f"ChromeDriver error: {error.msg}")
        input("Press Enter to close the browser...")
    except Exception as error:
        print(f"Automation failed: {error}")
        input("Press Enter to close the browser...")
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    login()
