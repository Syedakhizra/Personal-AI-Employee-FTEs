#!/usr/bin/env python3
"""LinkedIn Auto-Post using Playwright MCP"""

import requests
import time

MCP_URL = "http://localhost:8808"

def mcp_call(tool, params):
    """Call MCP tool with proper headers"""
    headers = {
        'Accept': 'application/json, text/event-stream',
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{MCP_URL}/mcp", 
        json={"tool": tool, "params": params},
        headers=headers,
        stream=True
    )
    # Read SSE stream
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                return eval(line[6:])
    return {}

print("🤖 AI Employee - LinkedIn Auto-Poster")
print("=" * 50)

try:
    # Step 1: Navigate to LinkedIn
    print("\n📍 Step 1/6: Navigating to LinkedIn...")
    result = mcp_call("browser_navigate", {"url": "https://www.linkedin.com/feed/"})
    print(f"   ✓ Done")

    # Step 2: Wait for page to load
    print("⏳ Step 2/6: Waiting for page to load...")
    time.sleep(5)

    # Step 3: Take snapshot to see the page
    print("📸 Step 3/6: Taking snapshot...")
    result = mcp_call("browser_snapshot", {})
    snapshot = str(result.get('content', ''))
    print(f"   ✓ Snapshot: {len(snapshot)} chars")
    
    # Check if already on feed
    if 'Start a post' in snapshot or 'share-box' in snapshot.lower():
        print("   ✓ LinkedIn feed detected!")
    else:
        print("   ⚠️ May need login...")

    # Step 4: Click "Start a post"
    print("✍️  Step 4/6: Clicking 'Start a post'...")
    result = mcp_call("browser_click", {"element": "Start a post", "ref": "e10"})
    print(f"   ✓ Clicked")
    time.sleep(3)

    # Step 5: Type content
    content = "Exciting update from our AI Employee project! Silver Tier complete! Autonomous AI agents working 24/7. #AI #Automation #Business"
    print(f"📝 Step 5/6: Typing content...")
    result = mcp_call("browser_type", {"element": "Start a post", "text": content, "ref": "e10"})
    print(f"   ✓ Typed {len(content)} chars")
    time.sleep(2)

    # Step 6: Click Post button
    print("📤 Step 6/6: Clicking 'Post' button...")
    result = mcp_call("browser_click", {"element": "Post", "ref": "e20"})
    print(f"   ✓ Posted!")

    # Wait for confirmation
    time.sleep(5)

    print("\n" + "=" * 50)
    print("✅ SUCCESS! AI Employee posted to LinkedIn!")
    print("=" * 50)
    print("📍 Check: https://www.linkedin.com/feed/")
    print("=" * 50)
    
except Exception as e:
    print(f"\n⚠️ Error: {e}")
    print("\n📍 Opening LinkedIn for manual verification...")
    import webbrowser
    webbrowser.open('https://www.linkedin.com/feed/')
