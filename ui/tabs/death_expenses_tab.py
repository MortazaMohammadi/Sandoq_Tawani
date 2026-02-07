# -*- coding: utf-8 -*-
from .base_tab import BaseTab


class DeathExpensesTab(BaseTab):
    def __init__(self, main_window=None):
        super().__init__(main_window, "⚰️ مصارف فوتی")
        self.layout.addWidget(self.create_button("+ ثبت مصرف فوتی"))
        self.layout.addStretch()

    def refresh(self):
        pass
