# -*- coding: utf-8 -*-
"""
Dialog for adding/editing groups
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QComboBox)
from db.groups_db import group_exists, get_group_by_id


class GroupDialog(QDialog):
    """Dialog for add/edit group"""
    group_saved = pyqtSignal()
    
    def __init__(self, parent=None, group_id=None):
        super().__init__(parent)
        self.group_id = group_id
        self.setWindowTitle("افزودن گروه جدید" if not group_id else "ویرایش گروه")
        self.setGeometry(100, 100, 400, 250)
        self.setModal(True)
        self.setLayoutDirection(Qt.RightToLeft)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Group name
        lbl_name = QLabel("نام گروه:")
        lbl_name.setStyleSheet("font-weight: bold;")
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("نام گروه را وارد کنید...")
        self.txt_name.setMinimumHeight(36)
        layout.addWidget(lbl_name)
        layout.addWidget(self.txt_name)
        
        # Leader (optional)
        lbl_leader = QLabel("رهبر گروه (اختیاری):")
        lbl_leader.setStyleSheet("font-weight: bold;")
        self.combo_leader = QComboBox()
        self.combo_leader.setMinimumHeight(36)
        self.combo_leader.addItem("بدون رهبر", None)
        layout.addWidget(lbl_leader)
        layout.addWidget(self.combo_leader)
        # populate leaders from members table
        from db import fetch_all
        members = fetch_all("SELECT id, full_name FROM members ORDER BY full_name")
        for m in members:
            self.combo_leader.addItem(m[1], m[0])
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_save = QPushButton("💾 ذخیره")
        btn_save.setMinimumHeight(36)
        btn_save.clicked.connect(self.save_group)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        
        btn_cancel = QPushButton("❌ لغو")
        btn_cancel.setMinimumHeight(36)
        btn_cancel.clicked.connect(self.reject)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Load existing data if editing
        if group_id:
            self.load_group_data()
    
    def load_group_data(self):
        """Load group data for editing"""
        group = get_group_by_id(self.group_id)
        if group:
            self.txt_name.setText(group[1])  # name
            leader_id = group[2]
            # select leader in combo if present
            if leader_id:
                idx = self.combo_leader.findData(leader_id)
                if idx >= 0:
                    self.combo_leader.setCurrentIndex(idx)
    
    def save_group(self):
        """Save group to database"""
        name = self.txt_name.text().strip()
        
        if not name:
            QMessageBox.warning(self, "خطا", "نام گروه نمی‌تواند خالی باشد!")
            return
        
        # Check for duplicates
        if not self.group_id and group_exists(name):
            QMessageBox.warning(self, "خطا", "گروهی با این نام قبلاً وجود دارد!")
            return
        
        if self.group_id and group_exists(name, self.group_id):
            QMessageBox.warning(self, "خطا", "گروهی دیگر با این نام وجود دارد!")
            return
        
        leader_id = self.combo_leader.currentData()
        
        # Import here to avoid circular imports
        from db.groups_db import add_group, update_group
        
        if self.group_id:
            success, msg = update_group(self.group_id, name, leader_id)
        else:
            success, msg = add_group(name, leader_id)
        
        if success:
            QMessageBox.information(self, "موفق", 
                "گروه جدید با موفقیت ایجاد شد!" if not self.group_id 
                else "گروه با موفقیت بروز شد!")
            self.group_saved.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "خطا", f"خطا: {msg}")
