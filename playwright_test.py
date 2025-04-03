from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument(
	'--disable-dev-shm-usage'
)  # Overcome limited resource problems

service = Service('/app/chromedriver-linux64/chromedriver')

driver = webdriver.Chrome(service=service, options=options)

try:
	# Open a webpage
	driver.get("https://example.com")

	# Get the title of the page
	title = driver.title
	print("Page Title:", title)

	# Locate an element (for demonstration, finding the <h1> element)
	element = driver.find_element(By.TAG_NAME, "h1")
	print("Heading:", element.text)

finally:
	# Close the browser
	driver.quit()
