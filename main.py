import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QHBoxLayout, QStackedWidget,
                             QListWidget, QToolButton, QLabel,
                             QAction, QMessageBox)

from ui.tabs.groups_tab import GroupsTab
from ui.tabs.members_tab import MembersTab
from ui.tabs.monthly_fee_tab import MonthlyFeeTab
from ui.tabs.collected_money_tab import CollectedMoneyTab
from ui.tabs.general_expenses_tab import GeneralExpensesTab
from ui.tabs.death_expenses_tab import DeathExpensesTab
from ui.tabs.loans_tab import LoansTab
from ui.tabs.summary_tab import SummaryTab
from ui.styles import LIGHT_STYLE, DARK_STYLE



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fund Management - صندوق تعاونی")
        self.resize(1100, 650)
        self.current_theme = 'light'

        # --- Menubar (Important basics) ---
        menubar = self.menuBar()
        file_menu = menubar.addMenu("پرونده")
        help_menu = menubar.addMenu("راهنما")

        act_exit = QAction("خروج", self)
        act_exit.triggered.connect(self.close)
        file_menu.addAction(act_exit)

        act_about = QAction("درباره", self)
        act_about.triggered.connect(self.about_dialog)
        help_menu.addAction(act_about)

        # --- Central ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Set Right-to-Left direction for Persian UI
        self.setLayoutDirection(Qt.RightToLeft)

        # --- Header ---
        header = QWidget()
        header.setFixedHeight(72)
        header.setObjectName("header")
        header.setStyleSheet("""
            #header {
                background-color: #ffffff;
                border-bottom: 3px solid #2563eb;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 10, 16, 10)
        header_layout.setSpacing(14)

        logo_lbl = QLabel("🔷")
        logo_lbl.setObjectName("logo")
        logo_lbl.setStyleSheet("font-size: 28px; padding: 4px;")
        
        title_lbl = QLabel("صندوق تعاونی - مدیریت مالی")
        title_lbl.setObjectName("title")

        header_layout.addWidget(logo_lbl)
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()

        btn_notifications = QToolButton()
        btn_notifications.setText("🔔 اعلان‌ها")
        btn_notifications.setToolTip("اعلان‌های جدید")
        
        btn_settings = QToolButton()
        btn_settings.setText("⚙️ تنظیمات")
        btn_settings.setToolTip("تنظیمات برنامه")

        btn_theme = QToolButton()
        btn_theme.setCheckable(True)
        btn_theme.setText("🌙")
        btn_theme.setToolTip("تغییر حالت روشن/تاریک")
        btn_theme.toggled.connect(self.toggle_theme)
        self.btn_theme = btn_theme

        btn_logout = QToolButton()
        btn_logout.setText("🚪 خروج")
        btn_logout.setToolTip("خروج از برنامه")
        btn_logout.clicked.connect(self.close)

        header_layout.addWidget(btn_notifications)
        header_layout.addWidget(btn_settings)
        header_layout.addWidget(btn_theme)
        header_layout.addWidget(btn_logout)

        layout.addWidget(header)

        # --- Body: sidebar + pages ---
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(12, 12, 12, 12)
        body_layout.setSpacing(12)

        # Sidebar (vertical list of pages)
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(260)
        self.sidebar.addItems([
            "📊 داشبورد / خلاصه",
            "👥 گروه‌ها",
            "👤 اعضا",
            "💰 هزینه ماهیانه",
            "💵 پول جمع‌آوری‌شده",
            "📋 مصارف عمومی",
            "⚰️ مصارف فوتی",
            "📑 قرض‌ها",
        ])
        body_layout.addWidget(self.sidebar)

        # Stacked pages
        self.pages = QStackedWidget()
        self.summary_tab = SummaryTab(self)
        self.groups_tab = GroupsTab(self)
        self.members_tab = MembersTab(self)
        self.monthly_fee_tab = MonthlyFeeTab(self)
        self.collected_tab = CollectedMoneyTab(self)
        self.general_exp_tab = GeneralExpensesTab(self)
        self.death_exp_tab = DeathExpensesTab(self)
        self.loans_tab = LoansTab(self)

        for w in [
            self.summary_tab,
            self.groups_tab,
            self.members_tab,
            self.monthly_fee_tab,
            self.collected_tab,
            self.general_exp_tab,
            self.death_exp_tab,
            self.loans_tab,
        ]:
            self.pages.addWidget(w)

        body_layout.addWidget(self.pages)
        layout.addWidget(body)

        # Connect sidebar selection to pages
        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

    def apply_theme(self, theme):
        if theme == 'dark':
            QApplication.instance().setStyleSheet(DARK_STYLE)
            # Update header styling for dark mode
            header = self.findChild(QWidget, "header")
            if header:
                header.setStyleSheet("""
                    #header {
                        background-color: #1a202c;
                        border-bottom: 3px solid #3b82f6;
                    }
                """)
            self.current_theme = 'dark'
            # Update table styles for dark mode
            if hasattr(self, 'groups_tab') and hasattr(self.groups_tab, 'apply_table_styles'):
                self.groups_tab.apply_table_styles()
            try:
                self.btn_theme.setText('☀️')
                self.btn_theme.setChecked(True)
            except Exception:
                pass
        else:
            QApplication.instance().setStyleSheet(LIGHT_STYLE)
            # Update header styling for light mode
            header = self.findChild(QWidget, "header")
            if header:
                header.setStyleSheet("""
                    #header {
                        background-color: #ffffff;
                        border-bottom: 3px solid #2563eb;
                    }
                """)
            self.current_theme = 'light'
            # Update table styles for light mode
            if hasattr(self, 'groups_tab') and hasattr(self.groups_tab, 'apply_table_styles'):
                self.groups_tab.apply_table_styles()
            try:
                self.btn_theme.setText('🌙')
                self.btn_theme.setChecked(False)
            except Exception:
                pass

    def toggle_theme(self, checked):
        self.apply_theme('dark' if checked else 'light')

    def about_dialog(self):
        QMessageBox.information(
            self,
            "درباره",
            "برنامه مدیریت صندوق\nPyQt5 + SQLite\n(صندوق تعاونی)"
        )

    def refresh_all(self):
        """Later we call this after any insert/update so all tabs can reload data."""
        for w in [
            self.summary_tab,
            self.groups_tab,
            self.members_tab,
            self.monthly_fee_tab,
            self.collected_tab,
            self.general_exp_tab,
            self.death_exp_tab,
            self.loans_tab,
        ]:
            if hasattr(w, "refresh"):
                w.refresh()


def main():
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    app.setFont(QFont("Tahoma", 10))
    win = MainWindow()
    # set default theme to light
    win.apply_theme('light')
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
