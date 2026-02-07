# -*- coding: utf-8 -*-
from .base_tab import BaseTab


class GroupsTab(BaseTab):
    def __init__(self, main_window=None):
        super().__init__(main_window, "👥 مدیریت گروه‌ها")
        self.layout.addWidget(self.create_button("+ افزودن گروه"))
        self.layout.addStretch()

    def refresh(self):
        pass
