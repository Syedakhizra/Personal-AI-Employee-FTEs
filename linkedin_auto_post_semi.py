#!/usr/bin/env python3
"""LinkedIn Auto-Post - Semi-Automated (Reads from Approved Folder)"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import time

print("\n🔗 LinkedIn Auto-Post (Semi-Automated)")
print("=" * 60)

SESSION_FILE = Path(__file__).parent / "linkedin_session.json"
VAULT_PATH = Path(__file__).parent / "AI_Employee_Vault"
APPROVED_FOLDER = VAULT_PATH / "Approved" / "Social_Media"
DONE_FOLDER = VAULT_PATH / "Done"

# Check for approved LinkedIn post files
approved_files = list(APPROVED_FOLDER.glob("*.md")) if APPROVED_FOLDER.exists() else []

if not approved_files:
    # Check Needs_Action for new posts
    needs_action = VAULT_PATH / "Needs_Action"
    if needs_action.exists():
        post_files = list(needs_action.glob("LINKEDIN_Post_*.md"))
        if post_files:
            print("\n⚠️  Found unapproved posts!")
            print("\nApprove them first:")
            for f in post_files:
                print(f"  - {f.name}")
            print("\nMove to Approved/Social_Media/ folder")
            input("\nPress Enter to exit...")
            exit(1)
    
    print("\n❌ No approved LinkedIn posts found!")
    print("\nSteps:")
    print("1. Run: python AI_Employee_Vault/watchers/linkedin_post_generator.py")
    print("2. Move file to /Approved/Social_Media/ folder")
    print("3. Run this script again")
    input("\nPress Enter to exit...")
    exit(1)

# Get the latest approved file
latest_file = sorted(approved_files)[-1]
print(f"\n✅ Found approved post: {latest_file.name}")

# Read content from approved file
print("📖 Reading content from approved file...")
content_text = latest_file.read_text(encoding='utf-8')

# Extract content between ## Content and ---
if "## Content" in content_text:
    content = content_text.split("## Content", 1)[1]
    if "---" in content:
        content = content.split("---")[0]
    content = content.strip()
else:
    content = content_text[:500]  # Fallback

print(f"   ✅ Content loaded ({len(content)} chars)")

if not SESSION_FILE.exists():
    print("\n❌ Session file not found!")
    print("First run: python linkedin_login_save.py")
    input("\nPress Enter to exit...")
    exit(1)

print("\n📍 Launching browser with saved session...")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(Path(__file__).parent / "playwright-profile"),
        headless=False,
        args=[
            '--disable-gpu',
            '--no-sandbox',
            '--disable-dev-shm-usage'
        ]
    )
    
    page = browser.pages[0] if browser.pages else browser.new_page()
    
    # Navigate to LinkedIn
    print("🌐 Opening LinkedIn feed...")
    page.goto("https://www.linkedin.com/feed/")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(10000)
    
    print("\n" + "=" * 60)
    print("👉 STEP 1: Click 'Start a post' button manually")
    print("=" * 60)
    print("\n   It's at the top of your feed.")
    print("   Looks like a box that says 'Start a post'")
    print("\n⏳ Waiting for you to click...")
    input("\n   Press Enter AFTER you clicked 'Start a post'...")
    
    # Wait for dialog to open
    page.wait_for_timeout(3000)
    
    # Check if dialog opened
    if not page.query_selector('div[role="textbox"]'):
        print("\n   ❌ Dialog not opened yet")
        print("   Please click 'Start a post' at the top of your feed")
        page.wait_for_timeout(30000)
    
    if not page.query_selector('div[role="textbox"]'):
        print("\n   ❌ Still not opened. Exiting...")
        browser.close()
        exit(1)
    
    print("\n   ✅ Dialog detected!")
    
    # Type content
    print(f"\n📝 STEP 2: Typing content ({len(content)} chars)...")
    try:
        textbox = page.locator('div[role="textbox"]').first
        textbox.fill(content)
        page.wait_for_timeout(3000)
        print("   ✅ Content typed!")
    except Exception as e:
        print(f"   ⚠️  Auto-type failed: {e}")
        print("   Please paste this content manually:")
        print("=" * 60)
        print(content)
        print("=" * 60)
        print("\n⏳ Waiting 30 seconds for you to paste...")
        page.wait_for_timeout(30000)
    
    # Click Post
    print("\n📤 STEP 3: Publishing post...")
    print("   (Waiting 5 seconds for you to click Post manually)")
    print("   The 'Post' button should be highlighted")
    
    # Try auto-click first
    try:
        post_btn = page.locator('button:has-text("Post")').first
        if post_btn.is_enabled():
            post_btn.click()
            page.wait_for_timeout(5000)
            print("   ✅ Auto-posted!")
        else:
            print("   ⏳ Please click 'Post' button manually...")
            page.wait_for_timeout(30000)
    except:
        print("   ⏳ Please click 'Post' button manually...")
        page.wait_for_timeout(30000)
    
    # Verify
    print("\n📍 Verifying post...")
    page.goto("https://www.linkedin.com/feed/")
    page.wait_for_timeout(5000)
    
    print("\n" + "=" * 60)
    print("✅ DONE!")
    print("=" * 60)
    print("\n📍 Check your post: https://www.linkedin.com/feed/")
    print("=" * 60)
    
    # Move file to Done folder
    print(f"\n📁 Moving to Done folder...")
    DONE_FOLDER.mkdir(parents=True, exist_ok=True)
    latest_file.rename(DONE_FOLDER / latest_file.name)
    print(f"   ✅ Moved: {latest_file.name}")
    
    browser.close()

input("\nPress Enter to exit...")
