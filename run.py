#!/usr/bin/env python3
"""
RansomwareGuard — Full System Launcher (PRO VERSION)
"""

import sys
import time
import threading
import webbrowser
from pathlib import Path

# ✅ Fix import path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import Config
from utils.logger import setup_logger
from utils.alert_manager import AlertManager

from core.entropy_analyzer import EntropyAnalyzer
from core.process_monitor import ProcessMonitor
from core.threat_engine import ThreatEngine
from core.response_engine import ResponseEngine
from core.file_monitor import FileSystemMonitor

from backup.snapshot_manager import SnapshotManager
from backup.backup_vault import BackupVault

from honeypot.canary_manager import CanaryManager
from ml.anomaly_detector import AnomalyDetector

from ui.dashboard_server import run_dashboard


def launch(watch_dir="./test_directory",
           backup_dir="./backups",
           port=5000,
           demo=False):

    logger = setup_logger("RansomwareGuard", "logs/ransomguard.log")

    watch_dir = Path(watch_dir)
    backup_dir = Path(backup_dir)

    watch_dir.mkdir(parents=True, exist_ok=True)
    backup_dir.mkdir(parents=True, exist_ok=True)

    print("\n🛡️ Initializing RansomwareGuard...\n")

    # ── Components ─────────────────────────────
    config = Config()
    alert_manager = AlertManager(config)

    entropy_analyzer = EntropyAnalyzer()
    anomaly_detector = AnomalyDetector()

    snapshot_manager = SnapshotManager(str(watch_dir), str(backup_dir))
    backup_vault = BackupVault(str(backup_dir))
    canary_manager = CanaryManager(str(watch_dir))

    response_engine = ResponseEngine(
        snapshot_manager,
        backup_vault,
        alert_manager
    )

    threat_engine = ThreatEngine(
        entropy_analyzer,
        anomaly_detector,
        response_engine
    )

    # ✅ FIX: Process monitor WITHOUT arguments
    process_monitor = ProcessMonitor()

    # ✅ LINK (VERY IMPORTANT)
    threat_engine.process_monitor = process_monitor

    file_monitor = FileSystemMonitor(
        str(watch_dir),
        threat_engine,
        canary_manager
    )

    # ── Canary files ───────────────────────────
    n = canary_manager.plant_canaries()
    print(f"🍯 Planted {n} canary files")

    # ── Snapshot ───────────────────────────────
    snap_id = snapshot_manager.create_snapshot("initial")
    print(f"💾 Snapshot created: {snap_id}")

    # ── Start monitors ─────────────────────────

    # File monitor (non-blocking)
    file_monitor.start()

    # ✅ FIX: Run process monitor in THREAD
    threading.Thread(
        target=process_monitor.start,
        daemon=True
    ).start()

    print(f"👁 Monitoring: {watch_dir.absolute()}")

    # ── Dashboard ─────────────────────────────
    threading.Thread(
        target=run_dashboard,
        args=(
            threat_engine,
            snapshot_manager,
            backup_vault,
            canary_manager,
            response_engine
        ),
        kwargs={"port": port},
        daemon=True
    ).start()

    # ── Demo Mode ─────────────────────────────
    if demo:
        from utils.demo_simulator import DemoSimulator
        sim = DemoSimulator(str(watch_dir), threat_engine)

        threading.Thread(
            target=sim.run_demo,
            daemon=True
        ).start()

        print("🎬 Auto Demo Started")

    print("\n✅ RansomwareGuard ACTIVE")
    print(f"🌐 Dashboard: http://localhost:{port}")
    print("Press Ctrl+C to stop\n")

    # Open browser
    time.sleep(2)
    try:
        webbrowser.open(f"http://localhost:{port}")
    except Exception:
        pass

    # ── Live stats ─────────────────────────────
    try:
        while True:
            stats = threat_engine.get_stats()

            print(
                f"\r[LIVE] Events: {stats.get('events', 0)} | "
                f"Threats: {stats.get('threats', 0)} | "
                f"Blocked: {stats.get('blocked', 0)}",
                end=""
            )

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")

        try:
            file_monitor.stop()
        except:
            pass

        try:
            process_monitor.stop()
        except:
            pass

        try:
            threat_engine.print_summary()
        except:
            pass

        print("\n✅ Shutdown complete\n")


# ── MAIN ─────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RansomwareGuard Launcher")

    parser.add_argument("--watch", default="./test_directory")
    parser.add_argument("--backup", default="./backups")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--demo", action="store_true")

    args = parser.parse_args()

    launch(args.watch, args.backup, args.port, args.demo)