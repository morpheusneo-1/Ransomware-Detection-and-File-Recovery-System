import sys
import os

# ✅ Fix import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import threading
import time

from core.file_monitor import FileSystemMonitor
from core.threat_engine import ThreatEngine
from core.process_monitor import ProcessMonitor
from core.response_engine import ResponseEngine
from core.entropy_analyzer import EntropyAnalyzer

from utils.alert_manager import AlertManager
from utils.config import Config

WATCH_DIR = "test_directory"


def main():
    print("\n🚨 Ransomware Guard Starting...\n")

    # ==============================
    # ✅ Initialize Core Components
    # ==============================

    entropy_analyzer = EntropyAnalyzer()

    # ✅ Config + Alert Manager (FIXED)
    config = Config()
    alert_manager = AlertManager(config)

    # ✅ Response Engine (FIXED)
    snapshot_manager = None          # You can upgrade later
    backup_vault = "backups"

    response_engine = ResponseEngine(
        snapshot_manager,
        backup_vault,
        alert_manager
    )

    # ✅ Threat Engine
    threat_engine = ThreatEngine(
        entropy_analyzer,
        None,
        response_engine
    )

    # ==============================
    # ✅ Process Monitor
    # ==============================

    process_monitor = ProcessMonitor()
    threat_engine.process_monitor = process_monitor

    # ==============================
    # ✅ File Monitor
    # ==============================

    file_monitor = FileSystemMonitor(
        WATCH_DIR,
        threat_engine,
        None
    )

    # ==============================
    # 🚀 Start System
    # ==============================

    file_monitor.start()
    threading.Thread(target=process_monitor.start, daemon=True).start()

    print("[+] System is running... Press Ctrl+C to stop.\n")

    # ==============================
    # 🔁 Main Loop
    # ==============================

    try:
        while True:
            stats = threat_engine.get_stats()

            print(
                f"[LIVE] Events: {stats.get('events', 0)} | "
                f"Threats: {stats.get('threats', 0)} | "
                f"Blocked: {stats.get('blocked', 0)} | "
                f"Files Protected: {stats.get('files_protected', 0)}"
            )

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[*] Shutting down...")

        file_monitor.stop()
        process_monitor.stop()

        print("\n====== SUMMARY ======")
        print(f"Events: {threat_engine.stats.get('events', 0)}")
        print(f"Threats: {threat_engine.stats.get('threats', 0)}")
        print(f"Blocked: {threat_engine.stats.get('blocked', 0)}")
        print(f"Files Protected: {threat_engine.stats.get('files_protected', 0)}")
        print("=====================\n")


if __name__ == "__main__":
    main()