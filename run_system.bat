REM arg: Name Units Place UpdateTime

start "Emulator: Vaccine_Unit" python emulator.py Vaccine_Unit Celsius Warehouse_Zone_A 7
timeout 2
start "Emulator: Food_Unit" python emulator.py Food_Unit Celsius Warehouse_Zone_B 11
timeout 2
start "Emulator: Warehouse_Ambient" python emulator.py Warehouse_Ambient Celsius Warehouse_Main 13
timeout 2
start "Emulator: Backup_Cooler" python emulator.py Backup_Cooler Celsius Warehouse_Backup 5
timeout 2
start "Emulator: Main_Power" python emulator.py Main_Power kWh Power_Station 6
timeout 2
start "ProTemp IOT Manager" python manager.py
timeout 5
start "ProTemp IOT GUI" python gui.py
