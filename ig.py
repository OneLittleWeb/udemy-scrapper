import pandas as pd
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

def setup_driver():
    """Setup Selenium WebDriver with options."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    return driver

def scrape_data(url):
    """Scrape data for a single URL using Selenium."""
    driver = setup_driver()
    driver.get(url)
    wait = WebDriverWait(driver, 10)  # Adjust timeout as needed
    try:
        total_students = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div:nth-of-type(1) > .ud-heading-xl"))).text
        reviews = driver.find_element(By.CSS_SELECTOR, "div:nth-of-type(2) > .ud-heading-xl").text
        social_media_links = driver.find_elements(By.CSS_SELECTOR, "div.instructor-profile--social-links--02JZE a")
        social_links = {link.text: link.get_attribute('href') for link in social_media_links}
        result = (url, total_students, reviews, str(social_links))
    except Exception as e:
        print(f"Error processing {url}: {e}")
        result = None
    finally:
        driver.quit()
    return result

def main():
    file_path = r'C:\Users\One Little Web\Desktop\udemy.csv'
    df = pd.read_csv(file_path)
    # Filter rows where Reviews is empty
    df_filtered = df[df['Reviews'].isna() | (df['Reviews'] == '')]
    df_filtered = df_filtered.head(4)  # Limit to the first 10 entries

    results = []
    # Use ThreadPoolExecutor to execute multiple instances of Selenium concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(scrape_data, row['url']): row for index, row in df_filtered.iterrows()}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    # Update DataFrame with results
    for url, total_students, reviews, social_links in results:
        idx = df.index[df['url'] == url].tolist()
        if idx:  # Ensure we have exactly one match
            df.at[idx[0], 'Total Students'] = total_students
            df.at[idx[0], 'Reviews'] = reviews
            df.at[idx[0], 'Social Media Links'] = social_links

    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    print("All data has been processed and saved.")

if __name__ == "__main__":
    main()
