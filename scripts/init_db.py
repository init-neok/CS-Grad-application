#!/usr/bin/env python3
"""Utility script for initializing the SQLite database."""

from __future__ import annotations

import argparse

from pathlib import Path
import sys

from werkzeug.security import generate_password_hash

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import (
    ApplicationRecord,
    Education,
    Profile,
    User,
    create_app,
    db,
)


def seed_sample_data() -> None:
    """Seed the database with multiple users and 100+ application records."""

    user_specs = [
        {
            "email": "alice@example.com",
            "preferred_name": "Alice",
            "gpa": 3.92,
            "gpa_scale": 4.0,
            "gre_total": 332,
            "toefl_total": 114,
            "research_experience": True,
            "internship_experience": True,
            "recommendation_strength": "strong",
            "notes": "NLP research + FAANG internship",
            "education": {
                "institution": "California Institute of Technology",
                "degree": "BS",
                "field_of_study": "Computer Science",
                "start_year": 2019,
                "end_year": 2023,
            },
        },
        {
            "email": "bob@example.com",
            "preferred_name": "Bob",
            "gpa": 3.66,
            "gpa_scale": 4.0,
            "gre_total": 317,
            "toefl_total": 107,
            "research_experience": False,
            "internship_experience": True,
            "recommendation_strength": "moderate",
            "notes": "Systems research assistant + SWE internship",
            "education": {
                "institution": "Purdue University",
                "degree": "BS",
                "field_of_study": "Computer Engineering",
                "start_year": 2018,
                "end_year": 2022,
            },
        },
        {
            "email": "carol@example.com",
            "preferred_name": "Carol",
            "gpa": 3.78,
            "gpa_scale": 4.0,
            "gre_total": 323,
            "toefl_total": 110,
            "research_experience": True,
            "internship_experience": True,
            "recommendation_strength": "strong",
            "notes": "Robotics lab & autonomous driving internship",
            "education": {
                "institution": "University of Wisconsin-Madison",
                "degree": "BS",
                "field_of_study": "Computer Science",
                "start_year": 2017,
                "end_year": 2021,
            },
        },
        {
            "email": "david@example.com",
            "preferred_name": "David",
            "gpa": 3.54,
            "gpa_scale": 4.0,
            "gre_total": 309,
            "toefl_total": 103,
            "research_experience": False,
            "internship_experience": True,
            "recommendation_strength": "average",
            "notes": "Backend developer with two internships",
            "education": {
                "institution": "University of Maryland",
                "degree": "BS",
                "field_of_study": "Information Science",
                "start_year": 2016,
                "end_year": 2020,
            },
        },
        {
            "email": "emma@example.com",
            "preferred_name": "Emma",
            "gpa": 3.81,
            "gpa_scale": 4.0,
            "gre_total": 326,
            "toefl_total": 111,
            "research_experience": True,
            "internship_experience": True,
            "recommendation_strength": "strong",
            "notes": "Computer vision + AR startup internship",
            "education": {
                "institution": "Georgia Institute of Technology",
                "degree": "BS",
                "field_of_study": "Computer Science",
                "start_year": 2018,
                "end_year": 2022,
            },
        },
        {
            "email": "frank@example.com",
            "preferred_name": "Frank",
            "gpa": 3.48,
            "gpa_scale": 4.0,
            "gre_total": 310,
            "toefl_total": 100,
            "research_experience": False,
            "internship_experience": False,
            "recommendation_strength": "average",
            "notes": "Career switcher with strong course projects",
            "education": {
                "institution": "Rutgers University",
                "degree": "BS",
                "field_of_study": "Mathematics",
                "start_year": 2015,
                "end_year": 2019,
            },
        },
        {
            "email": "grace@example.com",
            "preferred_name": "Grace",
            "gpa": 3.69,
            "gpa_scale": 4.0,
            "gre_total": 321,
            "toefl_total": 109,
            "research_experience": True,
            "internship_experience": True,
            "recommendation_strength": "strong",
            "notes": "Distributed systems + open-source contributor",
            "education": {
                "institution": "University of California, Davis",
                "degree": "BS",
                "field_of_study": "Computer Science",
                "start_year": 2018,
                "end_year": 2022,
            },
        },
        {
            "email": "henry@example.com",
            "preferred_name": "Henry",
            "gpa": 3.58,
            "gpa_scale": 4.0,
            "gre_total": 315,
            "toefl_total": 105,
            "research_experience": False,
            "internship_experience": True,
            "recommendation_strength": "moderate",
            "notes": "Embedded systems focus, strong TA experience",
            "education": {
                "institution": "University of Minnesota",
                "degree": "BS",
                "field_of_study": "Computer Engineering",
                "start_year": 2016,
                "end_year": 2020,
            },
        },
        {
            "email": "ivy@example.com",
            "preferred_name": "Ivy",
            "gpa": 3.95,
            "gpa_scale": 4.0,
            "gre_total": 334,
            "toefl_total": 116,
            "research_experience": True,
            "internship_experience": True,
            "recommendation_strength": "strong",
            "notes": "Top of class, published ML paper",
            "education": {
                "institution": "University of Waterloo",
                "degree": "BMath",
                "field_of_study": "Computer Science",
                "start_year": 2017,
                "end_year": 2021,
            },
        },
        {
            "email": "jason@example.com",
            "preferred_name": "Jason",
            "gpa": 3.42,
            "gpa_scale": 4.0,
            "gre_total": 305,
            "toefl_total": 101,
            "research_experience": False,
            "internship_experience": True,
            "recommendation_strength": "average",
            "notes": "Full-stack developer for nonprofit projects",
            "education": {
                "institution": "University of Texas at Dallas",
                "degree": "BS",
                "field_of_study": "Software Engineering",
                "start_year": 2015,
                "end_year": 2019,
            },
        },
        {
            "email": "kelly@example.com",
            "preferred_name": "Kelly",
            "gpa": 3.73,
            "gpa_scale": 4.0,
            "gre_total": 320,
            "toefl_total": 108,
            "research_experience": True,
            "internship_experience": True,
            "recommendation_strength": "strong",
            "notes": "Cybersecurity research + startup internship",
            "education": {
                "institution": "University of Colorado Boulder",
                "degree": "BS",
                "field_of_study": "Computer Science",
                "start_year": 2018,
                "end_year": 2022,
            },
        },
        {
            "email": "luis@example.com",
            "preferred_name": "Luis",
            "gpa": 3.6,
            "gpa_scale": 4.0,
            "gre_total": 312,
            "toefl_total": 105,
            "research_experience": True,
            "internship_experience": False,
            "recommendation_strength": "moderate",
            "notes": "AI research club lead from Brazil",
            "education": {
                "institution": "University of São Paulo",
                "degree": "BS",
                "field_of_study": "Computer Science",
                "start_year": 2016,
                "end_year": 2020,
            },
        },
    ]

    users: list[User] = []
    default_password = "pass1234"

    for spec in user_specs:
        user = User(
            email=spec["email"],
            password_hash=generate_password_hash(spec.get("password", default_password)),
        )
        db.session.add(user)
        profile = Profile(
            user=user,
            preferred_name=spec["preferred_name"],
            gpa=spec["gpa"],
            gpa_scale=spec.get("gpa_scale", 4.0),
            gre_total=spec["gre_total"],
            toefl_total=spec.get("toefl_total"),
            research_experience=spec.get("research_experience", False),
            internship_experience=spec.get("internship_experience", False),
            recommendation_strength=spec.get("recommendation_strength"),
            notes=spec.get("notes"),
        )
        db.session.add(profile)

        education_data = spec["education"]
        education = Education(
            user=user,
            institution=education_data["institution"],
            degree=education_data["degree"],
            field_of_study=education_data["field_of_study"],
            start_year=education_data["start_year"],
            end_year=education_data["end_year"],
            gpa=spec["gpa"],
            gpa_scale=spec.get("gpa_scale", 4.0),
            currently_enrolled=education_data.get("currently_enrolled", False),
        )
        db.session.add(education)
        users.append(user)

    db.session.flush()

    program_catalog = [
        {"university": "Stanford University", "program": "MS CS", "degree": "MS", "country": "USA"},
        {
            "university": "Massachusetts Institute of Technology",
            "program": "MS EECS",
            "degree": "MS",
            "country": "USA",
        },
        {"university": "Carnegie Mellon University", "program": "MS CS", "degree": "MS", "country": "USA"},
        {
            "university": "University of California, Berkeley",
            "program": "MS EECS",
            "degree": "MS",
            "country": "USA",
        },
        {
            "university": "University of Illinois Urbana-Champaign",
            "program": "MS CS",
            "degree": "MS",
            "country": "USA",
        },
        {
            "university": "University of Illinois Chicago",
            "program": "MS CS",
            "degree": "MS",
            "country": "USA",
        },
        {
            "university": "Georgia Institute of Technology",
            "program": "MS CS",
            "degree": "MS",
            "country": "USA",
        },
        {"university": "University of Washington", "program": "MS CS", "degree": "MS", "country": "USA"},
        {
            "university": "University of Southern California",
            "program": "MS CS",
            "degree": "MS",
            "country": "USA",
        },
        {"university": "University of Michigan", "program": "MS CS", "degree": "MS", "country": "USA"},
        {
            "university": "University of Texas at Austin",
            "program": "MS CS",
            "degree": "MS",
            "country": "USA",
        },
        {"university": "Cornell University", "program": "MEng CS", "degree": "MEng", "country": "USA"},
        {"university": "Columbia University", "program": "MS CS", "degree": "MS", "country": "USA"},
        {"university": "Princeton University", "program": "PhD CS", "degree": "PhD", "country": "USA"},
        {"university": "Harvard University", "program": "PhD CS", "degree": "PhD", "country": "USA"},
        {
            "university": "University of California, San Diego",
            "program": "MS CS",
            "degree": "MS",
            "country": "USA",
        },
        {
            "university": "University of California, Los Angeles",
            "program": "MS CS",
            "degree": "MS",
            "country": "USA",
        },
        {
            "university": "University of California, Davis",
            "program": "MS CS",
            "degree": "MS",
            "country": "USA",
        },
        {"university": "University of Toronto", "program": "MSc CS", "degree": "MS", "country": "Canada"},
        {"university": "University of Waterloo", "program": "MMath CS", "degree": "MS", "country": "Canada"},
        {
            "university": "University of British Columbia",
            "program": "MS CS",
            "degree": "MS",
            "country": "Canada",
        },
        {"university": "McGill University", "program": "MS CS", "degree": "MS", "country": "Canada"},
        {"university": "University of Oxford", "program": "MSc CS", "degree": "MS", "country": "UK"},
        {"university": "University of Cambridge", "program": "MPhil CS", "degree": "MS", "country": "UK"},
        {
            "university": "Imperial College London",
            "program": "MSc Computing",
            "degree": "MS",
            "country": "UK",
        },
        {"university": "ETH Zurich", "program": "MS CS", "degree": "MS", "country": "Switzerland"},
        {"university": "EPFL", "program": "MS CS", "degree": "MS", "country": "Switzerland"},
        {
            "university": "Technical University of Munich",
            "program": "MS Informatics",
            "degree": "MS",
            "country": "Germany",
        },
        {
            "university": "National University of Singapore",
            "program": "MS CS",
            "degree": "MS",
            "country": "Singapore",
        },
        {
            "university": "Nanyang Technological University",
            "program": "MS CS",
            "degree": "MS",
            "country": "Singapore",
        },
        {"university": "Tsinghua University", "program": "MS CS", "degree": "MS", "country": "China"},
        {"university": "Peking University", "program": "MS CS", "degree": "MS", "country": "China"},
        {
            "university": "Hong Kong University of Science and Technology",
            "program": "MS CS",
            "degree": "MS",
            "country": "Hong Kong",
        },
        {"university": "University of Hong Kong", "program": "MS CS", "degree": "MS", "country": "Hong Kong"},
        {"university": "University of Tokyo", "program": "MS CS", "degree": "MS", "country": "Japan"},
        {"university": "Seoul National University", "program": "MS CS", "degree": "MS", "country": "South Korea"},
    ]

    terms = ["Fall 2023", "Spring 2024", "Fall 2024", "Fall 2025"]
    result_cycle = ["Admit", "Admit", "Waitlist", "Reject"]
    application_records: list[ApplicationRecord] = []
    counter = 0

    for term in terms:
        for program in program_catalog:
            user = users[counter % len(users)]
            profile = user.profile
            result = result_cycle[counter % len(result_cycle)]
            funding = None
            if result == "Admit":
                funding = "Scholarship/TA"
            elif result == "Waitlist":
                funding = "Pending decision"

            application_records.append(
                ApplicationRecord(
                    user=user,
                    term=term,
                    result=result,
                    funding=funding,
                    notes=f"Seeded record for {program['university']} ({term})",
                    gpa=profile.gpa,
                    gpa_scale=profile.gpa_scale,
                    gre_total=profile.gre_total,
                    research_experience=profile.research_experience,
                    internship_experience=profile.internship_experience,
                    recommendation_strength=profile.recommendation_strength,
                    **program,
                )
            )
            counter += 1

    db.session.add_all(application_records)
    db.session.commit()
    print(
        f"Seeded {len(users)} users and {len(application_records)} application records covering "
        f"{len(program_catalog)} universities."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize the SQLite database")
    parser.add_argument(
        "--with-sample",
        action="store_true",
        help="Seed the database with demo users and applications.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop all tables before creating them (destructive).",
    )
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        if args.reset:
            db.drop_all()
        db.create_all()
        if args.with_sample:
            seed_sample_data()

    print("Database ready at instance/app.db")


if __name__ == "__main__":
    main()
