"""
CreditFit 360 - Database Layer
Production-grade SQLite persistence for:
1. User Authentication & Profile
2. Credit Assessments History (Personal, SME, Loan Readiness)
3. RBI Statutory Penalty & Bureau Disputes Tracking
4. DPDP Act 2023 Compliance & Consent Audit Logs
"""

import sqlite3
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import os
import shutil

import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Vercel Serverless compatibility: Root directory on Vercel is read-only
if os.environ.get("VERCEL") or not os.access(BASE_DIR, os.W_OK):
    tmp_dir = "/tmp" if os.path.exists("/tmp") else tempfile.gettempdir()
    DB_PATH = os.path.join(tmp_dir, "database.db")
    orig_db = os.path.join(BASE_DIR, "database.db")
    if os.path.exists(orig_db) and not os.path.exists(DB_PATH):
        try:
            shutil.copy2(orig_db, DB_PATH)
        except Exception:
            pass
else:
    DB_PATH = os.path.join(BASE_DIR, "database.db")



def get_db_connection():
    """Returns a SQLite connection with row factory configured."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes all database tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            occupation TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        );
    """)

    # 2. Credit Assessments Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credit_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            assessment_type TEXT NOT NULL, -- 'personal', 'sme', 'loan_readiness', 'decision_lab'
            score INTEGER NOT NULL,
            category TEXT,
            foir REAL,
            credit_utilisation REAL,
            monthly_income REAL,
            raw_input_json TEXT,
            result_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    # 3. Statutory Disputes & RBI Penalties Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statutory_disputes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            borrower_name TEXT NOT NULL,
            lender_name TEXT NOT NULL,
            bureau_name TEXT NOT NULL,
            grievance_date TEXT NOT NULL,
            resolution_date TEXT,
            delay_days INTEGER DEFAULT 0,
            penalty_amount REAL DEFAULT 0.0,
            error_description TEXT,
            status TEXT DEFAULT 'Drafted', -- 'Drafted', 'Notice Generated', 'Served', 'Resolved'
            notice_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    # 4. DPDP Act 2023 Consent Audit Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dpdp_consent_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            consent_type TEXT NOT NULL, -- 'FINANCIAL_PROFILING', 'ACCOUNT_AGGREGATOR_FETCH', 'DISPUTE_REPRESENTATION'
            purpose_code TEXT NOT NULL,
            status TEXT NOT NULL, -- 'GRANTED', 'REVOKED'
            ip_address TEXT,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    conn.commit()

    # Create a default demo user if none exists
    cursor.execute("SELECT id FROM users WHERE email = 'demo@creditfit360.com'")
    if not cursor.fetchone():
        hashed = generate_password_hash("Demo@123")
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, phone, occupation, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "demo@creditfit360.com",
            hashed,
            "Smita Dwivedi (Demo)",
            "+91 98765 43210",
            "Fintech Founder & Senior Analyst",
            "pro_member"
        ))
        demo_user_id = cursor.lastrowid

        # Insert a sample assessment for demo user
        sample_result = {
            "score": 765,
            "category": "Excellent Financial Health",
            "emi_burden": 24.5,
            "credit_utilisation": 18.2,
            "emergency_months": 5.4,
            "monthly_balance": 35000
        }
        cursor.execute("""
            INSERT INTO credit_assessments (user_id, assessment_type, score, category, foir, credit_utilisation, monthly_income, result_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            demo_user_id,
            "personal",
            765,
            "Excellent Financial Health",
            24.5,
            18.2,
            75000.0,
            json.dumps(sample_result)
        ))

        # Insert a sample dispute log for demo user
        cursor.execute("""
            INSERT INTO statutory_disputes (user_id, borrower_name, lender_name, bureau_name, grievance_date, resolution_date, delay_days, penalty_amount, error_description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            demo_user_id,
            "Smita Dwivedi",
            "HDFC Bank",
            "CIBIL",
            "2026-08-01",
            "2026-09-15",
            15,
            1500.0,
            "Closed Credit Card shown as active with delinquent status",
            "Notice Served"
        ))

        # Log DPDP consent for demo user
        cursor.execute("""
            INSERT INTO dpdp_consent_logs (user_id, consent_type, purpose_code, status, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            demo_user_id,
            "FINANCIAL_PROFILING",
            "PURPOSE_REVERSE_UNDERWRITE_V2",
            "GRANTED",
            "127.0.0.1",
            "CreditFit360 System Init"
        ))

        conn.commit()

    # Pre-seed verified account for founder Smita Dwivedi
    cursor.execute("SELECT id FROM users WHERE email = 'smitadwivedi03@gmail.com'")
    if not cursor.fetchone():
        hashed_smita = generate_password_hash("Demo@123")
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, phone, occupation, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "smitadwivedi03@gmail.com",
            hashed_smita,
            "Smita Dwivedi",
            "+91 99198 09421",
            "Fintech Founder & Senior Analyst",
            "verified_member"
        ))
        smita_user_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO credit_assessments (user_id, assessment_type, score, category, foir, credit_utilisation, monthly_income, result_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            smita_user_id,
            "personal",
            785,
            "Prime Tier-1 Creditworthiness",
            18.67,
            17.6,
            75000.0,
            json.dumps({
                "score": 785,
                "category": "Prime Tier-1 Creditworthiness",
                "full_name": "Smita Dwivedi",
                "monthly_income": 75000,
                "household_expenses": 22000,
                "existing_emi": 14000,
                "monthly_savings": 18000,
                "monthly_investment": 12000,
                "credit_score": 752,
                "credit_limit": 150000,
                "credit_outstanding": 26400,
                "credit_utilisation": 17.6,
                "active_loans": 1,
                "missed_payments": 0,
                "credit_applications": 1,
                "current_savings": 88000,
                "investments": 125000,
                "emergency_fund": 72000,
                "essential_expenses": 24000,
                "emi_burden": 18.67,
                "emergency_months": 3.0,
                "monthly_balance": 21000
            })
        ))
        conn.commit()

    conn.close()


# =====================================================================
# USER OPERATIONS
# =====================================================================

def create_user(email, password, full_name, phone=None, occupation=None):
    """Registers a new user with secure password hashing."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, phone, occupation)
            VALUES (?, ?, ?, ?, ?)
        """, (email.strip().lower(), password_hash, full_name.strip(), phone, occupation))
        conn.commit()
        user_id = cursor.lastrowid
        return {"success": True, "user_id": user_id}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "An account with this email address already exists."}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()


def authenticate_user(email, password):
    """Verifies user credentials and returns user dictionary."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
    user = cursor.fetchone()
    
    if user and check_password_hash(user["password_hash"], password):
        # Update last login
        cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user["id"],))
        conn.commit()
        user_dict = dict(user)
        user_dict.pop("password_hash", None)
        conn.close()
        return {"success": True, "user": user_dict}
    
    conn.close()
    return {"success": False, "message": "Invalid email or password."}


