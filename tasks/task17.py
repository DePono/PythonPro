import pandas as pd

# Загрузка CSV
df = pd.read_csv("googleplaystore.csv")

# Первые 10 строк
print("\n1. Первые 10 строк:")
print(df.head(10))

# Случайные 5 строк
print("\n2. Случайные 5 строк:")
print(df.sample(5))

# Размер датафрейма
print("\n3. Размер таблицы (строки, столбцы):")
print(df.shape)

# Количество пропущенных значений
print("\n4. Пропущенные значения по столбцам:")
print(df.isnull().sum())

# Отброс строк с пропущенными значениями
df_clean = df.dropna()
print("\n5. После удаления строк с пропущенными значениями:")
print(df_clean.shape)

# Рейтинги: мин, макс, среднее
print("\n6. Статистика по рейтингу:")
if "Rating" in df_clean.columns:
    print(f"Минимальный рейтинг: {df_clean['Rating'].min()}")
    print(f"Максимальный рейтинг: {df_clean['Rating'].max()}")
    print(f"Средний рейтинг: {df_clean['Rating'].mean():.2f}")
else:
    print("Столбец 'Rating' отсутствует!")

# Первые 10 приложений с рейтингом ≥ 4.9
print("\n7. Приложения с рейтингом не ниже 4.9:")
print(df_clean[df_clean["Rating"] >= 4.9].head(10)[["App", "Rating"]])

# 5 самых часто скачиваемых приложений
# Преобразуем колонку Installs (удалим + и запятые, приведем к int)
if "Installs" in df_clean.columns:
    df_clean = df_clean.copy()
    df_clean["Installs_clean"] = (
        df_clean["Installs"]
        .str.replace("+", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(int)
    )

    print("\n8. 5 самых часто скачиваемых приложений:")
    print(df_clean.sort_values("Installs_clean", ascending=False)[["App", "Installs"]].head(5))
else:
    print("Столбец 'Installs' отсутствует!")
