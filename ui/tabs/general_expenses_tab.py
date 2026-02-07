# -*- coding: utf-8 -*-
from .base_tab import BaseTab


class GeneralExpensesTab(BaseTab):
    def __init__(self, main_window=None):
        super().__init__(main_window, "📄 مال و مصارف عمومی")
        self.layout.addWidget(self.create_button("+ ثبت مصرف جدید"))
        self.layout.addStretch()

    def refresh(self):
        pass
