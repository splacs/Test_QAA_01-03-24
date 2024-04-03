import unittest
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

class LoginTest(unittest.TestCase):

    def setUp(self):
        # Configurações do Chrome
        chrome_options = webdriver.ChromeOptions()
        # Define o local do executável do Chrome
        chrome_options.binary_location = 'C:/Users/User/AppData/Local/Google/Chrome/Application/chrome.exe'
        # Inicializa o driver do Chrome com as opções configuradas
        self.driver = webdriver.Chrome(options=chrome_options)
        # Define um tempo de espera implícito de 10 segundos para o driver
        self.driver.implicitly_wait(10)

    def load_page(self, url):
        # Carrega uma página, tentando até 3 vezes em caso de falha
        attempts = 3
        while attempts > 0:
            try:
                self.driver.get(url)
                return
            except Exception as e:
                print(f"Failed to load page: {e}")
                attempts -= 1
                if attempts == 0:
                    raise
                print("Retrying...")

    def tearDown(self):
        # Espera por 5 segundos antes de fechar o navegador
        time.sleep(5)
        # Fecha o navegador
        self.driver.quit()

    # Teste para criar uma conta
    def test_create_account(self):
        # Carrega a página de criação de conta
        self.driver.get("http://automationpractice.pl/index.php?controller=authentication&back=myaccount")
        # Encontra o campo de e-mail de criação de conta e preenche com um e-mail válido
        email_input = self.driver.find_element(By.ID, "email_create")
        email_input.send_keys("valido@email.com")
        # Clica no botão para criar a conta
        create_account_button = self.driver.find_element(By.ID, "SubmitCreate")
        create_account_button.click()
        # Verifica se há uma mensagem de erro indicando falha na criação da conta
        error_message = self.driver.find_element(By.XPATH, "//div[contains(@class, 'alert-danger')]")
        self.assertTrue(error_message.is_displayed(), "Failed to create account")

        # Preenche os campos de nome, sobrenome e senha
        try:
            first_name_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "customer_firstname"))
            )
        except TimeoutException:
            create_account_button.click()
            first_name_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "customer_firstname"))
            )
        first_name_input.send_keys("João")
        last_name_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.ID, "customer_lastname"))
        )
        last_name_input.send_keys("Silva")
        password_input = WebDriverWait(self.driver, 40).until(
            EC.visibility_of_element_located((By.ID, "passwd"))
        )
        password_input.send_keys("123456")
        # Clica no botão de registro
        register_button = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.ID, "submitAccount"))
        )
        register_button.click()

    # Teste para fazer login com credenciais válidas
    def test_login_with_valid_credentials(self):
        # Carrega a página de login
        self.driver.get("http://automationpractice.pl/index.php?controller=authentication&back=myaccount")
        # Preenche o campo de e-mail com um e-mail válido
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys("valido@email.com")
        # Preenche o campo de senha
        password_input = self.driver.find_element(By.ID, "passwd")
        password_input.send_keys("123456")
        # Clica no botão de login
        signin_button = self.driver.find_element(By.XPATH, "//button[@id='SubmitLogin']")
        signin_button.click()
        # Verifica se a informação da conta está sendo exibida, indicando que o login foi bem-sucedido
        account_info = self.driver.find_element(By.CSS_SELECTOR, ".info-account")
        self.assertTrue(account_info.is_displayed(), "Failed to login with valid credentials")

    # Teste para fazer login com credenciais inválidas
    def test_login_with_invalid_credentials(self):
        # Carrega a página de login
        self.driver.get("http://automationpractice.pl/index.php?controller=authentication&back=myaccount")
        # Preenche o campo de e-mail com um e-mail inválido
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys("invalido123123.com")
        # Preenche o campo de senha com uma senha inválida
        password_input = self.driver.find_element(By.ID, "passwd")
        password_input.send_keys("invalido123123")
        # Clica no botão de login
        signin_button = self.driver.find_element(By.XPATH, "//button[@id='SubmitLogin']")
        signin_button.click()
        # Verifica se a mensagem de erro de autenticação está sendo exibida corretamente
        alert_message = self.driver.find_element(By.CSS_SELECTOR, ".alert-danger")
        self.assertEqual(alert_message.text, "Authentication failed.", "Failed to display error message for invalid credentials")

if __name__ == '__main__':
    unittest.main()
