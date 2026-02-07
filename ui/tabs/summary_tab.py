# -*- coding: utf-8 -*-
from .base_tab import BaseTab


class SummaryTab(BaseTab):
    def __init__(self, main_window=None):
        super().__init__(main_window, "📈 خلاصه و داشبورد")
        self.layout.addWidget(self.create_button("🔄 به روز رسانی داده‌ها"))
        self.layout.addStretch()

    def refresh(self):
        pass
