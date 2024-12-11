import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSlider, QPushButton, QLabel, QWidget, QComboBox, QCheckBox
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime

class Fluxxie(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Blue Light Filter (Flux-inspired)")
        self.setGeometry(100, 100, 400, 350)

        # Default values
        self.default_temp = 4500  # Default color temperature (K)
        self.default_brightness = 100  # Default brightness (percentage)
        self.current_temp = self.default_temp  # Current color temperature
        self.current_brightness = self.default_brightness  # Current brightness
        
        self.auto_adjust_enabled = True  # Auto adjust flag

        # Layout
        layout = QVBoxLayout()

        # Label for selecting monitor
        self.label_monitor = QLabel("Select Monitor(s)", self)
        layout.addWidget(self.label_monitor)

        # ComboBox for selecting specific monitor or all monitors
        self.monitor_combobox = QComboBox(self)
        self.monitor_combobox.addItem("All Monitors")
        self.monitor_combobox.addItems(self.get_available_monitors())
        layout.addWidget(self.monitor_combobox)

        # Label for color temperature slider
        self.label_temp = QLabel("Adjust Color Temperature (K)", self)
        layout.addWidget(self.label_temp)

        # Slider for color temperature adjustment
        self.slider_temp = QSlider(Qt.Horizontal, self)
        self.slider_temp.setMinimum(2700)  # Min color temperature (warm)
        self.slider_temp.setMaximum(6500)  # Max color temperature (cool)
        self.slider_temp.setValue(self.default_temp)  # Default value (neutral)
        self.slider_temp.setTickInterval(500)
        self.slider_temp.setSingleStep(100)
        self.slider_temp.valueChanged.connect(self.set_color_temperature)
        layout.addWidget(self.slider_temp)

        # Label to show the current color temperature value
        self.temp_value_label = QLabel(f"Current Value: {self.default_temp} K", self)
        layout.addWidget(self.temp_value_label)

        # Label for brightness slider
        self.label_brightness = QLabel("Adjust Brightness", self)
        layout.addWidget(self.label_brightness)

        # Slider for brightness adjustment
        self.slider_brightness = QSlider(Qt.Horizontal, self)
        self.slider_brightness.setMinimum(10)  # Min brightness (10%)
        self.slider_brightness.setMaximum(100)  # Max brightness (100%)
        self.slider_brightness.setValue(self.default_brightness)  # Default brightness (100%)
        self.slider_brightness.setTickInterval(10)
        self.slider_brightness.setSingleStep(5)
        self.slider_brightness.valueChanged.connect(self.set_brightness)
        layout.addWidget(self.slider_brightness)

        # Label to show the current brightness value
        self.brightness_value_label = QLabel(f"Current Value: {self.default_brightness}%", self)
        layout.addWidget(self.brightness_value_label)

        # Button to reset settings
        self.reset_button = QPushButton("Reset Settings", self)
        self.reset_button.clicked.connect(self.reset_settings)
        layout.addWidget(self.reset_button)

        # Button to simulate Night Mode (simulating fluxgui behavior)
        self.night_mode_button = QPushButton("Night Mode", self)
        self.night_mode_button.clicked.connect(self.set_night_mode)
        layout.addWidget(self.night_mode_button)

        # Checkbox to enable/disable time-based adjustments
        self.auto_adjust_checkbox = QCheckBox("Enable Time-Based Adjustments", self)
        self.auto_adjust_checkbox.setChecked(self.auto_adjust_enabled)
        self.auto_adjust_checkbox.stateChanged.connect(self.toggle_auto_adjust)
        layout.addWidget(self.auto_adjust_checkbox)

        self.setLayout(layout)

        # Start timer to check system time every minute (60000ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_adjust_time)
        self.timer.start(60000)  # Check every minute

        # Adjust immediately based on current time
        self.auto_adjust_time()

    def get_available_monitors(self):
        """
        Get the list of available monitors using xrandr.
        This will include HDMI-connected monitors as well.
        """
        result = subprocess.run("xrandr --verbose", shell=True, capture_output=True, text=True)
        lines = result.stdout.split("\n")
        monitors = []
        for line in lines:
            # Look for connected monitors and extract their names
            if " connected" in line:
                monitor_name = line.split()[0]
                monitors.append(monitor_name)
        return monitors

    def set_color_temperature(self, value):
        """
        Adjust the color temperature using xrandr.
        """
        # Update the label with the current value
        self.temp_value_label.setText(f"Current Value: {value} K")

        # Store the current color temperature
        self.current_temp = value

        # Calculate brightness multiplier based on color temperature
        brightness_multiplier = self.calculate_brightness_multiplier(value)

        # Adjust the brightness based on the calculated multiplier
        new_brightness = int(self.default_brightness * brightness_multiplier)
        self.slider_brightness.setValue(new_brightness)

        # Get selected monitor(s)
        selected_monitor = self.monitor_combobox.currentText()

        # Convert color temperature to RGB values using a simplified approach
        red = min(1.0, max(0.0, (value - 2700) / 3800.0))  # Warmer values increase red
        green = min(1.0, max(0.0, (value - 2700) / 3800.0))  # Neutral green value
        blue = min(1.0, max(0.0, (6500 - value) / 3800.0))  # Cooler values increase blue

        if selected_monitor == "All Monitors":
            # Apply to all monitors
            monitors = self.get_available_monitors()
            for monitor in monitors:
                command = f"xrandr --output {monitor} --gamma {red}:{green}:{blue} --brightness {new_brightness / 100.0}"
                subprocess.run(command, shell=True)
        else:
            # Apply to selected monitor only
            command = f"xrandr --output {selected_monitor} --gamma {red}:{green}:{blue} --brightness {new_brightness / 100.0}"
            subprocess.run(command, shell=True)

    def calculate_brightness_multiplier(self, temp_value):
        """
        Calculate a brightness multiplier based on the color temperature.
        Warmer color temperatures (2700K) have lower brightness, cooler temperatures (6500K) have higher brightness.
        """
        if temp_value <= 3000:
            return 0.7  # Low brightness for warm temperatures
        elif temp_value <= 4500:
            return 0.8  # Medium brightness for neutral temperatures
        elif temp_value <= 6000:
            return 1.0  # Normal brightness for cool temperatures
        else:
            return 1.1  # High brightness for very cool temperatures

    def set_brightness(self, value):
        """
        Adjust screen brightness using xrandr.
        This method should no longer be used independently; it works in sync with color temperature.
        """
        # Update the label with the current value
        self.brightness_value_label.setText(f"Current Value: {value}%")

        # Store the current brightness
        self.current_brightness = value

        # Get selected monitor(s)
        selected_monitor = self.monitor_combobox.currentText()

        brightness = value / 100.0

        if selected_monitor == "All Monitors":
            # Apply to all monitors
            monitors = self.get_available_monitors()
            for monitor in monitors:
                command = f"xrandr --output {monitor} --brightness {brightness}"
                subprocess.run(command, shell=True)
        else:
            # Apply to selected monitor only
            command = f"xrandr --output {selected_monitor} --brightness {brightness}"
            subprocess.run(command, shell=True)

    def reset_settings(self):
        """
        Reset to default screen settings and reflect it on the sliders.
        """
        # Get selected monitor(s)
        selected_monitor = self.monitor_combobox.currentText()

        # Reset to default settings (gamma and brightness)
        if selected_monitor == "All Monitors":
            # Apply reset to all monitors
            monitors = self.get_available_monitors()
            for monitor in monitors:
                # Reset gamma and brightness to default values
                subprocess.run(f"xrandr --output {monitor} --gamma 1:1:1 --brightness 1", shell=True)
        else:
            # Apply reset to selected monitor only
            subprocess.run(f"xrandr --output {selected_monitor} --gamma 1:1:1 --brightness 1", shell=True)

        # Reset sliders and labels
        self.slider_temp.setValue(self.default_temp)
        self.slider_brightness.setValue(self.default_brightness)
        self.temp_value_label.setText(f"Current Value: {self.default_temp} K")
        self.brightness_value_label.setText(f"Current Value: {self.default_brightness}%")

    def set_night_mode(self):
        """
        Set the color temperature to night mode (2700K) for a warm screen.
        """
        self.set_color_temperature(2700)

    def toggle_auto_adjust(self, state):
        """
        Toggle auto adjustment based on time.
        """
        self.auto_adjust_enabled = state == Qt.Checked
        self.auto_adjust_time()

    def auto_adjust_time(self):
        """
        Adjust the color temperature based on the time of day.
        """
        if not self.auto_adjust_enabled:
            return  # Do nothing if auto-adjust is off
        
        # Get the current time
        current_time = datetime.now().time()

        # Define time-based color temperature ranges
        # Daytime: Cool colors (6500K), Nighttime: Warm colors (2700K)
        if 7 <= current_time.hour < 19:
            # Daytime: Set to cool (6500K)
            self.set_color_temperature(6500)
        else:
            # Nighttime: Set to warm (2700K)
            self.set_color_temperature(2700)

# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Fluxxie()
    window.show()
    sys.exit(app.exec_())
