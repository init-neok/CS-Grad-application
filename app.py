from __future__ import annotations

from datetime import datetime
from functools import wraps
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from config import get_config


db = SQLAlchemy()


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    profile = db.relationship("Profile", back_populates="user", uselist=False)
    educations = db.relationship("Education", back_populates="user", cascade="all,delete")
    test_scores = db.relationship(
        "TestScore", back_populates="user", cascade="all,delete"
    )
    experiences = db.relationship(
        "Experience", back_populates="user", cascade="all,delete"
    )
    publications = db.relationship(
        "Publication", back_populates="user", cascade="all,delete"
    )
    applications = db.relationship(
        "ApplicationRecord", back_populates="user", cascade="all,delete"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Profile(TimestampMixin, db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    preferred_name = db.Column(db.String(80))
    gpa = db.Column(db.Float)
    gpa_scale = db.Column(db.Float, default=4.0)
    gre_total = db.Column(db.Integer)
    toefl_total = db.Column(db.Integer)
    research_experience = db.Column(db.Boolean, default=False)
    internship_experience = db.Column(db.Boolean, default=False)
    recommendation_strength = db.Column(db.String(32))
    notes = db.Column(db.Text)

    user = db.relationship("User", back_populates="profile")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "preferred_name": self.preferred_name,
            "gpa": self.gpa,
            "gpa_scale": self.gpa_scale,
            "gre_total": self.gre_total,
            "toefl_total": self.toefl_total,
            "research_experience": self.research_experience,
            "internship_experience": self.internship_experience,
            "recommendation_strength": self.recommendation_strength,
            "notes": self.notes,
        }


class Education(TimestampMixin, db.Model):
    __tablename__ = "educations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    institution = db.Column(db.String(120), nullable=False)
    degree = db.Column(db.String(80))
    field_of_study = db.Column(db.String(120))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    gpa = db.Column(db.Float)
    gpa_scale = db.Column(db.Float)
    currently_enrolled = db.Column(db.Boolean, default=False)

    user = db.relationship("User", back_populates="educations")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "institution": self.institution,
            "degree": self.degree,
            "field_of_study": self.field_of_study,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "gpa": self.gpa,
            "gpa_scale": self.gpa_scale,
            "currently_enrolled": self.currently_enrolled,
        }


class TestScore(TimestampMixin, db.Model):
    __tablename__ = "test_scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    test_type = db.Column(db.String(32), nullable=False)
    total_score = db.Column(db.Float)
    section = db.Column(db.String(32))
    score_details = db.Column(db.String(120))
    test_date = db.Column(db.String(32))

    user = db.relationship("User", back_populates="test_scores")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "test_type": self.test_type,
            "total_score": self.total_score,
            "section": self.section,
            "score_details": self.score_details,
            "test_date": self.test_date,
        }


class Experience(TimestampMixin, db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(32), nullable=False)  # research, internship, work
    organization = db.Column(db.String(120), nullable=False)
    role_title = db.Column(db.String(120))
    description = db.Column(db.Text)
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    ongoing = db.Column(db.Boolean, default=False)

    user = db.relationship("User", back_populates="experiences")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "organization": self.organization,
            "role_title": self.role_title,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "ongoing": self.ongoing,
        }


class Publication(TimestampMixin, db.Model):
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    venue = db.Column(db.String(120))
    year = db.Column(db.Integer)
    first_author = db.Column(db.Boolean, default=False)
    url = db.Column(db.String(200))

    user = db.relationship("User", back_populates="publications")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "venue": self.venue,
            "year": self.year,
            "first_author": self.first_author,
            "url": self.url,
        }


