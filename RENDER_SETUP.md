# Render Deployment Setup - URGENT FIX

## Problem
Images and resume not loading on https://portfolio-rbzp.onrender.com/ because environment variables are not set.

## Solution - Add Environment Variables on Render

### Step 1: Go to Render Dashboard
1. Visit: https://dashboard.render.com/
2. Click on your service: **sushil-portfolio**
3. Click on **"Environment"** tab in the left sidebar

### Step 2: Add These Environment Variables

Click **"Add Environment Variable"** and add each of these:

#### Variable 1: ALLOWED_HOSTS
```
Key: ALLOWED_HOSTS
Value: portfolio-rbzp.onrender.com,localhost,127.0.0.1
```

#### Variable 2: DEBUG
```
Key: DEBUG
Value: False
```

#### Variable 3: SECRET_KEY
```
Key: SECRET_KEY
Value: a)fi&8&v#zpvjdfys8&jak*b(gbyi0z45ri#tr!i3ux96ybgi%
```
**IMPORTANT**: Copy this exact value (or generate a new one if you prefer)

#### Variable 4: EMAIL_HOST_USER (Optional - for contact form)
```
Key: EMAIL_HOST_USER
Value: sushilchavan2468@gmail.com
```

#### Variable 5: EMAIL_HOST_PASSWORD (Optional - for contact form)
```
Key: EMAIL_HOST_PASSWORD
Value: crujmbzuyntkqzgk
```

### Step 3: Save and Deploy
1. After adding all variables, click **"Save Changes"**
2. Render will automatically trigger a redeploy
3. Wait 2-5 minutes for the build to complete

### Step 4: Verify
Once deployed, check:
- ✅ Profile image loads on homepage
- ✅ All 9 project images display on /projects page
- ✅ Resume download button works

## Alternative: Manual Redeploy

If auto-deploy doesn't trigger:
1. Go to your service dashboard
2. Click **"Manual Deploy"** button
3. Select **"Deploy latest commit"**
4. Wait for build to complete

## What to Expect After Deployment

### Images that should now display:
1. ✅ **Profile Image**: WhatsApp Image (About section)
2. ✅ **LexiMind**: ChatGPT Image
3. ✅ **Data Analyst Agent**: data.jpeg (already showing)
4. ✅ **DogCat Classifier**: catdog.jpeg (already showing)
5. ✅ **Weather Prediction**: weather.jpeg (already showing)
6. ✅ **Car Suggestion**: car.jpeg (already showing)
7. ✅ **Udemy Analytics**: Screenshot 2025-10-29 145617.png
8. ✅ **Smart Farming**: generate.jpeg (already showing)
9. ✅ **Pune Zomato**: Screenshot 2025-10-21 195226.png
10. ✅ **Pizza Sales**: Screenshot 2025-10-29 213443.png

### Resume download:
- ✅ "Download Resume" button should download `Sushil Chavan Resume.pdf`

## Troubleshooting

### If images still don't show after deployment:
1. **Check Render Logs**:
   - Go to service dashboard
   - Click "Logs" tab
   - Look for errors during collectstatic

2. **Clear Browser Cache**:
   - Press Ctrl+Shift+R (hard refresh)
   - Or open in incognito/private window

3. **Verify Build Completed**:
   - Check that build.sh ran successfully
   - Look for "collectstatic" in logs

4. **Check for 403/404 Errors**:
   - Open browser developer tools (F12)
   - Go to Network tab
   - Refresh page
   - Check if static files return 403 or 404

### Common Error Messages and Fixes:

**"DisallowedHost" Error**
- Fix: Make sure ALLOWED_HOSTS includes your Render domain

**"Static files not found"**
- Fix: Verify collectstatic ran in build logs
- Check that STATIC_ROOT and STATICFILES_DIRS are correct

**"500 Internal Server Error"**
- Fix: Set DEBUG=False and check logs for actual error

## Important Notes

1. **Never commit SECRET_KEY to Git** - Always use environment variables
2. **ALLOWED_HOSTS must include your domain** - Otherwise Django blocks requests
3. **collectstatic runs during build** - Check build.sh execution in logs
4. **WhiteNoise serves static files** - Already configured in settings.py

## Contact
If issues persist after following these steps, check:
- Render build logs for specific error messages
- Django logs in Render dashboard
- Static file paths in browser Network tab

---
**Created**: October 29, 2025
**Status**: Ready to deploy - just add environment variables!
