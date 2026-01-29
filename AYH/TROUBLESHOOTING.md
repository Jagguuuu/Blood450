# Troubleshooting Guide - Blood Donation System

## Common Issues and Solutions

### 1. CSRF Token Error on Login

**Error Message:** 
```
Forbidden (CSRF token from POST incorrect.): /accounts/login/
[22/Jan/2026 00:56:42] "POST /accounts/login/ HTTP/1.1" 403 2503
```

**Causes:**
- Browser cache issue
- Cookies disabled
- Incognito/Private mode without cookies
- Multiple tabs with stale tokens

**Solutions:**

#### Solution 1: Clear Browser Cache (Recommended)
1. **Chrome/Edge:**
   - Press `Ctrl + Shift + Delete`
   - Select "Cookies and other site data"
   - Select "Cached images and files"
   - Click "Clear data"

2. **Firefox:**
   - Press `Ctrl + Shift + Delete`
   - Select "Cookies" and "Cache"
   - Click "Clear Now"

#### Solution 2: Use Incognito/Private Window
1. Open a new incognito/private window
2. Navigate to `http://127.0.0.1:8000/accounts/login/`
3. Try logging in again

#### Solution 3: Hard Refresh the Page
1. Go to login page
2. Press `Ctrl + Shift + R` (Windows/Linux)
3. Or `Cmd + Shift + R` (Mac)
4. Try logging in again

#### Solution 4: Check Browser Settings
1. Ensure cookies are enabled:
   - Chrome: Settings → Privacy and security → Cookies
   - Enable "Allow all cookies"
2. Disable browser extensions that block cookies
3. Try a different browser

#### Solution 5: Restart Django Server
1. Stop the server (`Ctrl + C` in terminal)
2. Clear browser cache
3. Start server again: `python manage.py runserver`
4. Open fresh browser window
5. Navigate to login page

#### Solution 6: Use Different Port
```bash
python manage.py runserver 8080
```
Then access: `http://127.0.0.1:8080/accounts/login/`

---

### 2. "Module 'careapp' Not Found"

**Solution:**
Check `settings.py` has `'careapp'` in `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'careapp',
]
```

---

### 3. Template Not Found

**Solution:**
Check `settings.py` TEMPLATES configuration:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    },
]
```

---

### 4. Donors Not Getting Notified

**Check:**
1. Blood group matches between request and donor
2. Donor's `is_available` is `True`
3. Check Django admin → Notifications table

**Debug:**
```python
python manage.py shell
```
```python
from careapp.models import DonorProfile, BloodRequest, Notification

# Check donors
donors = DonorProfile.objects.filter(blood_group='A+', is_available=True)
print(f"Found {donors.count()} A+ donors")
for donor in donors:
    print(f"- {donor.user.username}: {donor.blood_group}, available={donor.is_available}")

# Check notifications
notifications = Notification.objects.all()
print(f"Total notifications: {notifications.count()}")
```

---

### 5. Can't Login (Invalid Credentials)

**Solution:**
Make sure you created demo users:
```bash
python create_demo_users.py
```

**Test Accounts:**
- Admin: `admin` / `admin123`
- Donor: `john_donor` / `donor123`

**Reset Password via Django Shell:**
```python
python manage.py shell
```
```python
from django.contrib.auth.models import User

# Reset admin password
admin = User.objects.get(username='admin')
admin.set_password('admin123')
admin.save()

# Reset donor password
donor = User.objects.get(username='john_donor')
donor.set_password('donor123')
donor.save()
```

---

### 6. Static Files Not Loading

**Solution:**
```bash
python manage.py collectstatic
```

For development, ensure `DEBUG = True` in settings.py

---

### 7. Database Locked Error

**Solution:**
1. Stop all Django processes
2. Delete `db.sqlite3`
3. Re-run migrations:
   ```bash
   python manage.py migrate
   python create_demo_users.py
   ```

---

### 8. Port Already in Use

**Error:** `Error: That port is already in use.`

**Solution:**
```bash
# Use different port
python manage.py runserver 8080

# Or kill existing process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

---

### 9. Migration Errors

**Solution:**
```bash
# Delete migrations
rm careapp/migrations/0*.py

# Recreate migrations
python manage.py makemigrations careapp
python manage.py migrate
```

---

### 10. Accept/Reject Buttons Not Working

**Check:**
1. Open browser console (F12)
2. Look for JavaScript errors
3. Check if fetch API is blocked

**Solution:**
- Ensure JavaScript is enabled
- Disable ad blockers
- Check CSRF token in cookies (F12 → Application → Cookies)

---

## Quick Fix for CSRF Token Issue

**The Fastest Solution:**

1. **Stop Django Server:**
   ```
   Press Ctrl + C in terminal
   ```

2. **Clear Browser Data:**
   - Close ALL browser windows/tabs
   - Reopen browser

3. **Restart Server:**
   ```bash
   python manage.py runserver
   ```

4. **Fresh Login:**
   - Open NEW browser window
   - Go to: `http://127.0.0.1:8000/accounts/login/`
   - Login with: `admin` / `admin123`

---

## Verification Checklist

✅ **Server Running:**
```bash
python manage.py check
# Expected: "System check identified no issues"
```

✅ **Database Working:**
```bash
python manage.py showmigrations
# All migrations should have [X]
```

✅ **Users Created:**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
print(User.objects.count())  # Should be > 0
```

✅ **URLs Working:**
- Login: http://127.0.0.1:8000/accounts/login/
- Admin: http://127.0.0.1:8000/admin/
- Demo: http://127.0.0.1:8000/demo/admin/create-request/

---

## Still Having Issues?

### Check Django Admin Panel
1. Login to admin: http://127.0.0.1:8000/admin/
2. Check data:
   - Users → Should see admin + donors
   - Donor profiles → Should see donor blood groups
   - Blood requests → Check any created requests
   - Notifications → Check auto-created notifications

### Enable Debug Mode
Already enabled by default (`DEBUG = True` in settings.py)

### Check Server Logs
Look at terminal output for error messages

---

## Contact Support

If all else fails:
1. Check `README_DEMO.md` for detailed setup
2. Review `START_HERE.md` for quick start
3. Read `IMPLEMENTATION_SUMMARY.md` for technical details

---

**Most Common Fix:** Clear browser cache and restart Django server! 🎯
