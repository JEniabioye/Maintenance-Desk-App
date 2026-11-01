
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget,
)
from PySide6.QtCore import Qt

from app.modules.clients.client_page import ClientPage

class MaintenanceDesk(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MaintenanceDesk")
        self.setMinimumSize(1100, 700)

        self.setup_ui()

    def setup_ui(self):
        # Main application container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(230)
        sidebar.setObjectName("sidebar")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 20)
        sidebar_layout.setSpacing(12)

        logo = QLabel("MaintenanceDesk")
        logo.setObjectName("logo")
        sidebar_layout.addWidget(logo)

        subtitle = QLabel("CLIENT & SERVICE MANAGEMENT")
        subtitle.setObjectName("subtitle")
        sidebar_layout.addWidget(subtitle)

        sidebar_layout.addSpacing(25)

        # Navigation
        self.pages = QStackedWidget()

        navigation = [
            ("Dashboard", 0),
            ("Clients", 1),
            ("Properties", 2),
            ("Equipment", 3),
            ("Maintenance Visits", 4),
            ("Equipment Faults", 5),
            ("Technicians", 6),
            ("Reports", 7),
            ("Settings", 8),
        ]

        for name, index in navigation:
            button = QPushButton(name)
            button.setObjectName("nav_button")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked=False, i=index: self.change_page(i)
            )

            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        version = QLabel("MaintenanceDesk v0.1")
        version.setObjectName("version")
        sidebar_layout.addWidget(version)

        # Main content area
        content = QFrame()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(35, 30, 35, 30)

        # Create pages
        self.create_pages()

        content_layout.addWidget(self.pages)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

    def create_pages(self):

        # Dashboard page
        dashboard = QWidget()
        dashboard_layout = QVBoxLayout(dashboard)
        dashboard_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        heading = QLabel("Dashboard")
        heading.setObjectName("page_heading")

        description = QLabel(
            "Welcome to MaintenanceDesk. Here's your service overview."
        )
        description.setObjectName("description")

        dashboard_layout.addWidget(heading)
        dashboard_layout.addWidget(description)
        dashboard_layout.addSpacing(25)

        # Dashboard summary cards
        cards_layout = QGridLayout()
        cards_layout.setSpacing(18)

        cards = [
            ("Total Clients", "0"),
            ("Maintenance Visits", "0"),
            ("Open Faults", "0"),
            ("Registered Equipment", "0"),
        ]

        for index, (title, value) in enumerate(cards):
            card = self.create_card(title, value)
            cards_layout.addWidget(card, index // 2, index % 2)

        dashboard_layout.addLayout(cards_layout)
        dashboard_layout.addSpacing(30)

        activity_heading = QLabel("Recent Activities")
        activity_heading.setObjectName("section_heading")

        activity_description = QLabel(
            "Your recent maintenance activities will appear here."
        )
        activity_description.setObjectName("description")

        dashboard_layout.addWidget(activity_heading)
        dashboard_layout.addWidget(activity_description)

        self.pages.addWidget(dashboard)
        self.pages.addWidget(ClientPage())

        # Other pages
        page_names = [
            "Properties",
            "Equipment",
            "Maintenance Visits",
            "Equipment Faults",
            "Technicians",
            "Reports",
            "Settings",
        ]

        for name in page_names:
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            heading = QLabel(name)
            heading.setObjectName("page_heading")

            message = QLabel(
                f"The {name.lower()} module will be developed in a later stage."
            )
            message.setObjectName("description")

            layout.addWidget(heading)
            layout.addWidget(message)

            self.pages.addWidget(page)

    def create_card(self, title, value):
        card = QFrame()
        card.setObjectName("dashboard_card")
        card.setMinimumHeight(130)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)

        title_label = QLabel(title)
        title_label.setObjectName("card_title")

        value_label = QLabel(value)
        value_label.setObjectName("card_value")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return card

    def change_page(self, index):
        self.pages.setCurrentIndex(index)


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QMainWindow {
            background-color: #F4F6FA;
        }

        #sidebar {
            background-color: #17243A;
        }

        #logo {
            color: white;
            font-size: 21px;
            font-weight: bold;
        }

        #subtitle {
            color: #9BAAC0;
            font-size: 9px;
        }

        #nav_button {
            background-color: transparent;
            color: #D5DEEA;
            border: none;
            text-align: left;
            padding: 12px;
            font-size: 13px;
            border-radius: 6px;
        }

        #nav_button:hover {
            background-color: #2C405E;
            color: white;
        }

        #version {
            color: #8292A9;
            font-size: 10px;
        }

        #content {
            background-color: #F4F6FA;
        }

        #page_heading {
            color: #17243A;
            font-size: 27px;
            font-weight: bold;
        }

        #description {
            color: #718096;
            font-size: 13px;
        }

        #section_heading {
            color: #17243A;
            font-size: 18px;
            font-weight: bold;
        }

        #dashboard_card {
            background-color: white;
            border: 1px solid #E5EAF1;
            border-radius: 10px;
        }

        #card_title {
            color: #718096;
            font-size: 13px;
        }

        #primary_button {
            background-color: #2563EB;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 9px 16px;
            font-weight: bold;
        }

        #primary_button:hover {
            background-color: #1D4ED8;
        }
        
        #card_value {
            color: #17243A;
            font-size: 30px;
            font-weight: bold;
        }
    """)

    window = MaintenanceDesk()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
