import asyncio
import aiohttp
import aiofiles
import re
import json
import logging
from urllib.parse import urlparse

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_RETRIES = 3  # Максимальное количество попыток повторного запроса
CONCURRENT_REQUESTS = 5  # Максимальное количество одновременных запросов


async def fetch_url(session, url, retry=0):

    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()  # Проверка на HTTP ошибки (4xx, 5xx)
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"Error fetching {url}: {e}")
        if retry < MAX_RETRIES:
            delay = 2 ** retry  # экспоненциальная задержка
            logging.info(f"Retrying {url} in {delay} seconds (attempt {retry + 1}/{MAX_RETRIES})")
            await asyncio.sleep(delay)
            return await fetch_url(session, url, retry + 1)
        else:
            logging.error(f"Max retries reached for {url}. Giving up.")
            return None
    except Exception as e:
        logging.exception(f"Unexpected error fetching {url}: {e}")
        return None


async def extract_data(html, url):

    try:
        title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        title = title_match.group(1) if title_match else "No title found"


        content_match = re.search(r"<article>(.*?)</article>", html, re.IGNORECASE | re.DOTALL) #Ищет тег article
        content = content_match.group(1) if content_match else "No content found"


        content = re.sub(r"<[^>]*>", "", content) #Убирает HTML-теги

        return {"url": url, "title": title, "content": content.strip()}  # strip() убирает пробелы в начале и конце
    except Exception as e:
        logging.exception(f"Error extracting data from {url}: {e}")
        return None


async def save_data(filename, data):

    try:
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=4, ensure_ascii=False))  # Красивое форматирование JSON
        logging.info(f"Data saved to {filename}")
    except Exception as e:
        logging.exception(f"Error saving data to {filename}: {e}")


async def scrape_page(session, url, semaphore):

    async with semaphore:  # Ограничение количества одновременных запросов
        html = await fetch_url(session, url)
        if html:
            data = await extract_data(html, url)
            if data:
                # Создаем имя файла на основе домена и пути
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                path = parsed_url.path.replace("/", "_") # Заменяем слеши на подчеркивания, чтобы не было проблем с путями
                filename = f"{domain}{path}.json".replace(".", "_") # Заменяем точки на подчеркивания, чтобы точно было расширение .json
                await save_data(filename, data)


async def main(urls):

    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)  # Семафор для ограничения количества одновременных запросов
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_page(session, url, semaphore) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == "__main__":

    urls = [
        "https://learn2play.ru/builds-poe-2/sledopit-bild-gajd-poe-2-yadovitaya-strela-gas-arrow/",
        "https://learn2play.ru/poe-2-bildi-i-gajdi-path-of-exile-2/",
        "https://learn2play.ru/builds-poe-2/tkach-bur-bild-gajd-poe-2-iskra/"
    ]
    asyncio.run(main(urls))