@echo off
echo ============================================================
echo   AI Employee Project - Cleanup Script
echo   Deleting old/test files, keeping only essential files
echo ============================================================
echo.

echo [1/5] Deleting old Gmail reply files...
del gmail_reply_final.py 2>nul
del gmail_reply_fixed.py 2>nul
del gmail_reply_manual.py 2>nul
del gmail_reply_sender.py 2>nul
del gmail_reply_storage.py 2>nul
del gmail_login_clean.py 2>nul
del gmail_login_quick.py 2>nul
del gmail_login_save.py 2>nul
del gmail_session.json 2>nul
echo   Done!

echo.
echo [2/5] Deleting old LinkedIn files...
del linkedin_auto_post_final.py 2>nul
del linkedin_auto_post_fixed.py 2>nul
del linkedin_auto_post_manual.py 2>nul
del linkedin_auto_post_v2.py 2>nul
del linkedin_auto_post_storage.py 2>nul
del linkedin_login_quick.py 2>nul
del linkedin_login_save.py 2>nul
del linkedin_verify.png 2>nul
del linkedin_mcp_post.py 2>nul
echo   Done!

echo.
echo [3/5] Deleting test/debug files...
del debug_browser.py 2>nul
del open_browser_simple.py 2>nul
del open_linkedin.py 2>nul
del start_mcp_persistent.py 2>nul
echo   Done!

echo.
echo [4/5] Deleting Python cache...
rmdir /s /q AI_Employee_Vault\watchers\__pycache__ 2>nul
rmdir /s /q __pycache__ 2>nul
del python 2>nul
echo   Done!

echo.
echo [5/5] Cleaning Playwright profile (optional)...
echo   Keeping profile for faster login...
echo   Done!

echo.
echo ============================================================
echo   CLEANUP COMPLETE!
echo ============================================================
echo.
echo Files kept:
echo   - gmail_auth_send.py (Gmail OAuth)
echo   - gmail_reply_api.py (Gmail API reply)
echo   - gmail_send_token.json (Gmail token)
echo   - linkedin_auto_post_semi.py (LinkedIn poster)
echo   - linkedin_post_generator.py (Content generator)
echo   - AI_Employee_Vault/watchers/*.py (All watchers)
echo   - All documentation files
echo.
echo ============================================================
pause
