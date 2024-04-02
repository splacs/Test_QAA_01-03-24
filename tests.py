import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginPageTests(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = 'C:/Users/User/AppData/Local/Google/Chrome/Application/chrome.exe'
        self.driver = webdriver.Chrome(options=chrome_options)

    def test_successful_login(self):
        self.driver.get("http://automationpractice.pl/index.php?controller=authentication&back=myaccount")
        username_input = self.driver.find_element(By.ID, "email")
        username_input.send_keys("seu_email@exemplo.com")
        password_input = self.driver.find_element(By.ID, "passwd")
        password_input.send_keys("sua_senha")
        login_button = self.driver.find_element(By.ID, "SubmitLogin")
        login_button.click()
        page_title = self.driver.title
        self.assertIn("My account", page_title)

    def test_invalid_credentials_login(self):
        self.driver.get("http://automationpractice.pl/index.php?controller=authentication&back=myaccount")
        username_input = self.driver.find_element(By.ID, "email")
        username_input.send_keys("email_invalido@exemplo.com")
        password_input = self.driver.find_element(By.ID, "passwd")
        password_input.send_keys("senha_invalida")
        login_button = self.driver.find_element(By.ID, "SubmitLogin")
        login_button.click()
        error_message = self.driver.find_element(By.CSS_SELECTOR, ".alert-danger").text
        self.assertIn("Authentication failed.", error_message)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
