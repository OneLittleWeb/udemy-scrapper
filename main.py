from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Set up the WebDriver (make sure to specify the correct path to your WebDriver)
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
})
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--v=1")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get("https://www.skool.com/@mishel-sharp-3298")

# Wait for the necessary elements to load
wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary

try:
    # Wait and extract data once elements are loaded
    username = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".styled__UserNameText-sc-24o0l3-1"))).text
    user_handle = driver.find_element(By.CSS_SELECTOR, ".styled__UserHandle-sc-1gipnml-6").text
    description = driver.find_element(By.CSS_SELECTOR, ".styled__Bio-sc-1gipnml-9").text
    last_active = driver.find_element(By.CSS_SELECTOR, ".styled__IconInfoItem-sc-1gipnml-7.Yssjy:nth-of-type(1) span").text
    joined_date = driver.find_element(By.CSS_SELECTOR, ".styled__IconInfoItem-sc-1gipnml-7.Yssjy:nth-of-type(2) span").text
    living_area = driver.find_element(By.CSS_SELECTOR, ".styled__IconInfoItem-sc-1gipnml-7.Yssjy:nth-of-type(3) span").text
    contributions = driver.find_element(By.CSS_SELECTOR, "div[style='border-width:1px 0px;'] a:nth-of-type(1) .Typography-sc-6btf7m-0.dxNuFR").text
    followers = driver.find_element(By.CSS_SELECTOR, "div[style='border-width:1px 0px;'] a:nth-of-type(2) .Typography-sc-6btf7m-0.dxNuFR").text
    following = driver.find_element(By.CSS_SELECTOR, "div[style='border-width:1px 0px;'] a:nth-of-type(3) .Typography-sc-6btf7m-0.dxNuFR").text
    youtube_link = driver.find_element(By.CSS_SELECTOR, "a[href*='youtube.com']").get_attribute('href')
    linkedin_link = driver.find_element(By.CSS_SELECTOR, "a[href*='linkedin.com']").get_attribute('href')
    facebook_link = driver.find_element(By.CSS_SELECTOR, "a[href*='facebook.com']").get_attribute('href')

    # Print extracted data
    print(f"Username: {username}")
    print(f"User Handle: {user_handle}")
    print(f"Description: {description}")
    print(f"Last Active: {last_active}")
    print(f"Joined Date: {joined_date}")
    print(f"Living Area: {living_area}")
    print(f"Contributions: {contributions}")
    print(f"Followers: {followers}")
    print(f"Following: {following}")
    print(f"YouTube Link: {youtube_link}")
    print(f"LinkedIn Link: {linkedin_link}")
    print(f"Facebook Link: {facebook_link}")

finally:
    # Clean up by closing the browser
    driver.quit()
