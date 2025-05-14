🧊 Smart Temp Tool (GUI Version for macOS)

The Smart Temp Tool is a Python-based GUI application that simulates and visualizes liquid temperature changes in a smart bottle or thermal environment. Users can load data, simulate heating/cooling time, and receive dynamic battery and power-saving feedback.

⸻

🚀 Features
	•	Load and validate structured data files (.csv, .xlsx, .json)
	•	Simulate temperature change visually with progress bars
	•	Real-time feedback on:
	•	Time to target temperature
	•	Power usage and battery level
	•	Overheating or freezing alerts
	•	Power-saving tips
	•	Export results to CSV or PDF
	•	Optional filters for drink type and max time
	•	Toggle between Celsius and Fahrenheit display

⸻

💻 Setup (macOS Only)

1. Requirements
	•	Python 3.10 or later must be installed
To check your version, run in Terminal:
python3 --version

https://www.python.org/downloads/mac-osx/


⸻

2. First-Time Setup (macOS Gatekeeper)

macOS may block the app when double-clicking due to security settings.

✅ Fix (One-Time Only):

Open Terminal and run:
xattr -d com.apple.quarantine ~/Downloads/MACsmart_temp_tool/gui_version/Start_Smart_Temp.command

If you moved the folder elsewhere (e.g. Documents), update the path accordingly.


⸻

3. Launch the App

After running the command above:
	•	Open the gui_version/ folder
	•	Double-click Start_Smart_Temp.command

This will:
	•	Automatically create a Python virtual environment
	•	Install required packages:
	•	pandas
	•	openpyxl
	•	reportlab
	•	Launch the GUI

No Terminal usage or admin access is required after the Gatekeeper step.


⸻

📂 Input File Format

Your data must include these columns:
	•	Liquid Type
	•	Initial Temperature
	•	Desired Temperature
	•	Ambient Temperature
	•	Time to Target
	•	Battery Level
	•	User Preference

🧪 Sample files are provided inside the sample_data/ folder.


⸻

📝 Notes
	•	Tested on macOS Monterey and newer with Python 3.10+
	•	Supports: .csv, .xlsx, .json
	•	For additional formats, the code must be modified by the author or a developer

⚠️ Disclaimer

This tool uses placeholder formulas and simulated values for educational and demonstration purposes only.
It is not intended for real-world product testing or safety-critical use.

You’re welcome to use or share this tool for personal projects, classwork, or non-commercial demos.

Please don’t sell, rebrand, or use this tool for any commercial purpose. 