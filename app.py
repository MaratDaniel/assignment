"""
CSCI 341 Assignment 3 - Part 3
Flask Web Application with CRUD Operations
Online Caregivers Platform
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import date, time, datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Database connection configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/caregivers_db')

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

# ============================================================================
# USER CRUD Operations
# ============================================================================

@app.route('/users')
def list_users():
    """List all users"""
    session = get_session()
    try:
        result = session.execute(text("SELECT * FROM \"user\" ORDER BY user_id"))
        users = [dict(row._mapping) for row in result]
        return render_template('users/list.html', users=users)
    finally:
        session.close()

@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    """Create a new user"""
    if request.method == 'POST':
        session = get_session()
        try:
            query = text("""
                INSERT INTO "user" (email, given_name, surname, city, phone_number, profile_description, password)
                VALUES (:email, :given_name, :surname, :city, :phone_number, :profile_description, :password)
            """)
            session.execute(query, {
                'email': request.form['email'],
                'given_name': request.form['given_name'],
                'surname': request.form['surname'],
                'city': request.form['city'],
                'phone_number': request.form['phone_number'],
                'profile_description': request.form.get('profile_description', ''),
                'password': request.form['password']
            })
            session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('list_users'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating user: {str(e)}', 'error')
        finally:
            session.close()
    return render_template('users/form.html', user=None)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def update_user(user_id):
    """Update a user"""
    session = get_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE "user"
                SET email = :email, given_name = :given_name, surname = :surname,
                    city = :city, phone_number = :phone_number,
                    profile_description = :profile_description, password = :password
                WHERE user_id = :user_id
            """)
            session.execute(query, {
                'user_id': user_id,
                'email': request.form['email'],
                'given_name': request.form['given_name'],
                'surname': request.form['surname'],
                'city': request.form['city'],
                'phone_number': request.form['phone_number'],
                'profile_description': request.form.get('profile_description', ''),
                'password': request.form['password']
            })
            session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('list_users'))
        else:
            result = session.execute(text("SELECT * FROM \"user\" WHERE user_id = :user_id"), {'user_id': user_id})
            user = result.fetchone()
            if user:
                user = dict(user._mapping)
                return render_template('users/form.html', user=user)
            else:
                flash('User not found!', 'error')
                return redirect(url_for('list_users'))
    except Exception as e:
        session.rollback()
        flash(f'Error updating user: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    session = get_session()
    try:
        session.execute(text("DELETE FROM \"user\" WHERE user_id = :user_id"), {'user_id': user_id})
        session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_users'))

# ============================================================================
# CAREGIVER CRUD Operations
# ============================================================================

@app.route('/caregivers')
def list_caregivers():
    """List all caregivers"""
    session = get_session()
    try:
        result = session.execute(text("""
            SELECT c.*, u.given_name, u.surname, u.email, u.city, u.phone_number
            FROM caregiver c
            JOIN "user" u ON c.caregiver_user_id = u.user_id
            ORDER BY c.caregiver_user_id
        """))
        caregivers = [dict(row._mapping) for row in result]
        return render_template('caregivers/list.html', caregivers=caregivers)
    finally:
        session.close()

@app.route('/caregivers/new', methods=['GET', 'POST'])
def create_caregiver():
    """Create a new caregiver"""
    if request.method == 'POST':
        session = get_session()
        try:
            # First create user, then caregiver
            user_query = text("""
                INSERT INTO "user" (email, given_name, surname, city, phone_number, profile_description, password)
                VALUES (:email, :given_name, :surname, :city, :phone_number, :profile_description, :password)
                RETURNING user_id
            """)
            result = session.execute(user_query, {
                'email': request.form['email'],
                'given_name': request.form['given_name'],
                'surname': request.form['surname'],
                'city': request.form['city'],
                'phone_number': request.form['phone_number'],
                'profile_description': request.form.get('profile_description', ''),
                'password': request.form['password']
            })
            user_id = result.fetchone()[0]
            
            caregiver_query = text("""
                INSERT INTO caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate)
                VALUES (:caregiver_user_id, :photo, :gender, :caregiving_type, :hourly_rate)
            """)
            session.execute(caregiver_query, {
                'caregiver_user_id': user_id,
                'photo': request.form.get('photo', ''),
                'gender': request.form['gender'],
                'caregiving_type': request.form['caregiving_type'],
                'hourly_rate': request.form['hourly_rate']
            })
            session.commit()
            flash('Caregiver created successfully!', 'success')
            return redirect(url_for('list_caregivers'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating caregiver: {str(e)}', 'error')
        finally:
            session.close()
    return render_template('caregivers/form.html', caregiver=None)

@app.route('/caregivers/<int:caregiver_id>/edit', methods=['GET', 'POST'])
def update_caregiver(caregiver_id):
    """Update a caregiver"""
    session = get_session()
    try:
        if request.method == 'POST':
            caregiver_query = text("""
                UPDATE caregiver
                SET photo = :photo, gender = :gender, caregiving_type = :caregiving_type, hourly_rate = :hourly_rate
                WHERE caregiver_user_id = :caregiver_user_id
            """)
            session.execute(caregiver_query, {
                'caregiver_user_id': caregiver_id,
                'photo': request.form.get('photo', ''),
                'gender': request.form['gender'],
                'caregiving_type': request.form['caregiving_type'],
                'hourly_rate': request.form['hourly_rate']
            })
            session.commit()
            flash('Caregiver updated successfully!', 'success')
            return redirect(url_for('list_caregivers'))
        else:
            result = session.execute(text("""
                SELECT c.*, u.given_name, u.surname, u.email, u.city, u.phone_number, u.profile_description
                FROM caregiver c
                JOIN "user" u ON c.caregiver_user_id = u.user_id
                WHERE c.caregiver_user_id = :caregiver_id
            """), {'caregiver_id': caregiver_id})
            caregiver = result.fetchone()
            if caregiver:
                caregiver = dict(caregiver._mapping)
                return render_template('caregivers/form.html', caregiver=caregiver)
            else:
                flash('Caregiver not found!', 'error')
                return redirect(url_for('list_caregivers'))
    except Exception as e:
        session.rollback()
        flash(f'Error updating caregiver: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_caregivers'))

@app.route('/caregivers/<int:caregiver_id>/delete', methods=['POST'])
def delete_caregiver(caregiver_id):
    """Delete a caregiver"""
    session = get_session()
    try:
        session.execute(text("DELETE FROM caregiver WHERE caregiver_user_id = :caregiver_id"), {'caregiver_id': caregiver_id})
        session.commit()
        flash('Caregiver deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting caregiver: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_caregivers'))

# ============================================================================
# MEMBER CRUD Operations
# ============================================================================

@app.route('/members')
def list_members():
    """List all members"""
    session = get_session()
    try:
        result = session.execute(text("""
            SELECT m.*, u.given_name, u.surname, u.email, u.city, u.phone_number
            FROM member m
            JOIN "user" u ON m.member_user_id = u.user_id
            ORDER BY m.member_user_id
        """))
        members = [dict(row._mapping) for row in result]
        return render_template('members/list.html', members=members)
    finally:
        session.close()

@app.route('/members/new', methods=['GET', 'POST'])
def create_member():
    """Create a new member"""
    if request.method == 'POST':
        session = get_session()
        try:
            user_query = text("""
                INSERT INTO "user" (email, given_name, surname, city, phone_number, profile_description, password)
                VALUES (:email, :given_name, :surname, :city, :phone_number, :profile_description, :password)
                RETURNING user_id
            """)
            result = session.execute(user_query, {
                'email': request.form['email'],
                'given_name': request.form['given_name'],
                'surname': request.form['surname'],
                'city': request.form['city'],
                'phone_number': request.form['phone_number'],
                'profile_description': request.form.get('profile_description', ''),
                'password': request.form['password']
            })
            user_id = result.fetchone()[0]
            
            member_query = text("""
                INSERT INTO member (member_user_id, house_rules, dependent_description)
                VALUES (:member_user_id, :house_rules, :dependent_description)
            """)
            session.execute(member_query, {
                'member_user_id': user_id,
                'house_rules': request.form.get('house_rules', ''),
                'dependent_description': request.form.get('dependent_description', '')
            })
            session.commit()
            flash('Member created successfully!', 'success')
            return redirect(url_for('list_members'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating member: {str(e)}', 'error')
        finally:
            session.close()
    return render_template('members/form.html', member=None)

@app.route('/members/<int:member_id>/edit', methods=['GET', 'POST'])
def update_member(member_id):
    """Update a member"""
    session = get_session()
    try:
        if request.method == 'POST':
            member_query = text("""
                UPDATE member
                SET house_rules = :house_rules, dependent_description = :dependent_description
                WHERE member_user_id = :member_user_id
            """)
            session.execute(member_query, {
                'member_user_id': member_id,
                'house_rules': request.form.get('house_rules', ''),
                'dependent_description': request.form.get('dependent_description', '')
            })
            session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('list_members'))
        else:
            result = session.execute(text("""
                SELECT m.*, u.given_name, u.surname, u.email, u.city, u.phone_number, u.profile_description
                FROM member m
                JOIN "user" u ON m.member_user_id = u.user_id
                WHERE m.member_user_id = :member_id
            """), {'member_id': member_id})
            member = result.fetchone()
            if member:
                member = dict(member._mapping)
                return render_template('members/form.html', member=member)
            else:
                flash('Member not found!', 'error')
                return redirect(url_for('list_members'))
    except Exception as e:
        session.rollback()
        flash(f'Error updating member: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_members'))

@app.route('/members/<int:member_id>/delete', methods=['POST'])
def delete_member(member_id):
    """Delete a member"""
    session = get_session()
    try:
        session.execute(text("DELETE FROM member WHERE member_user_id = :member_id"), {'member_id': member_id})
        session.commit()
        flash('Member deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting member: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_members'))

