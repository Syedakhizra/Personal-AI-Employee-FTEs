#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bronze Tier Verification Script

Verifies that all Bronze Tier deliverables are complete and functional.

Run: python verify_bronze.py /path/to/vault
"""

import sys
import os
from pathlib import Path

# Ensure UTF-8 output
if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None


class BronzeVerifier:
    """Verify Bronze Tier deliverables."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def check(self, condition: bool, name: str, warning: bool = False):
        """Check a condition and report result."""
        if condition:
            print(f"  [PASS] {name}")
            self.passed += 1
        else:
            symbol = "[WARN]" if warning else "[FAIL]"
            print(f"  {symbol} {name}")
            if warning:
                self.warnings += 1
            else:
                self.failed += 1
    
    def verify(self) -> bool:
        """Run all verification checks."""
        print("\nVerifying Bronze Tier Deliverables\n")
        print(f"Vault: {self.vault_path}\n")
        
        # 1. Required Markdown Files
        print("Required Markdown Files:")
        self.check((self.vault_path / "Dashboard.md").exists(), "Dashboard.md exists")
        self.check((self.vault_path / "Company_Handbook.md").exists(), "Company_Handbook.md exists")
        self.check((self.vault_path / "Business_Goals.md").exists(), "Business_Goals.md exists")
        self.check((self.vault_path / "Agent_Skills.md").exists(), "Agent_Skills.md exists")
        
        # 2. Required Folder Structure
        print("\nRequired Folder Structure:")
        required_folders = [
            "Inbox", "Needs_Action", "Done", "Plans",
            "Pending_Approval", "Approved", "Rejected",
            "Logs", "Accounting", "Briefings"
        ]
        for folder in required_folders:
            self.check((self.vault_path / folder).exists(), f"/{folder}/ folder exists")
        
        # 3. Watcher Scripts
        print("\nWatcher Scripts:")
        watchers_dir = self.vault_path / "watchers"
        self.check(watchers_dir.exists(), "watchers/ directory exists")
        self.check((watchers_dir / "base_watcher.py").exists(), "base_watcher.py exists")
        self.check((watchers_dir / "filesystem_watcher.py").exists(), "filesystem_watcher.py exists")
        self.check((watchers_dir / "orchestrator.py").exists(), "orchestrator.py exists")
        
        # 4. Python Syntax Check
        print("\nPython Syntax Validation:")
        import subprocess
        for script in ["base_watcher.py", "filesystem_watcher.py", "orchestrator.py"]:
            script_path = watchers_dir / script
            if script_path.exists():
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(script_path)],
                    capture_output=True,
                    text=True
                )
                self.check(result.returncode == 0, f"{script} syntax valid", warning=True)
            else:
                self.check(False, f"{script} syntax valid", warning=True)
        
        # 5. Dashboard Content Check
        print("\nDashboard Content:")
        dashboard = self.vault_path / "Dashboard.md"
        if dashboard.exists():
            content = dashboard.read_text(encoding='utf-8')
            self.check("last_updated:" in content, "Dashboard has last_updated field")
            self.check("status:" in content, "Dashboard has status field")
            self.check("Needs_Action" in content, "Dashboard references Needs_Action")
            self.check("Done" in content, "Dashboard references Done")
        
        # 6. Company Handbook Content
        print("\nCompany Handbook Content:")
        handbook = self.vault_path / "Company_Handbook.md"
        if handbook.exists():
            content = handbook.read_text(encoding='utf-8')
            self.check("Human-in-the-Loop" in content or "HITL" in content, "Handbook defines HITL")
            self.check("Approval" in content, "Handbook describes approval process")
            self.check("Rules" in content, "Handbook contains rules")
        
        # 7. Agent Skills Documentation
        print("\nAgent Skills Documentation:")
        skills = self.vault_path / "Agent_Skills.md"
        if skills.exists():
            content = skills.read_text(encoding='utf-8')
            self.check("Skill" in content, "Skills are documented")
            self.check("Claude" in content, "Claude Code integration documented")
        
        # 8. README Check
        print("\nProject Documentation:")
        readme = self.vault_path.parent / "README.md"
        self.check(readme.exists(), "README.md exists in project root")
        if readme.exists():
            content = readme.read_text(encoding='utf-8')
            self.check("Bronze" in content, "README mentions Bronze Tier")
            self.check("Prerequisites" in content, "README has prerequisites section")
            self.check("Quick Start" in content or "Installation" in content, "README has setup instructions")
        
        # Summary
        print("\n" + "=" * 50)
        print(f"[PASS] Passed: {self.passed}")
        print(f"[FAIL] Failed: {self.failed}")
        print(f"[WARN] Warnings: {self.warnings}")
        print("=" * 50)
        
        if self.failed == 0:
            print("\nBronze Tier Verification PASSED!\n")
            print("All required deliverables are complete.")
            print("\nNext steps:")
            print("1. Open the vault in Obsidian")
            print("2. Run: python watchers/orchestrator.py .")
            print("3. Drop a test file in /Inbox/")
            print("4. Watch the AI Employee process it!")
            return True
        else:
            print(f"\nBronze Tier Verification FAILED\n")
            print(f"{self.failed} required item(s) missing.")
            return False


def main():
    if len(sys.argv) < 2:
        vault_path = Path(__file__).parent
    else:
        vault_path = Path(sys.argv[1])
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    verifier = BronzeVerifier(vault_path)
    success = verifier.verify()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
