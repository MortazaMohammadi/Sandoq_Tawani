# -*- coding: utf-8 -*-
"""
Base Tab Widget for Fund Management Application
Provides consistent styling and structure for all tabs
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class BaseTab(QWidget):
    """Base class for all tab widgets with common functionality"""
    
    def __init__(self, main_window=None, title=""):
        super().__init__()
        self.main_window = main_window
        self.title = title
        
        # Set widget styling
        self.setStyleSheet("""
            BaseTab {
                background-color: transparent;
            }
        """)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        
        # Title label
        if title:
            title_label = QLabel(title)
            title_label.setObjectName("tab-title")
            title_label.setStyleSheet("""
                QLabel#tab-title {
                    font-size: 18px;
                    font-weight: bold;
                    padding: 8px 0px;
                    border-bottom: 2px solid;
                    border-color: #2563eb;
                    margin-bottom: 8px;
                }
            """)
            self.layout.addWidget(title_label)
            self.title_label = title_label
    
    def refresh(self):
        """Override this method in subclasses to refresh data"""
        pass
    
    def create_button(self, text, callback=None, style="primary"):
        """Create a styled button for the tab"""
        btn = QPushButton(text)
        btn.setMinimumHeight(40)
        btn.setCursor(Qt.PointingHandCursor)
        
        if style == "primary":
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-family: 'Segoe UI', 'Tahoma', sans-serif;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                    padding: 10px 22px;
                }
                QPushButton:pressed {
                    background-color: #1e40af;
                    padding: 10px 18px;
                }
            """)
        elif style == "secondary":
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #2563eb;
                    border: 2px solid #2563eb;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 8px 18px;
                    font-size: 13px;
                    font-family: 'Segoe UI', 'Tahoma', sans-serif;
                }
                QPushButton:hover {
                    background-color: #f0f4f8;
                    border: 2px solid #1d4ed8;
                    color: #1d4ed8;
                }
                QPushButton:pressed {
                    background-color: #e0e7ff;
                    border: 2px solid #1e40af;
                    color: #1e40af;
                }
            """)
        
        if callback:
            btn.clicked.connect(callback)
        return btn
    
    def create_button_group(self, buttons):
        """Create a horizontal group of buttons"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        for btn in buttons:
            layout.addWidget(btn)
        
        layout.addStretch()
        return container
