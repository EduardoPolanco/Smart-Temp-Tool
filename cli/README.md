📄 README.md (for CLI version)
# 🔥 Smart Temp CLI Tool

A command-line tool that analyzes heating/cooling time, power usage, and safety for various liquids based on temperature data.

## ✅ Features

- Accepts `.csv`, `.xlsx`, or `.json` files
- Calculates time to target temp, power usage, and safety alerts
- Allows filtering by drink type or time
- Optional Fahrenheit conversion
- Exports to CSV or PDF
- Easy to run on macOS or Windows with Python 3

## 📦 Requirements

- Python 3.8+
- pandas
- tabulate
- reportlab (only if exporting to PDF)

## 📂 Input File Format

Your data file must contain the following columns:

- `Liquid Type`
- `Initial Temperature`
- `Desired Temperature`
- `Ambient Temperature`
- `Time to Target`
- `Battery Level`
- `User Preference`

## 🚀 Usage

```bash
python3 smart_temp_cli.py

Optional flags:
--fahrenheit             # Convert temps to Fahrenheit
--export-csv results.csv # Export output to CSV
--export-pdf results.pdf # Export output to PDF

🛠 Example:
python3 smart_temp_cli.py --fahrenheit --export-csv output.csv

📄 Disclaimer

This tool is provided as an educational prototype based on preset examples and assumptions. It is not intended for production, monetization, or safety-critical use.