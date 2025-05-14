import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# ================== Core Functions ==================

def load_data(file_path):
    file_ext = file_path.lower()
    if file_ext.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_ext.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_ext.endswith('.json'):
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format Please use CSV, XLSX, or JSON.")

REQUIRED_COLUMNS = [
    "Liquid Type", "Initial Temperature", "Desired Temperature",
    "Ambient Temperature", "Time to Target", "Battery Level", "User Preference"
]

def validate_data(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {','.join(missing)}")

def calculate_core_metrics(df):
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
            alert = "⚠️ Overheating Risk" if target_temp > 90 else (
                "❄️ Freezing Risk" if target_temp < 0 else "✅ Normal")
            power_tip = "Consider reducing target temp to save battery." if power_use > 40 else "Efficient usage."
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
            results.append({"Liquid Type": row.get("Liquid Type", "Unknown"), "Error": str(e)})
    return results

def apply_filters(results, drink_type=None, max_time=None):
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

# ================== GUI ==================

class SmartTempGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Temp Tool")
        self.use_fahrenheit = tk.BooleanVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Data File").pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.load_file).pack(pady=5)

        tk.Label(self.root, text="Drink Type (optional)").pack(pady=5)
        self.drink_entry = tk.Entry(self.root)
        self.drink_entry.pack(pady=5)

        tk.Label(self.root, text="Max Time (min, optional)").pack(pady=5)
        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack(pady=5)

        tk.Checkbutton(self.root, text="Use Fahrenheit", variable=self.use_fahrenheit).pack(pady=5)

        tk.Button(self.root, text="Calculate", command=self.process).pack(pady=10)

        self.temp_label = tk.Label(self.root, text="Temperature Simulation")
        self.temp_label.pack(pady=(10, 0))
        self.temp_progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.temp_progress.pack(pady=(5, 10))

        self.battery_label = tk.Label(self.root, text="Battery Level")
        self.battery_label.pack()
        self.battery_progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.battery_progress.pack(pady=(0, 10))

        self.feedback_label = tk.Label(self.root, text="")
        self.feedback_label.pack(pady=5)

        self.result_box = tk.Text(self.root, height=20, width=90)
        self.result_box.pack(pady=5)

        tk.Button(self.root, text="Export to CSV", command=self.export_to_csv).pack(pady=5)
        tk.Button(self.root, text="Export to PDF", command=self.export_to_pdf).pack(pady=5)
        

    def load_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("JSON Files", "*.json")]
        )
        if self.file_path:
            self.result_box.insert(tk.END, f"Loaded file: {self.file_path}\n")

    def to_fahrenheit(self, c):
        return round((c * 9/5) + 32, 1)

    def simulate_temp_change(self, start, target, battery_level, time_to_target):
        display_start = self.to_fahrenheit(start) if self.use_fahrenheit.get() else start
        display_target = self.to_fahrenheit(target) if self.use_fahrenheit.get() else target
        unit = "°F" if self.use_fahrenheit.get() else "°C"

        self.temp_progress["maximum"] = abs(display_target - display_start)
        self.temp_progress["value"] = 0
        steps = int(abs(display_target - display_start))

        self.battery_progress["maximum"] = 100
        self.battery_progress["value"] = battery_level
        self.battery_label.config(text=f"Battery Level: {battery_level}%")
        self.feedback_label.config(text=f"Your drink will be ready in {time_to_target} min")

        def update(step=0):
            if step > steps:
                return
            self.temp_progress["value"] = step
            current = round(display_start + (step if display_target > display_start else -step), 1)
            self.temp_label.config(text=f"Temperature: {current}{unit}")
            self.root.update_idletasks()
            self.root.after(100, update, step + 1)

        update()

    def process(self):
        try:
            self.result_box.delete("1.0", tk.END)
            if not hasattr(self, 'file_path'):
                messagebox.showerror("Error", "No file selected.")
                return
            df = load_data(self.file_path)
            validate_data(df)
            self.result_box.insert(tk.END, "✅ Data validated. All required columns are present. \n")

            drink = self.drink_entry.get()
            drink = drink.strip().lower() if drink else None
            if drink and not drink.replace(" ", "").isalpha():
                messagebox.showerror(
                    "Input Error",
                    "❌ Drink Type must only contain letters. \n\n✅ Example: water, tea, iced coffee"
                )
                return
                
            max_time = self.time_entry.get()
            try:
                max_time = float(max_time) if max_time else None
            except ValueError:
                messagebox.showerror(
                    "Input Error",
                    "❌ Max Time must be a number.\n\n✅ Example: 2 or 5.5\nLeave it blank to skip this filter."
                )
                return

            filtered = apply_filters(calculate_core_metrics(df), drink, max_time)
            self.last_results = filtered
            if not filtered:
                self.result_box.insert(tk.END, "⚠️ No results matched the filters. \n")
                return

            self.result_box.insert(tk.END, "\n=== Calculation Results ===\n")
            for item in filtered:
                if "Error" in item:
                    self.result_box.insert(tk.END, f"Error: {item['Error']}\n")
                else:
                    initial = self.to_fahrenheit(item["Initial Temperature"]) if self.use_fahrenheit.get() else item["Initial Temperature"]
                    desired = self.to_fahrenheit(item["Desired Temperature"]) if self.use_fahrenheit.get() else item["Desired Temperature"]
                    unit = "°F" if self.use_fahrenheit.get() else "°C"

                    self.result_box.insert(tk.END, (
                        f"Liquid: {item['Liquid Type']}, Initial: {initial}{unit}, Desired: {desired}{unit}\n"
                    ))
                    self.simulate_temp_change(
                        item["Initial Temperature"],
                        item["Desired Temperature"],
                        item["Battery Level"],
                        item["Time to Target"]
                    )
                    self.result_box.insert(tk.END, (
                        f"Ambient: {item['Ambient Temperature']}{unit}, Time: {item['Time to Target']} min, Power: {item['Power Usage']}%, "
                        f"Alert: {item['Alert']}, Tip: {item['Power Saving Tip']}, Pref: {item['User Preference']}\n\n"
                    ))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def export_to_csv(self):
        if not hasattr(self, "last_results") or not self.last_results:
            messagebox.showerror("Error", "No data to export. Run a calculation first. ")
            return

        export_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save results as CSV"
        )
        if not export_path:
            return
        try:
            df = pd.DataFrame(self.last_results)
            df.to_csv(export_path, index=False)
            messagebox.showinfo("Success", f"Results exported to {export_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    def export_to_pdf(self):
        if not hasattr(self, "last_results") or not self.last_results:
            messagebox.showerror("Error", "No data to export. Run a calculation first.")
            return
        export_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save results as PDF"
        )
        if not export_path:
            return
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            pdf = canvas.Canvas(export_path, pagesize=letter)
            width, height = letter
            y = height - 40

            pdf.setFont("Helvetica", 10)
            pdf.drawString(50, y, "Smart Temp Tool - Exported Results")
            y -= 20

            for item in self.last_results:
                for key, value in item.items():
                    line = f"{key}: {value}"
                    pdf.drawString(50, y, line)
                    y -= 15
                    if y < 40:
                        pdf.showPage()
                        y = height - 40
                y -= 10 
            pdf.save()
            messagebox.showinfo("Success", f"PDF exported to {export_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

# ================== Run Mode Control ==================

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartTempGUI(root)
    root.mainloop()