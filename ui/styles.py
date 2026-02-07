# -*- coding: utf-8 -*-
"""
Themes and Styles for Fund Management Application
Light and Dark themes with professional styling
"""

LIGHT_STYLE = """
/* Main Window and Widgets */
QWidget {
  background-color: #f5f7fa;
  color: #2c3e50;
  font-family: 'Segoe UI', 'Tahoma', sans-serif;
  font-size: 13px;
}

QMainWindow {
  background-color: #f5f7fa;
}

QScrollArea {
  background-color: #f5f7fa;
  border: none;
}

/* Header Styling */
QMainWindow::separator {
  background-color: #e0e0e0;
}

/* MenuBar */
QMenuBar {
  background-color: #ffffff;
  border-bottom: 1px solid #d0d0d0;
  padding: 4px;
  color: #1a1a1a;
}

QMenuBar::item:hover {
  background-color: #e8f0ff;
}

QMenuBar::item:selected {
  background-color: #d4e4ff;
}

/* Menu */
QMenu {
  background-color: #ffffff;
  padding: 6px 0px;
  border: 1px solid #d0d0d0;
  border-radius: 4px;
  color: #1a1a1a;
}

QMenu::item:selected {
  background-color: #e8f0ff;
}

QMenu::item:hover {
  background-color: #f0f7ff;
}

QMenu::separator {
  background-color: #e0e0e0;
  height: 1px;
  margin: 4px 0px;
}

/* Sidebar - List Widget */
QListWidget {
  background-color: #ffffff;
  border: 1px solid #d4d4d4;
  padding: 8px;
  border-radius: 6px;
  outline: none;
  border-right: 3px solid #2563eb;
}

QListWidget::item {
  padding: 14px 12px;
  margin: 3px 0px;
  border-radius: 5px;
  font-size: 13px;
  color: #2c3e50;
  font-weight: 500;
}

QListWidget::item:hover {
  background-color: #f0f4f9;
  color: #000;
  border-left: 3px solid #2563eb;
  padding-left: 9px;
}

QListWidget::item:selected {
  background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2563eb, stop:1 #1d4ed8);
  color: #ffffff;
  font-weight: bold;
  border-radius: 5px;
  border-left: 3px solid #ffffff;
}

QListWidget::item:focus {
  outline: 2px solid #93c5fd;
}

/* Tool Buttons */
QToolButton {
  background: transparent;
  border: none;
  padding: 8px 12px;
  margin: 0px 2px;
  font-size: 13px;
  color: #2c3e50;
  border-radius: 4px;
  font-weight: 500;
}

QToolButton:hover {
  background-color: #e8f0ff;
  border-radius: 5px;
  color: #000;
  border: 1px solid #2563eb;
}

QToolButton:pressed {
  background-color: #d4e4ff;
  border: 1px solid #1d4ed8;
}

QToolButton:focus {
  border: 1px solid #2563eb;
}

/* Labels */
QLabel#title {
  font-weight: bold;
  font-size: 18px;
  color: #2c3e50;
  padding: 0px 6px;
}

QLabel#logo {
  font-size: 28px;
  padding: 2px 6px;
}

QLabel#tab-title {
  font-size: 18px;
  font-weight: bold;
  color: #2c3e50;
  padding: 8px 0px;
  border-bottom: 2px solid #2563eb;
  margin-bottom: 12px;
}

/* Message Box */
QMessageBox QLabel {
  color: #1a1a1a;
}

QMessageBox QPushButton {
  min-width: 60px;
  padding: 6px 12px;
  background-color: #2563eb;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  font-weight: bold;
}

QMessageBox QPushButton:hover {
  background-color: #1d4ed8;
}

QMessageBox QPushButton:pressed {
  background-color: #1e40af;
}

"""

DARK_STYLE = """
/* Main Window and Widgets */
QWidget {
  background-color: #0f1419;
  color: #cbd5e0;
  font-family: 'Segoe UI', 'Tahoma', sans-serif;
  font-size: 13px;
}

QMainWindow {
  background-color: #0f1419;
}

QScrollArea {
  background-color: #0f1419;
  border: none;
}

/* Header Styling */
QMainWindow::separator {
  background-color: #2d3748;
}

/* MenuBar */
QMenuBar {
  background-color: #1a202c;
  border-bottom: 1px solid #374151;
  padding: 4px;
  color: #e0e0e0;
}

QMenuBar::item:hover {
  background-color: #2d3748;
}

QMenuBar::item:selected {
  background-color: #374151;
}

/* Menu */
QMenu {
  background-color: #1a202c;
  padding: 6px 0px;
  border: 1px solid #374151;
  border-radius: 4px;
  color: #e0e0e0;
}

QMenu::item:selected {
  background-color: #2d3748;
}

QMenu::item:hover {
  background-color: #3a4557;
}

QMenu::separator {
  background-color: #374151;
  height: 1px;
  margin: 4px 0px;
}

/* Sidebar - List Widget */
QListWidget {
  background-color: #1a202c;
  border: 1px solid #374151;
  padding: 8px;
  border-radius: 6px;
  outline: none;
  border-right: 3px solid #3b82f6;
}

QListWidget::item {
  padding: 14px 12px;
  margin: 3px 0px;
  border-radius: 5px;
  font-size: 13px;
  color: #cbd5e0;
  font-weight: 500;
}

QListWidget::item:hover {
  background-color: #2d3748;
  color: #e8eef7;
  border-left: 3px solid #3b82f6;
  padding-left: 9px;
}

QListWidget::item:selected {
  background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3b82f6, stop:1 #1e40af);
  color: #ffffff;
  font-weight: bold;
  border-radius: 5px;
  border-left: 3px solid #ffffff;
}

QListWidget::item:focus {
  outline: 2px solid #60a5fa;
}

/* Tool Buttons */
QToolButton {
  background: transparent;
  border: none;
  padding: 8px 12px;
  margin: 0px 2px;
  font-size: 13px;
  color: #e0e0e0;
  border-radius: 4px;
  font-weight: 500;
}

QToolButton:hover {
  background-color: #2d3748;
  border-radius: 5px;
  color: #ffffff;
  border: 1px solid #3b82f6;
}

QToolButton:pressed {
  background-color: #3a4557;
  border: 1px solid #60a5fa;
}

QToolButton:focus {
  border: 1px solid #3b82f6;
}

/* Labels */
QLabel#title {
  font-weight: bold;
  font-size: 18px;
  color: #e0e0e0;
  padding: 0px 6px;
}

QLabel#logo {
  font-size: 28px;
  padding: 2px 6px;
}

QLabel#tab-title {
  font-size: 18px;
  font-weight: bold;
  color: #e0e0e0;
  padding: 8px 0px;
  border-bottom: 2px solid #3b82f6;
  margin-bottom: 12px;
}

/* Message Box */
QMessageBox QLabel {
  color: #e0e0e0;
}

QMessageBox QDialog {
  background-color: #1a202c;
}

QMessageBox QPushButton {
  min-width: 60px;
  padding: 6px 12px;
  background-color: #3b82f6;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  font-weight: bold;
}

QMessageBox QPushButton:hover {
  background-color: #2563eb;
}

QMessageBox QPushButton:pressed {
  background-color: #1d4ed8;
}

"""
