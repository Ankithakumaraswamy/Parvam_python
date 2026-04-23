# Selenium Test — Food Calorie Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def run_test():
    print("Starting Selenium Test...")
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    
    try:
        # First, register a test user
        driver.get("http://127.0.0.1:5000/register")
        
        # We append timestamp to make username unique across multiple test runs
        test_user = f"testuser_{int(time.time())}"
        
        driver.find_element(By.ID, "username").send_keys(test_user)
        driver.find_element(By.ID, "password").send_keys("testpass")
        
        goal_input = driver.find_element(By.ID, "goal")
        goal_input.clear()
        goal_input.send_keys("1500") 
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        
        # Now login
        driver.find_element(By.ID, "username").send_keys(test_user)
        driver.find_element(By.ID, "password").send_keys("testpass")
        driver.find_element(By.ID, "login-btn").click()
        time.sleep(1)
        
        # Log food items to exceed goal
        print("Logging meals to exceed goal...")
        for i in range(10):
            food_input = driver.find_element(By.ID, "food-item")
            food_input.clear()
            food_input.send_keys("Idli")
            
            cal_input = driver.find_element(By.ID, "calories")
            cal_input.clear()
            cal_input.send_keys("200")
            
            driver.find_element(By.ID, "log-btn").click()
            time.sleep(0.3)
            
        # Assert calorie limit exceeded warning
        print("Checking assertions...")
        warning = driver.find_element(By.CLASS_NAME, "calorie-exceeded")
        assert warning.is_displayed(), "Warning element is not displayed!"
        
        bar = driver.find_element(By.ID, "calorie-bar")
        class_attr = bar.get_attribute("class")
        
        assert "red" in class_attr, "Progress bar does not contain 'red' class!"
        print("[SUCCESS] Auto calorie limit warning PASSED")
        
    except Exception as e:
        print(f"[FAIL] Test FAILED: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Ensure the Flask app is running on port 5000 before running this test.")
    run_test()
