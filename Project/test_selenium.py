# ─────────────────────────────────────────────────────────────────────────────
#  Selenium Test — Password Vault
#  Run this AFTER starting the Flask server:  python app.py
#  Requires:  pip install selenium  +  ChromeDriver installed and in PATH
# ─────────────────────────────────────────────────────────────────────────────
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    driver.get("http://localhost:5000")

    # ── Test 1: Generate Password ─────────────────────────────────────────────
    gen_btn = driver.find_element(By.ID, "generate-btn")
    gen_btn.click()
    time.sleep(0.5)

    pwd_field = driver.find_element(By.ID, "password")
    pwd_value = pwd_field.get_attribute("value")
    assert len(pwd_value) == 12, f"❌ Password length wrong: {len(pwd_value)}"
    print("✅ Test 1 PASSED — Password generated with 12 characters")

    # ── Test 2: Strength bar visible ──────────────────────────────────────────
    bar = driver.find_element(By.ID, "strength-bar")
    assert bar.is_displayed(), "❌ Strength bar not visible"
    print("✅ Test 2 PASSED — Strength bar is displayed")

    # ── Test 3: Password field is now visible (type=text) ─────────────────────
    assert pwd_field.get_attribute("type") == "text", "❌ Password not revealed after generate"
    print("✅ Test 3 PASSED — Password field revealed after generation")

    # ── Test 4: Save a credential ─────────────────────────────────────────────
    driver.find_element(By.ID, "site").send_keys("TestSite")
    driver.find_element(By.ID, "username").send_keys("test@example.com")
    driver.find_element(By.ID, "save-btn").click()
    time.sleep(0.8)

    # Vault should show 1+ entry
    count_el = driver.find_element(By.ID, "entry-count")
    assert int(count_el.text) >= 1, "❌ Entry not saved to vault"
    print("✅ Test 4 PASSED — Credential saved and appears in vault")

    # ── Test 5: Show/hide toggle works ────────────────────────────────────────
    reveal_btns = driver.find_elements(By.CLASS_NAME, "reveal-btn")
    assert len(reveal_btns) > 0, "❌ No reveal buttons found"
    reveal_btns[0].click()
    time.sleep(0.3)
    pwd_span = driver.find_elements(By.CSS_SELECTOR, "[id^='pwd-']")[0]
    # After click, dots should be replaced by real password (no 'pwd-dots' class)
    assert "pwd-dots" not in pwd_span.get_attribute("class"), "❌ Password not revealed"
    print("✅ Test 5 PASSED — Per-entry show/hide toggle works")

    print("\n🎉 ALL TESTS PASSED!")

finally:
    driver.quit()