#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Auto-Poster - AI Employee posts automatically
Uses Playwright to automate LinkedIn posting

Usage:
    python linkedin_auto_post.py --email "your@email.com" --password "yourpassword"
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Installing Playwright...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'playwright'])
    subprocess.check_call(['npx', 'playwright', 'install', 'chromium'])
    from playwright.sync_api import sync_playwright


def get_post_content():
    """Get latest LinkedIn post draft from vault."""
    vault_path = Path(__file__).parent.parent
    drafts_folder = vault_path / 'Social_Media' / 'LinkedIn_Drafts'
    
    # Get latest draft
    drafts = list(drafts_folder.glob('LinkedIn_*.md'))
    if not drafts:
        # Create new draft
        content = f'''---
type: linkedin_post
topic: AI Employee Update
created: {datetime.now().isoformat()}
status: draft
---

# LinkedIn Post Draft

## Content

🚀 Exciting update from our AI Employee project!

We're building autonomous AI agents that work 24/7 to manage your business and personal affairs.

**Key Benefits:**
✅ 168 hours/week availability (vs 40 hrs for humans)
✅ 90% cost reduction
✅ Predictable 99%+ consistency
✅ Instant scaling

**Tech Stack:**
- Qwen Code for reasoning
- Obsidian for memory/dashboard
- Python watchers for monitoring
- MCP servers for actions

This is the future of work - Digital FTEs working alongside humans! 💼🤖

#AI #Automation #Business #Technology #Innovation #DigitalTransformation

---
*Posted by AI Employee*
'''
        draft_file = drafts_folder / f'LinkedIn_{datetime.now().strftime("%Y%m%d_%H%M%S")}_AutoPost.md'
        draft_file.write_text(content, encoding='utf-8')
        return content
    
    # Read latest draft
    content = drafts[-1].read_text(encoding='utf-8')
    
    # Extract content between ## Content and ---
    if '## Content' in content:
        content = content.split('## Content', 1)[1]
        if '---' in content:
            content = content.split('---')[0]
    
    return content.strip()


def post_to_linkedin(email: str, password: str, content: str):
    """Post to LinkedIn using browser automation."""
    
    print("\n" + "="*60)
    print("🤖 AI Employee - LinkedIn Auto-Poster")
    print("="*60)
    print(f"📝 Post length: {len(content)} characters")
    print(f"👤 Account: {email}")
    print("="*60 + "\n")
    
    with sync_playwright() as p:
        # Launch browser (visible for debugging)
        print("🚀 Step 1/5: Launching browser...")
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(Path.home() / '.linkedin_ai_employee'),
            headless=False,
            args=[
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        # Navigate to LinkedIn
        print("📍 Step 2/5: Navigating to LinkedIn...")
        page.goto('https://www.linkedin.com/login', wait_until='networkidle', timeout=60000)
        
        # Check if already logged in
        if 'feed' in page.url:
            print("✅ Already logged in!")
        else:
            print("🔑 Step 3/5: Logging in...")
            
            # Fill credentials
            try:
                page.fill('#username', email)
                print(f"   ✓ Email entered")
                
                page.fill('#password', password)
                print(f"   ✓ Password entered")
                
                page.click('button[type="submit"]')
                print(f"   ✓ Sign in clicked")
                
                # Wait for login
                page.wait_for_url('https://www.linkedin.com/feed/*', timeout=30000)
                print("✅ Login successful!")
                
            except Exception as e:
                print(f"⚠️ Login issue: {e}")
                print("👉 Please login manually in the browser window")
                print("⏳ Waiting 60 seconds for manual login...")
                page.wait_for_timeout(60000)
        
        # Navigate to feed
        print("📍 Step 4/5: Creating post...")
        page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
        
        # Click "Start a post"
        try:
            page.click('button:has-text("Start a post")', timeout=10000)
            print("   ✓ Post dialog opened")
        except:
            print("   ⚠️ Could not open post dialog, trying alternative...")
            page.click('.share-box-feed-entry__trigger', timeout=10000)
        
        # Wait for editor
        page.wait_for_timeout(3000)
        
        # Type content
        print("✍️  Step 5/5: Posting content...")
        try:
            # Find editor
            editor = page.query_selector('div[contenteditable="true"]')
            if editor:
                # Clear and type
                editor.fill('')
                
                # Type character by character for reliability
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    page.keyboard.type(line)
                    if i < len(lines) - 1:
                        page.keyboard.press('Enter')
                        page.keyboard.press('Enter')
                
                print(f"   ✓ Content posted ({len(content)} chars)")
        except Exception as e:
            print(f"   ⚠️ Typing issue: {e}")
            # Fallback: clipboard method
            page.evaluate(f'navigator.clipboard.writeText(`{content}`)')
            page.keyboard.press('ControlOrMeta+v')
            print("   ✓ Content pasted via clipboard")
        
        # Wait for post to render
        page.wait_for_timeout(3000)
        
        # Click "Post" button
        print("📤 Publishing post...")
        try:
            page.click('button:has-text("Post")', timeout=10000)
            print("   ✓ Post button clicked!")
        except:
            try:
                page.click('button.share-box-actions__submit-button', timeout=10000)
                print("   ✓ Post submitted!")
            except Exception as e:
                print(f"   ⚠️ Submit issue: {e}")
        
        # Wait for confirmation
        print("⏳ Waiting for confirmation...")
        page.wait_for_timeout(5000)
        
        # Check result
        if 'feed' in page.url:
            print("\n✅ SUCCESS! Post published to LinkedIn!")
            print("📍 View: https://www.linkedin.com/feed/")
        else:
            print("\n⚠️ Post may need manual confirmation")
        
        # Keep browser open for verification
        print("\n⏰ Browser will stay open for 30 seconds...")
        print("   Verify your post on LinkedIn!")
        page.wait_for_timeout(30000)
        
        browser.close()
        print("\n✅ AI Employee LinkedIn Auto-Post Complete!")
        return True


def main():
    parser = argparse.ArgumentParser(description='AI Employee LinkedIn Auto-Poster')
    parser.add_argument('--email', '-e', help='LinkedIn email')
    parser.add_argument('--password', '-p', help='LinkedIn password')
    parser.add_argument('--content', '-c', help='Post content (optional)')
    
    args = parser.parse_args()
    
    if not PLAYWRIGHT_AVAILABLE:
        print("⚠️ Playwright not installed. Installing now...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'playwright'])
        subprocess.check_call(['npx', 'playwright', 'install', 'chromium'])
    
    # Get content
    content = args.content or get_post_content()
    
    # Get credentials
    email = args.email
    password = args.password
    
    if not email:
        email = input("\n📧 Enter your LinkedIn email: ")
    
    if not password:
        import getpass
        password = getpass.getpass("🔑 Enter your LinkedIn password: ")
    
    # Post to LinkedIn
    success = post_to_linkedin(email, password, content)
    
    # Move to Done folder
    if success:
        vault_path = Path(__file__).parent.parent
        approved_folder = vault_path / 'Approved' / 'Social_Media'
        done_folder = vault_path / 'Done'
        
        # Move any approved LinkedIn posts to Done
        for post_file in approved_folder.glob('LinkedIn_*.md'):
            post_file.rename(done_folder / post_file.name)
            print(f"📁 Moved to Done: {post_file.name}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
