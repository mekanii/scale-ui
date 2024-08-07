# Scale-UI Project

## Overview

Scale-UI is a graphical user interface (GUI) application designed to manage and interact with various devices, including scales, standards, and calibration tools. The application is built using Python and Tkinter, providing a user-friendly interface for managing device settings, performing measurements, and handling data.

## Features

- **Device Management**: Add, update, and delete device entries.
- **Scale Interaction**: Measure and retrieve stable weight data from connected scales.
- **Standard Management**: Manage part standards, including adding, updating, and deleting entries.
- **Calibration Tools**: Access and manage calibration settings.
- **Asynchronous Operations**: Perform network requests asynchronously to ensure a responsive UI.
- **Theming**: Consistent and modern UI design using Tkinter.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/mekanii/scale-ui.git
    cd scale-ui
    ```

2. **Install dependencies**:
    Ensure you have Python installed. Then, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

    Alternatively, you can use the provided `install.bat` script to install the dependencies on Windows:
    ```bash
    install.bat
    ```

3. **Run the application**:
    ```bash
    python main.py
    ```

## Usage

### Main Window

Upon launching the application, you will see the main window with a sidebar and a content area. The sidebar allows you to navigate between different sections of the application:

- **Scale**: Interact with connected scales to measure and retrieve weight data.
- **Standards**: Manage part standards, including adding, updating, and deleting entries.
- **Calibration**: Access and manage calibration settings.
- **Devices**: Manage device entries, including adding, updating, and deleting devices.
- **About**: View information about the application.

### Adding a New Device

1. Navigate to the **Devices** section.
2. Click the "Add Device" button.
3. Fill in the required details in the dialog that appears.
4. Click "Submit" to save the new device entry.

### Measuring Weight

1. Navigate to the **Scale** section.
2. Click the "Measure" button to retrieve the stable weight data from the connected scale.

### Managing Standards

1. Navigate to the **Standards** section.
2. Use the "Add Standard" button to add a new part standard.
3. Use the "Reload" button to refresh the list of standards.
4. Click on a standard entry to update or delete it.

## Configuration

The application uses a `config.json` file to store configuration settings, including the base API URL. Ensure this file is present in the root directory of the project.

Example `config.json`:


