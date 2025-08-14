from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
import sys


class UnitConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engineering Unit Converter")
        self.setGeometry(300, 200, 400, 200) #(x_position, y_position, width, height)
 
        self.setStyleSheet("""
            QWidget {
                background-color: #ECEFF1; /* light grey-blue */
                font-family: Arial;
                font-size: 14px;
            }
            QComboBox, QLineEdit, QPushButton {
                padding: 6px;
                border-radius: 5px;
                border: 1px solid #B0BEC5;
            }
            QPushButton {
                background-color: #00BCD4; /* light blue */
                color: black;
                font-weight: bold;
            }
            QPushButton:hover {
                color: white;
                background-color: #0097A7;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #263238; /* deep grey */
            }
        """)


        # Dropdown for category
        self.category_box = QComboBox()
        self.category_box.addItems(["Length", 
                                    "Temperature", 
                                    "Pressure", 
                                    "Area", 
                                    "Volume", 
                                    "Weight", 
                                    "Mass", 
                                    "Velocity", 
                                    "Volumetric Flow Rate",
                                    "Mass Flow Rate",
                                    "Power",
                                    "Energy"])
        self.category_box.currentTextChanged.connect(self.update_units)

        # Unit selectors
        self.from_unit_box = QComboBox()
        self.to_unit_box = QComboBox()

        # Input value
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter value")

        # Switch button
        self.switch_btn = QPushButton()  # Simple arrow icon
        self.switch_btn.setFixedWidth(37)
        self.switch_btn.setIcon(QIcon("switch.png"))  # Path to your PNG file
        self.switch_btn.setIconSize(QSize(20, 20))    # Adjust icon size
        self.switch_btn.clicked.connect(self.switch_units)

        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert_units)

        # Output label
        self.result_label = QLabel("Result: -")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Category:"))
        top_layout.addWidget(self.category_box)

        unit_layout = QHBoxLayout()
        unit_layout.addWidget(self.from_unit_box)
        unit_layout.addWidget(self.switch_btn)
        unit_layout.addWidget(self.to_unit_box)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.input_field)
        main_layout.addLayout(unit_layout)
        main_layout.addWidget(self.convert_btn)
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

        # Initialize with first category
        self.update_units()

    def update_units(self):
        category = self.category_box.currentText()
        units = {
            "Length": ["m (SI)", "cm", "mm", "km", "inch", "ft", "mile", "yard"],
            "Temperature": ["K (SI)", "°C", "°F"],
            "Pressure": ["Pa (SI)", "kPa", "bar", "psi", "atm", "mmHg (Torr)", "mmH₂O", "inHg", "kg/cm²"],
            "Area": ["m² (SI)", "cm²", "mm²", "ft²", "in²", "hectare"],
            "Volume": ["m³ (SI)", "cm³", "mm³", "km³", "L", "mL", "ft³", "in³", "gal"],
            "Weight": ["N (SI)", "kgf", "lbf"],
            "Mass": ["kg (SI)", "g", "mg", "t", "lb", "oz"],
            "Velocity": ["m/s (SI)", "km/h", "mph", "ft/s", "in/s"],
            "Volumetric Flow Rate": ["m³/s (SI)", "L/min", "ft³/s", "gal/min"],
            "Mass Flow Rate": ["kg/s (SI)", "g/s", "lb/s", "t/h"],
            "Power": ["W (SI)", "kW", "hp", "BTU/h", "cal/s"],
            "Energy": ["J (SI)", "kJ", "cal", "kcal", "Wh", "kWh", "BTU"]
        }

        self.from_unit_box.clear()
        self.to_unit_box.clear()
        self.from_unit_box.addItems(units[category])
        self.to_unit_box.addItems(units[category])

    def convert_units(self):
        try:
            value = float(self.input_field.text())
        except ValueError:
            self.result_label.setText("Invalid number")
            return

        from_unit = self.from_unit_box.currentText()
        to_unit = self.to_unit_box.currentText()
        category = self.category_box.currentText()

        result = self.do_conversion(value, from_unit, to_unit, category)
        self.result_label.setText(f"Result: {result:.4f} {to_unit}")

    def switch_units(self):
        # Swap the selected units
        from_index = self.from_unit_box.currentIndex()
        to_index = self.to_unit_box.currentIndex()

        self.from_unit_box.setCurrentIndex(to_index)
        self.to_unit_box.setCurrentIndex(from_index)

    def do_conversion(self, value, from_unit, to_unit, category):
        if category == "Length":
            factors = {
                "m (SI)": 1,
                "cm": 0.01,
                "mm": 0.001,
                "km": 1000,
                "inch": 0.0254,
                "ft": 0.3048,
                "mile": 1609.344,
                "yard": 0.9144
            }
            return value * factors[from_unit] / factors[to_unit]

        elif category == "Temperature":
            if from_unit == "C":
                if to_unit == "F": return (value * 9/5) + 32
                if to_unit == "K (SI)": return value + 273.15
            elif from_unit == "F":
                if to_unit == "C": return (value - 32) * 5/9
                if to_unit == "K (SI)": return (value - 32) * 5/9 + 273.15
            elif from_unit == "K (SI)":
                if to_unit == "C": return value - 273.15
                if to_unit == "F": return (value - 273.15) * 9/5 + 32
            return value

        elif category == "Pressure":
            factors = {
                "Pa (SI)": 1,
                "kPa": 1000,
                "bar": 100000,
                "psi": 6894.757,
                "atm": 101325,
                "mmHg(Torr)": 133.322,
                "mmH20": 9.80665,
                "inHg": 3386.389,
                "kg/cm2": 98066.5
            }
            return value * factors[from_unit] / factors[to_unit]
        
        elif category == "Area":
            factors = {
                "m2 (SI)": 1,
                "cm2": 0.0001,
                "mm2": 0.000001,
                "ft2": 0.092903,
                "in2": 0.00064516,
                "hectare": 10000
            }
            return value * factors[from_unit] / factors[to_unit]
        
        elif category == "Volume":
            factors = {
                "m3 (SI)": 1,
                "cm3": 0.000001,
                "mm3": 0.000000001,
                "km3": 1000000000,
                "l": 0.001,
                "ml": 0.000001,
                "ft3": 0.0283168,
                "in3": 0.0000163871,
                "gal": 0.00378541
            }
            return value * factors[from_unit] / factors[to_unit]
        
        elif category == "Weight":
            factors = {
                "kgf": 9.80665,
                "lbf": 4.44822,
                "N (SI)": 1
            }
            return value * factors[from_unit] / factors[to_unit]
        
        elif category == "Mass":
            factors = {
                "kg (SI)": 1,
                "g": 0.001,
                "mg": 0.000001,
                "t": 1000,
                "lb": 0.453592,
                "oz": 0.0283495
            }
            return value * factors[from_unit] / factors[to_unit]
        
        elif category == "Velocity":
            factors = {
                "m/s (SI)": 1,
                "km/h": 0.277778,
                "mph": 0.44704,
                "ft/s": 0.3048,
                "in/s": 0.0254
            }
            return value * factors[from_unit] / factors[to_unit]
        
        elif category == "Volumetric Flow Rate":
            factors = {
                "m3/s (SI)": 1,
                "L/min": 0.001 / 60,
                "ft3/s": 0.0283168,
                "gal/min": 0.00378541 / 60
            }
            return value * factors[from_unit] / factors[to_unit]
            
        elif category == "Mass Flow Rate":
            factors = {
                "kg/s (SI)": 1,
                "g/s": 0.001,
                "lb/s": 0.453592,
                "t/h": 0.277778
            }
            return value * factors[from_unit] / factors[to_unit]
            
        elif category == "Power":
            factors = {
                "W (SI)": 1,
                "kW": 1000,
                "hp": 745.7,
                "BTU/h": 0.293071,
                "cal/s": 4.184,
                "kcal/s": 4184
            }
            return value * factors[from_unit] / factors[to_unit]
            
        elif category == "Energy":
            factors = {
                "J (SI)": 1,
                "kJ": 1000,
                "cal": 4.184,
                "kcal": 4184,
                "Wh": 3600,
                "kWh": 3600000,
                "BTU": 1055.06
            }
            return value * factors[from_unit] / factors[to_unit]

        return value


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnitConverter()
    window.setWindowIcon(QIcon("icon.ico"))  # Set your icon path here
    window.show()
    sys.exit(app.exec())
