from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service('/app/chromedriver-linux64/chromedriver')

driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(1920, 1080)

TIMEOUT = 90

try:
	driver.get('https://www.hotel-barcelonahouse.com/')

	title = driver.title
	print('Page Title:', title)

	element = driver.find_element(By.TAG_NAME, 'h1')
	print('Heading:', element.text)

	action_chains = ActionChains(driver)

	booking_button = driver.find_element(
		By.CSS_SELECTOR,
		'.roi-search-engine__field.roi-search-engine__field--action'
	)

	action_chains.move_to_element(booking_button)
	action_chains.click(booking_button).perform()

	calendar = WebDriverWait(driver, TIMEOUT).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, '.nd-calendario'))
	)

	calendar_first_frame = calendar.find_elements(
		By.CSS_SELECTOR, '.calendar.js-calendar'
	)[0].find_element(By.CSS_SELECTOR, '.calendar-days')

	calendar_days = WebDriverWait(calendar_first_frame, TIMEOUT).until(
		EC.presence_of_all_elements_located(
			(
				By.CSS_SELECTOR,
				'.calendar-day.calendar-day-number.day-available'
			)
		)
	)

	day_from = calendar_days[0]

	action_chains.move_to_element(day_from)
	action_chains.click(day_from).perform()

	action_btns = driver.find_element(
		By.CSS_SELECTOR, '#calendario-nodispo-botones-acciones'
	)

	change_days_btn = action_btns.find_element(
		By.CSS_SELECTOR, '.return-checkin.js-nodispo-return-checkin'
	)

	WebDriverWait(driver, 90).until(
		EC.invisibility_of_element_located(
			(By.CSS_SELECTOR, '#calendar-overlay')
		)
	)

	driver.get_screenshot_as_file(
		'/app/screenshots/success/1-click_day_from.png'
	)

	calendar_days = WebDriverWait(calendar_first_frame, TIMEOUT).until(
		EC.presence_of_all_elements_located(
			(
				By.CSS_SELECTOR,
				'.calendar-day.calendar-day-number.day-available'
			)
		)
	)

	day_to = calendar_days[0]

	action_chains.move_to_element(day_to)
	action_chains.click(day_to).perform()

	send_form_btn = WebDriverWait(action_btns, TIMEOUT).until(
		EC.visibility_of_element_located(
			(By.CSS_SELECTOR, '.send-form.spinner.js-nodispo-book-nodispo')
		)
	)

	driver.get_screenshot_as_file('/app/screenshots/success/2-click_day_to.png')

	action_chains.move_to_element(send_form_btn)
	action_chains.click(send_form_btn).perform()

	available_rooms = WebDriverWait(driver, TIMEOUT).until(
		EC.presence_of_element_located(
			(By.CSS_SELECTOR, '[data-testid="fn-availability-rooms"]')
		)
	)

	driver.get_screenshot_as_file(
		'/app/screenshots/success/2-send-form-and-get-available-rooms.png'
	)

finally:
	driver.get_screenshot_as_file('/app/screenshots/error/foo.png')
	driver.quit()