class ApplicationRecord(TimestampMixin, db.Model):
    __tablename__ = "application_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    university = db.Column(db.String(120), nullable=False)
    program = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(80))
    degree = db.Column(db.String(32))
    term = db.Column(db.String(32))
    result = db.Column(db.String(32), nullable=False)
    funding = db.Column(db.String(120))
    notes = db.Column(db.Text)
    gpa = db.Column(db.Float)
    gpa_scale = db.Column(db.Float)
    gre_total = db.Column(db.Integer)
    research_experience = db.Column(db.Boolean, default=False)
    internship_experience = db.Column(db.Boolean, default=False)
    recommendation_strength = db.Column(db.String(32))

    user = db.relationship("User", back_populates="applications")

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "university": self.university,
            "program": self.program,
            "country": self.country,
            "degree": self.degree,
            "term": self.term,
            "result": self.result,
            "funding": self.funding,
            "gpa": self.gpa,
            "gpa_scale": self.gpa_scale,
            "gre_total": self.gre_total,
            "research_experience": self.research_experience,
            "internship_experience": self.internship_experience,
            "recommendation_strength": self.recommendation_strength,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def to_user_dict(self) -> Dict[str, Any]:
        data = self.to_public_dict()
        data.update({"notes": self.notes})
        return data


# ---------------------------------------------------------------------------
# Application Factory & Utilities
# ---------------------------------------------------------------------------


