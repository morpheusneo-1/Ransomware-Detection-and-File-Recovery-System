import os
import time

TARGET_DIR = "test_directory"

def simulate_ransomware():
    print("🚨 Starting ransomware simulation...")

    for filename in os.listdir(TARGET_DIR):
        file_path = os.path.join(TARGET_DIR, filename)

        if file_path.endswith(".locked"):
            continue

        if os.path.isfile(file_path):
            base = os.path.splitext(file_path)[0]
            new_path = base + ".locked"

            try:
                os.rename(file_path, new_path)
                print(f"[SIMULATED] {filename} → {os.path.basename(new_path)}")
                time.sleep(1)

            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    simulate_ransomware()