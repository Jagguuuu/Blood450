# CSRF Token Error Fix Instructions

## Problem
Getting "Forbidden (CSRF token from POST incorrect.)" error when trying to create a blood request from the Django web interface.

## Root Cause
The CSRF cookie was not being properly set or was cached by the browser with an invalid/expired token.

## Fixes Applied

### 1. Added CSRF Context Processor
**File:** `AYH/settings.py`
- Added `'django.template.context_processors.csrf'` to `TEMPLATES['OPTIONS']['context_processors']`
- This ensures CSRF tokens are available in all templates

### 2. Added `@ensure_csrf_cookie` Decorator
**File:** `careapp/views.py`
- Added decorator to `admin_dashboard()` view
- Added decorator to `admin_create_request()` view
- This forces Django to set the CSRF cookie on the response

### 3. Enhanced CSRF Settings
**File:** `AYH/settings.py`
Added the following settings:
```python
CSRF_COOKIE_DOMAIN = None  # Allow cookies on all domains for development
CSRF_COOKIE_PATH = '/'  # Make CSRF cookie available for all paths
```

### 4. Expanded CSRF Trusted Origins
**File:** `AYH/settings.py`
Added additional trusted origins:
- `http://localhost:8000`
- `http://127.0.0.1:8000`
- `http://localhost`
- `http://127.0.0.1`

### 5. Added Debug Logging
**File:** `careapp/views.py`
Added debug prints to track CSRF tokens (will show in terminal)

## How to Test the Fix

### Step 1: Clear Browser Cache and Cookies
**For Chrome/Edge:**
1. Press `Ctrl+Shift+Delete` (or `Cmd+Shift+Delete` on Mac)
2. Select "Cookies and other site data" and "Cached images and files"
3. Choose "All time" as the time range
4. Click "Clear data"

**Or manually clear for localhost:**
1. Press `F12` to open DevTools
2. Go to "Application" tab
3. Under "Storage" → "Cookies" → select `http://127.0.0.1:8000`
4. Delete all cookies (especially `csrftoken` and `sessionid`)

### Step 2: Hard Refresh the Page
- Press `Ctrl+F5` (or `Cmd+Shift+R` on Mac) to force a hard refresh
- This ensures you get the latest page with the new CSRF cookie

### Step 3: Login Again
1. Go to `http://127.0.0.1:8000/`
2. Login with your admin credentials
3. Navigate to the dashboard or create request page

### Step 4: Try Creating a Request
1. Go to "Create Request" page
2. Fill in the form:
   - Blood Group: Select any (e.g., A+)
   - Units Needed: 1
   - Urgency Level: Select any (e.g., High)
   - Additional Notes: Optional
3. Click "Create Request & Notify Donors"

### Step 5: Check Terminal for Debug Output
If it still fails, check your terminal for these debug messages:
```
CSRF Token from POST: [should show a token]
CSRF Cookie: [should show a token]
```

If you see "NOT FOUND" for either, that indicates where the problem is.

## Additional Troubleshooting

### Issue: Still Getting CSRF Error After Following All Steps

#### Check 1: Verify CSRF Cookie is Set
1. Open DevTools (F12)
2. Go to "Application" tab → "Cookies" → `http://127.0.0.1:8000`
3. Look for a cookie named `csrftoken`
4. If it's not there, the cookie is not being set

**Solution:** Make sure you accessed the page via GET request first before submitting the form.

#### Check 2: Verify Form Has CSRF Token
1. Right-click on the form → "Inspect"
2. Look for an `<input>` tag with `name="csrfmiddlewaretoken"`
3. It should look like:
   ```html
   <input type="hidden" name="csrfmiddlewaretoken" value="...long token...">
   ```

**Solution:** If missing, the `{% csrf_token %}` template tag is not working. Check if you're using `{% csrf_token %}` inside the `<form>` tag.

#### Check 3: Browser Privacy Settings
Some browsers (like Brave or Firefox with strict privacy) block third-party cookies by default.

**Solution:**
- In your browser settings, allow cookies for `localhost` or `127.0.0.1`
- Or try in an Incognito/Private window with default settings

#### Check 4: Check CSRF Middleware is Enabled
Verify in `AYH/settings.py` that MIDDLEWARE includes:
```python
'django.middleware.csrf.CsrfViewMiddleware',
```

### Issue: Works for Some Forms But Not Others

This might be a form-specific issue. Check that EVERY form has:
1. `method="post"` attribute
2. `{% csrf_token %}` inside the form
3. Proper `action` attribute (or leave empty for same URL)

### Issue: CSRF Cookie is Set But Token Doesn't Match

This usually happens when:
1. Multiple browser tabs are open with different sessions
2. The server restarted and invalidated old tokens
3. Clock synchronization issues between client/server

**Solution:**
- Close ALL browser tabs for `localhost:8000`
- Clear cookies again
- Open ONE fresh tab and try again

## Verification Checklist

- [ ] Browser cache cleared
- [ ] Browser cookies cleared
- [ ] Hard refresh performed (Ctrl+F5)
- [ ] Logged in fresh
- [ ] CSRF cookie visible in DevTools
- [ ] Form has hidden CSRF input field
- [ ] Tried in incognito/private window
- [ ] Only one tab open for localhost:8000

## Testing Other Forms

The fixes should also apply to these forms:
- Login form (`/accounts/login/`)
- Logout form (in navbar)
- Donor response forms (`/respond/`)
- Any other POST forms in your application

## Rolling Back (If Needed)

If these changes cause issues, you can revert by:
1. Removing `@ensure_csrf_cookie` decorators from views
2. Removing the CSRF context processor from settings
3. Restoring the original `CSRF_TRUSTED_ORIGINS` list

## Notes

- The debug print statements in `admin_create_request()` can be removed after confirming the fix works
- In production, ensure `CSRF_COOKIE_SECURE = True` when using HTTPS
- Keep `CSRF_COOKIE_HTTPONLY = False` if you need JavaScript access to CSRF tokens for AJAX requests

## Success Indicators

You'll know it's fixed when:
1. No CSRF errors in the terminal
2. Form submission succeeds and redirects to dashboard
3. Success message appears: "Blood request created successfully! X compatible donor(s) notified."
4. New request appears in the dashboard
