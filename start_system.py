import subprocess
import time
import sys
import os

def run_command(command, title):
    print(f"Starting {title}...")
    subprocess.Popen(f'start "{title}" {command}', shell=True)

if __name__ == "__main__":
    # Emulators
    run_command("python emulator.py Vaccine_Unit Celsius Warehouse_Zone_A 7", "Emulator: Vaccine_Unit")
    time.sleep(1)
    run_command("python emulator.py Food_Unit Celsius Warehouse_Zone_B 11", "Emulator: Food_Unit")
    time.sleep(1)
    run_command("python emulator.py Warehouse_Ambient Celsius Warehouse_Main 13", "Emulator: Warehouse_Ambient")
    time.sleep(1)
    run_command("python emulator.py Backup_Cooler Celsius Warehouse_Backup 5", "Emulator: Backup_Cooler")
    time.sleep(1)
    run_command("python emulator.py Main_Power kWh Power_Station 6", "Emulator: Main_Power")
    time.sleep(1)

    # Manager
    run_command("python manager.py", "ProTemp IOT Manager")
    time.sleep(2)

    # GUI
    run_command("python gui.py", "ProTemp IOT GUI")

    print("System started successfully.")
