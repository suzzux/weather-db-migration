import enum
from sqlalchemy import Column, Integer, String, Float, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class WindDirectionEnum(enum.Enum):
    N = "N"; NNE = "NNE"; NE = "NE"; ENE = "ENE"
    E = "E"; ESE = "ESE"; SE = "SE"; SSE = "SSE"
    S = "S"; SSW = "SSW"; SW = "SW"; WSW = "WSW"
    W = "W"; WNW = "WNW"; NW = "NW"; NNW = "NNW"

class WeatherReport(Base):
    __tablename__ = "weather_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False)
    location_name = Column(String(100), nullable=False)
    wind_degree = Column(Integer, nullable=False)
    wind_kph = Column(Float, nullable=False)
    wind_direction = Column(Enum(WindDirectionEnum), nullable=False)
    last_updated = Column(Date, nullable=False)
    sunrise = Column(Time, nullable=False)

    # Зв'язок 1-до-1 з новою таблицею стану повітря
    air_quality = relationship("AirQuality", back_populates="weather_report", uselist=False, cascade="all, delete-orphan")

class AirQuality(Base):
    __tablename__ = "air_quality"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(Integer, ForeignKey("weather_reports.id", ondelete="CASCADE"), nullable=False, unique=True)

    carbon_monoxide = Column(Float, nullable=True)
    ozone = Column(Float, nullable=True)
    nitrogen_dioxide = Column(Float, nullable=True)
    sulphur_dioxide = Column(Float, nullable=True)
    pm2_5 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    us_epa_index = Column(Integer, nullable=True)
    gb_defra_index = Column(Integer, nullable=True)

    weather_report = relationship("WeatherReport", back_populates="air_quality")