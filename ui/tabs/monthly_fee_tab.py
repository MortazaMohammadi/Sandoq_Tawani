# -*- coding: utf-8 -*-
from .base_tab import BaseTab


class MonthlyFeeTab(BaseTab):
    def __init__(self, main_window=None):
        super().__init__(main_window, "💰 تعیین هزینه ماهیانه")
        self.layout.addWidget(self.create_button("📋 تعیین مبلغ ماهیانه"))
        self.layout.addStretch()

    def refresh(self):
        pass
