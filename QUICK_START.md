# Quick Start Guide

Get the CS Grad Application Insight Platform running in 5 minutes!

## Step 1: Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Initialize Database with Sample Data

```bash
python scripts/init_db.py --reset --with-sample
```

## Step 4: Run the Application

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Step 5: Open in Browser

Visit: **http://localhost:5000**

---

## Demo Credentials

After initialization, log in with:

| Email | Password |
|-------|----------|
| alice@example.com | pass1234 |
| bob@example.com | pass1234 |
| carol@example.com | pass1234 |

(All demo users use the same password)

---

## What to Try

### As a Guest
1. Visit **Home** to see platform statistics
2. Click **Explore** to search for application outcomes by:
   - University (e.g., "Stanford")
   - Program (e.g., "MS CS")
   - Degree type (MS, PhD, MEng)
   - Application result (Admit, Reject, Waitlist)

### After Login
1. Go to **Dashboard** (automatically redirected after login)
2. **Profile Snapshot**: Enter your background:
   - GPA and GPA scale
   - Test scores (GRE, TOEFL)
   - Research/internship experience
   - Recommendation letter strength
3. **Add Application Result**: Log your application outcomes:
   - University and program name
   - Application term and country
   - Your result (Admit/Reject/Waitlist)
   - Funding information
4. **My Applications**: View and manage your recorded applications
5. **Program Recommendations**: Get smart suggestions based on your profile:
   - **Reach**: Programs above your typical stats
   - **Match**: Programs matching your profile
   - **Safe**: Programs below your stats (high admission probability)

---

## Project Features

✅ User authentication (register, login, logout)
✅ Anonymized application data from 140+ records
✅ 35+ universities worldwide
✅ Advanced search and filtering
✅ Rule-based program recommendations
✅ Real-time data updates
✅ Responsive design (mobile-friendly)
✅ Clean REST API

---

## Key Pages

| Page | Purpose |
|------|---------|
| `/` | Home page with statistics |
| `/explore` | Search and browse application outcomes |
| `/auth` | Login and registration |
| `/dashboard` | User dashboard for profile and applications |

---

## Stopping the Server

Press `Ctrl+C` in your terminal to stop the Flask development server.

---

## Next Steps

- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Read [README.md](README.md) for detailed feature documentation
- Explore the API directly:
  - `/api/public/stats` - Platform statistics
  - `/api/search/applications` - Search applications

---

## Troubleshooting

### Python not found
```bash
# Use python3 instead
python3 -m venv venv
python3 -c "import flask"
```

### Port 5000 already in use
```bash
flask run --port 5001
```

### Database errors
```bash
# Reset database
rm instance/app.db
python scripts/init_db.py --with-sample
```

### Module import errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

Enjoy exploring! 🎓
