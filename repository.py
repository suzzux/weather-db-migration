from sqlalchemy.orm import joinedload
from models import WeatherReport

class WeatherRepository:
    def __init__(self, session):
        self.session = session

    def count_reports(self) -> int:
        return self.session.query(WeatherReport).count()

    def save_report(self, report: WeatherReport):
        self.session.add(report)

    def commit(self):
        self.session.commit()

    def get_by_country_and_date(self, country: str, target_date):
        return (
            self.session.query(WeatherReport)
            .options(joinedload(WeatherReport.air_quality))
            .filter(
                WeatherReport.country.ilike(f"%{country}%"),
                WeatherReport.last_updated == target_date
            )
            .all()
        )