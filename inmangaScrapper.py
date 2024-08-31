from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os
import time
import random
from PIL import Image
from io import BytesIO

driver_path = 'chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

urlBase = 'https://inmanga.com/ver/manga/Jojos-Bizarre-Adventure-Parte-7-Steel-Ball-Run/01/2c7361f8-bb98-4116-966a-657d7f8133cd' 
driver.get(urlBase)

urlInicial = 'https://pack-yak.intomanga.com/images/manga'
nombreManga = 'Jojos-Bizarre-Adventure-Parte-7-Steel-Ball-Run'
capituloActual = ''
carpetaGeneral = nombreManga
directorio_actual = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(carpetaGeneral):
    os.makedirs(carpetaGeneral)
    print(f"La carpeta '{carpetaGeneral}' ha sido creada en {directorio_actual}.")
else:
    print(f"La carpeta '{carpetaGeneral}' ya existe en {directorio_actual}.")


try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ChapList'))
    )
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')
    select_element = soup.find('select', id='ChapList')

    if select_element:
        option_elements = select_element.find_all('option')
        
        for option in option_elements:
            numCap = option.text

            nombreCarpetaCap = nombreManga + '-' + numCap
            carpetaCapituloRuta = os.path.join(carpetaGeneral,nombreCarpetaCap)
            if not os.path.exists(carpetaCapituloRuta):
                os.makedirs(carpetaCapituloRuta)
            time.sleep(20)
            container_div = soup.find('div', class_='PagesContainer')
            paginacion_dict = {}
            if container_div:
                a_tags = container_div.find_all('a')
                for a_tag in a_tags:
                        img_tag = a_tag.find('img')
                        if img_tag:
                            paginaId = img_tag.get('id')
                            numPagina = img_tag.get('data-pagenumber')
                            urlFinal = f'{urlInicial}/{nombreManga}/chapter/{numCap}/page/{numPagina}/{paginaId}'
                            print(urlFinal)
                            nombrePagina = nombreManga + '-' +  numPagina
                            time.sleep(random.randint(2,5))
                            response = requests.get(urlFinal)
                            imagen = Image.open(BytesIO(response.content))
                            if response.status_code == 200:
                                imagen = Image.open(BytesIO(response.content))
                                pathPagina = os.path.join(carpetaCapituloRuta, nombrePagina)

                            if not os.path.exists(pathPagina + '.png'):
                                imagen.save(pathPagina + '.png', 'PNG')
                                print(f"Imagen guardada en: {pathPagina}.png")
                            else:
                                print(f"La imagen ya existe en: {pathPagina}.png")
    else:
        print("No se encontró el elemento <select> con el ID especificado.")
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
