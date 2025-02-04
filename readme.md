**Update:**
As of now, I have decided to pause this project. The latest Linux Mint already came out with something I need..lol

---

# Fluxxie: The Blue Light Filter

## Overview

Fluxxie is a Python-based application inspired by both Flux (f.lux) and my personal experience working at a home improvement store. Drawing on the need to provide better lighting control and reduce eye strain in a workspace, this app lets users adjust their screen's color temperature and brightness based on time of day or personal preference.

The concept of Fluxxie was born out of the experiences working at a home improvement store, being surrounded by all kinds of lighting environments. I learned how great the effect could be on comfort and productivity. Fluxxie takes this knowledge and puts it onto digital screens in such a way that it serves as a tool to regulate blue light exposure and enable the practice of healthier screen use behavior.

The app is a flexible and user-friendly tool that changes your screen's appearance based on the time of day, similar to F.lux. However, it also offers manual control over color temperature and brightness to fit individual preferences. This project is currently in **beta**, and new features and improvements are planned.

Unlike f.lux, this app is based on time; not latitude and longitude; however future updates might or might not include this. That time-based feature isn't fully tested so it might or might not even work. But in theory, it should.

## Features

- **Time-Based Adjustments**: This automatically adjusts the color temperature of your screen by the time of day: cooler colors during the day at 6500K and warm tones at night at 2700K.
- **Manual Color Temperature Control**: Allows users to manually adjust the color temperature of their screen using a slider, ranging from **2700K (warm)** to **6500K (cool)**. This feature is useful for customizing screen appearance based on the time or lighting in your environment.

- **Brightness Control**: Automatically adjusts screen brightness based on the color temperature, but users can manually tweak the brightness using a slider for further customization.

- **Select Monitor**: Choose to apply the filter on a single monitor or all connected monitors. Thus, it is great for multiple-monitor setups.

- **Night Mode**: A simple toggle which changes the color temperature to **2700K** for reduced blue light exposure and comfortable late-night usage.

- **Real-time Feedback**: Sliders indicate present values of color temperature and brightness for easy viewing of the changes made.
- **Cross-Platform**: At this moment, it is built for **Linux**, but work is on to support more platforms.
## Installation

1. **Clone the Repository**:

    ```bash
    git clone github.com/0xNullLight/Fluxxie--The-Blue-Light-Filter.git
    ```

2. **Install Dependencies**:

The app requires `PyQt5` for the GUI and `xrandr` for managing display settings. Install the necessary dependencies:

    ```bash
    pip install pyqt5
    sudo apt-get install x11-xserver-utils
    ```

3. **Run the Application**:

    To launch the app, run the following command:

    ```bash
    python fluxxie.py
    ```

How to Use

- **Manual Adjustments**: Employ the sliders to set Color Temperature and Brightness. The Temp can be changed from **2700K** (warm) to **6500K** (cool); Brightness will change on its own with the selected Temp but will also be manually adjustable.

- **Night Mode**: Click the button **Night Mode** to lock the color temperature at **2700K**, which means less blue light for creating a comfortable environment for the late night.

- **Time-Based Auto-Adjust**: You can enable the auto-adjust feature to let the application itself change the color temperature throughout the day. During the day, the screen will remain set to **6500K** (cooler), shifting to **2700K** when nighttime falls.

- **Monitor Selection**: You are able to select which monitor, if you have more than one in use, you would like to apply the settings or apply changes to all.

- **Reset**: Click the **Reset** button to reset the color temperature and brightness to their default states.

## How It Works

- **System Integration**: The application uses `xrandr` commands to set your display's color temperature and brightness. It will calculate, based on the time of day, the gamma setting and brightness to maintain in order to create comfortable reading.

- **Automatic Time Adjustments**: If the check box is checked, it will automatically adjust the color temperature of the screen based on system time: **6500K** for daytime and **2700K** for nighttime.

- **Manual Customization**: The users are in full control, as they can set both the color temperature and brightness as needed to achieve perfect conditions on the screen in a specific environment.

- **Cross-Platform**: Currently Linux-based, the application can be ported to other operating systems, enabling users to control their screen's light temperature across any platform.

## Contributing

As this is currently in **beta**, any feedback or contributions are greatly appreciated. Please feel free to fork the repository, create pull requests, or report bugs.

### Future Improvements

- **Cross-Platform Support**: Plans to expand to **Windows** and **macOS** using the appropriate system calls for display settings.

- **Advanced Customization**: In the future, new features could be added such as gradual color temperature transitions, support for external APIs to more precisely calibrate colors, or integration with desktop themes.

- **Mobile Application**: The ability to create a mobile version of Fluxxie exists for users who would like blue light filtering on their smartphones and tablets.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
### Notes:
- Make sure to fill in the URL in the **Clone the Repository** section with the actual URL from your GitHub repository.
- The section **Future Improvements** can be expanded when further features or updates are being planned.
