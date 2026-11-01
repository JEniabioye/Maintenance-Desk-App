
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit,
    QTextEdit, QDialog, QFormLayout,
    QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt

from app.services.client_service import (
    get_all_clients,
    add_client,
    update_client,
    delete_client,
)


class ClientDialog(QDialog):

    def __init__(self, parent=None, client=None):
        super().__init__(parent)

        self.client = client
        self.setWindowTitle(
            "Edit Client" if client else "Register New Client"
        )
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.notes_input = QTextEdit()

        self.notes_input.setMaximumHeight(100)

        self.name_input.setPlaceholderText("Enter full name")
        self.phone_input.setPlaceholderText("Enter phone number")
        self.email_input.setPlaceholderText("Enter email address")
        self.notes_input.setPlaceholderText("Additional information")

        form.addRow("Full Name *", self.name_input)
        form.addRow("Phone Number *", self.phone_input)
        form.addRow("Email", self.email_input)
        form.addRow("Notes", self.notes_input)

        layout.addLayout(form)

        if client:
            self.name_input.setText(client.full_name)
            self.phone_input.setText(client.phone)
            self.email_input.setText(client.email or "")
            self.notes_input.setPlainText(client.notes or "")

        buttons = QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        save_button = QPushButton("Save Client")

        cancel_button.clicked.connect(self.reject)
        save_button.clicked.connect(self.save_client)

        buttons.addStretch()
        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout.addLayout(buttons)

    def save_client(self):

        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        if not name or not phone:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Full name and phone number are required."
            )
            return

        if self.client:
            success = update_client(
                self.client.id,
                name,
                phone,
                email,
                notes
            )

            if not success:
                QMessageBox.warning(
                    self, "Error", "Client could not be updated."
                )
                return

        else:
            add_client(name, phone, email, notes)

        self.accept()


class ClientPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.load_clients()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(18)

        # Page heading
        heading = QLabel("Client Management")
        heading.setObjectName("page_heading")

        description = QLabel(
            "Register, search and manage your clients."
        )
        description.setObjectName("description")

        main_layout.addWidget(heading)
        main_layout.addWidget(description)

        # Search and action buttons
        toolbar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by name, phone or email..."
        )
        self.search_input.setMinimumHeight(38)
        self.search_input.textChanged.connect(self.load_clients)

        add_button = QPushButton("+ Register Client")
        add_button.setMinimumHeight(38)
        add_button.setObjectName("primary_button")
        add_button.clicked.connect(self.open_add_dialog)

        toolbar.addWidget(self.search_input)
        toolbar.addWidget(add_button)

        main_layout.addLayout(toolbar)

        # Clients table
        self.table = QTableWidget()

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Client Name",
            "Phone Number",
            "Email",
            "Date Registered",
            "Client ID"
        ])

        self.table.setColumnHidden(4, True)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        main_layout.addWidget(self.table)

        # Edit and delete buttons
        actions = QHBoxLayout()

        edit_button = QPushButton("Edit Selected")
        delete_button = QPushButton("Delete Selected")

        edit_button.clicked.connect(self.edit_client)
        delete_button.clicked.connect(self.remove_client)

        actions.addStretch()
        actions.addWidget(edit_button)
        actions.addWidget(delete_button)

        main_layout.addLayout(actions)

    def load_clients(self):

        search_text = self.search_input.text().strip()

        clients = get_all_clients(search_text)

        self.table.setRowCount(0)

        for client in clients:

            row = self.table.rowCount()
            self.table.insertRow(row)

            values = [
                client.full_name,
                client.phone,
                client.email or "",
                client.created_at.strftime("%d %b %Y"),
                client.id
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setFlags(
                    item.flags() &
                    ~Qt.ItemFlag.ItemIsEditable
                )
                self.table.setItem(row, column, item)

    def selected_client_id(self):

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.information(
                self,
                "Select Client",
                "Please select a client first."
            )
            return None

        return self.table.item(row, 4).text()

    def open_add_dialog(self):

        dialog = ClientDialog(self)

        if dialog.exec():
            self.load_clients()

    def edit_client(self):

        client_id = self.selected_client_id()

        if not client_id:
            return

        clients = get_all_clients()
        client = next(
            (item for item in clients if item.id == client_id),
            None
        )

        if not client:
            QMessageBox.warning(
                self, "Not Found", "Client record not found."
            )
            return

        dialog = ClientDialog(self, client)

        if dialog.exec():
            self.load_clients()

    def remove_client(self):

        client_id = self.selected_client_id()

        if not client_id:
            return

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this client?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:

            success, message = delete_client(client_id)

            if success:
                QMessageBox.information(
                    self, "Success", message
                )
            else:
                QMessageBox.warning(
                    self, "Cannot Delete", message
                )

            self.load_clients()
