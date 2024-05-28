from flask import Flask, request
import logging
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
CORS(app)

def find_apply_elements(driver):
    # List to store the elements containing the word 'apply'
    apply_elements = []

    # Wait for buttons and links to load
    try:
        WebDriverWait(driver, 5, 0.2).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))
        )
    except TimeoutException:
        app.logger.info("No buttons found within the timeout period.")

    try:
        WebDriverWait(driver, 5, 0.2).until(
            EC.element_to_be_clickable((By.TAG_NAME, "a"))
        )
    except TimeoutException:
        app.logger.info("No links found within the timeout period.")

    buttons = driver.find_elements(By.TAG_NAME, 'button')
    links = driver.find_elements(By.TAG_NAME, 'a')

    # Search for the word 'apply' in buttons and links and their child elements
    for element in buttons + links:
        if 'apply' in element.text.lower():
            apply_elements.append(element)
        for child in element.find_elements(By.XPATH, './/*'):
            if 'apply' in child.text.lower():
                apply_elements.append(child)

    return apply_elements

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    options = Options()
    driver = webdriver.Remote(
        command_executor='http://selenium:4444',
        options=options)
    
    driver.set_page_load_timeout(10)  # Set page load timeout to 10 seconds

    driver.get(url)


    app.logger.info(f"Current URL: {driver.current_url}")  # check url
    # Apply the logic to the entire DOM
    apply_elements = find_apply_elements(driver)

    # Find all iframes eon the pag
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')

    for iframe in iframes:
        # Switch to the iframe
        driver.switch_to.frame(iframe)

        # Apply the logic to the iframe
        apply_elements += find_apply_elements(driver)

        # Switch back to the main document before moving to the next iframe
        driver.switch_to.default_content()

    driver.quit()

    app.logger.info(f"Found {len(apply_elements)} elements containing the word 'apply'")

    return {"message": "Scraping completed successfully"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)