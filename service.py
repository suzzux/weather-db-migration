import csv
from datetime import datetime
from models import WeatherReport, WindDirectionEnum
from config import SessionLocal

def load_csv_initial(filepath="GlobalWeatherRepository.csv"):
    session = SessionLocal()
    if session.query(WeatherReport).count() > 0:
        print("База вже містить дані, пропускаємо завантаження.")
        session.close()
        return

    with open(filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            
            # Парсимо дату (формат "2024-05-16 13:15") та час сходу сонця ("05:45 AM")
            dt_date = datetime.strptime(row["last_updated"].split()[0], "%Y-%m-%d").date()
            dt_sunrise = datetime.strptime(row["sunrise"].strip(), "%I:%M %p").time()

            report = WeatherReport(
                country=row["country"],
                location_name=row["location_name"],
                wind_degree=int(row["wind_degree"]),
                wind_kph=float(row["wind_kph"]),
                wind_direction=WindDirectionEnum[row["wind_direction"]],
                last_updated=dt_date,
                sunrise=dt_sunrise,
                air_quality_carbon_monoxide=float(row["air_quality_Carbon_Monoxide"]),
                air_quality_ozone=float(row["air_quality_Ozone"]),
                air_quality_nitrogen_dioxide=float(row["air_quality_Nitrogen_dioxide"]),
                air_quality_sulphur_dioxide=float(row["air_quality_Sulphur_dioxide"]),
                air_quality_pm2_5=float(row["air_quality_PM2.5"]),
                air_quality_pm10=float(row["air_quality_PM10"]),
                air_quality_us_epa_index=int(row["air_quality_us-epa-index"]),
                air_quality_gb_defra_index=int(row["air_quality_gb-defra-index"]),
            )
            session.add(report)
        session.commit()
    session.close()
    print("Дані успішно завантажено з CSV!")

if __name__ == "__main__":
    load_csv_initial()