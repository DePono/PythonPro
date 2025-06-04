import pandas as pd

# Загрузка датасета
df = pd.read_csv("day.csv")

# 1. Первичный анализ
print("Первые 5 строк:")
print(df.head())

print("\nНазвания столбцов:")
print(df.columns.tolist())

print("\nПропущенные значения:")
print(df.isnull().sum())

# 2. Итерирование по строкам: подсчёт аренд в выходные и будние дни
weekend_total = 0
weekday_total = 0

for index, row in df.iterrows():
    if row['weekday'] in [0, 6]:  # воскресенье или суббота
        weekend_total += row['cnt']
    else:
        weekday_total += row['cnt']

print(f"\nОбщее количество аренд в выходные дни: {weekend_total}")
print(f"Общее количество аренд в будние дни: {weekday_total}")

# 3. Преобразование категориальных переменных в one-hot encoding
df_encoded = pd.get_dummies(df, columns=['season', 'weathersit', 'mnth', 'weekday'], drop_first=True)

print("\nПервые 5 строк после преобразования категориальных переменных:")
print(df_encoded.head())

# 4. Группировка данных по месяцам: среднее количество аренд
avg_rentals_by_month = df.groupby('mnth')['cnt'].mean().sort_index()
print("\nСреднее количество аренд по месяцам:")
print(avg_rentals_by_month)

# 5. Обработка пропущенных значений (на всякий случай)
print("\nПовторная проверка пропущенных значений:")
print(df.isnull().sum())

df_filled = df.fillna(df.mean(numeric_only=True))  # Заполнение средними значениями
# Альтернатива: df_dropped = df.dropna()
