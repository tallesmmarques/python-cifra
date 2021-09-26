from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

app = Flask(__name__)

@app.route("/search")
def getList():
  # -------------------------- Requisição do CifraClub ------------------------- #
  search = request.args.get('q')
  if not search:
    return {
      "error": "Falta string de pesquisa"
    }

  url = f'https://www.cifraclub.com.br/?q={search}'
  option = Options()
  option.headless = True
  driver = webdriver.Firefox(options=option)

  driver.get(url)
  table = driver.find_element_by_css_selector('div.gsc-expansionArea')
  html_content = table.get_attribute('outerHTML')
  driver.close()
  driver.quit()

  # ---------------------------- Tratativa de Dados ---------------------------- #
  soup = BeautifulSoup(html_content, 'html.parser')
  results = soup.find_all('div', class_='gsc-table-result')

  data = []
  for i, result in enumerate(results):
    cell = result.find('a')
    if "(letra da música)" in cell.text:
      continue
    res = {
      "id": i,
      "name": cell.text,
      "link": cell['href']
    }
    data.append(res)
  return {
    "data": data
  }

@app.route("/getmusic")
def getMusic():
  # -------------------------- Requisição do CifraClub ------------------------- #
  url = request.args.get('link')
  if not url:
    return {
      "error": "Falta o link da música"
    }

  option = Options()
  option.headless = True
  driver = webdriver.Firefox(options=option)

  driver.get(url)
  table = driver.find_element_by_css_selector('div.cifra')
  html_content = table.get_attribute('outerHTML')
  driver.close()
  driver.quit()

  # ---------------------------- Tratativa de Dados ---------------------------- #
  soup = BeautifulSoup(html_content, 'html.parser')
  name = soup.find('h1', class_='t1').text
  author = soup.find('h2', class_='t3').text
  # div.player-placeholder>img
  img_youtube = soup.find('div', class_='player-placeholder').img['src']
  cod = img_youtube.split('/vi/')[1].split('/')[0]
  youtube = f"https://www.youtube.com/watch?v={cod}"

  return {
    "name": name,
    "author": author,
    "linkCifra": url,
    "linkYoutube": youtube
  }

if __name__ == '__main__':
  app.run(debug=True)