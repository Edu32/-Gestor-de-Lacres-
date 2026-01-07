from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://sim.contrail.com.br/users/sign_in")  # <-- ALTERE AQUI

input("Site abriu corretamente? Pressione ENTER para sair...")
driver.quit()