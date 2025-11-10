````markdown
# CS Grad Application Insight Platform

A web-based platform for collecting, browsing, and analyzing historical Computer Science graduate application records.

Users can:

- Contribute their own (anonymized) profiles and application results.
- Explore past application outcomes with rich filters.
- Get program suggestions based on similar backgrounds.

This project is implemented with:

- **Frontend:** Web interface (HTML/CSS/JS)
- **Backend:** Python (Flask recommended)
- **Database:** SQLite

---

## 1. Project Overview

Many CS applicants struggle to evaluate their chances because:

- Information is scattered across forums, spreadsheets, screenshots.
- Data is unstructured and not easily searchable.
- There is no simple tool to answer: _“Where did people like me get admitted?”_

**Goal:** Build a centralized, structured, privacy-preserving platform that:

1. Aggregates historical application records.
2. Allows users to submit and manage their own data.
3. Provides powerful filtering for public exploration.
4. Offers simple rule-based “match suggestions” using existing data.

Target use case: course project demonstrating full-stack development with Python + SQLite.

---

## 2. Features

### 2.1 Public (Guest) Features

- **Home Page**
  - Platform introduction.
  - Key statistics:
    - Total number of applications.
    - Number of universities and programs.
    - Recently added application records.

- **Explore Applications**
  - Filter and search by:
    - University
    - Country/Region
    - Program (e.g., MS CS, MS DS, PhD CS)
    - Degree type (MS/PhD)
    - Term (e.g., Fall 2025)
    - Result (Admit / Reject / Waitlist)
  - View anonymized applicant snapshots:
    - GPA range
    - Test score range
    - Whether they have research, internships, publications
  - Sort by admit rate, university name, or other fields.

### 2.2 Registered User Features

- **Authentication**
  - Register with email + password.
  - Login/logout using secure sessions.
  - Passwords stored as hashes (no plain text).

- **Profile & Background Management**
  - Maintain personal background, including:
    - Education history (institutions, degrees, GPA)
    - Test scores (GRE, TOEFL/IELTS, etc.)
    - Research experience
    - Internships / work experience
    - Recommendation letter strength (self-reported)
    - Publications (title, venue, first-author flag)

- **Application Records Management**
  - Add application entries:
    - University, program, term
    - Result (Admit/Reject/Waitlist)
    - Funding / scholarship information
    - Notes (e.g., “interview required”, “priority deadline”, etc.)
  - Edit / delete own entries.
  - If a university or program does not exist:
    - User can submit a new entry (directly added or marked for review).

- **“Match Me” Suggestions (Rule-Based)**
  - Use the logged-in user’s background to:
    - Find historically similar profiles.
    - Recommend programs grouped as:
      - **Reach** (above typical admitted stats)
      - **Match** (similar to successful cases)
      - **Safe** (below or near median admitted stats)
  - Implemented with transparent rules (e.g., GPA, test scores, research flags),
    suitable for a course project (no complex ML required).

### 2.3 Admin Features (Optional)

For extended versions:

- Manage university/program dictionaries.
- Approve or correct user-submitted universities/programs.
- Flag or remove invalid/abusive records.

---

## 3. Tech Stack

**Frontend**

- HTML5, CSS3, JavaScript
- Optional UI frameworks: Bootstrap / Tailwind CSS

**Backend**

- Python 3.x
- Flask (or similar Python web framework)

**Database**

- SQLite
  - Simple file-based database.
  - Easy to initialize, backup, and inspect.

---

## 4. Architecture

Classic three-layer architecture:

1. **Presentation Layer (Frontend)**
   - Templates rendered via Flask (Jinja2) or static HTML + AJAX.
2. **Application Layer (Backend, Python)**
   - Request routing.
   - Input validation.
   - Business logic for profiles, applications, search, and match suggestions.
   - Authentication & authorization.
3. **Data Layer (SQLite)**
   - Relational schema modeling applicants, institutions, programs, and records.

