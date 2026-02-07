# -*- coding: utf-8 -*-
from .base_tab import BaseTab


class CollectedMoneyTab(BaseTab):
    def __init__(self, main_window=None):
        super().__init__(main_window, "💵 ثبت پول جمع‌آوری‌شده")
        self.layout.addWidget(self.create_button("+ ثبت پول جدید"))
        self.layout.addStretch()

    def refresh(self):
        pass
