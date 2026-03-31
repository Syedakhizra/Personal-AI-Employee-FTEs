#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File System Watcher - Monitors a drop folder for new files.

This is the Bronze Tier watcher - it monitors a folder for any new files
dropped by the user and creates action files for Claude Code to process.

Usage:
    python filesystem_watcher.py /path/to/vault

The watcher will:
1. Monitor the /Inbox folder for new files
2. Copy files to /Needs_Action with metadata
3. Create accompanying .md file with file info
4. Track processed files to avoid duplicates
"""

import os
import sys
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from base_watcher import BaseWatcher, sanitize_filename


class FilesystemWatcher(BaseWatcher):
    """
    Watcher that monitors a drop folder for new files.
    
    When a file is detected:
    1. Copy it to /Needs_Action/
    2. Create a .md metadata file
    3. Claude Code will process and move to /Done/
    """
    
    def __init__(self, vault_path: str, check_interval: int = 5):
        """
        Initialize the filesystem watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 5 for responsive file drops)
        """
        super().__init__(vault_path, check_interval)
        
        # Watch the Inbox folder for incoming files
        self.watch_folder = self.inbox
        
        # Also watch a separate drop folder if configured
        self.drop_folder = Path(os.getenv('DROP_FOLDER', self.watch_folder))
        
        self.logger.info(f"Watching folder: {self.watch_folder}")
        self.logger.info(f"Drop folder: {self.drop_folder}")
    
    def _get_file_hash(self, filepath: Path) -> str:
        """
        Calculate MD5 hash of a file for duplicate detection.
        
        Args:
            filepath: Path to the file
            
        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Error hashing file: {e}")
            return str(filepath)
    
    def _get_file_info(self, filepath: Path) -> Dict[str, Any]:
        """
        Get file metadata.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dictionary with file information
        """
        try:
            stat = filepath.stat()
            return {
                'name': filepath.name,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'extension': filepath.suffix.lower(),
                'path': str(filepath),
            }
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return {
                'name': filepath.name,
                'size': 0,
                'extension': filepath.suffix.lower(),
                'path': str(filepath),
            }
    
    def _scan_folder(self, folder: Path) -> List[Path]:
        """
        Scan a folder for new files.
        
        Args:
            folder: Folder to scan
            
        Returns:
            List of new file paths
        """
        new_files = []
        
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            return new_files
        
        try:
            for filepath in folder.iterdir():
                if filepath.is_file():
                    file_hash = self._get_file_hash(filepath)
                    
                    # Check if already processed
                    if file_hash not in self.processed_ids:
                        self.logger.info(f"New file detected: {filepath.name}")
                        new_files.append({
                            'path': filepath,
<<<<<<< HEAD
                            'hash': file_hash
=======
                            'hash': file_hash,
                            'id': file_hash  # Add id field for base class
>>>>>>> edbe72d (silver tier)
                        })
        except Exception as e:
            self.logger.error(f"Error scanning folder: {e}")
        
        return new_files
    
    def check_for_updates(self) -> list:
        """
        Check for new files in the watch folder.
        
        Returns:
            List of new file dictionaries
        """
        new_files = []
        
        # Scan inbox folder
        inbox_files = self._scan_folder(self.watch_folder)
        new_files.extend(inbox_files)
        
        # Scan drop folder if different
        if self.drop_folder != self.watch_folder:
            drop_files = self._scan_folder(self.drop_folder)
            # Avoid duplicates
            for f in drop_files:
                if f['hash'] not in [x['hash'] for x in new_files]:
                    new_files.append(f)
        
        return new_files
    
    def create_action_file(self, item) -> Path:
        """
        Create a .md action file for a dropped file.
        
        Args:
            item: Dictionary with 'path' and 'hash' keys
            
        Returns:
            Path to the created metadata file
        """
        source_path = item['path']
        file_hash = item['hash']
        
        # Get file info
        file_info = self._get_file_info(source_path)
        
        # Create sanitized filename
        safe_name = sanitize_filename(file_info['name'])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Destination paths
        dest_file = self.needs_action / f"FILE_{timestamp}_{safe_name}"
        meta_file = self.needs_action / f"FILE_{timestamp}_{safe_name}.md"
        
        # Copy the file to Needs_Action
        try:
            shutil.copy2(source_path, dest_file)
            self.logger.info(f"Copied file to: {dest_file.name}")
        except Exception as e:
            self.logger.error(f"Error copying file: {e}")
            raise
        
        # Create metadata markdown file
        content = self._create_frontmatter(
            item_type="file_drop",
<<<<<<< HEAD
            id=file_hash,
=======
            item_id=file_hash,
>>>>>>> edbe72d (silver tier)
            original_name=f'"{file_info["name"]}"',
            file_size=file_info['size'],
            file_type=f'"{file_info["extension"]}"',
            received=f'"{file_info["modified"]}"'
        )
        
        content += f"""
## File Dropped for Processing

**Original Name:** {file_info['name']}
**Size:** {self._format_size(file_info['size'])}
**Type:** {file_info['extension']}
**Modified:** {file_info['modified']}

---

## Content Preview

<!-- AI Employee: Analyze this file and suggest actions -->

"""
        
        # Add content preview for text files
        if file_info['extension'] in ['.txt', '.md', '.py', '.js', '.json', '.csv', '.xml', '.html']:
            try:
                preview = source_path.read_text(encoding='utf-8', errors='ignore')[:1000]
                content += f"""
```{file_info['extension'].lstrip('.')}
{preview}
{"..." if len(preview) >= 1000 else ""}
```

"""
            except Exception as e:
                content += f"*Could not preview file: {e}*\n\n"
        
        content += f"""
## Suggested Actions

- [ ] Review file content
- [ ] Categorize file
- [ ] Take appropriate action
- [ ] Move to /Done when complete

---
*Detected by File System Watcher at {datetime.now().isoformat()}*
"""
        
        # Write metadata file
        meta_file.write_text(content)
        
        # Remove original from inbox (we've copied it)
        try:
            source_path.unlink()
            self.logger.info(f"Removed original from inbox: {source_path.name}")
        except Exception as e:
            self.logger.warning(f"Could not remove original file: {e}")
        
        return meta_file
    
    def _format_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted string (e.g., "1.5 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"


def main():
    """Main entry point for the filesystem watcher."""
    if len(sys.argv) < 2:
        # Try to find vault relative to script location
        vault_path = Path(__file__).parent.parent
        print(f"Using vault path: {vault_path}")
    else:
        vault_path = Path(sys.argv[1])

    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)

    watcher = FilesystemWatcher(str(vault_path), check_interval=5)

    print(f"\nFile System Watcher Started")
    print(f"Watching: {watcher.watch_folder}")
    print(f"Output: {watcher.needs_action}")
    print(f"\nDrop files into the Inbox folder to trigger processing.")
    print("Press Ctrl+C to stop.\n")

    watcher.run()


if __name__ == "__main__":
    main()
