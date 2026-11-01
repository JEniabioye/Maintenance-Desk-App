
import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def generate_id():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_id
    )
    full_name: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    properties: Mapped[list["Property"]] = relationship(
        back_populates="client"
    )


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_id
    )
    client_id: Mapped[str] = mapped_column(
        ForeignKey("clients.id")
    )
    name: Mapped[str] = mapped_column(String(150))
    address: Mapped[str] = mapped_column(Text)

    client: Mapped["Client"] = relationship(
        back_populates="properties"
    )
    equipment: Mapped[list["Equipment"]] = relationship(
        back_populates="property"
    )
    visits: Mapped[list["MaintenanceVisit"]] = relationship(
        back_populates="property"
    )


class Technician(Base):
    __tablename__ = "technicians"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_id
    )
    full_name: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_id
    )
    property_id: Mapped[str] = mapped_column(
        ForeignKey("properties.id")
    )
    name: Mapped[str] = mapped_column(String(150))
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    serial_number: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)

    property: Mapped["Property"] = relationship(
        back_populates="equipment"
    )
    faults: Mapped[list["Fault"]] = relationship(
        back_populates="equipment"
    )


class MaintenanceVisit(Base):
    __tablename__ = "maintenance_visits"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_id
    )
    property_id: Mapped[str] = mapped_column(
        ForeignKey("properties.id")
    )
    technician_id: Mapped[str | None] = mapped_column(
        ForeignKey("technicians.id"), nullable=True
    )
    visit_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(
        String(30), default="scheduled"
    )
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    property: Mapped["Property"] = relationship(
        back_populates="visits"
    )
    serviced_equipment: Mapped[list["VisitEquipment"]] = relationship(
        back_populates="visit"
    )
    faults: Mapped[list["Fault"]] = relationship(
        back_populates="visit"
    )


class VisitEquipment(Base):
    __tablename__ = "visit_equipment"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_id
    )
    visit_id: Mapped[str] = mapped_column(
        ForeignKey("maintenance_visits.id")
    )
    equipment_id: Mapped[str] = mapped_column(
        ForeignKey("equipment.id")
    )
    work_performed: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    condition_after: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "visit_id", "equipment_id",
            name="unique_equipment_per_visit"
        ),
    )

    visit: Mapped["MaintenanceVisit"] = relationship(
        back_populates="serviced_equipment"
    )


class Fault(Base):
    __tablename__ = "faults"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_id
    )
    equipment_id: Mapped[str] = mapped_column(
        ForeignKey("equipment.id")
    )
    visit_id: Mapped[str | None] = mapped_column(
        ForeignKey("maintenance_visits.id"), nullable=True
    )
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(
        String(30), default="medium"
    )
    status: Mapped[str] = mapped_column(
        String(30), default="open"
    )
    diagnosis: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
    reported_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    equipment: Mapped["Equipment"] = relationship(
        back_populates="faults"
    )
    visit: Mapped["MaintenanceVisit"] = relationship(
        back_populates="faults"
    )