# ============================================================================
# ADDRESS CRUD Operations
# ============================================================================

@app.route('/addresses')
def list_addresses():
    """List all addresses"""
    session = get_session()
    try:
        result = session.execute(text("""
            SELECT a.*, u.given_name, u.surname
            FROM address a
            JOIN member m ON a.member_user_id = m.member_user_id
            JOIN "user" u ON m.member_user_id = u.user_id
            ORDER BY a.member_user_id
        """))
        addresses = [dict(row._mapping) for row in result]
        return render_template('addresses/list.html', addresses=addresses)
    finally:
        session.close()

@app.route('/addresses/new', methods=['GET', 'POST'])
def create_address():
    """Create a new address"""
    if request.method == 'POST':
        session = get_session()
        try:
            query = text("""
                INSERT INTO address (member_user_id, house_number, street, town)
                VALUES (:member_user_id, :house_number, :street, :town)
            """)
            session.execute(query, {
                'member_user_id': request.form['member_user_id'],
                'house_number': request.form['house_number'],
                'street': request.form['street'],
                'town': request.form['town']
            })
            session.commit()
            flash('Address created successfully!', 'success')
            return redirect(url_for('list_addresses'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating address: {str(e)}', 'error')
        finally:
            session.close()
    session = get_session()
    try:
        result = session.execute(text("SELECT member_user_id FROM member ORDER BY member_user_id"))
        members = [dict(row._mapping) for row in result]
        return render_template('addresses/form.html', address=None, members=members)
    finally:
        session.close()

@app.route('/addresses/<int:member_id>/edit', methods=['GET', 'POST'])
def update_address(member_id):
    """Update an address"""
    session = get_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE address
                SET house_number = :house_number, street = :street, town = :town
                WHERE member_user_id = :member_user_id
            """)
            session.execute(query, {
                'member_user_id': member_id,
                'house_number': request.form['house_number'],
                'street': request.form['street'],
                'town': request.form['town']
            })
            session.commit()
            flash('Address updated successfully!', 'success')
            return redirect(url_for('list_addresses'))
        else:
            result = session.execute(text("SELECT * FROM address WHERE member_user_id = :member_id"), {'member_id': member_id})
            address = result.fetchone()
            if address:
                address = dict(address._mapping)
                return render_template('addresses/form.html', address=address, members=[])
            else:
                flash('Address not found!', 'error')
                return redirect(url_for('list_addresses'))
    except Exception as e:
        session.rollback()
        flash(f'Error updating address: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_addresses'))

@app.route('/addresses/<int:member_id>/delete', methods=['POST'])
def delete_address(member_id):
    """Delete an address"""
    session = get_session()
    try:
        session.execute(text("DELETE FROM address WHERE member_user_id = :member_id"), {'member_id': member_id})
        session.commit()
        flash('Address deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting address: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_addresses'))

# ============================================================================
# JOB CRUD Operations
# ============================================================================

@app.route('/jobs')
def list_jobs():
    """List all jobs"""
    session = get_session()
    try:
        result = session.execute(text("""
            SELECT j.*, u.given_name, u.surname
            FROM job j
            JOIN member m ON j.member_user_id = m.member_user_id
            JOIN "user" u ON m.member_user_id = u.user_id
            ORDER BY j.job_id
        """))
        jobs = [dict(row._mapping) for row in result]
        return render_template('jobs/list.html', jobs=jobs)
    finally:
        session.close()

@app.route('/jobs/new', methods=['GET', 'POST'])
def create_job():
    """Create a new job"""
    if request.method == 'POST':
        session = get_session()
        try:
            query = text("""
                INSERT INTO job (member_user_id, required_caregiving_type, other_requirements, date_posted)
                VALUES (:member_user_id, :required_caregiving_type, :other_requirements, :date_posted)
            """)
            session.execute(query, {
                'member_user_id': request.form['member_user_id'],
                'required_caregiving_type': request.form['required_caregiving_type'],
                'other_requirements': request.form.get('other_requirements', ''),
                'date_posted': request.form['date_posted']
            })
            session.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('list_jobs'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating job: {str(e)}', 'error')
        finally:
            session.close()
    session = get_session()
    try:
        result = session.execute(text("SELECT member_user_id FROM member ORDER BY member_user_id"))
        members = [dict(row._mapping) for row in result]
        return render_template('jobs/form.html', job=None, members=members)
    finally:
        session.close()

@app.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
def update_job(job_id):
    """Update a job"""
    session = get_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE job
                SET member_user_id = :member_user_id, required_caregiving_type = :required_caregiving_type,
                    other_requirements = :other_requirements, date_posted = :date_posted
                WHERE job_id = :job_id
            """)
            session.execute(query, {
                'job_id': job_id,
                'member_user_id': request.form['member_user_id'],
                'required_caregiving_type': request.form['required_caregiving_type'],
                'other_requirements': request.form.get('other_requirements', ''),
                'date_posted': request.form['date_posted']
            })
            session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('list_jobs'))
        else:
            result = session.execute(text("SELECT * FROM job WHERE job_id = :job_id"), {'job_id': job_id})
            job = result.fetchone()
            if job:
                job = dict(job._mapping)
                result2 = session.execute(text("SELECT member_user_id FROM member ORDER BY member_user_id"))
                members = [dict(row._mapping) for row in result2]
                return render_template('jobs/form.html', job=job, members=members)
            else:
                flash('Job not found!', 'error')
                return redirect(url_for('list_jobs'))
    except Exception as e:
        session.rollback()
        flash(f'Error updating job: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_jobs'))

