from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout


class QInformation(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QHBoxLayout()
        layout_gold = QHBoxLayout()
        layout_food = QHBoxLayout()
        layout_rock = QHBoxLayout()

        info_gold = QLabel("Gold:")
        self.data_gold = QLabel("0")
        layout_gold.addWidget(info_gold)
        layout_gold.addWidget(self.data_gold)
        layout_gold.addStretch()
        layout.addLayout(layout_gold)

        info_food = QLabel("Food:")
        self.data_food = QLabel("0")
        layout_food.addWidget(info_food)
        layout_food.addWidget(self.data_food)
        layout_food.addStretch()
        layout.addLayout(layout_food)

        info_rock = QLabel("Rock:")
        self.data_rock = QLabel("0")
        layout_rock.addWidget(info_rock)
        layout_rock.addWidget(self.data_rock)
        layout_rock.addStretch()
        layout.addLayout(layout_rock)

        layout.addStretch()
        self.setLayout(layout)

    def gold(self, value):
        self.data_gold.setText(str(value))

    def food(self, value):
        self.data_food.setText(str(value))

    def rock(self, value):
        self.data_rock.setText(str(value))
