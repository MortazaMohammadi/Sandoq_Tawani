# -*- coding: utf-8 -*-
from .base_tab import BaseTab


class LoansTab(BaseTab):
    def __init__(self, main_window=None):
        super().__init__(main_window, "📝 مدیریت قرض‌ها")
        self.layout.addWidget(self.create_button("+ ثبت قرض جدید"))
        self.layout.addStretch()

    def refresh(self):
        pass