@app.route('/jobs/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    """Delete a job"""
    session = get_session()
    try:
        session.execute(text("DELETE FROM job WHERE job_id = :job_id"), {'job_id': job_id})
        session.commit()
        flash('Job deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting job: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_jobs'))

# ============================================================================
# JOB_APPLICATION CRUD Operations
# ============================================================================

@app.route('/job_applications')
def list_job_applications():
    """List all job applications"""
    session = get_session()
    try:
        result = session.execute(text("""
            SELECT ja.*, u1.given_name AS caregiver_name, u1.surname AS caregiver_surname,
                   u2.given_name AS member_name, u2.surname AS member_surname, j.required_caregiving_type
            FROM job_application ja
            JOIN caregiver c ON ja.caregiver_user_id = c.caregiver_user_id
            JOIN "user" u1 ON c.caregiver_user_id = u1.user_id
            JOIN job j ON ja.job_id = j.job_id
            JOIN member m ON j.member_user_id = m.member_user_id
            JOIN "user" u2 ON m.member_user_id = u2.user_id
            ORDER BY ja.job_id, ja.date_applied
        """))
        applications = [dict(row._mapping) for row in result]
        return render_template('job_applications/list.html', applications=applications)
    finally:
        session.close()

@app.route('/job_applications/new', methods=['GET', 'POST'])
def create_job_application():
    """Create a new job application"""
    if request.method == 'POST':
        session = get_session()
        try:
            query = text("""
                INSERT INTO job_application (caregiver_user_id, job_id, date_applied)
                VALUES (:caregiver_user_id, :job_id, :date_applied)
            """)
            session.execute(query, {
                'caregiver_user_id': request.form['caregiver_user_id'],
                'job_id': request.form['job_id'],
                'date_applied': request.form['date_applied']
            })
            session.commit()
            flash('Job application created successfully!', 'success')
            return redirect(url_for('list_job_applications'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating job application: {str(e)}', 'error')
        finally:
            session.close()
    session = get_session()
    try:
        caregivers = session.execute(text("SELECT caregiver_user_id FROM caregiver ORDER BY caregiver_user_id"))
        jobs = session.execute(text("SELECT job_id FROM job ORDER BY job_id"))
        return render_template('job_applications/form.html', application=None,
                             caregivers=[dict(row._mapping) for row in caregivers],
                             jobs=[dict(row._mapping) for row in jobs])
    finally:
        session.close()

@app.route('/job_applications/<int:caregiver_id>/<int:job_id>/edit', methods=['GET', 'POST'])
def update_job_application(caregiver_id, job_id):
    """Update a job application"""
    session = get_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE job_application
                SET date_applied = :date_applied
                WHERE caregiver_user_id = :caregiver_id AND job_id = :job_id
            """)
            session.execute(query, {
                'caregiver_id': caregiver_id,
                'job_id': job_id,
                'date_applied': request.form['date_applied']
            })
            session.commit()
            flash('Job application updated successfully!', 'success')
            return redirect(url_for('list_job_applications'))
        else:
            result = session.execute(text("""
                SELECT * FROM job_application
                WHERE caregiver_user_id = :caregiver_id AND job_id = :job_id
            """), {'caregiver_id': caregiver_id, 'job_id': job_id})
            application = result.fetchone()
            if application:
                application = dict(application._mapping)
                caregivers = session.execute(text("SELECT caregiver_user_id FROM caregiver ORDER BY caregiver_user_id"))
                jobs = session.execute(text("SELECT job_id FROM job ORDER BY job_id"))
                return render_template('job_applications/form.html', application=application,
                                     caregivers=[dict(row._mapping) for row in caregivers],
                                     jobs=[dict(row._mapping) for row in jobs])
            else:
                flash('Job application not found!', 'error')
                return redirect(url_for('list_job_applications'))
    except Exception as e:
        session.rollback()
        flash(f'Error updating job application: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_job_applications'))

@app.route('/job_applications/<int:caregiver_id>/<int:job_id>/delete', methods=['POST'])
def delete_job_application(caregiver_id, job_id):
    """Delete a job application"""
    session = get_session()
    try:
        session.execute(text("""
            DELETE FROM job_application
            WHERE caregiver_user_id = :caregiver_id AND job_id = :job_id
        """), {'caregiver_id': caregiver_id, 'job_id': job_id})
        session.commit()
        flash('Job application deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting job application: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_job_applications'))

# ============================================================================
# APPOINTMENT CRUD Operations
# ============================================================================

@app.route('/appointments')
def list_appointments():
    """List all appointments"""
    session = get_session()
    try:
        result = session.execute(text("""
            SELECT a.*, u1.given_name AS caregiver_name, u1.surname AS caregiver_surname,
                   u2.given_name AS member_name, u2.surname AS member_surname
            FROM appointment a
            JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
            JOIN "user" u1 ON c.caregiver_user_id = u1.user_id
            JOIN member m ON a.member_user_id = m.member_user_id
            JOIN "user" u2 ON m.member_user_id = u2.user_id
            ORDER BY a.appointment_date, a.appointment_time
        """))
        appointments = [dict(row._mapping) for row in result]
        return render_template('appointments/list.html', appointments=appointments)
    finally:
        session.close()

@app.route('/appointments/new', methods=['GET', 'POST'])
def create_appointment():
    """Create a new appointment"""
    if request.method == 'POST':
        session = get_session()
        try:
            query = text("""
                INSERT INTO appointment (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status)
                VALUES (:caregiver_user_id, :member_user_id, :appointment_date, :appointment_time, :work_hours, :status)
            """)
            session.execute(query, {
                'caregiver_user_id': request.form['caregiver_user_id'],
                'member_user_id': request.form['member_user_id'],
                'appointment_date': request.form['appointment_date'],
                'appointment_time': request.form['appointment_time'],
                'work_hours': request.form['work_hours'],
                'status': request.form['status']
            })
            session.commit()
            flash('Appointment created successfully!', 'success')
            return redirect(url_for('list_appointments'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating appointment: {str(e)}', 'error')
        finally:
            session.close()
    session = get_session()
    try:
        caregivers = session.execute(text("SELECT caregiver_user_id FROM caregiver ORDER BY caregiver_user_id"))
        members = session.execute(text("SELECT member_user_id FROM member ORDER BY member_user_id"))
        return render_template('appointments/form.html', appointment=None,
                             caregivers=[dict(row._mapping) for row in caregivers],
                             members=[dict(row._mapping) for row in members])
    finally:
        session.close()

@app.route('/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
def update_appointment(appointment_id):
    """Update an appointment"""
    session = get_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE appointment
                SET caregiver_user_id = :caregiver_user_id, member_user_id = :member_user_id,
                    appointment_date = :appointment_date, appointment_time = :appointment_time,
                    work_hours = :work_hours, status = :status
                WHERE appointment_id = :appointment_id
            """)
            session.execute(query, {
                'appointment_id': appointment_id,
                'caregiver_user_id': request.form['caregiver_user_id'],
                'member_user_id': request.form['member_user_id'],
                'appointment_date': request.form['appointment_date'],
                'appointment_time': request.form['appointment_time'],
                'work_hours': request.form['work_hours'],
                'status': request.form['status']
            })
            session.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('list_appointments'))
        else:
            result = session.execute(text("SELECT * FROM appointment WHERE appointment_id = :appointment_id"), {'appointment_id': appointment_id})
            appointment = result.fetchone()
            if appointment:
                appointment = dict(appointment._mapping)
                caregivers = session.execute(text("SELECT caregiver_user_id FROM caregiver ORDER BY caregiver_user_id"))
                members = session.execute(text("SELECT member_user_id FROM member ORDER BY member_user_id"))
                return render_template('appointments/form.html', appointment=appointment,
                                     caregivers=[dict(row._mapping) for row in caregivers],
                                     members=[dict(row._mapping) for row in members])
            else:
                flash('Appointment not found!', 'error')
                return redirect(url_for('list_appointments'))
    except Exception as e:
        session.rollback()
        flash(f'Error updating appointment: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_appointments'))

@app.route('/appointments/<int:appointment_id>/delete', methods=['POST'])
def delete_appointment(appointment_id):
    """Delete an appointment"""
    session = get_session()
    try:
        session.execute(text("DELETE FROM appointment WHERE appointment_id = :appointment_id"), {'appointment_id': appointment_id})
        session.commit()
        flash('Appointment deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting appointment: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_appointments'))

# ============================================================================
# Home Page
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

