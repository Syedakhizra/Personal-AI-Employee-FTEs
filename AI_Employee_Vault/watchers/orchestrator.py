#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator - Master process for the AI Employee system.

The orchestrator:
1. Manages watcher processes (start, stop, monitor)
2. Triggers Claude Code to process /Needs_Action items
3. Updates the [[Dashboard]] with current status
4. Handles scheduled tasks (daily briefings, etc.)
5. Implements human-in-the-loop approval workflow

Usage:
    python orchestrator.py /path/to/vault

Orchestrator Modes:
- run: Normal operation (default)
- process: Process pending items once and exit
- status: Show current system status
"""

import os
import sys
import subprocess
import time
import json
import signal
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import threading
import logging


class Orchestrator:
    """
    Master orchestrator for the AI Employee system.
    
    Coordinates watchers, Claude Code processing, and dashboard updates.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.watchers_dir = self.vault_path / 'watchers'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure directories exist
        for dir_path in [self.needs_action, self.plans, self.pending_approval, 
                         self.approved, self.done, self.logs]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Watcher processes
        self.watcher_processes: Dict[str, subprocess.Popen] = {}
        
        # State
        self.running = False
        self.qwen_available = self._check_qwen_code()
        
        self.logger.info(f"Orchestrator initialized for vault: {self.vault_path}")
        self.logger.info(f"Qwen Code available: {self.qwen_available}")
    
    def _setup_logging(self):
        """Configure logging."""
        log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}_orchestrator.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Orchestrator')
    
    def _check_qwen_code(self) -> bool:
        """Check if Qwen Code is installed and available."""
        try:
<<<<<<< HEAD
=======
            # On Windows, use shell=True to find .cmd files in PATH
