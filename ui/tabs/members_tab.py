# -*- coding: utf-8 -*-
from .base_tab import BaseTab


class MembersTab(BaseTab):
    def __init__(self, main_window=None):
        super().__init__(main_window, "👤 مدیریت اعضا")
        self.layout.addWidget(self.create_button("+ افزودن عضو"))
        self.layout.addStretch()

    def refresh(self):
        pass
