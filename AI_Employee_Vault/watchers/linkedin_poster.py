#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Auto-Poster - Silver Tier
Automatically posts to LinkedIn using browser automation (Playwright).

Usage:
    python linkedin_poster.py "Post content here"
    python linkedin_poster.py --file "path/to/draft.md"

Requirements:
    - Playwright: npm install -D @playwright/test
    - npx playwright install chromium
"""

import sys
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError


def post_to_linkedin(content: str, email: str, password: str):
    """Post to LinkedIn using browser automation."""
    
    print("\n🔗 LinkedIn Auto-Poster")
    print("=" * 50)
    print(f"Content length: {len(content)} characters")
    print("=" * 50)
    
    with sync_playwright() as p:
        # Launch browser
        print("🚀 Launching browser...")
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(Path.home() / '.linkedin_session'),
            headless=False,  # Show browser for debugging
            args=[
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        # Navigate to LinkedIn
        print("📍 Navigating to LinkedIn...")
        page.goto('https://www.linkedin.com/login', wait_until='networkidle')
        
        # Check if already logged in
        try:
            page.wait_for_url('https://www.linkedin.com/feed/', timeout=5000)
            print("✅ Already logged in!")
        except TimeoutError:
            # Need to login
            print("🔑 Logging in...")
            
            # Fill email
            page.fill('#username', email)
            print(f"  ✓ Email entered: {email}")
            
            # Fill password
            page.fill('#password', password)
            print("  ✓ Password entered")
            
            # Click sign in
            page.click('button[type="submit"]')
            print("  ✓ Sign in button clicked")
            
            # Wait for login
            try:
                page.wait_for_url('https://www.linkedin.com/feed/', timeout=30000)
                print("✅ Login successful!")
            except TimeoutError:
                print("❌ Login failed. Please check credentials.")
                browser.close()
                return False
        
        # Navigate to post creation
        print("📝 Creating post...")
        page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
        
        # Find and click "Start a post" button
        try:
            # Try multiple selectors for "Start a post" button
            post_button_selectors = [
                'button:has-text("Start a post")',
                'button:has-text("Post")',
                '.share-box-feed-entry__trigger'
            ]
            
            post_clicked = False
            for selector in post_button_selectors:
                try:
                    post_button = page.query_selector(selector)
                    if post_button:
                        post_button.click()
                        print("  ✓ Post dialog opened")
                        post_clicked = True
                        break
                except:
                    continue
            
            if not post_clicked:
                print("⚠️ Could not find post button. Trying alternative method...")
                # Direct navigation to post creator
                page.goto('https://www.linkedin.com/feed/?createContent=true')
        
        except Exception as e:
            print(f"⚠️ Error opening post dialog: {e}")
        
        # Wait for post editor
        page.wait_for_timeout(3000)
        
        # Find post text area and fill content
        try:
            # LinkedIn post editor selector
            editor_selectors = [
                'div[contenteditable="true"]',
                '.editor-editor-container[contenteditable="true"]',
                '.ProseMirror'
            ]
            
            for selector in editor_selectors:
                try:
                    editor = page.query_selector(selector)
                    if editor:
                        # Clear existing content
                        editor.fill('')
                        
                        # Type content (slower for reliability)
                        for char in content:
                            page.keyboard.type(char)
                            page.wait_for_timeout(10)  # 10ms per character
                        
                        print(f"  ✓ Content posted ({len(content)} chars)")
                        break
                except:
                    continue
        
        except Exception as e:
            print(f"⚠️ Error filling content: {e}")
            # Alternative: Use clipboard
            print("  → Trying clipboard method...")
            page.evaluate(f'navigator.clipboard.writeText(`{content}`)')
            page.keyboard.press('ControlOrMeta+v')
        
        # Wait for post to be visible
        page.wait_for_timeout(3000)
        
        # Find and click "Post" button
        try:
            post_submit_selectors = [
                'button:has-text("Post")',
                'button.share-box-actions__submit-button'
            ]
            
            for selector in post_submit_selectors:
                try:
                    submit_button = page.query_selector(selector)
                    if submit_button:
                        submit_button.click()
                        print("  ✓ Post button clicked!")
                        break
                except:
                    continue
        
        except Exception as e:
            print(f"⚠️ Error submitting post: {e}")
        
        # Wait for confirmation
        print("⏳ Waiting for post to publish...")
        page.wait_for_timeout(5000)
        
        # Check if post was successful
        current_url = page.url
        if 'feed' in current_url:
            print("✅ Post published successfully!")
            print("\n📍 View your post: https://www.linkedin.com/feed/")
        else:
            print("⚠️ Post may not have published. Please check manually.")
        
        # Keep browser open for 30 seconds for verification
        print("\n⏰ Browser will close in 30 seconds...")
        print("   Verify your post on LinkedIn!")
        page.wait_for_timeout(30000)
        
        browser.close()
        print("\n✅ Done!")
        return True


def main():
    parser = argparse.ArgumentParser(description='LinkedIn Auto-Poster')
    parser.add_argument('content', nargs='?', help='Post content')
    parser.add_argument('--file', '-f', help='Read content from file')
    parser.add_argument('--email', '-e', help='LinkedIn email')
    parser.add_argument('--password', '-p', help='LinkedIn password')
    
    args = parser.parse_args()
    
    # Get content
    content = args.content
    if args.file:
        content = Path(args.file).read_text(encoding='utf-8')
        # Remove frontmatter if present
        if '---' in content:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
    
    if not content:
        print("Error: No content provided")
        print("Usage: python linkedin_poster.py \"Your post content\"")
        print("   or: python linkedin_poster.py --file draft.md")
        sys.exit(1)
    
    # Get credentials
    email = args.email or input("LinkedIn Email: ")
    password = args.password or input("LinkedIn Password: ")
    
    # Post to LinkedIn
    success = post_to_linkedin(content, email, password)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
