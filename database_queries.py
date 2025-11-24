from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Date, Time, DECIMAL, Text, CheckConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import date, time
import os

# db hookup change this if its diff
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/caregivers_db')

# spin up engine + session right away so i dont forget later
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# models go here
class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)

class Caregiver(Base):
    __tablename__ = 'caregiver'
    caregiver_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    photo = Column(String(255))
    gender = Column(String(20), nullable=False)
    caregiving_type = Column(String(50), nullable=False)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)

class Member(Base):
    __tablename__ = 'member'
    member_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)

class Address(Base):
    __tablename__ = 'address'
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), primary_key=True)
    house_number = Column(String(20), nullable=False)
    street = Column(String(255), nullable=False)
    town = Column(String(100), nullable=False)

class Job(Base):
    __tablename__ = 'job'
    job_id = Column(Integer, primary_key=True)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    required_caregiving_type = Column(String(50), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(Date, nullable=False)

class JobApplication(Base):
    __tablename__ = 'job_application'
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), primary_key=True)
    job_id = Column(Integer, ForeignKey('job.job_id', ondelete='CASCADE'), primary_key=True)
    date_applied = Column(Date, nullable=False)

class Appointment(Base):
    __tablename__ = 'appointment'
    appointment_id = Column(Integer, primary_key=True)
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), nullable=False)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(DECIMAL(4, 2), nullable=False)
    status = Column(String(20), nullable=False)