Frontend interacts with backend via standard HTTP requests and JSON APIs.

---

## 5. Database Schema (High-Level)

Suggested core tables (simplified names; can be adapted):

- `universities`
  - `id`, `name`, `country`, `city`, `rank` (optional)
- `programs`
  - `id`, `university_id`, `name`, `degree_type` (MS/PhD), `track`
- `applicants`
  - `id`, `email`, `password_hash`, `nickname`,
    `final_decision_program_id` (nullable, FK to `programs`)
- `educations`
  - `id`, `applicant_id`, `university_name` or `university_id`,
    `degree`, `major`, `gpa`, `start_year`, `end_year`
- `scores`
  - `id`, `applicant_id`, `gre_v`, `gre_q`, `gre_aw`,
    `toefl_total`, `ielts_total`, `other_tests`
- `experiences`
  - `id`, `applicant_id`, `type` (research/internship/work),
    `title`, `institution`, `start_date`, `end_date`, `description`
- `publications`
  - `id`, `applicant_id`, `title`, `venue`, `is_first_author`
- `recommendations`
  - `id`, `applicant_id`, `strength` (e.g., Strong / Normal / Weak),
    `count`
- `applications`
  - `id`, `applicant_id`, `program_id`,
    `term`, `result`, `funding`, `scholarship_detail`, `note`

Relations:

- One university → many programs.
- One applicant → many applications.
- `applications` links applicants and programs.
- Background details normalized into separate tables.

The exact schema should be defined in `schema.sql` or `models.py`.

---

## 6. Project Structure (Suggested)

```bash
cs-grad-application-insight-platform/
├─ app.py                 # Flask entrypoint
├─ config.py              # Configuration (DB path, secret key, etc.)
├─ models.py              # Database models / ORM
├─ routes/
│  ├─ auth.py             # Register/Login/Logout
│  ├─ profile.py          # Background info CRUD
│  ├─ applications.py     # Application records CRUD
│  ├─ explore.py          # Public search & listing
│  └─ match.py            # Match suggestion logic
├─ templates/             # Jinja2 HTML templates
│  ├─ base.html
│  ├─ index.html
│  ├─ login.html
│  ├─ register.html
│  ├─ dashboard.html
│  ├─ applications.html
│  ├─ explore.html
│  └─ match.html
├─ static/
│  ├─ css/
│  └─ js/
├─ data/
│  └─ app.db              # SQLite database file
├─ scripts/
│  └─ init_db.py          # DB initialization script
├─ schema.sql             # SQL schema definition
├─ requirements.txt
└─ README.md
````

You can modify this layout as long as responsibilities remain clear.

---

## 7. Installation & Setup

### 7.1 Requirements

* Python 3.9+
* pip
* (Optional) virtualenv

### 7.2 Setup Steps

```bash
# 1. Clone repository
git clone <YOUR_REPO_URL>.git
cd cs-grad-application-insight-platform

# 2. Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize SQLite database
# Option A: using Python init script
python scripts/init_db.py

# Option B: using schema.sql directly
# sqlite3 data/app.db < schema.sql

# 5. Run development server
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

