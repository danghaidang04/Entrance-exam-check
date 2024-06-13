from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from ocr import convert
import pandas as pd

# Set the data
data = pd.DataFrame(columns=['SBD', 'Họ và tên', 'Ngữ văn', 'Toán',
                             'Ngoại ngữ', 'Anh (ĐK)', 'Pháp (ĐK)', 'Toán chuyên',
                             'Văn chuyên', 'Lý chuyên', 'Hóa chuyên',
                             'Sinh chuyên', 'Sử chuyên', 'Địa chuyên',
                             'Anh chuyên', 'Nhật chuyên', 'Pháp chuyên'])

# Initialize the Chrome driver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

# Open the web page
driver.get('https://tradiem.haiphong.edu.vn/TraCuu')

# Locate the input elements and the submit button
sbd_input = driver.find_element(By.NAME, 'SOBAODANH')
captcha_input = driver.find_element(By.NAME, 'ConfirmCode')
submit_button = driver.find_element(By.ID, 'btnsubmit')


def automatic_captcha():
    # Locate the captcha image element
    captcha_image = driver.find_element(By.ID, 'ImgCaptcha')

    # Get the captcha image URL
    captcha_src = captcha_image.get_attribute('src')

    # Download the captcha image
    captcha_response = requests.get(captcha_src)
    captcha_image_path = 'captcha.png'
    with open(captcha_image_path, 'wb') as f:
        f.write(captcha_response.content)
    captcha = convert(captcha_image_path)
    captcha_input.send_keys(captcha)
    submit_button.click()
    time.sleep(1)


def manual_captcha():
    # Pause the script to allow captcha entry
    captcha = input("Please enter the captcha manually and press Enter...")
    captcha_input.send_keys(captcha)
    submit_button.click()
    time.sleep(1)


# List of ID
IDs = [240355, 280147, 200769, 150408, 270188, 210063, 100643]

# Enter the required details
for ID in IDs:
    sbd_input.send_keys(ID)  # replace with actual number

    # Choose the captcha entry method
    manual_captcha()

    # Find the error message element
    error_message = driver.find_element(By.ID, 'err-msg').text
    # Print the results
    while error_message:
        print("Thông báo lỗi:", error_message)
        captcha_input.clear()
        manual_captcha()
        error_message = driver.find_element(By.ID, 'err-msg').text

    # Print the results
    name = driver.find_element(By.ID, 'ts-name').text
    print("Họ tên:", name)
    subject_scores = driver.find_element(By.ID, 'ts-mark').text
    print("Điểm các môn:", subject_scores)

    # Parse the scores into a dictionary
    scores = {}
    for line in subject_scores.split(";"):
        subject, score = line.split(':')
        subject = subject.strip()
        score = score.strip()
        if score[-1] == '.':
            score = score[:-1]
        scores[subject] = score
    # Create new row. If the subject is not found, set the score to -100
    new_row = [ID, name]
    for subject in ['Ngữ văn', 'Toán', 'Ngoại ngữ', 'Anh (ĐK)', 'Pháp (ĐK)', 'Toán chuyên',
                    'Văn chuyên', 'Lý chuyên', 'Hóa chuyên', 'Sinh chuyên', 'Sử chuyên',
                    'Địa chuyên', 'Anh chuyên', 'Nhật chuyên', 'Pháp chuyên']:
        if subject in scores:
            new_row.append(scores[subject])
        else:
            new_row.append(-100)
    data.loc[len(data)] = new_row

    # Clear the input fields
    sbd_input.clear()
    captcha_input.clear()

# Close the driver
driver.quit()

# Store the data as a CSV file
data.to_csv('data.csv', index=False)
