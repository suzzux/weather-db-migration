import csv
from datetime import datetime
from models import WeatherReport, AirQuality, WindDirectionEnum
from repository import WeatherRepository

class WeatherService:
    def __init__(self, repository: WeatherRepository):
        self.repo = repository

    @staticmethod
    def calculate_should_go_outside(epa_index: int, pm2_5: float, co: float) -> bool:
        """
        Формула: варто виходити на вулицю (True), якщо:
        1) Індекс чистоти повітря US EPA <= 2 (Good або Moderate)
        2) Дрібнодисперсний пил PM2.5 < 35.0 мкг/м³
        3) Чадний газ (CO) < 1000.0 мкг/м³
        """
        return epa_index <= 2 and pm2_5 < 35.0 and co < 1000.0

    def import_from_csv_if_empty(self, filepath="GlobalWeatherRepository.csv", limit=500):
        if self.repo.count_reports() > 0:
            return

        print("База порожня. Імпортуємо дані з CSV у нову структуру...")
        with open(filepath, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i >= limit:
                    break
                
                dt_date = datetime.strptime(row["last_updated"].split()[0], "%Y-%m-%d").date()
                dt_sunrise = datetime.strptime(row["sunrise"].strip(), "%I:%M %p").time()

                epa = int(row["air_quality_us-epa-index"])
                pm25 = float(row["air_quality_PM2.5"])
                co = float(row["air_quality_Carbon_Monoxide"])

                # Визначаємо за формулою, чи варто виходити на вулицю
                go_outside = self.calculate_should_go_outside(epa, pm25, co)

                report = WeatherReport(
                    country=row["country"],
                    location_name=row["location_name"],
                    wind_degree=int(row["wind_degree"]),
                    wind_kph=float(row["wind_kph"]),
                    wind_direction=WindDirectionEnum[row["wind_direction"]],
                    last_updated=dt_date,
                    sunrise=dt_sunrise,
                    air_quality=AirQuality(
                        carbon_monoxide=co,
                        ozone=float(row["air_quality_Ozone"]),
                        nitrogen_dioxide=float(row["air_quality_Nitrogen_dioxide"]),
                        sulphur_dioxide=float(row["air_quality_Sulphur_dioxide"]),
                        pm2_5=pm25,
                        pm10=float(row["air_quality_PM10"]),
                        us_epa_index=epa,
                        gb_defra_index=int(row["air_quality_gb-defra-index"]),
                        should_go_outside=go_outside
                    )
                )
                self.repo.save_report(report)
            self.repo.commit()
        print("Імпорт завершено успішно!")

    def search_weather(self, country: str, date_str: str):
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return self.repo.get_by_country_and_date(country, target_date)