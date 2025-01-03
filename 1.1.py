import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Функція для отримання курсу валют за конкретну дату
def get_currency_rate(date, currency_code='USD'):
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    params = {
        'date': date.strftime('%Y%m%d'),  # Формат дати: YYYYMMDD
        'json': 'true'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if item['cc'] == currency_code:
                return item['rate']
    return None

# Отримання курсу за останній тиждень
def get_last_week_rates(currency_code='USD'):
    today = datetime.now()
    rates = []
    dates = []
    for i in range(1, 8):  # Останні 7 днів
        date = today - timedelta(days=i)
        rate = get_currency_rate(date, currency_code)
        if rate:
            dates.append(date.strftime('%Y-%m-%d'))
            rates.append(rate)
    return dates, rates

# Побудова графіка
def plot_currency_rate(currency_code='USD'):
    dates, rates = get_last_week_rates(currency_code)
    plt.figure(figsize=(10, 6))
    plt.plot(dates, rates, marker='o', label=f'{currency_code} Rate')
    plt.title(f'Курс {currency_code} за останній тиждень', fontsize=16)
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Курс (UAH)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Виклик функції для побудови графіка
if __name__ == "__main__":
    plot_currency_rate('USD')