# App will run at:
# http://localhost:5000
```

---

## 8. Example Dependencies

`requirements.txt` (example):

```txt
Flask>=2.3.0
Werkzeug>=2.3.0
itsdangerous>=2.1.0
Jinja2>=3.1.0
SQLAlchemy>=2.0.0      # optional but recommended
python-dotenv>=1.0.0   # for environment variables
```

You may add more packages if needed (e.g., for forms or login helpers).

---

## 9. API Overview (Simplified)

Example REST-style endpoints (names can be adjusted):

### Auth

* `POST /api/register`
* `POST /api/login`
* `POST /api/logout`

### Profile & Background

* `GET /api/profile`
* `PUT /api/profile`
* `POST /api/education`
* `PUT /api/education/<id>`
* `DELETE /api/education/<id>`
* Similar endpoints for scores, experiences, publications, recommendations.

### Applications

* `GET /api/applications/my`
* `POST /api/applications`
* `PUT /api/applications/<id>`
* `DELETE /api/applications/<id>`

### Public Search

* `GET /api/search/applications`

  * Query params: `university`, `program`, `country`, `degree`, `term`, `result`, etc.

### Match Suggestions

* `GET /api/match/suggestions`

  * Uses current user’s background.
  * Returns a list of programs labeled as `reach/match/safe` with simple rule-based logic.

A more detailed API specification can be placed in `docs/api.md`.

---

## 10. Privacy & Disclaimer

* Public views are anonymized:

  * No real names, emails, or direct identifiers.
* Only aggregated or de-identified attributes are shown (e.g., GPA range, score bands).
* Data is **self-reported** and provided **for reference only**.
* No guarantee of admission outcomes; users should treat the platform as supporting evidence, not an oracle.

---

## 11. Future Extensions

* Support CSV/JSON import of historical records.
* Advanced visualization (admission distribution by GPA, test scores, etc.).
* Basic ML-based recommendation (if allowed by course scope).
* Migration from SQLite to MySQL/PostgreSQL for production use.

---

## License

Specify your chosen license here (e.g., MIT, Apache 2.0, or course-specific).

```markdown
MIT License (example)
Copyright (c) ...
```

---

## Implementation Status

A minimal but functional reference implementation is available in this repository.
It ships a Flask + SQLite stack with REST endpoints that cover authentication,
profile management, application CRUD, public search, and rule-based match
suggestions.

### Project Layout

- `app.py` – Flask app factory, SQLAlchemy models, and all API/public routes.
- `config.py` – environment-aware configuration (override via env vars).
- `requirements.txt` – Python dependencies (Flask + SQLAlchemy).
- `templates/index.html` – lightweight landing page that surfaces basic stats.
- `scripts/init_db.py` – CLI helper to create the SQLite database and optionally seed demo data.
- `instance/app.db` – default SQLite database location (auto-created).

### Quick Start

```bash
python -m venv venv
source venv/bin/activate              # Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py --with-sample
export FLASK_APP=app.py
flask run
```

Navigate to `http://localhost:5000` for the landing page or use any REST client
against the `/api/*` endpoints.

### Web UI Highlights

- **Home** – stats snapshot plus links to the explorer & dashboard.
- **Explore (`/explore`)** – browser-based search with filters, result sorting,
  and a live table backed by `/api/search/applications`.
- **Auth (`/auth`)** – login/registration tabs that call `POST /api/login` and
  `POST /api/register`.
- **Dashboard (`/dashboard`)** – profile editor, application submission form,
  inline table management (with delete), and one-click match suggestions that
  surface reach/match/safe groups via `/api/match/suggestions`.

These pages are implemented with lightweight Bootstrap + vanilla JS residing in
`templates/` and `static/js`. They consume the same REST endpoints that can be
used directly for automation or external clients.

### Demo Dataset

`python scripts/init_db.py --reset --with-sample` now seeds a dozen anonymized
users plus 140+ historical application entries that span 36 well-known schools,
including Stanford, MIT, UIUC, UIC, Georgia Tech, Toronto, Oxford, ETH, NUS,
Tsinghua, and more. This richer dataset keeps the public explorer interesting
and ensures the match-suggestion logic has enough signal to demonstrate reach /
match / safe groupings.

### API Highlights

- `POST /api/register`, `POST /api/login`, `POST /api/logout`
- `GET/PUT /api/profile`
- `GET|POST /api/education`, `/api/scores`, `/api/experiences`, `/api/publications`
- `GET /api/applications/my`, `POST /api/applications`,
  `PUT|DELETE /api/applications/<id>`
- `GET /api/search/applications` for public exploration with filters
- `GET /api/match/suggestions` for reach/match/safe grouping (requires profile GPA)

See `scripts/init_db.py --help` for database initialization options and
`/api/public/stats` for home-page statistics.

---

```
```