def print_separator(title):
    """prints a chunky divider"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def execute_query(query, description):
    """just runs whatever text block and dumps rows"""
    print(f"\n{description}")
    print("-" * 80)
    try:
        result = session.execute(text(query))
        rows = result.fetchall()
        if rows:
            # grab col names so table print looks nice
            columns = result.keys()
            # print header bar
            print(" | ".join(str(col) for col in columns))
            print("-" * 80)
            # Print rows
            for row in rows:
                print(" | ".join(str(val) for val in row))
        else:
            print("No results found.")
    except Exception as e:
        print(f"Error: {e}")
    print()

def main():
    print_separator("CSCI 341 Assignment 3 - Part 2: Database Queries")
    
    # section 1 create stuff
    print_separator("1. CREATE SQL STATEMENTS")
    print("Note: Tables should already be created using schema.sql")
    print("If tables don't exist, run schema.sql first.")
    
    # section 2 inserts (again schema.sql shouldve done it)
    print_separator("2. INSERT SQL STATEMENTS")
    print("Note: Data should already be inserted using schema.sql")
    print("If data is missing, run schema.sql first.")
    
    # section 3 updates sql
    print_separator("3. UPDATE SQL STATEMENTS")
    
    # phone upd for arman armanov
    print("3.1 Updating phone number of Arman Armanov to +77773414141...")
    update_query_1 = """
    UPDATE "user"
    SET phone_number = '+77773414141'
    WHERE given_name = 'Arman' AND surname = 'Armanov';
    """
    session.execute(text(update_query_1))
    session.commit()
    print("✓ Phone number updated successfully")
    
    # double check upd
    verify_query = """
    SELECT given_name, surname, phone_number
    FROM "user"
    WHERE given_name = 'Arman' AND surname = 'Armanov';
    """
    execute_query(verify_query, "Verification - Arman Armanov's phone number:")
    
    # 3.2 Add commission fee to Caregivers' hourly rate
    print("3.2 Adding commission fee to Caregivers' hourly rate...")
    update_query_2 = """
    UPDATE caregiver
    SET hourly_rate = CASE
        WHEN hourly_rate < 10 THEN hourly_rate + 0.3
        ELSE hourly_rate * 1.10
    END;
    """
    session.execute(text(update_query_2))
    session.commit()
    print("✓ Commission fee added successfully")
    
    verify_query_2 = """
    SELECT caregiver_user_id, hourly_rate
    FROM caregiver
    ORDER BY caregiver_user_id;
    """
    execute_query(verify_query_2, "Verification - Updated hourly rates:")
    
    # section 4 delete sqls
    print_separator("4. DELETE SQL STATEMENTS")
    
    # amina posted too many jobs
    print("4.1 Deleting jobs posted by Amina Aminova...")
    delete_query_1 = """
    DELETE FROM job
    WHERE member_user_id IN (
        SELECT member_user_id
        FROM member
        WHERE member_user_id IN (
            SELECT user_id
            FROM "user"
            WHERE given_name = 'Amina' AND surname = 'Aminova'
        )
    );
    """
    session.execute(text(delete_query_1))
    session.commit()
    print("✓ Jobs deleted successfully")
    
    verify_query_3 = """
    SELECT j.job_id, u.given_name, u.surname
    FROM job j
    JOIN member m ON j.member_user_id = m.member_user_id
    JOIN "user" u ON m.member_user_id = u.user_id
    WHERE u.given_name = 'Amina' AND u.surname = 'Aminova';
    """
    execute_query(verify_query_3, "Verification - Remaining jobs by Amina Aminova (should be empty):")
    
    # delete  members on kaba street
    print("4.2 Deleting all members who live on Kabanbay Batyr street...")
    delete_query_2 = """
    DELETE FROM member
    WHERE member_user_id IN (
        SELECT member_user_id
        FROM address
        WHERE street = 'Kabanbay Batyr'
    );
    """
    session.execute(text(delete_query_2))
    session.commit()
    print("✓ Members deleted successfully")
    
    # confirm street list empty
    verify_query_4 = """
    SELECT m.member_user_id, u.given_name, u.surname, a.street
    FROM member m
    JOIN "user" u ON m.member_user_id = u.user_id
    JOIN address a ON m.member_user_id = a.member_user_id
    WHERE a.street = 'Kabanbay Batyr';
    """
    execute_query(verify_query_4, "Verification - Remaining members on Kabanbay Batyr (should be empty):")
    
    # section 5
    print_separator("5. SIMPLE QUERIES")
    
    #show who accepted who
    query_5_1 = """
    SELECT 
        cg.given_name AS caregiver_given_name,
        cg.surname AS caregiver_surname,
        m.given_name AS member_given_name,
        m.surname AS member_surname
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN "user" cg ON c.caregiver_user_id = cg.user_id
    JOIN member mem ON a.member_user_id = mem.member_user_id
    JOIN "user" m ON mem.member_user_id = m.user_id
    WHERE a.status = 'confirmed';
    """
    execute_query(query_5_1, "5.1 Caregiver and member names for accepted appointments:")
    
    #find soft spoken 
    query_5_2 = """
    SELECT job_id, other_requirements
    FROM job
    WHERE other_requirements LIKE '%soft-spoken%';
    """
    execute_query(query_5_2, "5.2 Job IDs containing 'soft-spoken' in requirements:")
    
    # babysitter hours
    query_5_3 = """
    SELECT 
        a.appointment_id,
        a.work_hours,
        c.caregiving_type
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    WHERE c.caregiving_type = 'babysitter';
    """
    execute_query(query_5_3, "5.3 Work hours of all babysitter positions:")
    
    #elderly care with no pets rule
    query_5_4 = """
    SELECT DISTINCT
        u.user_id,
        u.given_name,
        u.surname,
        u.city,
        m.house_rules
    FROM member m
    JOIN "user" u ON m.member_user_id = u.user_id
    JOIN job j ON m.member_user_id = j.member_user_id
    WHERE j.required_caregiving_type = 'elderly care'
        AND u.city = 'Astana'
        AND m.house_rules LIKE '%No pets%';
    """
    execute_query(query_5_4, "5.4 Members looking for Elderly Care in Astana with 'No pets' rule:")
    
    # section 6
    print_separator("6. COMPLEX QUERIES")
    
    # headcount per job
    query_6_1 = """
    SELECT 
        j.job_id,
        u.given_name || ' ' || u.surname AS member_name,
        COUNT(ja.caregiver_user_id) AS number_of_applicants
    FROM job j
    JOIN member m ON j.member_user_id = m.member_user_id
    JOIN "user" u ON m.member_user_id = u.user_id
    LEFT JOIN job_application ja ON j.job_id = ja.job_id
    GROUP BY j.job_id, u.given_name, u.surname
    ORDER BY j.job_id;
    """
    execute_query(query_6_1, "6.1 Number of applicants for each job:")
    
    #total confirmd hours
    query_6_2 = """
    SELECT 
        SUM(a.work_hours) AS total_hours
    FROM appointment a
    WHERE a.status = 'confirmed';
    """
    execute_query(query_6_2, "6.2 Total hours spent by caregivers for all accepted appointments:")
    
    #avg payout for confirmd caregivers
    query_6_3 = """
    SELECT 
        AVG(c.hourly_rate * a.work_hours) AS average_pay
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    WHERE a.status = 'confirmed';
    """
    execute_query(query_6_3, "6.3 Average pay of caregivers based on accepted appointments:")
    
    query_6_4 = """
    SELECT 
        u.given_name,
        u.surname,
        c.hourly_rate,
        SUM(a.work_hours) AS total_hours,
        SUM(c.hourly_rate * a.work_hours) AS total_earnings
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN "user" u ON c.caregiver_user_id = u.user_id
    WHERE a.status = 'confirmed'
    GROUP BY u.given_name, u.surname, c.hourly_rate
    HAVING SUM(c.hourly_rate * a.work_hours) > (
        SELECT AVG(sub_c.hourly_rate * sub_a.work_hours)
        FROM appointment sub_a
        JOIN caregiver sub_c ON sub_a.caregiver_user_id = sub_c.caregiver_user_id
        WHERE sub_a.status = 'confirmed'
    )
    ORDER BY total_earnings DESC;
    """
    execute_query(query_6_4, "6.4 Caregivers who earn above average based on accepted appointments:")
    
    # section 7
    print_separator("7. QUERY WITH A DERIVED ATTRIBUTE")
    
    # calc total cost per caregiver per confirmd appt
    query_7 = """
    SELECT 
        a.appointment_id,
        u.given_name || ' ' || u.surname AS caregiver_name,
        a.work_hours,
        c.hourly_rate,
        (c.hourly_rate * a.work_hours) AS total_cost
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN "user" u ON c.caregiver_user_id = u.user_id
    WHERE a.status = 'confirmed'
    ORDER BY a.appointment_id;
    """
    execute_query(query_7, "7. Total cost to pay for caregivers for all accepted appointments:")
    
    # section 8
    print_separator("8. VIEW OPERATION")
    
    # build a view
    print("Creating view: job_applications_view")
    create_view_query = """
    CREATE OR REPLACE VIEW job_applications_view AS
    SELECT 
        ja.job_id,
        j.required_caregiving_type,
        j.other_requirements,
        ja.date_applied,
        u.given_name AS applicant_given_name,
        u.surname AS applicant_surname,
        u.email AS applicant_email,
        c.caregiving_type,
        c.hourly_rate
    FROM job_application ja
    JOIN job j ON ja.job_id = j.job_id
    JOIN caregiver c ON ja.caregiver_user_id = c.caregiver_user_id
    JOIN "user" u ON c.caregiver_user_id = u.user_id;
    """
    session.execute(text(create_view_query))
    session.commit()
    print("✓ View created successfully")
    
    # Query the view
    view_query = """
    SELECT * FROM job_applications_view
    ORDER BY job_id, date_applied;
    """
    execute_query(view_query, "8. View: All job applications and applicants:")
    
    print_separator("END OF QUERIES")
    print("All queries executed successfully!")
    
    session.close()

if __name__ == "__main__":
    main()

