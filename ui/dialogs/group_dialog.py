# -*- coding: utf-8 -*-
"""
Dialog for adding/editing groups
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QComboBox,
                             QFrame, QGroupBox)
from db.groups_db import group_exists, get_group_by_id


class GroupDialog(QDialog):
    """Dialog for add/edit/view group"""
    group_saved = pyqtSignal()
    
    def __init__(self, parent=None, group_id=None, view_mode=False):
        super().__init__(parent)
        self.group_id = group_id
        self.view_mode = view_mode
        
        if view_mode:
            self.setWindowTitle("مشاهده گروه")
        elif group_id:
            self.setWindowTitle("ویرایش گروه")
        else:
            self.setWindowTitle("افزودن گروه جدید")
            
        self.setGeometry(100, 100, 500, 350)
        self.setModal(True)
        self.setLayoutDirection(Qt.RightToLeft)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        if self.view_mode:
            self.setup_view_mode(layout)
        else:
            self.setup_edit_mode(layout)
        
        # Load existing data if editing or viewing
        if group_id:
            self.load_group_data()
    
    def setup_view_mode(self, layout):
        """Setup beautiful view mode layout"""
        # Title
        title_label = QLabel("📋 جزئیات گروه")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2563eb;
            margin-bottom: 10px;
        """)
        layout.addWidget(title_label)
        
        # Info container
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.StyledPanel)
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(15)
        
        # Group ID
        self.lbl_id = QLabel()
        self.lbl_id.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            padding: 8px 12px;
            background-color: #e2e8f0;
            border-radius: 6px;
        """)
        info_layout.addWidget(self.lbl_id)
        
        # Group Name
        self.lbl_name = QLabel()
        self.lbl_name.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1e293b;
            padding: 10px 15px;
            background-color: #ffffff;
            border: 2px solid #cbd5e1;
            border-radius: 8px;
        """)
        info_layout.addWidget(self.lbl_name)
        
        # Leader
        self.lbl_leader = QLabel()
        self.lbl_leader.setStyleSheet("""
            font-size: 14px;
            color: #374151;
            padding: 10px 15px;
            background-color: #ffffff;
            border: 2px solid #cbd5e1;
            border-radius: 8px;
        """)
        info_layout.addWidget(self.lbl_leader)
        
        # Created Date
        self.lbl_created = QLabel()
        self.lbl_created.setStyleSheet("""
            font-size: 14px;
            color: #374151;
            padding: 10px 15px;
            background-color: #ffffff;
            border: 2px solid #cbd5e1;
            border-radius: 8px;
        """)
        info_layout.addWidget(self.lbl_created)
        
        layout.addWidget(info_frame)
        
        # Close button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_close = QPushButton("✖️ بستن")
        btn_close.setMinimumHeight(40)
        btn_close.setMinimumWidth(120)
        btn_close.clicked.connect(self.accept)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)
    
    def setup_edit_mode(self, layout):
        """Setup edit mode layout"""
        # Group name
        lbl_name = QLabel("نام گروه:")
        lbl_name.setStyleSheet("font-weight: bold; font-size: 14px; color: #374151;")
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("نام گروه را وارد کنید...")
        self.txt_name.setMinimumHeight(40)
        self.txt_name.setStyleSheet("""
            QLineEdit {
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #2563eb;
            }
        """)
        layout.addWidget(lbl_name)
        layout.addWidget(self.txt_name)
        
        # Leader (optional)
        lbl_leader = QLabel("رهبر گروه (اختیاری):")
        lbl_leader.setStyleSheet("font-weight: bold; font-size: 14px; color: #374151;")
        self.combo_leader = QComboBox()
        self.combo_leader.setMinimumHeight(40)
        self.combo_leader.addItem("بدون رهبر", None)
        self.combo_leader.setStyleSheet("""
            QComboBox {
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QComboBox:focus {
                border-color: #2563eb;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        layout.addWidget(lbl_leader)
        layout.addWidget(self.combo_leader)
        
        # populate leaders from members table
        from db import fetch_all
        members = fetch_all("SELECT id, full_name FROM members ORDER BY full_name")
        for m in members:
            self.combo_leader.addItem(m[1], m[0])
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        btn_save = QPushButton("💾 ذخیره")
        btn_save.setMinimumHeight(40)
        btn_save.setMinimumWidth(120)
        btn_save.clicked.connect(self.save_group)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        
        btn_cancel = QPushButton("❌ لغو")
        btn_cancel.setMinimumHeight(40)
        btn_cancel.setMinimumWidth(120)
        btn_cancel.clicked.connect(self.reject)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addStretch()
        layout.addLayout(btn_layout)
    
    def load_group_data(self):
        """Load group data for editing or viewing"""
        from utils.date_utils import format_datetime_to_persian
        
        group = get_group_by_id(self.group_id)
        if group:
            gid, name, leader_id, leader_name, created = group
            
            if self.view_mode:
                # Format data for view mode
                created_p = format_datetime_to_persian(created)
                leader_display = leader_name if leader_name != '-' else "بدون رهبر"
                
                self.lbl_id.setText(f"🔢 شناسه گروه: {gid}")
                self.lbl_name.setText(f"🏷️ نام گروه: {name}")
                self.lbl_leader.setText(f"👑 رهبر گروه: {leader_display}")
                self.lbl_created.setText(f"📅 تاریخ ایجاد: {created_p}")
            else:
                # Load data for edit mode
                self.txt_name.setText(name)
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
