#!/usr/bin/env python3
"""
RansomwareGuard Setup & Quick-Start Script
Run this first to verify installation and prepare the environment.
"""

import sys
import os
import subprocess
from pathlib import Path

BANNER = """
╔══════════════════════════════════════════╗
║   RansomwareGuard — Setup & Verification ║
╚══════════════════════════════════════════╝
"""

def check_python():
    print("[1/5] Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"  ✗ Python {version.major}.{version.minor} found — need 3.8+")
        sys.exit(1)
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")

def install_dependencies():
    print("\n[2/5] Installing dependencies...")
    packages = [
        ("watchdog",      "watchdog>=3.0.0"),
        ("psutil",        "psutil>=5.9.0"),
        ("sklearn",       "scikit-learn>=1.3.0"),
        ("numpy",         "numpy>=1.24.0"),
        ("flask",         "flask>=3.0.0"),
        ("flask_cors",    "flask-cors>=4.0.0"),
    ]
    for import_name, pkg in packages:
        try:
            __import__(import_name)
            print(f"  ✓ {pkg.split('>=')[0]} already installed")
        except ImportError:
            print(f"  → Installing {pkg}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"  ✓ {pkg.split('>=')[0]} installed")
            else:
                print(f"  ✗ Failed to install {pkg}: {result.stderr[:100]}")

def create_directories():
    print("\n[3/5] Creating project directories...")
    dirs = [
        "test_directory",
        "backups/snapshots",
        "backups/vault",
        "logs/incidents",
        "quarantine",
        "ml/models",
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {d}/")

def create_test_files():
    print("\n[4/5] Creating test files for demo...")
    test_dir = Path("test_directory")
    files = {
        "company_report_2024.txt":   "Q4 Financial Report\nRevenue: $2.4M\nNet Profit: $480K\n",
        "employee_data.csv":          "ID,Name,Dept,Salary\n001,Alice,Eng,95000\n002,Bob,HR,60000\n",
        "project_notes.txt":          "Project Alpha - Phase 2\nDeadline: Dec 31\nTeam: 5 engineers\n",
        "database_schema.sql":        "CREATE TABLE users (id INT, name VARCHAR(100));\n",
        "configuration.json":         '{"app": "RansomwareGuard", "version": "1.0.0", "debug": false}\n',
        "important_document.txt":     "CONFIDENTIAL: This is an important business document.\n" * 10,
        "backup_notes.txt":           "Backup schedule: Daily at 2AM\nRetention: 30 days\n",
        "client_contracts.txt":       "Contract #2024-001: Services agreement...\n" * 5,
    }
    for filename, content in files.items():
        fpath = test_dir / filename
        if not fpath.exists():
            with open(fpath, "w") as f:
                f.write(content)
            print(f"  ✓ {filename}")
        else:
            print(f"  → {filename} (exists)")

def verify_imports():
    print("\n[5/5] Verifying module imports...")
    modules = [
        ("core.entropy_analyzer",  "EntropyAnalyzer"),
        ("core.threat_engine",     "ThreatEngine"),
        ("core.response_engine",   "ResponseEngine"),
        ("backup.snapshot_manager","SnapshotManager"),
        ("backup.backup_vault",    "BackupVault"),
        ("honeypot.canary_manager","CanaryManager"),
        ("ml.anomaly_detector",    "AnomalyDetector"),
        ("utils.config",           "Config"),
        ("utils.alert_manager",    "AlertManager"),
    ]
    sys.path.insert(0, str(Path(__file__).parent))
    all_ok = True
    for module, cls in modules:
        try:
            mod = __import__(module, fromlist=[cls])
            getattr(mod, cls)
            print(f"  ✓ {module}.{cls}")
        except Exception as e:
            print(f"  ✗ {module}.{cls} — {e}")
            all_ok = False
    return all_ok

def print_next_steps():
    print("\n" + "="*50)
    print("  🎉 Setup Complete! Next Steps:")
    print("="*50)
    print()
    print("  1. Run demo simulation:")
    print("     python main.py --watch ./test_directory --demo")
    print()
    print("  2. Open dashboard (browser):")
    print("     open ui/static/index.html")
    print()
    print("  3. Monitor a real directory:")
    print("     python main.py --watch /your/important/files")
    print()
    print("  4. Train ML model:")
    print("     python main.py --train --watch ./test_directory")
    print()
    print("  5. Full server with API:")
    print("     python main.py --watch ./test_directory --demo")
    print("     # Dashboard at http://localhost:5000")
    print()

if __name__ == "__main__":
    print(BANNER)
    check_python()
    install_dependencies()
    create_directories()
    create_test_files()
    ok = verify_imports()
    print_next_steps()
    if not ok:
        print("  ⚠️  Some imports failed. Run: pip install -r requirements.txt")
        sys.exit(1)
    print("  ✅ RansomwareGuard is ready!\n")
