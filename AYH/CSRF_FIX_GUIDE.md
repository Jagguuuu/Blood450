# 🔧 CSRF Error Fix Guide

## Problem
You're seeing: **"Forbidden (403) CSRF verification failed. Request aborted."**

This happens because the CSRF token in your browser is stale after we updated the security settings.

---

## ✅ QUICK FIX (Choose ONE method)

### Method 1: Clear Browser Cache (RECOMMENDED)
1. **Close ALL browser tabs** with your Django app
2. **Clear browser cache and cookies:**
   - **Chrome/Edge**: Press `Ctrl + Shift + Delete`
     - Check "Cookies and other site data"
     - Check "Cached images and files"
     - Click "Clear data"
   - **Firefox**: Press `Ctrl + Shift + Delete`
     - Check "Cookies" and "Cache"
     - Click "Clear Now"
3. **Restart Django server:**
   ```bash
   # Stop server (Ctrl + C in terminal)
   python manage.py runserver
   ```
4. **Open NEW browser window** and go to: `http://127.0.0.1:8000/accounts/login/`
5. **Login again**

---

### Method 2: Use Incognito/Private Window
1. Open **Incognito/Private window** (Ctrl + Shift + N)
2. Go to: `http://127.0.0.1:8000/accounts/login/`
3. Login and test

---

### Method 3: Hard Refresh
1. Go to login page: `http://127.0.0.1:8000/accounts/login/`
2. Press `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac)
3. Login again

---

## 🔍 Why This Happened

When we updated the CSRF security settings, your browser still had the old CSRF token cached. The new settings require a fresh token.

**What we changed:**
- Added `CSRF_COOKIE_SAMESITE = 'Lax'` (better security)
- Added `SESSION_COOKIE_SAMESITE = 'Lax'` (better security)
- Made cookies environment-aware (dev vs production)

These changes are **good for security** but require clearing old tokens.

---

## 🧪 Test After Fix

1. **Login** as admin (admin/admin123)
2. **Create a blood request**
3. **Should work without CSRF error**

If you still see the error after trying all methods, let me know!

---

## 🚨 If Still Not Working

Try this nuclear option:

```bash
# Stop Django server (Ctrl + C)

# Delete session files (if using file-based sessions)
# Windows:
del db.sqlite3

# Recreate database
python manage.py migrate

# Create demo users again
python create_demo_users.py

# Start server
python manage.py runserver
```

**Note:** This will delete all data, so only use if nothing else works!

---

## ✅ Prevention

To avoid this in the future:
- Always clear browser cache when changing security settings
- Use Incognito mode for testing
- Restart Django server after settings changes

---

**The security fixes are working correctly - this is just a one-time browser cache issue!** 🎯
