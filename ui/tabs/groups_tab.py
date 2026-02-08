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
        self.table.setLayoutDirection(Qt.RightToLeft)  # Ensure RTL layout for table
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["🔢 شناسه", "🏷️ نام گروه", "👑 رهبر", "📅 تاریخ ایجاد", "⚡ عملیات"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(False)  # Disable alternating row colors for uniform appearance
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setLayoutDirection(Qt.RightToLeft)  # Ensure RTL for all content
        self.apply_table_styles()
        
        # Make table expandable to fill available space
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Setup column widths with better proportions
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        
        # Set fixed widths for ID and actions columns
        header.resizeSection(0, 100)  # ID column
        header.resizeSection(4, 120)  # Actions column (3 buttons * 32px + spacing)
        
        # Context menu
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.doubleClicked.connect(lambda idx: self.edit_group_by_id(int(self.table.item(idx.row(),0).text().split()[-1])))
        
        self.layout.addWidget(self.table, 1)  # Add stretch factor to table
        self.layout.addStretch(0)  # Remove extra stretch at bottom
        
        self.refresh()
    
    def apply_table_styles(self):
        """Apply beautiful theme-aware styles to table"""
        is_dark_mode = self.main_window and hasattr(self.main_window, 'current_theme') and self.main_window.current_theme == 'dark'
        
        if is_dark_mode:
            stylesheet = """
                QTableWidget {
                    background-color: #1e293b;
                    border: 2px solid #334155;
                    gridline-color: #334155;
                    selection-background-color: #3b82f6;
                }
                QTableWidget::item {
                    padding: 12px 8px;
                    margin: 2px;
                    border: none;
                    color: #e2e8f0;
                    background-color: #1e293b;
                    text-align: right;
                }
                QTableWidget::item:selected {
                    background-color: #3b82f6;
                    color: #ffffff;
                }
                QTableWidget::item:hover {
                    background-color: #334155;
                }
                QHeaderView::section {
                    background-color: #0f172a;
                    padding: 16px 12px;
                    border: none;
                    font-weight: 700;
                    font-size: 14px;
                    color: #f1f5f9;
                    border-bottom: 3px solid #3b82f6;
                    text-align: right;
                }
                QTableWidget QScrollBar:vertical {
                    background-color: #1e293b;
                    width: 12px;
                }
                QTableWidget QScrollBar::handle:vertical {
                    background-color: #475569;
                    min-height: 30px;
                }
                QTableWidget QScrollBar::handle:vertical:hover {
                    background-color: #64748b;
                }
            """
        else:
            stylesheet = """
                QTableWidget {
                    background-color: #ffffff;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                    gridline-color: #e2e8f0;
                    selection-background-color: #dbeafe;
                }
                QTableWidget::item {
                    padding: 12px 8px;
                    margin: 2px;
                    border: none;
                    border-radius: 6px;
                    color: #1e293b;
                    background-color: #ffffff;
                    text-align: right;
                }
                QTableWidget::item:selected {
                    background-color: #dbeafe;
                    color: #1e293b;
                    border-radius: 6px;
                    border: 1px solid #3b82f6;
                }
                QTableWidget::item:hover {
                    background-color: #f8fafc;
                    border-radius: 6px;
                }
                QHeaderView::section {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f8fafc, stop:1 #e2e8f0);
                    padding: 16px 12px;
                    border: none;
                    font-weight: 700;
                    font-size: 14px;
                    color: #1e293b;
                    border-bottom: 3px solid #3b82f6;
                    border-radius: 8px 8px 0 0;
                    text-align: right;
                }
                QTableWidget QScrollBar:vertical {
                    background-color: #f8fafc;
                    width: 12px;
                    border-radius: 6px;
                }
                QTableWidget QScrollBar::handle:vertical {
                    background-color: #cbd5e1;
                    border-radius: 6px;
                    min-height: 30px;
                }
                QTableWidget QScrollBar::handle:vertical:hover {
                    background-color: #94a3b8;
                }
            """
        
        self.table.setStyleSheet(stylesheet)
    
    def get_button_style(self, button_type='view'):
        """Get beautiful theme-aware button styles"""
        is_dark_mode = self.main_window and hasattr(self.main_window, 'current_theme') and self.main_window.current_theme == 'dark'
        
        if button_type == 'view':
            if is_dark_mode:
                return """
                    QPushButton {
                        background-color: #10b981;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 4px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #059669;
                    }
                    QPushButton:pressed {
                        background-color: #047857;
                    }
                """
            else:
                return """
                    QPushButton {
                        background-color: #10b981;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 4px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #059669;
                    }
                    QPushButton:pressed {
                        background-color: #047857;
                    }
                """
        
        elif button_type == 'edit':
            if is_dark_mode:
                return """
                    QPushButton {
                        background-color: #3b82f6;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 4px;
                        font-size: 16px;
                        font-weight: bold;
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
                        background-color: #3b82f6;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 4px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2563eb;
                    }
                    QPushButton:pressed {
                        background-color: #1e40af;
                    }
                """
        
        elif button_type == 'delete':
            if is_dark_mode:
                return """
                    QPushButton {
                        background-color: #ef4444;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 4px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #dc2626;
                    }
                    QPushButton:pressed {
                        background-color: #b91c1c;
                    }
                """
            else:
                return """
                    QPushButton {
                        background-color: #ef4444;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 4px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #dc2626;
                    }
                    QPushButton:pressed {
                        background-color: #b91c1c;
                    }
                """
        
        return ""
        
        return ""
    
    def refresh(self):
        """Refresh groups table with beautiful styling"""
        self.table.setRowCount(0)
        groups = get_all_groups()
        
        from utils.date_utils import format_datetime_to_persian
        for idx, group in enumerate(groups):
            self.table.insertRow(idx)
            self.table.setRowHeight(idx, 65)  # Increased row height for better button fit
            
            # ID with icon - RTL alignment for consistency
            item_id = QTableWidgetItem(f"🔢 {group[0]}")
            item_id.setFlags(item_id.flags() & ~Qt.ItemIsEditable)
            item_id.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # RTL alignment for consistency
            item_id.setToolTip("شناسه گروه")
            self.table.setItem(idx, 0, item_id)
            
            # Name with icon
            item_name = QTableWidgetItem(f"🏷️ {group[1]}")
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            item_name.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_name.setToolTip("نام گروه")
            self.table.setItem(idx, 1, item_name)
            
            # Leader with icon
            leader_name = group[3] if len(group) > 3 and group[3] else "بدون رهبر"
            leader_icon = "👑" if leader_name != "بدون رهبر" else "👤"
            item_leader = QTableWidgetItem(f"{leader_icon} {leader_name}")
            item_leader.setFlags(item_leader.flags() & ~Qt.ItemIsEditable)
            item_leader.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_leader.setToolTip("رهبر گروه")
            self.table.setItem(idx, 2, item_leader)
            
            # Created date with icon
            created = group[4] if len(group) > 4 and group[4] else "-"
            created_formatted = format_datetime_to_persian(created)
            item_created = QTableWidgetItem(f"📅 {created_formatted}")
            item_created.setFlags(item_created.flags() & ~Qt.ItemIsEditable)
            item_created.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_created.setToolTip("تاریخ ایجاد گروه")
            self.table.setItem(idx, 3, item_created)

            # Actions cell with proper padding and flexible layout
            actions_cell = QWidget()
            actions_cell.setStyleSheet("background-color: transparent; padding: 0px; margin: 0px;")
            actions_cell.setLayoutDirection(Qt.RightToLeft)  # Ensure RTL for buttons
            actions_layout = QHBoxLayout(actions_cell)
            actions_layout.setContentsMargins(2, 4, 2, 4)  # Reduced margins for better fit
            actions_layout.setSpacing(4)  # Reduced spacing
            actions_layout.setDirection(QHBoxLayout.RightToLeft)  # Explicit RTL direction

            # View button - make it more compact
            btn_view = QPushButton("👁️")
            btn_view.setCursor(Qt.PointingHandCursor)
            btn_view.setFixedSize(32, 32)  # Smaller, square buttons
            btn_view.setStyleSheet(self.get_button_style('view'))
            btn_view.setToolTip("نمایش گروه")
            btn_view.clicked.connect(lambda _, gid=group[0]: self.view_group(gid))

            # Edit button - make it more compact
            btn_edit = QPushButton("✏️")
            btn_edit.setCursor(Qt.PointingHandCursor)
            btn_edit.setFixedSize(32, 32)  # Smaller, square buttons
            btn_edit.setStyleSheet(self.get_button_style('edit'))
            btn_edit.setToolTip("ویرایش گروه")
            btn_edit.clicked.connect(lambda _, gid=group[0]: self.edit_group_by_id(gid))

            # Delete button - make it more compact
            btn_del = QPushButton("🗑️")
            btn_del.setCursor(Qt.PointingHandCursor)
            btn_del.setFixedSize(32, 32)  # Smaller, square buttons
            btn_del.setStyleSheet(self.get_button_style('delete'))
            btn_del.setToolTip("حذف گروه")
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
        """Open dialog to view group details"""
        dialog = GroupDialog(self, group_id, view_mode=True)
        dialog.exec_()
