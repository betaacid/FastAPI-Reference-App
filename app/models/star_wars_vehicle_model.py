from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from database import Base


class StarWarsVehicle(Base):
    __tablename__ = "star_wars_vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=True)
    manufacturer: Mapped[str] = mapped_column(String, nullable=True)
    cost_in_credits: Mapped[str] = mapped_column(String, nullable=True)
    length: Mapped[str] = mapped_column(String, nullable=True)
    max_atmosphering_speed: Mapped[str] = mapped_column(String, nullable=True)
    crew: Mapped[str] = mapped_column(String, nullable=True)
    passengers: Mapped[str] = mapped_column(String, nullable=True)
    cargo_capacity: Mapped[str] = mapped_column(String, nullable=True)
    consumables: Mapped[str] = mapped_column(String, nullable=True)
    vehicle_class: Mapped[str] = mapped_column(String, nullable=True)
    pilots: Mapped[str] = mapped_column(String, nullable=True)
    efficiency: Mapped[float] = mapped_column(Integer, nullable=True)
