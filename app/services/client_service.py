
from sqlalchemy import select, or_

from app.database.connection import SessionLocal
from app.database.models import Client


def get_all_clients(search_text=""):
    """Retrieve all clients, optionally filtered by search text."""

    with SessionLocal() as session:
        statement = select(Client)

        if search_text:
            search = f"%{search_text}%"

            statement = statement.where(
                or_(
                    Client.full_name.ilike(search),
                    Client.phone.ilike(search),
                    Client.email.ilike(search),
                )
            )

        statement = statement.order_by(Client.created_at.desc())

        return session.scalars(statement).all()


def add_client(full_name, phone, email="", notes=""):
    """Register a new client."""

    with SessionLocal() as session:
        client = Client(
            full_name=full_name,
            phone=phone,
            email=email or None,
            notes=notes or None,
        )

        session.add(client)
        session.commit()

        return client.id


def update_client(client_id, full_name, phone, email="", notes=""):
    """Update an existing client."""

    with SessionLocal() as session:
        client = session.get(Client, client_id)

        if client is None:
            return False

        client.full_name = full_name
        client.phone = phone
        client.email = email or None
        client.notes = notes or None

        session.commit()
        return True


def delete_client(client_id):
    """Delete a client who has no associated properties."""

    with SessionLocal() as session:
        client = session.get(Client, client_id)

        if client is None:
            return False, "Client not found."

        if client.properties:
            return False, (
                "This client has registered properties. "
                "Remove or reassign those properties first."
            )

        session.delete(client)
        session.commit()

        return True, "Client deleted successfully."