def create_app(config_name: Optional[str] = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(get_config(config_name))
    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    return app


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        return fn(*args, **kwargs)

    return wrapper


def get_current_user() -> Optional[User]:
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


def update_model_from_json(model, data: Dict[str, Any], fields: List[str]) -> None:
    for field in fields:
        if field in data:
            setattr(model, field, data[field])


def get_public_stats() -> Dict[str, Any]:
    total_applications = ApplicationRecord.query.count()
    university_count = db.session.query(ApplicationRecord.university).distinct().count()
    program_count = db.session.query(ApplicationRecord.program).distinct().count()
    recent = (
        ApplicationRecord.query.order_by(ApplicationRecord.created_at.desc())
        .limit(5)
        .all()
    )
    return {
        "total_applications": total_applications,
        "universities": university_count,
        "programs": program_count,
        "recent_applications": [record.to_public_dict() for record in recent],
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


def register_routes(app: Flask) -> None:
    @app.context_processor
    def inject_current_user():
        return {"current_user": get_current_user()}

    @app.route("/")
    def home():
        stats = get_public_stats()
        return render_template("index.html", stats=stats)

    @app.route("/explore")
    def explore_page():
        stats = get_public_stats()
        return render_template("explore.html", stats=stats)

    @app.route("/auth")
    def auth_page():
        if get_current_user():
            return redirect(url_for("dashboard_page"))
        next_url = request.args.get("next") or url_for("dashboard_page")
        return render_template("auth.html", next_url=next_url)

    @app.route("/dashboard")
    def dashboard_page():
        user = get_current_user()
        if not user:
            next_url = request.args.get("next") or request.path
            return redirect(url_for("auth_page", next=next_url))
        return render_template("dashboard.html")

    # -------- Auth --------
    @app.route("/api/register", methods=["POST"])
    def register():
        payload = request.get_json(silent=True) or {}
        email = (payload.get("email") or "").strip().lower()
        password = payload.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409

        user = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id

        return jsonify({"message": "Registered successfully", "user": user.to_dict()})

    @app.route("/api/login", methods=["POST"])
    def login():
        payload = request.get_json(silent=True) or {}
        email = (payload.get("email") or "").strip().lower()
        password = payload.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not password or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        session["user_id"] = user.id
        return jsonify({"message": "Logged in", "user": user.to_dict()})

    @app.route("/api/logout", methods=["POST"])
    def logout():
        session.pop("user_id", None)
        return jsonify({"message": "Logged out"})

    # -------- Profile --------
    @app.route("/api/profile", methods=["GET"])
    @login_required
    def get_profile():
        user = get_current_user()
        assert user
        profile = user.profile.to_dict() if user.profile else {}
        return jsonify(
            {
                "user": user.to_dict(),
                "profile": profile,
                "educations": [e.to_dict() for e in user.educations],
                "test_scores": [score.to_dict() for score in user.test_scores],
                "experiences": [exp.to_dict() for exp in user.experiences],
                "publications": [pub.to_dict() for pub in user.publications],
            }
        )

    @app.route("/api/profile", methods=["PUT"])
    @login_required
    def update_profile():
        user = get_current_user()
        assert user
        payload = request.get_json(silent=True) or {}

        if user.profile is None:
            user.profile = Profile(user=user)

        fields = [
            "preferred_name",
            "gpa",
            "gpa_scale",
            "gre_total",
            "toefl_total",
            "research_experience",
            "internship_experience",
            "recommendation_strength",
            "notes",
        ]
        update_model_from_json(user.profile, payload, fields)
        db.session.commit()
        return jsonify({"message": "Profile updated", "profile": user.profile.to_dict()})

    # -------- Education --------
    @app.route("/api/education", methods=["GET", "POST"])
    @login_required
    def education_collection():
        user = get_current_user()
        assert user
        if request.method == "GET":
            return jsonify([edu.to_dict() for edu in user.educations])

        payload = request.get_json(silent=True) or {}
        required_fields = ["institution"]
        if not all(payload.get(field) for field in required_fields):
            return jsonify({"error": "Institution is required"}), 400

        edu = Education(user=user)
        fields = [
            "institution",
            "degree",
            "field_of_study",
            "start_year",
            "end_year",
            "gpa",
            "gpa_scale",
            "currently_enrolled",
        ]
        update_model_from_json(edu, payload, fields)
        db.session.add(edu)
        db.session.commit()
        return jsonify(edu.to_dict()), 201

    @app.route("/api/education/<int:education_id>", methods=["PUT", "DELETE"])
    @login_required
    def education_resource(education_id: int):
        user = get_current_user()
        assert user
        education = Education.query.filter_by(id=education_id, user_id=user.id).first()
        if not education:
            return jsonify({"error": "Education entry not found"}), 404

        if request.method == "DELETE":
            db.session.delete(education)
            db.session.commit()
            return jsonify({"message": "Education entry deleted"})

        payload = request.get_json(silent=True) or {}
        fields = [
            "institution",
            "degree",
            "field_of_study",
            "start_year",
            "end_year",
            "gpa",
            "gpa_scale",
            "currently_enrolled",
        ]
        update_model_from_json(education, payload, fields)
        db.session.commit()
        return jsonify(education.to_dict())

    # -------- Test Scores --------
    @app.route("/api/scores", methods=["GET", "POST"])
    @login_required
    def score_collection():
        user = get_current_user()
        assert user
        if request.method == "GET":
            return jsonify([score.to_dict() for score in user.test_scores])

        payload = request.get_json(silent=True) or {}
        if not payload.get("test_type"):
            return jsonify({"error": "test_type is required"}), 400

        score = TestScore(user=user)
        fields = [
            "test_type",
            "total_score",
            "section",
            "score_details",
            "test_date",
        ]
        update_model_from_json(score, payload, fields)
        db.session.add(score)
        db.session.commit()
        return jsonify(score.to_dict()), 201

    @app.route("/api/scores/<int:score_id>", methods=["PUT", "DELETE"])
    @login_required
    def score_resource(score_id: int):
        user = get_current_user()
        assert user
        score = TestScore.query.filter_by(id=score_id, user_id=user.id).first()
        if not score:
            return jsonify({"error": "Score entry not found"}), 404

        if request.method == "DELETE":
            db.session.delete(score)
            db.session.commit()
            return jsonify({"message": "Score entry deleted"})

        payload = request.get_json(silent=True) or {}
        fields = [
            "test_type",
            "total_score",
            "section",
            "score_details",
            "test_date",
        ]
        update_model_from_json(score, payload, fields)
        db.session.commit()
        return jsonify(score.to_dict())

    # -------- Experiences --------
    @app.route("/api/experiences", methods=["GET", "POST"])
    @login_required
    def experience_collection():
        user = get_current_user()
        assert user
        if request.method == "GET":
            return jsonify([exp.to_dict() for exp in user.experiences])

        payload = request.get_json(silent=True) or {}
        if not payload.get("category") or not payload.get("organization"):
            return jsonify({"error": "category and organization are required"}), 400

        experience = Experience(user=user)
        fields = [
            "category",
            "organization",
            "role_title",
            "description",
            "start_date",
            "end_date",
            "ongoing",
        ]
        update_model_from_json(experience, payload, fields)
        db.session.add(experience)
        db.session.commit()
        return jsonify(experience.to_dict()), 201

    @app.route("/api/experiences/<int:experience_id>", methods=["PUT", "DELETE"])
    @login_required
    def experience_resource(experience_id: int):
        user = get_current_user()
        assert user
        experience = Experience.query.filter_by(id=experience_id, user_id=user.id).first()
        if not experience:
            return jsonify({"error": "Experience not found"}), 404

        if request.method == "DELETE":
            db.session.delete(experience)
            db.session.commit()
            return jsonify({"message": "Experience deleted"})

        payload = request.get_json(silent=True) or {}
        fields = [
            "category",
            "organization",
            "role_title",
            "description",
            "start_date",
            "end_date",
            "ongoing",
        ]
        update_model_from_json(experience, payload, fields)
        db.session.commit()
        return jsonify(experience.to_dict())

    # -------- Publications --------
    @app.route("/api/publications", methods=["GET", "POST"])
    @login_required
    def publication_collection():
        user = get_current_user()
        assert user
        if request.method == "GET":
            return jsonify([pub.to_dict() for pub in user.publications])

        payload = request.get_json(silent=True) or {}
        if not payload.get("title"):
            return jsonify({"error": "title is required"}), 400

        publication = Publication(user=user)
        fields = ["title", "venue", "year", "first_author", "url"]
        update_model_from_json(publication, payload, fields)
        db.session.add(publication)
        db.session.commit()
        return jsonify(publication.to_dict()), 201

    @app.route("/api/publications/<int:publication_id>", methods=["PUT", "DELETE"])
    @login_required
    def publication_resource(publication_id: int):
        user = get_current_user()
        assert user
        publication = Publication.query.filter_by(id=publication_id, user_id=user.id).first()
        if not publication:
            return jsonify({"error": "Publication not found"}), 404

        if request.method == "DELETE":
            db.session.delete(publication)
            db.session.commit()
            return jsonify({"message": "Publication deleted"})

        payload = request.get_json(silent=True) or {}
        fields = ["title", "venue", "year", "first_author", "url"]
        update_model_from_json(publication, payload, fields)
        db.session.commit()
        return jsonify(publication.to_dict())

    # -------- Applications --------
    @app.route("/api/applications/my", methods=["GET"])
    @login_required
    def my_applications():
        user = get_current_user()
        assert user
        return jsonify([record.to_user_dict() for record in user.applications])

    @app.route("/api/applications", methods=["POST"])
    @login_required
    def create_application():
        user = get_current_user()
        assert user
        payload = request.get_json(silent=True) or {}
        if not payload.get("university") or not payload.get("program") or not payload.get("result"):
            return jsonify({"error": "university, program, and result are required"}), 400

        record = ApplicationRecord(user=user)
        fields = [
            "university",
            "program",
            "country",
            "degree",
            "term",
            "result",
            "funding",
            "notes",
            "gpa",
            "gpa_scale",
            "gre_total",
            "research_experience",
            "internship_experience",
            "recommendation_strength",
        ]
        update_model_from_json(record, payload, fields)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_user_dict()), 201

    @app.route("/api/applications/<int:application_id>", methods=["PUT", "DELETE"])
    @login_required
    def application_resource(application_id: int):
        user = get_current_user()
        assert user
        record = ApplicationRecord.query.filter_by(id=application_id, user_id=user.id).first()
        if not record:
            return jsonify({"error": "Application record not found"}), 404

        if request.method == "DELETE":
            db.session.delete(record)
            db.session.commit()
            return jsonify({"message": "Application deleted"})

        payload = request.get_json(silent=True) or {}
        fields = [
            "university",
            "program",
            "country",
            "degree",
            "term",
            "result",
            "funding",
            "notes",
            "gpa",
            "gpa_scale",
            "gre_total",
            "research_experience",
            "internship_experience",
            "recommendation_strength",
        ]
        update_model_from_json(record, payload, fields)
        db.session.commit()
        return jsonify(record.to_user_dict())

    # -------- Public Search & Stats --------
    @app.route("/api/public/stats")
    def public_stats_endpoint():
        return jsonify(get_public_stats())

    @app.route("/api/search/applications", methods=["GET"])
    def search_applications():
        query = ApplicationRecord.query
        filters = {
            "university": request.args.get("university"),
            "country": request.args.get("country"),
            "program": request.args.get("program"),
            "degree": request.args.get("degree"),
            "term": request.args.get("term"),
            "result": request.args.get("result"),
        }
        for field, value in filters.items():
            if value:
                query = query.filter(getattr(ApplicationRecord, field).ilike(f"%{value}%"))

        sort = request.args.get("sort", "recent")
        if sort == "university":
            query = query.order_by(ApplicationRecord.university.asc())
        elif sort == "program":
            query = query.order_by(ApplicationRecord.program.asc())
        else:
            query = query.order_by(ApplicationRecord.created_at.desc())

        limit = min(int(request.args.get("limit", 50)), 200)
        records = query.limit(limit).all()
        return jsonify([record.to_public_dict() for record in records])

    # -------- Match Suggestions --------
    @app.route("/api/match/suggestions", methods=["GET"])
    @login_required
    def match_suggestions():
        user = get_current_user()
        assert user
        if not user.profile or not user.profile.gpa or not user.profile.gpa_scale:
            return (
                jsonify({"error": "Complete your profile with GPA details to get suggestions."}),
                400,
            )

        user_gpa_norm = user.profile.gpa / (user.profile.gpa_scale or 1)
        user_gre = user.profile.gre_total or 0

        stats = aggregate_program_stats()
        if not stats:
            return jsonify({"message": "Not enough admitted records for suggestions", "data": []})

        reach: List[Dict[str, Any]] = []
        match: List[Dict[str, Any]] = []
        safe: List[Dict[str, Any]] = []

        for key, info in stats.items():
            avg_gpa = info.get("avg_gpa")
            if avg_gpa is None:
                continue
            gpa_gap = user_gpa_norm - avg_gpa
            gre_gap = 0.0
            if info.get("avg_gre") and user_gre:
                gre_gap = (user_gre - info["avg_gre"]) / 340.0
            composite = (gpa_gap * 0.7) + (gre_gap * 0.3)
            entry = {
                "program_key": key,
                "university": info["university"],
                "program": info["program"],
                "degree": info["degree"],
                "avg_gpa": round(avg_gpa, 3),
                "avg_gre": info.get("avg_gre"),
                "admit_rate": info.get("admit_rate"),
                "sample_size": info["total"],
                "score_gap": round(composite, 3),
            }
            if composite >= 0.05:
                safe.append(entry)
            elif composite <= -0.05:
                reach.append(entry)
            else:
                match.append(entry)

        result_payload = {
            "reach": sorted(reach, key=lambda r: r["score_gap"])[:5],
            "match": sorted(match, key=lambda r: abs(r["score_gap"]))[:5],
            "safe": sorted(safe, key=lambda r: -r["score_gap"])[:5],
        }
        return jsonify(result_payload)


def aggregate_program_stats() -> Dict[str, Dict[str, Any]]:
    records = ApplicationRecord.query.all()
    stats: Dict[str, Dict[str, Any]] = {}
    for record in records:
        key = f"{record.university}::{record.program}::{record.degree or ''}"
        entry = stats.setdefault(
            key,
            {
                "university": record.university,
                "program": record.program,
                "degree": record.degree,
                "gpa_values": [],
                "gre_values": [],
                "total": 0,
                "admitted": 0,
            },
        )
        normalized_gpa = None
        if record.gpa and record.gpa_scale:
            normalized_gpa = record.gpa / record.gpa_scale

        if record.result and record.result.lower() == "admit":
            entry["admitted"] += 1
            if normalized_gpa is not None:
                entry["gpa_values"].append(normalized_gpa)
            if record.gre_total:
                entry["gre_values"].append(record.gre_total)

        entry["total"] += 1

    for key, info in stats.items():
        if info["gpa_values"]:
            info["avg_gpa"] = sum(info["gpa_values"]) / len(info["gpa_values"])
        else:
            info["avg_gpa"] = None
        if info["gre_values"]:
            info["avg_gre"] = int(sum(info["gre_values"]) / len(info["gre_values"]))
        else:
            info["avg_gre"] = None
        info["admit_rate"] = round(info["admitted"] / info["total"], 3) if info["total"] else 0
        info.pop("gpa_values", None)
        info.pop("gre_values", None)
    return stats


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
