import enum
from sqlalchemy import Column, Integer, String, Float, Date, Time, Enum
from config import Base

# Enum для напрямку вітру
class WindDirectionEnum(enum.Enum):
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"

class WeatherReport(Base):
    __tablename__ = "weather_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Базові колонки:
    country = Column(String(100), nullable=False)                       # текстова
    location_name = Column(String(100), nullable=False)                 # місто (для зручності)
    wind_degree = Column(Integer, nullable=False)                       # ціле число
    wind_kph = Column(Float, nullable=False)                            # дробове число
    wind_direction = Column(Enum(WindDirectionEnum), nullable=False)    # enumeration
    last_updated = Column(Date, nullable=False)                         # дата
    sunrise = Column(Time, nullable=False)                              # час

    # Колонки варіанта №2 (Стан повітря / Air Quality):
    air_quality_carbon_monoxide = Column(Float, nullable=True)
    air_quality_ozone = Column(Float, nullable=True)
    air_quality_nitrogen_dioxide = Column(Float, nullable=True)
    air_quality_sulphur_dioxide = Column(Float, nullable=True)
    air_quality_pm2_5 = Column(Float, nullable=True)
    air_quality_pm10 = Column(Float, nullable=True)
    air_quality_us_epa_index = Column(Integer, nullable=True)
    air_quality_gb_defra_index = Column(Integer, nullable=True)