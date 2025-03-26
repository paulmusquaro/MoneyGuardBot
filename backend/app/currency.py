import asyncio
import httpx
from bs4 import BeautifulSoup

async def get_usd_exchange_rate():
    url = "https://bank.gov.ua/ua/markets/exchangerates"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
        
        soup = BeautifulSoup(response.text, "html.parser")
        rate_tag = soup.find("td", text="USD")
        
        if rate_tag:
            next_tds = rate_tag.find_next_siblings("td")  # Отримуємо всі наступні комірки
            if len(next_tds) >= 3:  # Переконуємось, що є хоча б 3 комірки
                rate = next_tds[2].text.strip().replace(',', '.').replace(' ', '')
                return float(rate)
        
        raise ValueError("Не вдалося знайти курс USD")
    
    except httpx.RequestError as e:
        raise ValueError(f"Помилка підключення: {e}")


"""
async def main():
    try:
        rate = await get_usd_exchange_rate()
        print(f"Отриманий курс: {rate}")
    except Exception as e:
        print(f"Помилка: {e}")

asyncio.run(main())"
"""
