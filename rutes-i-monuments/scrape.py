from bs4 import BeautifulSoup
import requests

url = "https://www.catalunyamedieval.es/edificacions-de-caracter-religios/ermites/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
ermites = soup.find_all("li", class_="ermita")
for ermita in ermites:
    link = ermita.find("a")
    print(link.get("href"), link.text)