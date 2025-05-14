import pandas as pd
import os
import argparse
from tabulate import tabulate  # ADDED for pretty table output

# Optional: Fahrenheit converter
def to_fahrenheit(c):
    return round((c * 9/5) + 32, 1)

# Load data CSV, Excel, or JSON
def load_data(file_path):
    """Load data from CSV, Excel, or JSON into a dataframe"""
    file_ext = file_path.lower()
    if file_ext.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_ext.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_ext.endswith('.json'):
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format Please use CSV, XLSX, or JSON.")

# Required columns for validation
REQUIRED_COLUMNS = [
    "Liquid Type",
    "Initial Temperature",
    "Desired Temperature",
    "Ambient Temperature",
    "Time to Target",
    "Battery Level",
    "User Preference"
]

def validate_data(df):
    """Check if all required columns are present in the data."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {','.join(missing)}")
    print("✅ data validated. All required columns are present.")

def calculate_core_metrics(df):
    """Calculate time to heat/cool, power consumption, and safety status."""
    results = []

    for index, row in df.iterrows():
        try:
            start_temp = float(row["Initial Temperature"])
            target_temp = float(row["Desired Temperature"])
            ambient_temp = float(row["Ambient Temperature"])
            battery_level = float(row["Battery Level"])

            temp_diff = abs(target_temp - start_temp)

            time_to_target = temp_diff * 0.5
            power_use = temp_diff * 0.8

            if ambient_temp > 30:
                time_to_target *= 0.9
                power_use *= 0.85
            elif ambient_temp < 10:
                time_to_target *= 1.2
                power_use *= 1.1

            time_to_target = round(time_to_target, 2)
            power_use = round(power_use, 2)

            if target_temp > 90:
                alert = "⚠️ Overheating Risk"
            elif target_temp < 0:
                alert = "❄️ Freezing Risk"
            else:
                alert = "✅ Normal"

            if power_use > 40:
                power_tip = "Consider reducing target temp to save battery."
            else:
                power_tip = "Efficient usage."

            results.append({
                "Liquid Type": row["Liquid Type"],
                "Initial Temperature": start_temp,
                "Desired Temperature": target_temp,
                "Ambient Temperature": ambient_temp,
                "Battery Level": battery_level,
                "Time to Target": time_to_target,
                "Power Usage": power_use,
                "Alert": alert,
                "Power Saving Tip": power_tip,
                "User Preference": row["User Preference"]
            })
        except Exception as e:
            results.append({
                "Liquid Type": row.get("Liquid Type", "Unknown"),
                "Error": str(e)
            })
    return results

def apply_filters(results, drink_type=None, max_time=None):
    """Filter results by drink type and/or max heating time."""
    filtered = []
    for item in results:
        if "Error" in item:
            filtered.append(item)
            continue
        if drink_type and item["Liquid Type"].lower() != drink_type.lower():
            continue
        if max_time is not None and item["Time to Target"] > max_time:
            continue
        filtered.append(item)
    return filtered

def main():
    parser = argparse.ArgumentParser(description="Smart Temp CLI Tool")
    parser.add_argument("--fahrenheit", action="store_true", help="Convert temperatures to Fahrenheit")
    parser.add_argument("--export-csv", metavar="CSV_PATH", help="Export results to CSV")
    parser.add_argument("--export-pdf", metavar="PDF_PATH", help="Export results to PDF (requires reportlab)")
    args = parser.parse_args()

    print("🔍 Smart Temp tool - File Loader")
    file_path = input("Enter the path to your data file(CSV, XLSX, or JSON): ").strip()

    if not os.path.exists(file_path):
        print("❌ File not found. Please check the path and try again.")
        return
    try:
        df = load_data(file_path)
        validate_data(df)
        print("✅ File successfully loaded and validated. Calculating metrics... \n")

        calculated_results = calculate_core_metrics(df)

        drink_type = input("Filter by drink type (press Enter to skip): ").strip()
        time_limit_input = input("Filter by max heat time in minutes (press Enter to skip): ").strip()
        time_limit = float(time_limit_input) if time_limit_input else None

        filtered_results = apply_filters(calculated_results, drink_type or None, time_limit)

        if not filtered_results:
            print("No matching results found.")
            return

        table_data = []
        for item in filtered_results:
            if "Error" in item:
                table_data.append([item["Liquid Type"], "ERROR", item["Error"]])
            else:
                start = to_fahrenheit(item["Initial Temperature"]) if args.fahrenheit else item["Initial Temperature"]
                end = to_fahrenheit(item["Desired Temperature"]) if args.fahrenheit else item["Desired Temperature"]
                unit = "°F" if args.fahrenheit else "°C"

                table_data.append([
                    item["Liquid Type"],
                    f"{start}{unit}",
                    f"{end}{unit}",
                    f"{item['Ambient Temperature']}{unit}",
                    f"{item['Time to Target']} min",
                    f"{item['Power Usage']}%",
                    item["Alert"],
                    item["Power Saving Tip"],
                    item["User Preference"]
                ])

        headers = ["Liquid", "Start Temp", "Target Temp", "Ambient", "Time", "Power", "Alert", "Tip", "Preference"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

        if args.export_csv:
            pd.DataFrame(filtered_results).to_csv(args.export_csv, index=False)
            print(f"✅ Results exported to CSV: {args.export_csv}")

        if args.export_pdf:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            pdf = canvas.Canvas(args.export_pdf, pagesize=letter)
            width, height = letter
            y = height - 40

            pdf.setFont("Helvetica", 10)
            pdf.drawString(50, y, "Smart Temp CLI Export")
            y -= 20

            for item in filtered_results:
                for key, value in item.items():
                    pdf.drawString(50, y, f"{key}: {value}")
                    y -= 15
                    if y < 40:
                        pdf.showPage()
                        y = height - 40
                y -= 10
            pdf.save()
            print(f"✅ Results exported to PDF: {args.export_pdf}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()