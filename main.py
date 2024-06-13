from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from captcha_finding import convert

# Initialize the Chrome driver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

# Open the web page
driver.get('https://tradiem.haiphong.edu.vn/TraCuu')

# Locate the input elements and the submit button
sbd_input = driver.find_element(By.NAME, 'SOBAODANH')
captcha_input = driver.find_element(By.NAME, 'ConfirmCode')
submit_button = driver.find_element(By.ID, 'btnsubmit')

# Enter the required details
sbd_input.send_keys('240355')  # replace with actual number

# Locate the captcha image element
captcha_image = driver.find_element(By.ID, 'ImgCaptcha')

# Get the captcha image URL
captcha_src = captcha_image.get_attribute('src')

# Download the captcha image
captcha_response = requests.get(captcha_src)
captcha_image_path = 'captcha.png'
with open(captcha_image_path, 'wb') as f:
    f.write(captcha_response.content)

# Pause the script to allow manual captcha entry
#captcha = input("Please enter the captcha manually and press Enter...")
captcha = convert(captcha_image_path)
captcha_input.send_keys(captcha)

# Click the submit button
submit_button.click()

# Wait for the results to load
time.sleep(3)

# Extract the required information
subject_scores = driver.find_element(By.ID, 'ts-mark').text
error_message = driver.find_element(By.ID, 'err-msg').text
# Print the results

print("Điểm các môn:", subject_scores)
print("Thông báo lỗi:", error_message)

# Close the driver
driver.quit()