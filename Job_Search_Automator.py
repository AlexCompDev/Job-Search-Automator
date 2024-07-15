from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
)
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Укажем логин и пароль
LOGIN = "Логин"
PASSWORD = "Пароль"

# Указываем URL первой страницы с вакансиями
base_url = "Ссылка на вакансию с квери параметрами"

# Указываем название резюме
vacancy_title = "Название резюме"

# Создаем экземпляр драйвера Chrome
driver = webdriver.Chrome()

# Переходим на сайт https://hh.ru/
driver.get("https://hh.ru/")

# Ждем загрузки страницы
driver.implicitly_wait(5)

# Check for captcha
captcha_locator = (
    By.XPATH,
    "//h1[@data-qa='title' and contains(text(), 'Подтвердите, что вы не робот')]",
)

while True:
    try:
        captcha_element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(captcha_locator)
        )
        input("Введите капчу и авторизуйтесь, затем нажмите Enter...")
    except TimeoutException:
        break

# Найдем первую кнопку по XPath
button1 = driver.find_element(
    By.XPATH, "//*[@id='HH-React-Root']/div/div/div[3]/div/div/div/div/div[5]/a"
)

# Произведем клик по первой кнопке
button1.click()

# Ждем загрузки страницы
driver.implicitly_wait(2)

# Найдем вторую кнопку по XPath
button2 = driver.find_element(
    By.XPATH,
    "//*[@id='HH-React-Root']/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[1]/div/div/div[2]/form/div[4]/button[2]",
)

# Произведем клик по второй кнопке
button2.click()

# Ждем загрузки страницы
driver.implicitly_wait(2)

# Найдем поле ввода e-mail по XPath
input_field_email = driver.find_element(
    By.XPATH,
    "//*[@id='HH-React-Root']/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[1]/div/div/form/div[1]/fieldset/input",
)

# Вводим текст в поле e-mail
input_field_email.send_keys(LOGIN)

# Найдем поле ввода пароля по XPath
input_field_password = driver.find_element(
    By.XPATH,
    "//*[@id='HH-React-Root']/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[1]/div/div/form/div[2]/fieldset/input",
)

# Вводим текст в поле пароля
input_field_password.send_keys(PASSWORD)

# Найдем кнопку входа по XPath
login_button = driver.find_element(
    By.XPATH,
    "/html/body/div[5]/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[1]/div/div/form/div[6]/button[1]",
)

# Произведем клик по кнопке входа
login_button.click()

# Ждем загрузки страницы
driver.implicitly_wait(2)

# Ждем, пока пользователь введет капчу и авторизуется
input("Введите капчу и авторизуйтесь, затем нажмите Enter...")

# поднимаем резюме по кнопке
button1 = driver.find_elements(By.XPATH, "//button[contains(text(), 'Поднять')]")
button2 = driver.find_elements(
    By.XPATH, "//div[@data-qa='applicant-index-nba-action_update-resumes']"
)

if button1:
    button1[0].click()
elif button2:
    button2[0].click()


# Check for captcha again
while True:
    try:
        captcha_element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(captcha_locator)
        )
        input("Введите капчу и авторизуйтесь, затем нажмите Enter...")
    except TimeoutException:
        break


# Check for captcha again
try:
    captcha_element = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(captcha_locator)
    )
    input("Введите капчу и авторизуйтесь, затем нажмите Enter...")
except TimeoutException:
    pass

# Создаем файл links.txt и сохраняем все ссылки на вакансии
with open("links.txt", "w") as f:
    page = 0
    while True:
        url = f"{base_url}&page={page}"
        driver.get(url)
        time.sleep(2)  # добавляем задержку в 2 секунды
        vacancies = driver.find_elements(
            By.CSS_SELECTOR,
            "#a11y-main-content > div > div > div > div > h2 > span > a",
        )
        for vacancy in vacancies:
            href = vacancy.get_attribute("href")
            f.write(href + "\n")
            # Выводим название вакансии в терминал
            vacancy_name = vacancy.find_element(By.XPATH, ".//span").text
            print(f"Вакансия найдена: {vacancy_name}")
        page += 1
        # Check for captcha again
        try:
            captcha_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(captcha_locator)
            )
            input("Введите капчу и авторизуйтесь, затем нажмите Enter...")
        except TimeoutException:
            pass

        # Ждем загрузки страницы
        time.sleep(3)

        # Проверяем, есть ли кнопка "Далее" на странице
        try:
            next_button = driver.find_element(By.XPATH, "//a[@data-qa='pager-next']")
        except NoSuchElementException:
            # Если кнопки "Далее" нет, то это последняя страница
            break

print("Файл links.txt создан успешно")

# Проверяем, если файл links.txt пустой, то ждем 10 секунд и проверяем снова
for i in range(4):
    if os.path.getsize("links.txt") == 0:
        print(f"Файл links.txt пустой, ждем 10 секунд и проверяем снова ({i+1}/4)")
        time.sleep(10)
    else:
        break
else:
    print("Файл links.txt остался пустым после 4 попыток")
    exit()

# Переходим по каждой ссылке из файла links.txt
try:
    with open("links.txt", "r") as f:
        for link in f.readlines():
            link = link.strip()
            try:
                driver.get(link)
                driver.implicitly_wait(2)

                # Проверяем наличие капчи снова
                try:
                    element_captcha = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located(captcha_locator)
                    )
                    input("Введите капчу и авторизуйтесь, затем нажмите Enter...")
                except TimeoutException:
                    pass

                # Ждем загрузки страницы
                time.sleep(3)

                # Найти кнопку "Откликнуться"
                button_response = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[text()='Откликнуться']/ancestor::a")
                    )
                )
                button_response.click()

                # Дождаться появления модального окна ответа
                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "RESPONSE_MODAL_FORM_ID"))
                )

                # Найти элемент с текстом названия вакансии
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//*[contains(text(), '{}')]".format(vacancy_title),
                            )
                        )
                    )
                    element.click()

                except TimeoutException:
                    with open("bad.txt", "a") as f:
                        f.write(link + "\n")
                    continue

                # Найти кнопку "Сопроводительное письмо"
                button_letter = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@data-qa='vacancy-response-letter-toggle']",
                        )
                    )
                )
                try:
                    button_letter.click()
                except ElementClickInterceptedException:
                    with open("bad.txt", "a") as f:
                        f.write(link + "\n")
                    continue

                # Найти элемент текстовой области
                text_area = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//textarea[@data-qa='vacancy-response-popup-form-letter-input']",
                        )
                    )
                )

                # Прочитать текст из файла cv.txt
                with open("cv.txt", "r") as f:
                    text_from_file = f.read()

                # Ввести текст в текстовую область
                text_area.send_keys(text_from_file)

                # Ждем 4 секунды перед закрытием модального окна
                time.sleep(4)

                # Найти кнопку "Откликнуться"
                button_response_locator = (
                    By.XPATH,
                    "//button/span[text()='Откликнуться']",
                )

                try:
                    button_response = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(button_response_locator)
                    )
                    button_response.click()
                    print("Успешно! Кнопка 'Откликнуться' найдена и кликнута.")
                except:
                    print("Неудача! Кнопка 'Откликнуться' не найдена.")

                    time.sleep(7)

            except Exception as e:
                print(f"Ошибка: {e}")
                with open("bad.txt", "a") as f:
                    f.write(link + "\n")
                continue

    print("Скрипт завершился без ошибок!")
finally:
    driver.quit()
