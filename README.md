# ProTemp IOT

## Overview
ProTemp IOT is an industrial-grade IoT system designed for monitoring cold chain storage facilities. It ensures the safety and integrity of sensitive goods such as vaccines and food products by providing real-time monitoring of temperature, humidity, and power consumption. The system enforces strict safety protocols and triggers automated alarms and backup systems in case of critical failures.

## Features
- **Real-time Monitoring**: Tracks temperature and humidity across multiple zones (Vaccine Unit, Food Unit, Warehouse Ambient).
- **Power Management**: Monitors main power consumption and manages backup cooling systems.
- **Automated Alerts**: Triggers audio and visual alarms for temperature breaches (e.g., thaw risk, freezing risk).
- **Backup Control**: Automatically activates backup coolers when critical thresholds are exceeded.
- **Data Logging**: Persists all sensor data and alarm events to a local SQLite database for audit trails.
- **Industrial GUI**: A robust dashboard for visualizing system status and managing connections.

## Project Structure
- `gui.py`: The main control dashboard built with PyQt5.
- `manager.py`: The central logic unit that processes sensor data and enforces safety rules.
- `emulator.py`: Simulates industrial IoT devices (Freezers, Sensors, Meters).
- `agent.py`: Core MQTT communication module.
- `data_acq.py`: Database management module using SQLite.

## Installation
1. Clone the repository.
2. Install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To start the entire system (Emulators, Manager, and GUI), run the included Python launcher:

```bash
python start_system.py
```

Alternatively, you can run the batch file on Windows:
```bash
run_system.bat
```

## Configuration
- **MQTT Broker**: Configured in `init.py`.
- **Database**: Data is stored in `data/warehouse.db`.
