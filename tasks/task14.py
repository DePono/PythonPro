import requests
import csv

API_KEY = "your_api_key_here"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

CITIES = ["Москва", "Нью-Йорк", "Токио", "Лондон", "Берлин"]
weather_data = []

def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "ru"
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # вызовет исключение для кодов 4xx/5xx

        data = response.json()
        return {
            "Город": city,
            "Температура (°C)": data["main"]["temp"],
            "Влажность (%)": data["main"]["humidity"],
            "Скорость ветра (м/с)": data["wind"]["speed"],
            "Описание": data["weather"][0]["description"]
        }

    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP для {city}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения для {city}: {e}")
    except KeyError:
        print(f"Неверный формат ответа для {city}")
    return None

# Получаем погоду по каждому городу
for city in CITIES:
    result = get_weather(city)
    if result:
        weather_data.append(result)

# Анализ температур
temps = [entry["Температура (°C)"] for entry in weather_data]
if temps:
    avg_temp = sum(temps) / len(temps)
    hottest = max(weather_data, key=lambda x: x["Температура (°C)"])
    coldest = min(weather_data, key=lambda x: x["Температура (°C)"])

    print("\n🌡️ Результаты:")
    for entry in weather_data:
        print(f'{entry["Город"]}: {entry["Температура (°C)"]}°C, {entry["Описание"]}')

    print(f"\nСредняя температура: {avg_temp:.1f}°C")
    print(f"Самый тёплый город: {hottest['Город']} ({hottest['Температура (°C)']}°C)")
    print(f"Самый холодный город: {coldest['Город']} ({coldest['Температура (°C)']}°C)")

    # Сохраняем в CSV
    with open("weather_data.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=weather_data[0].keys())
        writer.writeheader()
        writer.writerows(weather_data)

    print("Данные сохранены в weather_data.csv")
else:
    print("Не удалось получить данные ни по одному городу.")
