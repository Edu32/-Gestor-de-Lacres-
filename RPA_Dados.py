from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
import os
import time
# ======================
# CONFIGURAÇÃO DO CHROME
# ======================
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# WAIT (obrigatório para evitar erro de tempo)
wait = WebDriverWait(driver, 20)

# ======================
# ACESSAR SITE
# ======================
driver.get("https://sim.contrail.com.br/users/sign_in")  # <-- coloque a URL real

# ======================
# LOGIN
# ======================
wait.until(
    EC.presence_of_element_located((By.ID, "user_email"))
).send_keys("maria.paixao@contrail.com.br")

driver.find_element(By.ID, "password-input").send_keys("Mp@0102024")

wait = WebDriverWait(driver, 20)

botao_login = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit' and contains(., 'log in')]")
    )
)

botao_login.click()

# ---- ABA  ---- 
menu_relatorios = wait.until(
    EC.element_to_be_clickable((By.ID, "navbarReportsDropdown"))
)
menu_relatorios.click()

# Força submenu Metabase
driver.execute_script("""
let submenu = document.evaluate(
    "/html/body/nav/div[2]/ul[1]/li[2]/div/div[1]/ul",
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
).singleNodeValue;

if (submenu) {
    submenu.classList.add("show");
    submenu.style.display = "block";
}
""")

# Movimentos TIJU
movimentos_tiju = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "/html/body/nav/div[2]/ul[1]/li[2]/div/div[1]/ul/li[6]/a")
    )
)

driver.execute_script("arguments[0].click();", movimentos_tiju)

# Periodo 
hoje = datetime.now()
data_d_1 = hoje - timedelta(days=1)

# Nome do mês em português
meses = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
}

mes = meses[data_d_1.month]
dia = data_d_1.day
ano = data_d_1.year

data_formatada = f"{mes} {dia}, {ano}"
print("Data D-1 formatada:", data_formatada)

wait = WebDriverWait(driver, 30)

# localizar o iframe do Metabase
iframe_metabase = wait.until(EC.presence_of_element_located((
    By.XPATH, "//iframe[contains(@src, 'metabase')]"
)))

# entrar no iframe
driver.switch_to.frame(iframe_metabase)

print("Entrou no iframe do Metabase")

botao_data = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//div[@role='button' and .//div[text()='DATA']]"
)))

botao_data.click()


intervalo_fixo = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//span[text()='Intervalo de datas fixo…']/ancestor::button"
)))
intervalo_fixo.click()

aba_em = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//button[@role='tab']//span[text()='Em']"
)))
aba_em.click()

campo_data = wait.until(EC.presence_of_element_located((
    By.XPATH, "//input[@data-dates-input='true']"
)))

campo_data.click()
campo_data.send_keys(Keys.CONTROL, "a")
campo_data.send_keys(Keys.DELETE)
campo_data.send_keys(data_formatada)

botao_adicionar = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//span[text()='Adicionar filtro']/ancestor::button"
)))
botao_adicionar.click()



# final
menu_download = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//button[@data-testid='public-or-embedded-dashcard-menu']"
)))

# Mantine às vezes ignora click normal
driver.execute_script("arguments[0].click();", menu_download)

print("Menu de três pontos clicado")

botao_download = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//div[text()='Fazer download de resultados']/ancestor::button"
)))

driver.execute_script("arguments[0].click();", botao_download)

print("Download de resultados acionado")

# esperar opção XLSX ficar visível
xlsx_label = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//label[.//span[text()='.xlsx']]"
    ))
)

# clique forçado (mantine safe)
driver.execute_script("arguments[0].click();", xlsx_label)

# esperar botão Baixar ficar clicável
botao_baixar = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[@data-testid='download-results-button']"
    ))
)

# clique final
driver.execute_script("arguments[0].click();", botao_baixar)
 
pasta_download = r"C:\Users\maria.paixao\Downloads"

# AGUARDAR DOWNLOAD (ATÉ 1 MINUTO)
# ======================
tempo_maximo = 60  # segundos
inicio = time.time()

print("Aguardando conclusão do download (.xlsx)...")

while True:
    arquivos_xlsx = [
        f for f in os.listdir(pasta_download)
        if f.endswith(".xlsx") and not f.endswith(".crdownload")
    ]

    if arquivos_xlsx:
        print("✅ Download concluído com sucesso:", arquivos_xlsx[-1])
        break

    if time.time() - inicio > tempo_maximo:
        print("⚠ Tempo máximo de 1 minuto atingido. Encerrando mesmo assim.")
        break

    time.sleep(2)

print("Fechando navegador...")
driver.quit()
print("Robô finalizado com sucesso 🚀")

