# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QToolButton,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QHeaderView, QMenu, QAbstractItemView)
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSizePolicy
from .base_tab import BaseTab
from db.groups_db import get_all_groups, delete_group
from ui.dialogs.group_dialog import GroupDialog


class GroupsTab(BaseTab):
    def __init__(self, main_window=None):
        super().__init__(main_window, "👥 مدیریت گروه‌ها")
        self.main_window = main_window
        
        # Add button
        add_btn = self.create_button("+ افزودن گروه جدید", self.add_group)
        self.layout.addWidget(add_btn)
        
        # Table for groups
        from utils.date_utils import to_persian_digits

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["شناسه", "نام گروه", "رهبر", "تاریخ ایجاد", "عملیات"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.apply_table_styles()
        
        # Make table expandable to fill available space
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Setup column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        # Context menu
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.doubleClicked.connect(lambda idx: self.edit_group_by_id(int(self.table.item(idx.row(),0).text())))
        
        self.layout.addWidget(self.table, 1)  # Add stretch factor to table
        self.layout.addStretch(0)  # Remove extra stretch at bottom
        
        self.refresh()
    
    def apply_table_styles(self):
        """Apply theme-aware styles to table"""
        is_dark_mode = self.main_window and hasattr(self.main_window, 'current_theme') and self.main_window.current_theme == 'dark'
        
        if is_dark_mode:
            stylesheet = """
                QTableWidget {
                    background-color: #1a202c;
                    border: 1px solid #2d3748;
                    border-radius: 8px;
                    gridline-color: #2d3748;
                }
                QTableWidget::item {
                    padding: 0px;
                    margin: 0px;
                    border: none;
                    color: #cbd5e0;
                }
                QTableWidget::item:selected {
                    background-color: #2d3748;
                    color: #e2e8f0;
                }
                QHeaderView::section {
                    background-color: #0f1419;
                    padding: 12px 8px;
                    border: none;
                    font-weight: 600;
                    color: #cbd5e0;
                    border-bottom: 2px solid #2d3748;
                }
            """
        else:
            stylesheet = """
                QTableWidget {
                    background-color: #ffffff;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                }
                QTableWidget::item {
                    padding: 0px;
                    margin: 0px;
                    border: none;
                    color: #2c3e50;
                }
                QTableWidget::item:selected {
                    background-color: #e8f0ff;
                    color: #000000;
                }
                QHeaderView::section {
                    background-color: #f8f9fb;
                    padding: 12px 8px;
                    border: none;
                    font-weight: 600;
                    color: #2c3e50;
                    border-bottom: 2px solid #e0e0e0;
                }
            """
        
        self.table.setStyleSheet(stylesheet)
    
    def get_button_style(self, button_type='view'):
        """Get theme-aware button styles"""
        is_dark_mode = self.main_window and hasattr(self.main_window, 'current_theme') and self.main_window.current_theme == 'dark'
        
        if button_type == 'view':
            if is_dark_mode:
                return """
                    QPushButton {
                        background-color: #2d3748;
                        color: #cbd5e0;
                        border: 1px solid #4a5568;
                        border-radius: 5px;
                        padding: 2px 6px;
                        font-weight: 600;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #4a5568;
                        color: #e2e8f0;
                    }
                    QPushButton:pressed {
                        background-color: #1a202c;
                    }
                """
            else:
                return """
                    QPushButton {
                        background-color: #f3f4f6;
                        color: #374151;
                        border: 1px solid #d1d5db;
                        border-radius: 5px;
                        padding: 2px 6px;
                        font-weight: 600;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #e5e7eb;
                    }
                    QPushButton:pressed {
                        background-color: #d1d5db;
                    }
                """
        
        elif button_type == 'edit':
            if is_dark_mode:
                return """
                    QPushButton {
                        background-color: #3b82f6;
                        color: #ffffff;
                        border: none;
                        border-radius: 5px;
                        padding: 2px 6px;
                        font-weight: 600;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #2563eb;
                    }
                    QPushButton:pressed {
                        background-color: #1d4ed8;
                    }
                """
            else:
                return """
                    QPushButton {
                        background-color: #2563eb;
                        color: #ffffff;
                        border: none;
                        border-radius: 5px;
                        padding: 2px 6px;
                        font-weight: 600;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #1d4ed8;
                    }
                    QPushButton:pressed {
                        background-color: #1e40af;
                    }
                """
        
        elif button_type == 'delete':
            if is_dark_mode:
                return """
                    QPushButton {
                        background-color: #7f1d1d;
                        color: #fca5a5;
                        border: 1px solid #b91c1c;
                        border-radius: 5px;
                        padding: 2px 6px;
                        font-weight: 600;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #b91c1c;
                        color: #fecaca;
                    }
                    QPushButton:pressed {
                        background-color: #991b1b;
                    }
                """
            else:
                return """
                    QPushButton {
                        background-color: #fee2e2;
                        color: #dc2626;
                        border: 1px solid #fecaca;
                        border-radius: 5px;
                        padding: 2px 6px;
                        font-weight: 600;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #fecaca;
                    }
                    QPushButton:pressed {
                        background-color: #fca5a5;
                    }
                """
        
        return ""
    
    def refresh(self):
        """Refresh groups table"""
        self.table.setRowCount(0)
        groups = get_all_groups()
        
        from utils.date_utils import format_datetime_to_persian
        for idx, group in enumerate(groups):
            self.table.insertRow(idx)
            self.table.setRowHeight(idx, 48)
            
            # ID
            item_id = QTableWidgetItem(str(group[0]))
            item_id.setFlags(item_id.flags() & ~Qt.ItemIsEditable)
            item_id.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(idx, 0, item_id)
            
            # Name
            item_name = QTableWidgetItem(group[1])
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            item_name.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(idx, 1, item_name)
            
            # Leader (leader_name is at index 3 when using JOIN)
            leader_name = group[3] if len(group) > 3 and group[3] else "-"
            item_leader = QTableWidgetItem(str(leader_name))
            item_leader.setFlags(item_leader.flags() & ~Qt.ItemIsEditable)
            item_leader.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(idx, 2, item_leader)
            
            # Created date (formatted Persian)
            created = group[4] if len(group) > 4 and group[4] else "-"
            item_created = QTableWidgetItem(format_datetime_to_persian(created))
            item_created.setFlags(item_created.flags() & ~Qt.ItemIsEditable)
            item_created.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(idx, 3, item_created)

            # Actions cell with proper padding
            actions_cell = QWidget()
            actions_cell.setStyleSheet("background-color: transparent; padding: 0px; margin: 0px;")
            actions_layout = QHBoxLayout(actions_cell)
            actions_layout.setContentsMargins(6, 6, 6, 6)
            actions_layout.setSpacing(5)

            # View button
            btn_view = QPushButton("نمایش")
            btn_view.setCursor(Qt.PointingHandCursor)
            btn_view.setFixedSize(62, 36)
            btn_view.setStyleSheet(self.get_button_style('view'))
            btn_view.clicked.connect(lambda _, gid=group[0]: self.view_group(gid))

            # Edit button
            btn_edit = QPushButton("ویرایش")
            btn_edit.setCursor(Qt.PointingHandCursor)
            btn_edit.setFixedSize(62, 36)
            btn_edit.setStyleSheet(self.get_button_style('edit'))
            btn_edit.clicked.connect(lambda _, gid=group[0]: self.edit_group_by_id(gid))

            # Delete button
            btn_del = QPushButton("حذف")
            btn_del.setCursor(Qt.PointingHandCursor)
            btn_del.setFixedSize(58, 36)
            btn_del.setStyleSheet(self.get_button_style('delete'))
            btn_del.clicked.connect(lambda _, gid=group[0], gname=group[1]: self.delete_group_by_id(gid, gname))

            actions_layout.addWidget(btn_view)
            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_del)

            self.table.setCellWidget(idx, 4, actions_cell)
    
    def add_group(self):
        """Open dialog to add new group"""
        dialog = GroupDialog(self)
        dialog.group_saved.connect(self.on_group_saved)
        dialog.exec_()
    
    def edit_group_by_id(self, group_id):
        dialog = GroupDialog(self, group_id)
        dialog.group_saved.connect(self.on_group_saved)
        dialog.exec_()

    def delete_group_by_id(self, group_id, group_name=None):
        """Delete group by id (used by action button)"""
        if not group_name:
            group_name = str(group_id)
        msg = QMessageBox(self)
        msg.setWindowTitle("تایید حذف")
        msg.setText(f"آیا از حذف گروه '{group_name}' مطمئن هستید؟\n\nاین عملیات قابل بازگشت نیست!")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # set Persian text on buttons
        yes_btn = msg.button(QMessageBox.Yes)
        no_btn = msg.button(QMessageBox.No)
        if yes_btn:
            yes_btn.setText("بله")
        if no_btn:
            no_btn.setText("خیر")
        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            success, msg_text = delete_group(group_id)
            if success:
                QMessageBox.information(self, "موفق", msg_text)
                self.on_group_saved()
            else:
                QMessageBox.critical(self, "خطا", f"خطا: {msg_text}")
    
    def show_context_menu(self, position):
        """Show context menu on right-click"""
        menu = QMenu(self)
        
        edit_action = menu.addAction("✏️ ویرایش")
        delete_action = menu.addAction("🗑️ حذف")
        
        action = menu.exec_(self.table.mapToGlobal(position))
        
        if action == edit_action:
            current_row = self.table.currentRow()
            if current_row >= 0:
                gid = int(self.table.item(current_row, 0).text())
                self.edit_group_by_id(gid)
        elif action == delete_action:
            current_row = self.table.currentRow()
            if current_row >= 0:
                gid = int(self.table.item(current_row, 0).text())
                gname = self.table.item(current_row, 1).text()
                self.delete_group_by_id(gid, gname)
    
    def on_group_saved(self):
        """Called when group is saved, refresh data and notify main window"""
        self.refresh()
        if self.main_window and hasattr(self.main_window, 'refresh_all'):
            self.main_window.refresh_all()

    def view_group(self, group_id):
        from db.groups_db import get_group_by_id
        from utils.date_utils import format_datetime_to_persian
        group = get_group_by_id(group_id)
        if not group:
            QMessageBox.warning(self, "خطا", "گروه پیدا نشد!")
            return
        gid, name, leader_id, leader_name, created = group
        created_p = format_datetime_to_persian(created)
        info = f"نام گروه: {name}\nرهبر: {leader_name}\nتاریخ ایجاد: {created_p}"
        QMessageBox.information(self, "جزئیات گروه", info)