def get_user_by_id(user_id):
    """Fetches user details by user ID."""
    if not user_id:
        return None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, full_name, phone, occupation, role, created_at, last_login FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# =====================================================================
# ASSESSMENT OPERATIONS
# =====================================================================

def save_assessment(user_id, assessment_type, score, category, foir, credit_utilisation, monthly_income, raw_input, result_data):
    """Persists a calculated credit / loan readiness assessment to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO credit_assessments (
                user_id, assessment_type, score, category, foir, credit_utilisation, monthly_income, raw_input_json, result_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            assessment_type,
            int(score),
            str(category),
            float(foir or 0.0),
            float(credit_utilisation or 0.0),
            float(monthly_income or 0.0),
            json.dumps(raw_input or {}),
            json.dumps(result_data or {})
        ))
        conn.commit()
        assessment_id = cursor.lastrowid
        return {"success": True, "assessment_id": assessment_id}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()


def get_user_assessments(user_id, limit=20):
    """Retrieves chronological assessment history for a user."""
    if not user_id:
        return []
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, assessment_type, score, category, foir, credit_utilisation, monthly_income, result_json, created_at
        FROM credit_assessments
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        try:
            d["result"] = json.loads(d.get("result_json") or "{}")
        except Exception:
            d["result"] = {}
        results.append(d)
    return results


# =====================================================================
# STATUTORY DISPUTES OPERATIONS
# =====================================================================

def save_statutory_dispute(user_id, borrower_name, lender_name, bureau_name, grievance_date, resolution_date, delay_days, penalty_amount, error_description, notice_text, status="Drafted"):
    """Saves an RBI statutory penalty dispute or legal notice draft."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO statutory_disputes (
                user_id, borrower_name, lender_name, bureau_name, grievance_date, resolution_date, delay_days, penalty_amount, error_description, notice_text, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            borrower_name,
            lender_name,
            bureau_name,
            grievance_date,
            resolution_date,
            int(delay_days or 0),
            float(penalty_amount or 0.0),
            error_description,
            notice_text,
            status
        ))
        conn.commit()
        dispute_id = cursor.lastrowid
        return {"success": True, "dispute_id": dispute_id}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()


def get_user_disputes(user_id):
    """Retrieves all statutory dispute records for a given user."""
    if not user_id:
        return []
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM statutory_disputes
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# =====================================================================
# DPDP ACT 2023 CONSENT & ERASURE (PRIVACY CENTER)
# =====================================================================

def log_dpdp_consent(user_id, consent_type, purpose_code, status="GRANTED", ip_address=None, user_agent=None):
    """Logs an explicit consent record under India's DPDP Act 2023."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dpdp_consent_logs (user_id, consent_type, purpose_code, status, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, consent_type, purpose_code, status, ip_address, user_agent))
    conn.commit()
    conn.close()


def get_user_consent_logs(user_id):
    """Fetches all DPDP consent audit logs for a user."""
    if not user_id:
        return []
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM dpdp_consent_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def erase_user_data(user_id):
    """
    Executes the 'Right to Erasure' mandated under Section 12 of India's DPDP Act 2023.
    Permanently deletes all personal records, assessments, and disputes for the user.
    """
    if not user_id:
        return {"success": False, "message": "User not authenticated."}
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete related data first
        cursor.execute("DELETE FROM credit_assessments WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM statutory_disputes WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM dpdp_consent_logs WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return {"success": True, "message": "All user data has been permanently and irreversibly erased as per DPDP Act 2023."}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()


def export_user_data(user_id):
    """
    Executes the 'Data Portability' mandate under DPDP Act 2023.
    Exports all user data as a consolidated JSON package.
    """
    user = get_user_by_id(user_id)
    if not user:
        return None
    assessments = get_user_assessments(user_id)
    disputes = get_user_disputes(user_id)
    consents = get_user_consent_logs(user_id)

    return {
        "export_metadata": {
            "entity": "CreditFit 360",
            "compliance": "Digital Personal Data Protection Act (DPDP) 2023",
            "exported_at": datetime.utcnow().isoformat() + "Z"
        },
        "user_profile": user,
        "assessments": assessments,
        "statutory_disputes": disputes,
        "consent_history": consents
    }
