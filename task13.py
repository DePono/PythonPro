import requests
from bs4 import BeautifulSoup

URL = "https://ru.wikipedia.org/wiki/Python"
HEADINGS = [ 'h3']

response = requests.get(URL)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(HEADINGS)

    with open("headings_by_level.txt", "w", encoding="utf-8") as file:
        for tag in headings:
            level = tag.name.upper()

            # Проверка: если есть span.mw-headline — берём его текст
            span = tag.find("span", class_="mw-headline")
            text = span.text.strip() if span else tag.text.strip()

            if text:  # исключаем пустые строки
                file.write(f"{level}: {text}\n")

    print("Заголовки сохранены в headings_by_level.txt")
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")
