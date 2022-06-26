import time
import json

from mycroft import MycroftSkill, intent_file_handler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Fichero JSON donde almacenar la informacion
ficheroJSON = "/home/serggom/data.json"
informacion = {'asignaturas': [], 'usuario': [], 'eventos': [], 'mensajes': []}


def inicio_sesion(self):
    # Datos de acceso fijos
    usuario = 'e71180769r'
    contrasena = 'p5irZ9Jm4@9C#6WUaE!z9%@V'

    # Modo headless
    options = Options()
    options.headless = True
    options.add_argument("--windows-size=1920,1200")

    self.speak("Buscando la informacion...")

    # Acceso a pagina
    driver = webdriver.Chrome(options=options)
    driver.get('https://campusvirtual.uva.es/login/index.php')

    # Inicio de sesion
    driver.find_element(by=By.NAME, value='adAS_username').send_keys(usuario)
    driver.find_element(
        by=By.NAME, value='adAS_password').send_keys(contrasena)
    driver.find_element(by=By.NAME, value='adAS_submit').click()

    # Aceptar cookies
    driver.implicitly_wait(10)
    driver.find_element(
        by=By.XPATH, value='/html/body/div[1]/div/a[1]').click()

    return driver


class AsignaturasCampus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('campus.asignaturas.intent')
    def handle_campus_asignaturas(self, message):
        driver = inicio_sesion(self)

        # Acceso al perfil
        URLPerfil = driver.find_element(
            by=By.XPATH, value='/html/body/div[4]/div[2]/header/div/div/div/div[1]/div[1]/div/div[1]/a').get_attribute('href')
        driver.get(URLPerfil)

        # Acceso a la seccion de asignaturas
        time.sleep(2)
        driver.find_element(
            by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[2]/div/div/ul/li[1]/a').click()

        # Obtencion de las asignaturas
        time.sleep(2)
        elementos = driver.find_element(
            by=By.XPATH, value='/html/body/div[4]/div[2]/div/div/section/div/div/div/div[2]/div/div/div/div[1]').find_elements(by=By.TAG_NAME, value='a')

        for elemento in elementos:
            informacion['asignaturas'].append({
                'nombre': elemento.text.split(' (')[0].capitalize()
            })

        with open(ficheroJSON, 'w') as ficheroDatos:
                json.dump(informacion, ficheroDatos, indent=4)

        # Lectura de la informacion del fichero JSON
        with open(ficheroJSON) as ficheroAsignaturas:
            data = json.load(ficheroAsignaturas)
            self.speak("Sus asignaturas son las siguientes:")

            for subject in data['asignaturas']:
                self.speak(subject['nombre'])

        # # Respuesta con las asignaturas
        # for elemento in elementos:
        #     if len(elemento.text) > 0:
        #         self.speak(elemento.text.split(' (')[0].capitalize())


def create_skill():
    return AsignaturasCampus()

