#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base Watcher - Abstract base class for all AI Employee watchers.

Watchers are lightweight Python scripts that run continuously in the background,
monitoring various inputs (Gmail, WhatsApp, filesystem, etc.) and creating
actionable .md files for Claude Code to process.

All watchers follow the same pattern:
1. Poll for new items at regular intervals
2. Create .md files in /Needs_Action folder
3. Track processed items to avoid duplicates
"""

import time
import logging
<<<<<<< HEAD
=======
import os
>>>>>>> edbe72d (silver tier)
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher implementations.
    
    Subclasses must implement:
    - check_for_updates(): Return list of new items to process
    - create_action_file(item): Create .md file in Needs_Action folder
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        self.logs = self.vault_path / 'Logs'
        self.check_interval = check_interval
        
        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Track processed items (in-memory for now)
        self.processed_ids: set = set()
        
        # State file for persistence across restarts
        self.state_file = self.vault_path / f'.watcher_{self.__class__.__name__}.state'
        self._load_state()
        
    def _setup_logging(self):
        """Configure logging to file and console."""
        log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}_{self.__class__.__name__}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _load_state(self):
        """Load processed IDs from state file (if exists)."""
        if self.state_file.exists():
            try:
                content = self.state_file.read_text()
                self.processed_ids = set(content.strip().split('\n')) - {''}
                self.logger.info(f"Loaded {len(self.processed_ids)} processed IDs from state")
            except Exception as e:
                self.logger.warning(f"Could not load state file: {e}")
                self.processed_ids = set()
        else:
            self.processed_ids = set()
    
    def _save_state(self):
        """Save processed IDs to state file."""
        try:
            content = '\n'.join(str(id) for id in self.processed_ids)
<<<<<<< HEAD
            self.state_file.write_text(content)
        except Exception as e:
            self.logger.error(f"Could not save state file: {e}")
=======
            with open(self.state_file, 'w', encoding='utf-8') as f:
                f.write(content)
                f.flush()  # Force flush to disk
                os.fsync(f.fileno())  # Ensure data is written to disk
            self.logger.info(f"Saved {len(self.processed_ids)} processed IDs to state file")
        except Exception as e:
            self.logger.error(f"Could not save state file: {e}")
            self.logger.error(f"State file path: {self.state_file}")
            self.logger.error(f"Processed IDs count: {len(self.processed_ids)}")
>>>>>>> edbe72d (silver tier)
    
    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process.
        
        Returns:
            List of new items (each item should have a unique 'id' field)
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create a .md action file for an item.
        
        Args:
            item: The item to process
            
        Returns:
            Path to the created file
        """
        pass
    
    def _create_frontmatter(self, item_type: str, item_id: str, **kwargs) -> str:
        """
        Create YAML frontmatter for action files.
        
        Args:
            item_type: Type of item (email, whatsapp, file_drop, etc.)
            item_id: Unique identifier
            **kwargs: Additional frontmatter fields
            
        Returns:
            YAML frontmatter string
        """
        frontmatter = f"""---
type: {item_type}
id: {item_id}
received: {datetime.now().isoformat()}
status: pending
priority: normal
"""
        for key, value in kwargs.items():
            frontmatter += f"{key}: {value}\n"
        
        frontmatter += "---\n"
        return frontmatter
    
    def run(self):
        """
        Main run loop for the watcher.
        
        Continuously checks for updates and creates action files.
        Saves state periodically to survive restarts.
        """
        self.logger.info(f"Starting {self.__class__.__name__}")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info(f"Check interval: {self.check_interval}s")
        
        try:
            while True:
                try:
                    # Check for new items
                    items = self.check_for_updates()
                    
                    if items:
                        self.logger.info(f"Found {len(items)} new item(s)")
                    
                    for item in items:
                        try:
                            filepath = self.create_action_file(item)
                            self.logger.info(f"Created action file: {filepath.name}")
<<<<<<< HEAD
                            
                            # Track as processed
                            item_id = item.get('id', str(filepath))
                            self.processed_ids.add(item_id)
                            
                        except Exception as e:
                            self.logger.error(f"Error creating action file: {e}")
                    
                    # Save state every cycle
=======

                            # Track as processed
                            item_id = item.get('id', str(filepath))
                            self.processed_ids.add(item_id)

                            # Save state immediately after each file
                            self._save_state()

                        except Exception as e:
                            self.logger.error(f"Error creating action file: {e}")

                    # Also save state at end of cycle
>>>>>>> edbe72d (silver tier)
                    self._save_state()
                    
                except Exception as e:
                    self.logger.error(f"Error in check cycle: {e}")
                
                # Wait before next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Watcher stopped by user")
            self._save_state()
        except Exception as e:
            self.logger.error(f"Fatal error: {e}")
            self._save_state()
            raise
    
    def stop(self):
        """Clean shutdown of the watcher."""
        self.logger.info("Stopping watcher...")
        self._save_state()


# Utility function for common watcher operations
def sanitize_filename(name: str) -> str:
    """
    Sanitize a string for use as a filename.
    
    Args:
        name: Original name
        
    Returns:
        Sanitized filename-safe string
    """
    # Remove or replace problematic characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip()


def extract_keywords(text: str, keywords: list) -> list:
    """
    Extract matching keywords from text.
    
    Args:
        text: Text to search
        keywords: List of keywords to look for
        
    Returns:
        List of matched keywords
    """
    text_lower = text.lower()
    return [kw for kw in keywords if kw.lower() in text_lower]
