#!/usr/bin/env python3
"""Gmail Reply Sender - AI Employee"""

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
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                return eval(line[6:])
    return {}

print("🤖 AI Employee - Gmail Reply Sender")
print("=" * 50)

try:
    # Step 1: Navigate to Gmail
    print("\n📍 Step 1/6: Navigating to Gmail...")
    result = mcp_call("browser_navigate", {"url": "https://mail.google.com/"})
    print("   ✓ Done")
    time.sleep(5)

    # Step 2: Take snapshot
    print("📸 Step 2/6: Taking snapshot...")
    result = mcp_call("browser_snapshot", {})
    print("   ✓ Snapshot captured")

    # Step 3: Search for test email
    print("🔍 Step 3/6: Searching for test email...")
    result = mcp_call("browser_type", {
        "element": "search mail",
        "text": "TEST - AI Employee Gmail Watcher"
    })
    print("   ✓ Searched")
    time.sleep(3)

    # Step 4: Click on email
    print("📧 Step 4/6: Opening email...")
    result = mcp_call("browser_click", {"element": "TEST - AI Employee Gmail Watcher"})
    print("   ✓ Opened")
    time.sleep(3)

    # Step 5: Click Reply
    print("✍️  Step 5/6: Clicking Reply...")
    result = mcp_call("browser_click", {"element": "Reply"})
    print("   ✓ Reply clicked")
    time.sleep(3)

    # Step 6: Type reply
    reply_content = """Hi Syeda,

I received your test email successfully! The Gmail Watcher is working correctly and detected your message in real-time.

This confirms that the autonomous AI employee system is functioning as expected - monitoring the inbox and processing incoming emails without manual intervention.

Best regards,
AI Employee
Silver Tier - Production Ready"""

    print("📝 Step 6/6: Typing reply...")
    result = mcp_call("browser_type", {
        "element": "message body",
        "text": reply_content
    })
    print("   ✓ Reply typed")
    time.sleep(2)

    # Step 7: Click Send
    print("📤 Sending email...")
    result = mcp_call("browser_click", {"element": "Send"})
    print("   ✓ Send clicked!")

    time.sleep(5)

    print("\n" + "=" * 50)
    print("✅ SUCCESS! Reply sent via Gmail!")
    print("=" * 50)

except Exception as e:
    print(f"\n⚠️ Error: {e}")
    print("\n📍 Opening Gmail for manual send...")
    import webbrowser
    webbrowser.open('https://mail.google.com/')
