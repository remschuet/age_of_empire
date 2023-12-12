from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

class QInformation(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Dictionnaire pour stocker les données
        self.data_dict = {
            'gold': {'label': QLabel("Gold:"), 'value': QLabel("0")},
            'food': {'label': QLabel("Food:"), 'value': QLabel("0")},
            'rock': {'label': QLabel("Rock:"), 'value': QLabel("0")},
            'wood': {'label': QLabel("Wood:"), 'value': QLabel("0")}
        }

        layout = QHBoxLayout()

        for resource, widgets in self.data_dict.items():
            resource_layout = QHBoxLayout()
            resource_layout.addWidget(widgets['label'])
            resource_layout.addWidget(widgets['value'])
            resource_layout.addStretch()
            layout.addLayout(resource_layout)

        layout.addStretch()
        self.setLayout(layout)

    def set_resource(self, resource_values: dict):
        for resource in resource_values.keys():
            if resource in self.data_dict:
                self.data_dict[resource]['value'].setText(str(resource_values[resource]))
