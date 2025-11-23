#!/usr/bin/env python3
"""
Database initialization script with realistic CS graduate application data.
Generates 500+ application records with varied universities, programs, degrees, and outcomes.
"""

import random
from datetime import datetime, timedelta
from app import create_app, db
from app import (
    User,
    Profile,
    Education,
    TestScore,
    Experience,
    Publication,
    RecommendationLetter,
    ApplicationRecord,
)


# Real universities and their countries
UNIVERSITIES = [
    # Top US Universities
    ("Stanford University", "USA"),
    ("MIT", "USA"),
    ("Carnegie Mellon University", "USA"),
    ("University of California, Berkeley", "USA"),
    ("University of Washington", "USA"),
    ("University of Texas at Austin", "USA"),
    ("University of Illinois Urbana-Champaign", "USA"),
    ("Cornell University", "USA"),
    ("Princeton University", "USA"),
    ("Harvard University", "USA"),
    ("UC San Diego", "USA"),
    ("University of Wisconsin-Madison", "USA"),
    ("Georgia Institute of Technology", "USA"),
    ("University of Pennsylvania", "USA"),
    ("Northwestern University", "USA"),
    ("Columbia University", "USA"),
    ("Yale University", "USA"),
    ("University of Michigan", "USA"),
    ("UC Irvine", "USA"),
    ("Purdue University", "USA"),
    # Canadian Universities
    ("University of Toronto", "Canada"),
    ("University of British Columbia", "Canada"),
    ("McGill University", "Canada"),
    ("University of Waterloo", "Canada"),
    ("McMaster University", "Canada"),
    # UK Universities
    ("University of Cambridge", "UK"),
    ("University of Oxford", "UK"),
    ("Imperial College London", "UK"),
    ("University College London", "UK"),
    ("University of Edinburgh", "UK"),
    ("University of Manchester", "UK"),
    # European Universities
    ("ETH Zurich", "Switzerland"),
    ("Technical University of Munich", "Germany"),
    ("Delft University of Technology", "Netherlands"),
    # Asian Universities
    ("National University of Singapore", "Singapore"),
    ("Nanyang Technological University", "Singapore"),
    ("University of Tokyo", "Japan"),
    ("Seoul National University", "South Korea"),
    ("Hong Kong University of Science and Technology", "Hong Kong"),
]

# CS-related programs
PROGRAMS = [
    "Computer Science",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Science",
    "Software Engineering",
    "Computer Engineering",
    "Cybersecurity",
    "Human-Computer Interaction",
    "Computer Networks",
    "Computer Vision",
    "Natural Language Processing",
    "Distributed Systems",
    "Database Systems",
    "Cloud Computing",
]

# Names for generated applicants
FIRST_NAMES = [
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Eve",
    "Frank",
    "Grace",
    "Henry",
    "Iris",
    "Jack",
    "Karen",
    "Liam",
    "Mia",
    "Noah",
    "Olivia",
    "Patrick",
    "Quinn",
    "Rachel",
    "Sam",
    "Taylor",
    "Uma",
    "Victor",
    "Wendy",
    "Xavier",
    "Yvonne",
    "Zoe",
    "Zhang",
    "Wang",
    "Liu",
    "Chen",
    "Patel",
    "Kumar",
    "Silva",
    "Garcia",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Chen",
    "Wang",
    "Zhang",
    "Liu",
    "Patel",
    "Kumar",
    "Singh",
    "Sharma",
    "Gupta",
]

COMPANIES = [
    "Google",
    "Microsoft",
    "Amazon",
    "Facebook/Meta",
    "Apple",
    "Tesla",
    "IBM",
    "Oracle",
    "LinkedIn",
    "Intel",
    "Qualcomm",
    "Nvidia",
    "TikTok/ByteDance",
    "Adobe",
    "Salesforce",
    "Uber",
    "Airbnb",
    "Netflix",
    "Stripe",
    "Databricks",
    "OpenAI",
    "DeepMind",
    "Startup XYZ",
    "Tech Company ABC",
]

UNIVERSITIES_UNDERGRAD = [
    "Stanford University",
    "MIT",
    "UC Berkeley",
    "CMU",
    "University of Washington",
    "University of Texas at Austin",
    "University of Illinois",
    "Cornell University",
    "Tsinghua University",
    "Peking University",
    "National University of Singapore",
    "University of Toronto",
    "IIT Delhi",
    "IIT Mumbai",
    "Fudan University",
    "Shanghai Jiao Tong University",
    "Zhejiang University",
]

