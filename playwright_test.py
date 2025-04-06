from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
service = Service('./chromedriver-linux64/chromedriver')

driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(1920, 1080)

TIMEOUT = 30

try:
	driver.get('https://www.hotel-barcelonahouse.com/')

	title = driver.title
	print('Page Title:', title)

	element = driver.find_element(By.TAG_NAME, 'h1')
	print('Heading:', element.text)

	btn_accept_cookies = WebDriverWait(driver, TIMEOUT).until(
		EC.presence_of_element_located(
			(By.CSS_SELECTOR, '#cookiescript_accept')
		)
	)

	action_chains = ActionChains(driver)
	action_chains.move_to_element(btn_accept_cookies)
	action_chains.click().perform()


	booking_button = driver.find_element(
		By.CSS_SELECTOR,
		'.roi-search-engine__field.roi-search-engine__field--action'
	)

	calendar_btn = driver.find_element(
		By.CSS_SELECTOR, (
			'.roi-search-engine__field'
			'.roi-search-engine__field--calendar'
			'.js-roicalendar-trigger'
		)
	)

	action_chains.move_to_element(calendar_btn)
	action_chains.click().perform()

	booking_calendar = WebDriverWait(driver, TIMEOUT).until(
		EC.visibility_of_element_located((By.CSS_SELECTOR, '#roicalendar'))
	)

	driver.get_screenshot_as_file(
		'./screenshots/success/1-click-calendar.png'
	)

	first_booking_calendar = booking_calendar.find_element(
		By.CSS_SELECTOR, '.js-calendar-month'
	)

	booking_days = first_booking_calendar.find_elements(
		By.CSS_SELECTOR, '.roi-cal__day.js-calendar-day[role="button"]'
	)

	booking_day_from = booking_days[0]
	booking_day_to = booking_days[-1]

	action_chains.move_to_element(booking_day_from)
	action_chains.click().perform()
	action_chains.move_to_element(booking_day_to)
	action_chains.click().perform()

	driver.get_screenshot_as_file(
		'./screenshots/success/2-click-booking_dates.png'
	)

	action_chains.move_to_element(booking_button)
	action_chains.click().perform()

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
	day_from.click()

	action_btns = driver.find_element(
		By.CSS_SELECTOR, '#calendario-nodispo-botones-acciones'
	)

	change_days_btn = action_btns.find_element(
		By.CSS_SELECTOR, '.return-checkin.js-nodispo-return-checkin'
	)

	WebDriverWait(driver, TIMEOUT).until(
		EC.invisibility_of_element_located(
			(By.CSS_SELECTOR, '#calendar-overlay')
		)
	)

	WebDriverWait(driver, TIMEOUT).until(
		EC.element_to_be_clickable(
			(By.CSS_SELECTOR, '.calendar-day.calendar-day-number.day-available')
		)
	)

	print('element is clickable')

	driver.get_screenshot_as_file(
		'./screenshots/success/3-click_day_from.png'
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
	day_to.click()

	send_form_btn = WebDriverWait(action_btns, TIMEOUT).until(
		EC.visibility_of_element_located(
			(By.CSS_SELECTOR, '.send-form.spinner.js-nodispo-book-nodispo')
		)
	)

	driver.get_screenshot_as_file('./screenshots/success/4-click_day_to.png')

	action_chains.move_to_element(send_form_btn)
	action_chains.click().perform()

	available_rooms = WebDriverWait(driver, TIMEOUT).until(
		EC.presence_of_element_located(
			(By.CSS_SELECTOR, '[data-testid="fn-availability-rooms"]')
		)
	)

	driver.get_screenshot_as_file(
		'./screenshots/success/5-send-form-and-get-available-rooms.png'
	)

	rooms = available_rooms.find_elements(
		By.CSS_SELECTOR,
		'div[data-testid="fn-accordion"] div[data-testid="fn-board"]'
	)

	add_button = rooms[0].find_element(
		By.CSS_SELECTOR,
		'div[class^="PriceDetailstyles__ContainerButtonStyles"]'
	)

	action_chains.move_to_element(add_button)
	action_chains.click().perform()

	shoping_cart = WebDriverWait(driver, TIMEOUT).until(
		EC.presence_of_all_elements_located(
			(By.CSS_SELECTOR, '#shoppingCartContainer')
		)
	)

	driver.get_screenshot_as_file(
		'./screenshots/success/6-click-add-button.png'
	)

finally:
	driver.get_screenshot_as_file('./screenshots/error/foo.png')
	driver.quit()
