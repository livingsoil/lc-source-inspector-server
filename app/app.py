from flask import Flask, request
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

app = Flask(__name__)
CORS(app)

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

    driver.get(url)

    try:
        # Wait up to 10 seconds for the page to load and for an element with the id 'dynamic-content' to be present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dynamic-content"))
        )
    finally:
        buttons = driver.find_elements('button')
        links = driver.find_elements('a')

        print(f"Found {len(buttons)} buttons and {len(links)} links")

        driver.quit()

    return 'Test completed'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)