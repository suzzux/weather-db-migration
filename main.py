from config import SessionLocal
from repository import WeatherRepository
from service import WeatherService

def main():
    session = SessionLocal()
    repo = WeatherRepository(session)
    service = WeatherService(repo)

    # Якщо базу щойно створили з нуля — заповнить її автоматично
    service.import_from_csv_if_empty()

    print("\n=== Погодний Моніторинг (Варіант 18: Стан повітря) ===")
    country = input("Введіть назву країни англійською (наприклад, Ukraine або Afghanistan): ").strip()
    date_str = input("Введіть дату у форматі РРРР-ММ-ДД (наприклад, 2024-05-16): ").strip()

    try:
        results = service.search_weather(country, date_str)
        if not results:
            print("\nНа жаль, за цими параметрами записів не знайдено.")
        else:
            for r in results:
                aq = r.air_quality
                verdict = "ТАК (повітря чисте)" if aq.should_go_outside else "НІ (повітря забруднене!)"
                print("\n" + "=" * 50)
                print(f"Країна: {r.country} | Місто: {r.location_name}")
                print(f"Дата оновлення: {r.last_updated} | Схід сонця: {r.sunrise}")
                print(f"Вітер: {r.wind_kph} км/год, {r.wind_degree}° ({r.wind_direction.value})")
                print("--- Стан повітря ---")
                print(f"PM2.5: {aq.pm2_5} | PM10: {aq.pm10} | CO: {aq.carbon_monoxide} | O3: {aq.ozone}")
                print(f"Індекс US EPA: {aq.us_epa_index} | Індекс GB DEFRA: {aq.gb_defra_index}")
                print(f">>> ЧИ ВАРТО ВИХОДИТИ НА ВУЛИЦЮ: {verdict}")
                print("=" * 50)
    except ValueError:
        print("Помилка: неправильний формат дати! Використовуйте РРРР-ММ-ДД.")
    finally:
        session.close()

if __name__ == "__main__":
    main()