>>>>>>> edbe72d (silver tier)
            result = subprocess.run(
                ['qwen', '--version'],
                capture_output=True,
                text=True,
<<<<<<< HEAD
                timeout=10
=======
                timeout=10,
                shell=True
>>>>>>> edbe72d (silver tier)
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            self.logger.warning("Qwen Code not found in PATH")
            return False
    
    def _count_files(self, folder: Path) -> int:
        """Count .md files in a folder."""
        if not folder.exists():
            return 0
        return len([f for f in folder.iterdir() if f.suffix == '.md'])
    
    def _update_dashboard(self):
        """Update the Dashboard.md with current status."""
        if not self.dashboard.exists():
            self.logger.warning("Dashboard.md not found")
            return

        try:
            content = self.dashboard.read_text(encoding='utf-8')

            # Update timestamp
            content = content.replace(
                'last_updated: 2026-02-28T00:00:00Z',
                f'last_updated: {datetime.now().isoformat()}Z'
            )

            # Update stats section (simple replacement)
            pending_count = self._count_files(self.needs_action)
            plans_count = self._count_files(self.plans)
            approval_count = self._count_files(self.pending_approval)
            done_count = self._count_files(self.done)

            # Log the update
            self.logger.info(f"Dashboard updated - Pending: {pending_count}, Plans: {plans_count}, Approval: {approval_count}")

            self.dashboard.write_text(content, encoding='utf-8')
            
        except Exception as e:
            self.logger.error(f"Error updating dashboard: {e}")
    
    def _process_needs_action(self):
        """
        Process items in /Needs_Action folder.

        This triggers Claude Code to analyze and create action plans.
        Only processes files that haven't been processed yet.
        """
        items = [f for f in self.needs_action.iterdir() if f.suffix == '.md']

        if not items:
            return

        # Filter out already processed files
        new_items = []
        for item_file in items:
            try:
                content = item_file.read_text(encoding='utf-8')
                # Skip if already has processed status or plan exists
                plan_file = self.plans / f"PLAN_{item_file.stem}.md"
                if plan_file.exists():
                    continue  # Plan already created, skip
                if 'status: processed' in content:
                    continue  # Already processed
                new_items.append(item_file)
            except Exception as e:
                self.logger.error(f"Error checking file {item_file.name}: {e}")

        if not new_items:
            return

        self.logger.info(f"Processing {len(new_items)} new item(s) in Needs_Action")

        for item_file in new_items:
            try:
                # Read the file to understand what needs to be done
                content = item_file.read_text(encoding='utf-8')

                # Create a plan file for Claude to work with (only if it doesn't exist)
                plan_file = self.plans / f"PLAN_{item_file.stem}.md"
                
                if not plan_file.exists():
                    plan_content = f"""---
created: {datetime.now().isoformat()}
status: pending
source: [[{item_file.name}]]
type: action_plan
---

# Action Plan

## Source
Processing: {item_file.name}

## Objective
<!-- Qwen Code will define the objective here -->

## Steps
- [ ] Analyze source file
- [ ] Determine required actions
- [ ] Execute or request approval

## Notes
<!-- Qwen Code will add notes here -->

---
*Created by Orchestrator at {datetime.now().isoformat()}*
"""
                    plan_file.write_text(plan_content, encoding='utf-8')
                    self.logger.info(f"Created plan for: {item_file.name}")
                else:
                    self.logger.debug(f"Plan already exists for: {item_file.name}")

            except Exception as e:
                self.logger.error(f"Error processing {item_file.name}: {e}")
<<<<<<< HEAD
    
=======

    def _process_plans_with_qwen(self):
        """
        Run Qwen Code on pending plan files.

        This is the auto-invoke logic that triggers Qwen Code to:
        1. Read plan files with status: pending
        2. Process the plan (analyze, execute, create approvals)
        3. Update plan status to: processed
        """
        if not self.qwen_available:
            self.logger.warning("Qwen Code not available, skipping plan processing")
            return

        # Find pending plans
        pending_plans = []
        for plan_file in self.plans.iterdir():
            if plan_file.suffix != '.md':
                continue
            try:
                content = plan_file.read_text(encoding='utf-8')
                if 'status: pending' in content:
                    pending_plans.append(plan_file)
            except Exception as e:
                self.logger.error(f"Error reading plan {plan_file.name}: {e}")

        if not pending_plans:
            return

        self.logger.info(f"Processing {len(pending_plans)} pending plan(s) with Qwen Code")

        for plan_file in pending_plans:
            try:
                self.logger.info(f"Invoking Qwen Code for: {plan_file.name}")

                # Read the plan content
                plan_content = plan_file.read_text(encoding='utf-8')
                
                # Extract source file from plan
                source_match = None
                for line in plan_content.split('\n'):
                    if 'Processing:' in line:
                        source_match = line.split('Processing:')[1].strip()
                        break
                
                source_file = self.needs_action / source_match if source_match else None
                
                # Read source file content if exists
                source_content = ""
                if source_file and source_file.exists():
                    try:
                        source_content = source_file.read_text(encoding='utf-8')
                    except:
                        pass

                # Build the prompt for Qwen Code with explicit instructions
                prompt = f"""You are an AI Employee. Process this task AUTOMATICALLY.

**PLAN FILE:** {plan_file.absolute()}
**PLAN CONTENT:**
{plan_content}

**SOURCE FILE:** {source_file.absolute() if source_file else "N/A"}
**SOURCE CONTENT:**
{source_content if source_content else "No source file"}

**YOUR TASK (Execute ALL steps automatically):**
1. Read and understand the plan above
2. If source file exists in Needs_Action, read and categorize it
3. Move the source file from Needs_Action to Done folder
4. Update the plan file: change "status: pending" to "status: processed"
5. Mark all checkboxes [ ] as [x] in the plan
6. Add notes about what you did

**IMPORTANT:** Do NOT ask questions. Do NOT wait for input. Execute ALL steps automatically now.
Use -y flag to auto-approve all file operations.

Start executing now:"""

                # Run Qwen Code with the prompt using --approval-mode yolo for auto-approval
                result = subprocess.run(
                    ['qwen', prompt, '--approval-mode', 'yolo'],
                    text=True,
                    timeout=300,  # 5 minutes per plan
                    shell=True,
                    cwd=str(self.vault_path)
                )

                if result.returncode == 0:
                    self.logger.info(f"Successfully processed: {plan_file.name}")
                else:
                    self.logger.error(f"Qwen Code error for {plan_file.name}: exit code {result.returncode}")

            except subprocess.TimeoutExpired:
                self.logger.error(f"Timeout processing plan: {plan_file.name}")
            except Exception as e:
                self.logger.error(f"Error processing plan {plan_file.name}: {e}")

>>>>>>> edbe72d (silver tier)
    def _check_approvals(self):
        """
        Check for approved actions ready to execute.
        
        In Bronze tier, this just logs the approval.
        Higher tiers would execute MCP actions here.
        """
        approved_files = [f for f in self.approved.iterdir() if f.suffix == '.md']
        
        for approved_file in approved_files:
            self.logger.info(f"Approved action ready: {approved_file.name}")
            # In Bronze tier, we just notify
            # Higher tiers would execute the action via MCP
            
            # Move to Done after "execution"
            try:
                dest = self.done / approved_file.name
                approved_file.rename(dest)
                self.logger.info(f"Moved to Done: {approved_file.name}")
            except Exception as e:
                self.logger.error(f"Error moving approved file: {e}")
    
    def start_watcher(self, watcher_name: str) -> bool:
        """
        Start a watcher process.
        
        Args:
            watcher_name: Name of the watcher script (without .py)
            
        Returns:
            True if started successfully
        """
        watcher_script = self.watchers_dir / f"{watcher_name}.py"
        
        if not watcher_script.exists():
            self.logger.error(f"Watcher script not found: {watcher_script}")
            return False
        
        if watcher_name in self.watcher_processes:
            self.logger.warning(f"Watcher already running: {watcher_name}")
            return True
        
        try:
            # Start watcher as subprocess
            proc = subprocess.Popen(
                [sys.executable, str(watcher_script), str(self.vault_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.watcher_processes[watcher_name] = proc
            self.logger.info(f"Started watcher: {watcher_name} (PID: {proc.pid})")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting watcher: {e}")
            return False
    
    def stop_watcher(self, watcher_name: str) -> bool:
        """
        Stop a watcher process.
        
        Args:
            watcher_name: Name of the watcher
            
        Returns:
            True if stopped successfully
        """
        if watcher_name not in self.watcher_processes:
            return True
        
        try:
            proc = self.watcher_processes[watcher_name]
            proc.terminate()
            proc.wait(timeout=5)
            del self.watcher_processes[watcher_name]
            self.logger.info(f"Stopped watcher: {watcher_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error stopping watcher: {e}")
            # Force kill
            proc.kill()
            return True
    
    def start_all_watchers(self):
<<<<<<< HEAD
        """Start all available watchers."""
        # For Bronze tier, just start the filesystem watcher
        self.start_watcher('filesystem_watcher')
        
        # Higher tiers would start gmail_watcher, whatsapp_watcher, etc.
=======
        """Start all available watchers (Silver Tier)."""
        # Bronze: Filesystem watcher
        self.start_watcher('filesystem_watcher')
        
        # Silver Tier: Gmail Watcher
        self.start_watcher('gmail_watcher')
        
        # Silver Tier: LinkedIn Scheduler (runs hourly)
        # Note: LinkedIn scheduler creates drafts, not continuous watcher
        # self.start_watcher('linkedin_scheduler')
        
        # Higher tiers: gmail_watcher, whatsapp_watcher, etc.
>>>>>>> edbe72d (silver tier)
    
    def stop_all_watchers(self):
        """Stop all watcher processes."""
        for watcher_name in list(self.watcher_processes.keys()):
            self.stop_watcher(watcher_name)
    
    def run_once(self):
        """Process pending items once (no continuous loop)."""
        self.logger.info("Running single processing cycle")
        self._update_dashboard()
        self._process_needs_action()
<<<<<<< HEAD
        self._check_approvals()
    
=======
        self._process_plans_with_qwen()
        self._check_approvals()

>>>>>>> edbe72d (silver tier)
    def run(self, check_interval: int = 30):
        """
        Main orchestrator loop.
        
        Args:
            check_interval: Seconds between checks
        """
        self.running = True
        self.logger.info("Starting orchestrator main loop")
        self.logger.info(f"Check interval: {check_interval}s")
        
        # Start watchers
        self.start_all_watchers()
        
        # Main loop
        try:
            while self.running:
                try:
                    # Update dashboard
                    self._update_dashboard()
<<<<<<< HEAD
                    
                    # Process pending items
                    self._process_needs_action()
                    
=======

                    # Process pending items (create plans)
                    self._process_needs_action()

                    # Process plans with Qwen Code (auto-invoke)
                    self._process_plans_with_qwen()

>>>>>>> edbe72d (silver tier)
                    # Check approvals
                    self._check_approvals()
                    
                    # Monitor watcher health
                    for name, proc in list(self.watcher_processes.items()):
                        if proc.poll() is not None:
                            self.logger.warning(f"Watcher {name} died, restarting...")
                            self.start_watcher(name)
                    
                except Exception as e:
                    self.logger.error(f"Error in orchestrator loop: {e}")
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Orchestrator stopped by user")
        finally:
            self.stop()
    
    def stop(self):
        """Clean shutdown of the orchestrator."""
        self.logger.info("Stopping orchestrator...")
        self.running = False
        self.stop_all_watchers()
        self._update_dashboard()
        self.logger.info("Orchestrator stopped")
    
    def status(self) -> Dict:
        """Get current system status."""
        return {
            'vault_path': str(self.vault_path),
            'qwen_available': self.qwen_available,
            'watchers': {
                name: proc.pid if proc else 'stopped'
                for name, proc in self.watcher_processes.items()
            },
            'folders': {
                'needs_action': self._count_files(self.needs_action),
                'plans': self._count_files(self.plans),
                'pending_approval': self._count_files(self.pending_approval),
                'approved': self._count_files(self.approved),
                'done': self._count_files(self.done),
            },
            'dashboard_exists': self.dashboard.exists(),
        }


def print_status(orchestrator: Orchestrator):
    """Print system status in a formatted way."""
    status = orchestrator.status()

    print("\nAI Employee System Status\n")
    print(f"Vault: {status['vault_path']}")
    print(f"Qwen Code: {'Available' if status['qwen_available'] else 'Not Available'}")
    print(f"Dashboard: {'Exists' if status['dashboard_exists'] else 'Missing'}")
    print("\nFolder Contents:")
    for folder, count in status['folders'].items():
        print(f"   {folder}: {count} file(s)")
    print("\nWatchers:")
    if status['watchers']:
        for name, pid in status['watchers'].items():
            print(f"   {name}: PID {pid}")
    else:
        print("   (none running)")
    print()


def main():
    """Main entry point for the orchestrator."""
    if len(sys.argv) < 2:
        # Try to find vault relative to script location
        vault_path = Path(__file__).parent
        print(f"Using vault path: {vault_path}")
    else:
        vault_path = Path(sys.argv[1])
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    orchestrator = Orchestrator(str(vault_path))
    
    # Parse command
    command = sys.argv[2] if len(sys.argv) > 2 else 'run'
    
    if command == 'status':
        print_status(orchestrator)
    elif command == 'process':
        print("Processing pending items...\n")
        orchestrator.run_once()
        print("Processing complete")
        print_status(orchestrator)
    elif command == 'run':
        print(f"\nAI Employee Orchestrator Started")
        print(f"Vault: {vault_path}")
        print(f"Qwen Code: {'Available' if orchestrator.qwen_available else 'Not Available'}")
        print(f"\nPress Ctrl+C to stop.\n")
        orchestrator.run()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python orchestrator.py <vault_path> [run|process|status]")
        sys.exit(1)


if __name__ == "__main__":
    main()