JOURNALS = ["Q1", "Q2", "Q3", "Q4"]

RECOMMENDATION_TYPES = ["Research Advisor", "Course Instructor", "Employer"]


def generate_email(first_name: str, last_name: str) -> str:
    """Generate a unique email address."""
    return f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 9999)}@example.com"


def generate_gpa() -> tuple[float, float]:
    """Generate realistic GPA with scale."""
    # Most students have GPA between 3.0 and 4.0
    gpa = round(random.gauss(3.6, 0.3), 2)
    gpa = max(0.0, min(4.0, gpa))
    return gpa, 4.0


def generate_gre_score() -> int:
    """Generate realistic GRE score (260-340 range)."""
    # Most scores concentrated around 320-330
    score = int(random.gauss(320, 12))
    score = max(260, min(340, score))
    return score


def generate_toefl_score() -> int:
    """Generate realistic TOEFL score (0-120 range)."""
    # Most non-native speakers score 90-110
    score = int(random.gauss(100, 10))
    score = max(0, min(120, score))
    return score


def generate_admission_result() -> str:
    """Generate realistic admission result with varying probabilities."""
    # Top programs: 10-30% admit rate
    # Mid programs: 30-50% admit rate
    # Easier programs: 50-80% admit rate
    r = random.random()
    if r < 0.25:
        return "Accept"
    elif r < 0.5:
        return "Reject"
    else:
        return "Waitlist"


