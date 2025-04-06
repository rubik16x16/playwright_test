from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import TimeoutException, WebDriverWait

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
service = Service('./chromedriver-linux64/chromedriver')

driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(1920, 1080)

action_chains = ActionChains(driver)

TIMEOUT = 30
SHORT_TIMEOUT = 10

def find_availability(passed_days):

	first_available_day_index = 0
	passed_days_count = 0
	day_from = None

	calendar = WebDriverWait(driver, TIMEOUT).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, '.nd-calendario'))
	)

	calendar_days = WebDriverWait(calendar, TIMEOUT).until(
		EC.presence_of_all_elements_located(
			(
				By.CSS_SELECTOR,
				'.calendar-day.calendar-day-number'
			)
		)
	)

	WebDriverWait(driver, TIMEOUT).until(
		EC.element_to_be_clickable(
			(By.CSS_SELECTOR, '.calendar-day.calendar-day-number.day-available')
		)
	)

	for index, calendar_day in enumerate(calendar_days):
		if 'day-available' in calendar_day.get_attribute('class'):

			if passed_days_count < passed_days:
				passed_days_count += 1
				continue
			first_available_day_index = index
			day_from = calendar_day
			break
		else:
			continue

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

	calendar_days = WebDriverWait(calendar, TIMEOUT).until(
		EC.presence_of_all_elements_located(
			(
				By.CSS_SELECTOR,
				'.calendar-day.calendar-day-number'
			)
		)
	)

	for index, calendar_day in enumerate(calendar_days):
		if 'day-available' in calendar_day.get_attribute('class') and index > first_available_day_index:
			day_to = calendar_day
			break
		else:
			continue

	day_to.click()

	send_form_btn = WebDriverWait(action_btns, TIMEOUT).until(
		EC.visibility_of_element_located(
			(By.CSS_SELECTOR, '.send-form.spinner.js-nodispo-book-nodispo')
		)
	)

	driver.get_screenshot_as_file('./screenshots/success/4-click_day_to.png')

	action_chains.move_to_element(send_form_btn)
	action_chains.click().perform()

	try:

		available_rooms = WebDriverWait(driver, SHORT_TIMEOUT).until(
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, '[data-testid="fn-availability-rooms"]')
			)
		)

		return available_rooms

	except TimeoutException:

		return False

def main ():
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

		driver.get_screenshot_as_file(
			'./screenshots/success/5-send-form-and-get-available-rooms.png'
		)

		passed_days = 0
		available_rooms = find_availability(passed_days)

		while not available_rooms:
			passed_days += 1
			available_rooms = find_availability(passed_days)

			print('No available rooms, trying again...')

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
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, '#shoppingCartContainer')
			)
		)

		driver.get_screenshot_as_file(
			'./screenshots/success/6-click-add-button.png'
		)

		continue_btn = shoping_cart.find_element(
			By.CSS_SELECTOR,
			'button[data-testid=fn-shopping-cart-book-button]'
		)

		action_chains.move_to_element(continue_btn)
		action_chains.click().perform()

		confirmation_box = WebDriverWait(driver, TIMEOUT).until(
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, 'div[class^=DesktopConfirmationstyles]')
			)
		)

		name_input = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'input[data-testid=fn-input-cli_nombre]'
		)
		name_input.send_keys('John Doe')

		last_name_input = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'input[data-testid=fn-input-cli_apellidos]'
		)
		last_name_input.send_keys('Smith')
		email_input = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'input[data-testid=fn-input-cli_email]'
		)
		email_input.send_keys('test@gmail.com')

		email2_input = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'input[data-testid=fn-input-email2]'
		)
		email2_input.send_keys('test@gmail.com')

		postal_code_input = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'input[data-testid=fn-input-dir_cod_postal]'
		)
		postal_code_input.send_keys('08001')
		country_select = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'section[data-testid=fn-select-cli_codigo_pais]'
		)
		country_select.click()

		country_option = WebDriverWait(country_select, TIMEOUT).until(
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, 'li#react-select-2-option-0-1')
			)
		)

		country_option.click()

		phone_input = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'input[data-testid=fn-input-cli_telefono]'
		)
		phone_input.send_keys('123456789')
		mobile_input = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'input[data-testid=fn-input-telefono_mobile]'
		)
		mobile_input.send_keys('987654321')
		comment_input = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'textarea[data-testid=fn-textarea-cli_comentario]'
		)
		comment_input.send_keys('Test comment')
		driver.get_screenshot_as_file(
			'./screenshots/success/7-fill_confirmation_form.png'
		)

		owner_card_input = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'input[data-testid=fn-input-titular_tarjeta]'
		)
		owner_card_input.send_keys('John Doe')

		input_card_number = confirmation_box.find_element(
			By.CSS_SELECTOR,
			'iframe#iframe-cardNumber'
		)
		action_chains.move_to_element(input_card_number)
		action_chains.click()
		action_chains.send_keys(12345678901234567).perform()

		driver.get_screenshot_as_file(
			'./screenshots/success/8-fill_credit_card_form.png'
		)


	finally:
		driver.get_screenshot_as_file('./screenshots/error/foo.png')
		driver.quit()

main()