def create_sample_data():
    """Create sample data for CS graduate applications."""
    app = create_app()

    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        print("Starting data initialization...")

        # Generate 500 application records with associated user data
        num_users = 100  # 100 users, each with 5 applications on average
        applications_created = 0

        for user_idx in range(num_users):
            # Create user
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            email = generate_email(first_name, last_name)

            user = User(
                email=email,
                password_hash="hashed_password_placeholder",
            )
            db.session.add(user)
            db.session.flush()  # Get user ID

            # Create profile
            gpa, gpa_scale = generate_gpa()
            profile = Profile(
                user_id=user.id,
                preferred_name=f"{first_name} {last_name}",
                gpa=gpa,
                gpa_scale=gpa_scale,
                gre_total=generate_gre_score() if random.random() > 0.3 else None,
                toefl_total=generate_toefl_score()
                if random.random() > 0.5 else None,
                research_experience=random.random() > 0.4,
                internship_experience=random.random() > 0.3,
                recommendation_strength=random.choice(
                    ["Strongly Recommend", "Recommend"]
                ),
                notes=f"Applicant {user_idx + 1}",
            )
            db.session.add(profile)

            # Create education records
            edu = Education(
                user_id=user.id,
                institution=random.choice(UNIVERSITIES_UNDERGRAD),
                degree="Bachelor" if random.random() > 0.2 else "Master",
                field_of_study="Computer Science",
                start_year=random.randint(2015, 2020),
                end_year=random.randint(2019, 2023),
                gpa=round(random.uniform(2.8, 4.0), 2),
                gpa_scale=4.0,
                currently_enrolled=False,
            )
            db.session.add(edu)

            # Create test scores
            if random.random() > 0.2:  # 80% have GRE
                gre = TestScore(
                    user_id=user.id,
                    test_type="GRE",
                    total_score=generate_gre_score(),
                    section="Quantitative",
                    score_details=f"Q: {random.randint(150, 170)}, V: {random.randint(150, 170)}, AW: {random.randint(3, 6)}",
                    test_date=f"{random.randint(2021, 2023)}-{random.randint(1, 12):02d}",
                )
                db.session.add(gre)

            if random.random() > 0.4:  # 60% have TOEFL/IELTS
                test_type = random.choice(["TOEFL", "IELTS"])
                score = TestScore(
                    user_id=user.id,
                    test_type=test_type,
                    total_score=generate_toefl_score()
                    if test_type == "TOEFL" else random.randint(6, 9),
                    test_date=f"{random.randint(2021, 2023)}-{random.randint(1, 12):02d}",
                )
                db.session.add(score)

            # Create experience records
            num_experiences = random.randint(1, 3)
            for _ in range(num_experiences):
                exp = Experience(
                    user_id=user.id,
                    category=random.choice(["Work", "Research", "Internship"]),
                    organization=random.choice(COMPANIES),
                    role_title=random.choice(
                        [
                            "Software Engineer",
                            "Research Assistant",
                            "Data Scientist",
                            "Intern",
                            "ML Engineer",
                        ]
                    ),
                    description="Worked on various projects and tasks",
                    start_date=f"{random.randint(2019, 2022)}-{random.randint(1, 12):02d}",
                    end_date=f"{random.randint(2020, 2023)}-{random.randint(1, 12):02d}",
                    ongoing=random.random() > 0.7,
                )
                db.session.add(exp)

            # Create publications (some have them, some don't)
            if random.random() > 0.6:  # 40% have publications
                num_pubs = random.randint(1, 3)
                for pub_idx in range(num_pubs):
                    pub = Publication(
                        user_id=user.id,
                        title=f"Research Paper {pub_idx + 1}: Novel Approach to CS Problem",
                        venue=random.choice(
                            ["ICML", "NeurIPS", "ICCV", "CVPR", "ACL", "IEEE"]
                        ),
                        year=random.randint(2020, 2023),
                        first_author=random.random() > 0.5,
                        url=f"https://example.com/paper{pub_idx + 1}",
                    )
                    db.session.add(pub)

            # Create recommendation letters (most applicants have them)
            if random.random() > 0.1:  # 90% have at least one recommendation letter
                num_letters = random.randint(2, 4)
                recommender_names = [
                    "Prof. Johnson",
                    "Dr. Chen",
                    "Prof. Smith",
                    "Dr. Davis",
                    "Prof. Kumar",
                    "Dr. Martinez",
                ]
                for letter_idx in range(num_letters):
                    letter = RecommendationLetter(
                        user_id=user.id,
                        recommender_name=random.choice(recommender_names),
                        relationship=random.choice(
                            ["Research Advisor", "Course Instructor", "Employer"]
                        ),
                        rating=random.choice(
                            ["Strongly Recommend", "Recommend"]
                        ),
                        organization=random.choice(COMPANIES + UNIVERSITIES_UNDERGRAD),
                        notes=f"Strong recommendation for {first_name}",
                    )
                    db.session.add(letter)

            db.session.commit()

            # Create applications for this user
            num_applications = random.randint(3, 8)
            applied_universities = random.sample(UNIVERSITIES, num_applications)

            for uni_idx, (university, country) in enumerate(applied_universities):
                program = random.choice(PROGRAMS)
                degree = random.choice(["Master", "PhD"])
                semester = random.choice(
                    ["Fall 2022", "Spring 2023", "Fall 2023", "Spring 2024", "Fall 2024"]
                )
                result = generate_admission_result()
                funding = (
                    random.choice(
                        [
                            "Full Scholarship",
                            "Partial Scholarship",
                            "No Funding",
                            "TA Position",
                        ]
                    )
                    if result == "Accept"
                    else None
                )

                app_record = ApplicationRecord(
                    user_id=user.id,
                    university=university,
                    program=program,
                    country=country,
                    degree=degree,
                    term=semester,
                    result=result,
                    funding=funding,
                    notes=f"Application for {program} at {university}",
                    gpa=gpa,
                    gpa_scale=gpa_scale,
                    gre_total=profile.gre_total,
                    research_experience=profile.research_experience,
                    internship_experience=profile.internship_experience,
                    recommendation_strength=profile.recommendation_strength,
                )
                db.session.add(app_record)
                applications_created += 1

            if (user_idx + 1) % 10 == 0:
                print(f"Created {user_idx + 1} users, {applications_created} applications")
                db.session.commit()

        db.session.commit()
        print(
            f"\nDatabase initialization complete!"
        )
        print(
            f"Created {num_users} users with {applications_created} total applications"
        )

        # Print some statistics
        total_apps = ApplicationRecord.query.count()
        accept_count = ApplicationRecord.query.filter_by(result="Accept").count()
        reject_count = ApplicationRecord.query.filter_by(result="Reject").count()
        waitlist_count = ApplicationRecord.query.filter_by(
            result="Waitlist"
        ).count()

        print(f"\nStatistics:")
        print(f"  Total Applications: {total_apps}")
        print(f"  Accepts: {accept_count} ({accept_count/total_apps*100:.1f}%)")
        print(f"  Rejects: {reject_count} ({reject_count/total_apps*100:.1f}%)")
        print(
            f"  Waitlists: {waitlist_count} ({waitlist_count/total_apps*100:.1f}%)"
        )

        # Print university statistics
        unis = db.session.query(ApplicationRecord.university).distinct().all()
        progs = db.session.query(ApplicationRecord.program).distinct().all()

        print(f"\n  Unique Universities: {len(unis)}")
        print(f"  Unique Programs: {len(progs)}")


if __name__ == "__main__":
    create_sample_data()
