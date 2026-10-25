from flask import Flask, render_template, request, jsonify, session, redirect, send_file, Response, send_from_directory
from datetime import datetime
import os
import json
import random
import io
import db
from ai_engine import (
    process_assistant_query,
    simulate_reverse_underwriting,
    generate_rbi_statutory_notice,
    calculate_rbi_statutory_penalty
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
app.secret_key = os.environ.get("SECRET_KEY", "creditfit360-secret-key")

# Static files route fallback for Vercel and local environments
@app.route("/static/<path:filename>")
def serve_static(filename):
    for folder in [
        os.path.join(BASE_DIR, "public", "static"),
        os.path.join(BASE_DIR, "static")
    ]:
        target = os.path.join(folder, filename)
        if os.path.exists(target):
            return send_from_directory(folder, filename)
    return send_from_directory(os.path.join(BASE_DIR, "static"), filename)

# Initialize SQLite database schema
db.init_db()


# =========================================================
# HOME / LOGIN
# =========================================================

@app.route("/")
@app.route("/api/index")
@app.route("/api/index.py")
def login():
    return render_template("login.html")


@app.route("/favicon.ico")
def favicon():
    return "", 204


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():
    result = session.get("creditFitResult")
    user = session.get("user")
    past_assessments = []
    disputes = []
    if user and user.get("id"):
        past_assessments = db.get_user_assessments(user["id"], limit=5)
        disputes = db.get_user_disputes(user["id"])
    return render_template(
        "dashboard.html",
        result=result,
        user=user,
        past_assessments=past_assessments,
        disputes=disputes
    )



# =========================================================
# PERSONAL CREDITFIT
# =========================================================

@app.route("/personal-credit")
def personal_credit():
    return render_template("personal_credit.html")


# =========================================================
# SME CREDIT SCORE
# =========================================================

@app.route("/sme-credit-score")
def sme_credit_score():
    return render_template("sme_credit_score.html")


# =========================================================
# LOAN READINESS
# =========================================================

@app.route("/loan-readiness")
def loan_readiness():
    return render_template("loan_readiness.html")


# =========================================================
# REPORTS / CREDIT RESULT
# =========================================================

@app.route("/credit-result")
@app.route("/reports")
def credit_result():
    result = session.get("creditFitResult")
    return render_template("credit_result.html", result=result)


# =========================================================
# WHAT-IF SIMULATOR (FINTWIN)
# =========================================================

@app.route("/what-if-simulator")
def what_if_simulator():
    result = session.get("creditFitResult")
    return render_template("what_if_simulator.html", result=result)


# =========================================================
# MONEYMAP (CASH FLOW & BUDGET TRACKING)
# =========================================================

@app.route("/moneymap")
def moneymap():
    result = session.get("creditFitResult")
    return render_template("moneymap.html", result=result)


# =========================================================
# DECISION LAB (A/B SCENARIO COMPARISON)
# =========================================================

@app.route("/decision-lab")
def decision_lab():
    result = session.get("creditFitResult")
    return render_template("decision_lab.html", result=result)


# =========================================================
# WEALTH PATH (GOAL PLANNING & MILESTONES)
# =========================================================

@app.route("/wealth-path")
def wealth_path():
    result = session.get("creditFitResult")
    return render_template("wealth_path.html", result=result)


# =========================================================
# DEFENSE & APPROVAL SUITE (REVERSE UNDERWRITER + RBI ENFORCER)
# =========================================================

@app.route("/defense-suite")
@app.route("/financial-defense")
def defense_suite():
    result = session.get("creditFitResult")
    return render_template("defense_suite.html", result=result)


@app.route("/api/reverse-underwrite", methods=["POST"])
def api_reverse_underwrite():
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or {}
        session_result = session.get("creditFitResult") or {}
        
        # Merge session profile as default if not supplied in form
        if not data.get("monthly_income") and session_result.get("monthly_income"):
            data["monthly_income"] = session_result.get("monthly_income")
        if not data.get("existing_emi") and session_result.get("existing_emi"):
            data["existing_emi"] = session_result.get("existing_emi")
        if not data.get("credit_score") and session_result.get("credit_score"):
            data["credit_score"] = session_result.get("credit_score")
        if not data.get("credit_limit") and session_result.get("credit_limit"):
            data["credit_limit"] = session_result.get("credit_limit")
        if not data.get("credit_outstanding") and session_result.get("credit_outstanding"):
            data["credit_outstanding"] = session_result.get("credit_outstanding")
        if not data.get("missed_payments") and session_result.get("missed_payments"):
            data["missed_payments"] = session_result.get("missed_payments")
            
        underwrite_result = simulate_reverse_underwriting(data)
        return jsonify(underwrite_result)
    except Exception as e:
        app.logger.exception("Error in reverse underwriting API")
        return jsonify({
            "success": False,
            "message": f"Simulation failed: {str(e)}"
        }), 500


@app.route("/api/generate-statutory-notice", methods=["POST"])
def api_generate_statutory_notice():
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or {}
        session_result = session.get("creditFitResult") or {}
        
        if not data.get("full_name") and session_result.get("full_name"):
            data["full_name"] = session_result.get("full_name")
            
        notice_result = generate_rbi_statutory_notice(data)
        
        user = session.get("user")
        if user and user.get("id") and notice_result.get("success"):
            db.save_statutory_dispute(
                user_id=user["id"],
                borrower_name=data.get("borrower_name") or data.get("full_name") or user.get("full_name") or "Borrower",
                lender_name=data.get("lender_name") or "Lender / Credit Bureau",
                bureau_name=data.get("bureau_name") or "CIBIL",
                grievance_date=data.get("grievance_date") or datetime.now().strftime("%Y-%m-%d"),
                resolution_date=data.get("resolution_date"),
                delay_days=data.get("delay_days", 0),
                penalty_amount=data.get("penalty_amount", 0.0),
                error_description=data.get("error_description", ""),
                notice_text=notice_result.get("notice_text", ""),
                status="Notice Generated"
            )

        return jsonify(notice_result)
    except Exception as e:
        app.logger.exception("Error generating statutory notice")
        return jsonify({
            "success": False,
            "message": f"Notice generation failed: {str(e)}"
        }), 500


@app.route("/api/calculate-rbi-penalty", methods=["POST"])
def api_calculate_rbi_penalty():
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or {}
        sub_date = data.get("submission_date") or ""
        resolved_date = data.get("resolved_date") or None
        
        penalty_result = calculate_rbi_statutory_penalty(sub_date, resolved_date)
        return jsonify(penalty_result)
    except Exception as e:
        app.logger.exception("Error calculating RBI penalty")
        return jsonify({
            "success": False,
            "message": f"Penalty calculation failed: {str(e)}"
        }), 500


# =========================================================
# SETTINGS
# =========================================================

@app.route("/settings")
def settings():
    return render_template("settings.html")


# =========================================================
# ABOUT US
# =========================================================

@app.route("/about")
@app.route("/about-us")
def about():
    return render_template("about.html")


# =========================================================
# DISCLAIMER
# =========================================================

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")


# =========================================================
# LOGOUT & AUTHENTICATION APIs
# =========================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip()
    password = str(data.get("password", "")).strip()
    full_name = str(data.get("full_name", "")).strip()
    phone = str(data.get("phone", "")).strip()

    if not email or not password or not full_name:
        return jsonify({"success": False, "message": "Full name, email, and password are required."}), 400

    res = db.create_user(email=email, password=password, full_name=full_name, phone=phone)
    if res.get("success"):
        auth_res = db.authenticate_user(email, password)
        if auth_res.get("success"):
            session["user"] = auth_res["user"]
        return jsonify({"success": True, "message": "Account created successfully!"})
    return jsonify(res), 400


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip()
    password = str(data.get("password", "")).strip()

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    res = db.authenticate_user(email, password)
    if res.get("success"):
        session["user"] = res["user"]
        return jsonify({"success": True, "message": "Welcome back!"})
    return jsonify(res), 401


@app.route("/api/current-user")
def api_current_user():
    user = session.get("user")
    return jsonify({"authenticated": bool(user), "user": user})


# =========================================================
# LOAN READINESS & DEFENSE DOSSIER (PDF / PRINTABLE)
# =========================================================

@app.route("/dossier")
@app.route("/download-dossier")
def generate_dossier():
    result = session.get("creditFitResult")
    user = session.get("user")

    if not result:
        if user and user.get("id"):
            past = db.get_user_assessments(user["id"], limit=1)
            if past:
                result = past[0].get("result") or {}

    if not result:
        result = {
            "score": 765,
            "category": "Prime Tier-1 Creditworthiness",
            "full_name": user.get("full_name") if user else "Smita Dwivedi (Borrower)",
            "monthly_income": 75000,
            "existing_emi": 18500,
            "credit_utilisation": 18.2,
            "emi_burden": 24.6,
            "emergency_months": 4.8,
            "monthly_balance": 32500,
            "credit_score": 760
        }

    borrower_name = result.get("full_name") or (user.get("full_name") if user else "Valued Borrower")
    score = result.get("score") or result.get("total_score") or 750
    foir = float(result.get("emi_burden") or 25.0)
    utilization = float(result.get("credit_utilisation") or 20.0)
    emergency_months = float(result.get("emergency_months") or 3.5)
    monthly_income = float(result.get("monthly_income") or 60000.0)
    existing_emi = float(result.get("existing_emi") or 15000.0)
    monthly_balance = float(result.get("monthly_balance") or (monthly_income - existing_emi - 20000.0))

    allowed_max_emi = max(0.0, (monthly_income * 0.50) - existing_emi)
    r = 0.095 / 12
    n = 60
    factor = ((1 + r)**n - 1) / (r * (1 + r)**n)
    max_loan = allowed_max_emi * factor

    dossier_id = f"CF360-IND-{datetime.now().strftime('%Y%m')}-{random.randint(1000, 9999)}"
    issued_date = datetime.now().strftime("%d %B %Y, %H:%M IST")

    category = result.get("category") or "Prime Tier-1 Approved"
    verdict_status = "APPROVED (Prime PSU / Private)" if foir <= 45 and score >= 650 else "CONDITIONAL (Restructure FOIR)"

    bank_odds = {
        "sbi": min(98, max(45, int(score * 0.12 + (50 - foir) * 0.4))),
        "hdfc": min(99, max(50, int(score * 0.13 + (50 - foir) * 0.35))),
        "icici": min(97, max(48, int(score * 0.125 + (50 - foir) * 0.38))),
        "kotak": min(96, max(42, int(score * 0.12 + (50 - foir) * 0.32)))
    }

    return render_template(
        "dossier.html",
        dossier_id=dossier_id,
        issued_date=issued_date,
        borrower_name=borrower_name,
        score=score,
        category=category,
        verdict_status=verdict_status,
        max_sanctionable=max_loan,
        max_emi=allowed_max_emi,
        foir=round(foir, 1),
        credit_utilisation=round(utilization, 1),
        emergency_months=round(emergency_months, 1),
        monthly_balance=round(monthly_balance, 2),
        bank_odds=bank_odds,
        dossier_json=json.dumps({
            "dossier_id": dossier_id,
            "borrower_name": borrower_name,
            "score": score,
            "category": category,
            "foir": foir,
            "credit_utilisation": utilization,
            "max_loan_estimate": round(max_loan, 2),
            "issued_date": issued_date
        })
    )


# =========================================================
# INDIA STACK: ACCOUNT AGGREGATOR (AA) SIMULATION
# =========================================================

@app.route("/api/account-aggregator/request-otp", methods=["POST"])
def aa_request_otp():
    data = request.get_json(silent=True) or {}
    phone = str(data.get("phone", "")).strip() or "9876543210"
    fip_handle = str(data.get("fip_handle", "")).strip() or "HDFC_BANK@onemoney"

    tx_id = f"AA-TXN-{datetime.now().strftime('%y%m%d%H%M')}-{random.randint(100, 999)}"
    return jsonify({
        "success": True,
        "transaction_id": tx_id,
        "fip_handle": fip_handle,
        "phone_masked": f"+91 ******{phone[-4:] if len(phone)>=4 else '3210'}",
        "simulated_otp": "123456",
        "message": "OTP dispatched via RBI-regulated Account Aggregator (Demo OTP: 123456)"
    })


@app.route("/api/account-aggregator/verify-and-fetch", methods=["POST"])
def aa_verify_and_fetch():
    data = request.get_json(silent=True) or {}
    otp = str(data.get("otp", "")).strip()
    phone = str(data.get("phone", "")).strip()
    bank_name = str(data.get("bank", "")).strip() or "HDFC Bank"

    if otp != "123456" and len(otp) != 6:
        return jsonify({
            "success": False,
            "message": "Invalid OTP. For test simulation, please use '123456'."
        }), 400

    user = session.get("user")
    user_id = user.get("id") if user else None

    if user_id:
        db.log_dpdp_consent(
            user_id=user_id,
            consent_type="ACCOUNT_AGGREGATOR_FETCH",
            purpose_code="RBI_AA_FIP_INGESTION_V1",
            status="GRANTED",
            ip_address=request.remote_addr,
            user_agent=str(request.user_agent)
        )

    user_full_name = user.get("full_name") if user else "Smita Dwivedi"
    
    verified_payload = {
        "verified_by_fip": True,
        "bank_name": bank_name,
        "fip_provider": f"{bank_name} (FIP-AA-094)",
        "consent_artifact_id": f"AA-ART-{random.randint(100000, 999999)}",
        "timestamp": datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        "full_name": user_full_name,
        "age": 28,
        "employment_type": "Salaried",
        "employment_years": 4.0,
        "monthly_income": 75000,
        "household_expenses": 22000,
        "existing_emi": 14000,
        "monthly_savings": 18000,
        "monthly_investment": 12000,
        "credit_score": 752,
        "credit_limit": 150000,
        "credit_outstanding": 26400,
        "active_loans": 1,
        "missed_payments": 0,
        "credit_applications": 1,
        "current_savings": 88000,
        "investments": 125000,
        "emergency_fund": 72000,
        "essential_expenses": 24000
    }

    return jsonify({
        "success": True,
        "message": f"Bank statement successfully verified via {bank_name} Account Aggregator.",
        "financials": verified_payload,
        "data": verified_payload
    })



# =========================================================
# DPDP ACT 2023: PRIVACY & CONSENT GOVERNANCE
# =========================================================

@app.route("/privacy-consent-center")
@app.route("/privacy-center")
def privacy_consent_center():
    user = session.get("user")
    consent_logs = []
    if user and user.get("id"):
        consent_logs = db.get_user_consent_logs(user["id"])
    return render_template("privacy_center.html", user=user, consent_logs=consent_logs)


@app.route("/api/export-user-data")
def export_user_data_api():
    user = session.get("user")
    if not user or not user.get("id"):
        guest_data = {
            "entity": "CreditFit 360",
            "session_user": "Guest Explorer",
            "active_credit_result": session.get("creditFitResult"),
            "compliance": "DPDP Act 2023 - Right to Portability"
        }
        resp = Response(json.dumps(guest_data, indent=2), mimetype="application/json")
        resp.headers["Content-Disposition"] = "attachment; filename=CreditFit360_Guest_Data.json"
        return resp

    data = db.export_user_data(user["id"])
    resp = Response(json.dumps(data, indent=2), mimetype="application/json")
    resp.headers["Content-Disposition"] = f"attachment; filename=CreditFit360_UserData_{user['id']}.json"
    return resp


@app.route("/api/erase-user-data", methods=["POST"])
def erase_user_data_api():
    user = session.get("user")
    if not user or not user.get("id"):
        session.clear()
        return jsonify({"success": True, "message": "Guest session data erased successfully."})

    res = db.erase_user_data(user["id"])
    session.clear()
    return jsonify(res)



# =========================================================
# FITAI FINANCIAL CO-PILOT / ASSISTANT
# =========================================================

@app.route("/assistant")
@app.route("/ai-copilot")
def assistant():
    result = session.get("creditFitResult")
    return render_template("assistant.html", result=result)


@app.route("/api/assistant-chat", methods=["POST"])
def assistant_chat():
    try:
        data = request.get_json(silent=True) or {}
        message = str(data.get("message", "")).strip()
        
        if not message:
            return jsonify({
                "success": False,
                "reply": "Please provide a question or select an action chip."
            }), 400

        # Context can be passed explicitly from client, or pulled from Flask session
        context = data.get("context")
        if not context or not isinstance(context, dict):
            context = session.get("creditFitResult") or {}

        history = data.get("history") or []

        response_data = process_assistant_query(
            query=message,
            session_data=context,
            history=history
        )

        return jsonify({
            "success": True,
            **response_data
        })

    except Exception as e:
        app.logger.exception("Error processing assistant chat")
        return jsonify({
            "success": False,
            "reply": "⚠️ An error occurred while analyzing financial data. Please try again."
        }), 500


@app.route("/api/assistant-quick-actions", methods=["GET"])
def assistant_quick_actions():
    result = session.get("creditFitResult") or {}
    score = result.get("score") or result.get("total_score") or 0
    foir = result.get("emi_burden") or 0
    
    prompts = [
        "How can I raise my credit score by 50 points in 90 days?",
        "Can I afford a new loan? Calculate my safe borrowing capacity.",
        "How do I reduce my credit card utilization below 30%?",
        "Draft an official dispute letter for an erroneous CIBIL entry.",
        "Explain the Snowball vs Avalanche debt payoff method."
    ]
    
    return jsonify({
        "success": True,
        "score": score,
        "foir": foir,
        "prompts": prompts
    })


# =========================================================
# CALCULATE PERSONAL CREDIT SCORE
# =========================================================

@app.route("/calculate-score", methods=["POST"])
def calculate_score():

    try:
        data = request.get_json(silent=True)

        if not data:
            data = request.form.to_dict()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        # -------------------------------------------------
        # BASIC INFORMATION
        # -------------------------------------------------

        full_name = str(data.get("full_name", "")).strip()

        age = float(data.get("age", 0) or 0)

        employment_type = str(
            data.get("employment_type", "")
        ).strip()

        monthly_income = float(
            data.get("monthly_income", 0) or 0
        )

        employment_years = float(
            data.get("employment_years", 0) or 0
        )

        # -------------------------------------------------
        # FINANCIAL POSITION
        # -------------------------------------------------

        household_expenses = float(
            data.get("household_expenses", 0) or 0
        )

        existing_emi = float(
            data.get("existing_emi", 0) or 0
        )

        monthly_savings = float(
            data.get("monthly_savings", 0) or 0
        )

        monthly_investment = float(
            data.get("monthly_investment", 0) or 0
        )

        # -------------------------------------------------
        # CREDIT INFORMATION
        # -------------------------------------------------

        credit_score = float(
            data.get("credit_score", 0) or 0
        )

        credit_limit = float(
            data.get("credit_limit", 0) or 0
        )

        credit_outstanding = float(
            data.get("credit_outstanding", 0) or 0
        )

        active_loans = int(
            data.get("active_loans", 0) or 0
        )

        missed_payments = int(
            data.get("missed_payments", 0) or 0
        )

        credit_applications = int(
            data.get("credit_applications", 0) or 0
        )

        # -------------------------------------------------
        # SAVINGS / EMERGENCY
        # -------------------------------------------------

        current_savings = float(
            data.get("current_savings", 0) or 0
        )

        investments = float(
            data.get("investments", 0) or 0
        )

        emergency_fund = float(
            data.get("emergency_fund", 0) or 0
        )

        essential_expenses = float(
            data.get("essential_expenses", 0) or 0
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if age < 0 or age > 120:
            return jsonify({
                "success": False,
                "message": "Please enter a valid age."
            }), 400

        if not 0 <= credit_score <= 900:
            return jsonify({
                "success": False,
                "message": "Credit score must be between 0 and 900."
            }), 400

        if min(
            monthly_income,
            employment_years,
            household_expenses,
            existing_emi,
            monthly_savings,
            monthly_investment,
            credit_limit,
            credit_outstanding,
            current_savings,
            investments,
            emergency_fund,
            essential_expenses,
            active_loans,
            missed_payments,
            credit_applications
        ) < 0:

            return jsonify({
                "success": False,
                "message": "Values cannot be negative."
            }), 400

        # =================================================
        # CREDIT UTILISATION
        # =================================================

        if credit_limit > 0:
            credit_utilisation = (
                credit_outstanding / credit_limit
            ) * 100
        else:
            credit_utilisation = (
                100 if credit_outstanding > 0 else 0
            )

        credit_utilisation = max(
            0, min(100, credit_utilisation)
        )

        # =================================================
        # EMI BURDEN
        # =================================================

        if monthly_income > 0:
            emi_burden = (
                existing_emi / monthly_income
            ) * 100
        else:
            emi_burden = (
                100 if existing_emi > 0 else 0
            )

        emi_burden = max(
            0, min(100, emi_burden)
        )

        # =================================================
        # MONTHLY BALANCE
        # =================================================

        monthly_balance = (
            monthly_income
            - household_expenses
            - existing_emi
            - monthly_savings
            - monthly_investment
        )

        # =================================================
        # EMERGENCY FUND MONTHS
        # =================================================

        if essential_expenses > 0:
            emergency_months = (
                current_savings / essential_expenses
            )
        else:
            emergency_months = 0

        # =================================================
        # 1. CREDIT BEHAVIOUR - MAX 30
        # =================================================

        if credit_score >= 750:
            credit_behaviour = 30
        elif credit_score >= 700:
            credit_behaviour = 26
        elif credit_score >= 650:
            credit_behaviour = 21
        elif credit_score >= 600:
            credit_behaviour = 15
        else:
            credit_behaviour = 8

        credit_behaviour -= missed_payments * 4

        credit_behaviour = max(
            0, min(30, credit_behaviour)
        )

        # =================================================
        # 2. DEBT MANAGEMENT - MAX 20
        # =================================================

        if emi_burden <= 20:
            debt_management = 20
        elif emi_burden <= 30:
            debt_management = 17
        elif emi_burden <= 40:
            debt_management = 13
        elif emi_burden <= 50:
            debt_management = 8
        else:
            debt_management = 4

        # =================================================
        # 3. CREDIT UTILISATION - MAX 15
        # =================================================

        if credit_utilisation <= 30:
            utilisation_score = 15
        elif credit_utilisation <= 50:
            utilisation_score = 11
        elif credit_utilisation <= 75:
            utilisation_score = 7
        else:
            utilisation_score = 3

        # =================================================
        # 4. SAVINGS - MAX 20
        # =================================================

        if emergency_months >= 6:
            savings_score = 20
        elif emergency_months >= 3:
            savings_score = 16
        elif emergency_months >= 1:
            savings_score = 10
        else:
            savings_score = 4

        # =================================================
        # 5. FINANCIAL STABILITY - MAX 15
        # =================================================

        stability_score = 0

        if monthly_balance > 0:
            stability_score += 6

        if employment_years >= 3:
            stability_score += 5
        elif employment_years >= 1:
            stability_score += 3
        else:
            stability_score += 1

        if monthly_savings > 0:
            stability_score += 2

        if monthly_investment > 0:
            stability_score += 2

        stability_score = max(
            0, min(15, stability_score)
        )

        # =================================================
        # TOTAL SCORE
        # =================================================

        total_score = (
            credit_behaviour
            + debt_management
            + utilisation_score
            + savings_score
            + stability_score
        )

        total_score = max(
            0, min(100, round(total_score))
        )

        # =================================================
        # CATEGORY
        # =================================================

        if total_score >= 80:
            category = "Excellent"
        elif total_score >= 70:
            category = "Good"
        elif total_score >= 50:
            category = "Moderate"
        else:
            category = "Needs Improvement"

        # =================================================
        # EMI AFFORDABILITY
        # =================================================

        emi_affordability = round(
            max(0, min(100, 100 - emi_burden))
        )

        # =================================================
        # STRENGTHS
        # =================================================

        strengths = []

        if credit_score >= 700:
            strengths.append("Good credit score")

        if credit_utilisation <= 30:
            strengths.append("Healthy credit utilisation")

        if emi_burden <= 30:
            strengths.append("Manageable EMI burden")

        if emergency_months >= 3:
            strengths.append("Good emergency savings")

        if monthly_balance > 0:
            strengths.append("Positive monthly balance")

        # =================================================
        # IMPROVEMENTS
        # =================================================

        improvements = []

        if credit_score < 700:
            improvements.append("Improve credit score")

        if credit_utilisation > 30:
            improvements.append("Reduce credit utilisation")

        if emi_burden > 30:
            improvements.append("Review EMI burden")

        if emergency_months < 3:
            improvements.append("Build emergency savings")

        if monthly_balance <= 0:
            improvements.append("Review monthly expenses")

        if missed_payments > 0:
            improvements.append("Avoid missed payments")

        # =================================================
        # RESULT
        # Keep the old JSON response format compatible
        # =================================================

        result = {
            "success": True,

            "full_name": full_name,
            "age": age,
            "employment_type": employment_type,

            "monthly_income": monthly_income,
            "employment_years": employment_years,

            "household_expenses": household_expenses,
            "existing_emi": existing_emi,
            "monthly_savings": monthly_savings,
            "monthly_investment": monthly_investment,

            "credit_score": credit_score,
            "credit_limit": credit_limit,
            "credit_outstanding": credit_outstanding,
            "credit_utilisation": round(
                credit_utilisation, 2
            ),

            "active_loans": active_loans,
            "missed_payments": missed_payments,
            "credit_applications": credit_applications,

            "current_savings": current_savings,
            "investments": investments,
            "emergency_fund": emergency_fund,
            "essential_expenses": essential_expenses,

            "emi_burden": round(emi_burden, 2),
            "emergency_months": round(
                emergency_months, 2
            ),
            "monthly_balance": round(
                monthly_balance, 2
            ),

            "emi_affordability": emi_affordability,

            "credit_behaviour": credit_behaviour,
            "debt_management": debt_management,
            "utilisation_score": utilisation_score,
            "savings_score": savings_score,
            "stability_score": stability_score,

            "total_score": total_score,
            "score": total_score,
            "category": category,

            "strengths": strengths,
            "improvements": improvements,

            "breakdown": {
                "creditBehaviour": credit_behaviour,
                "debtManagement": debt_management,
                "creditUtilisation": utilisation_score,
                "savingsEmergency": savings_score,
                "financialStability": stability_score
            },

            "metrics": {
                "emiBurden": round(emi_burden, 2),
                "creditUtilisation": round(credit_utilisation, 2),
                "emergencyMonths": round(emergency_months, 2),
                "monthlyBalance": round(monthly_balance, 2)
            },

            "insights": {
                "strengths": strengths,
                "improvements": improvements
            },

            "disclaimer": (
                "This is an educational estimate, not an official "
                "credit bureau score or loan approval decision."
            )
        }

        # Save result for Dashboard and Reports
        session["creditFitResult"] = result

        # Persist to database if authenticated
        user = session.get("user")
        if user and user.get("id"):
            db.save_assessment(
                user_id=user["id"],
                assessment_type="personal",
                score=total_score,
                category=category,
                foir=emi_burden,
                credit_utilisation=credit_utilisation,
                monthly_income=monthly_income,
                raw_input=data,
                result_data=result
            )
            db.log_dpdp_consent(
                user_id=user["id"],
                consent_type="FINANCIAL_PROFILING",
                purpose_code="PERSONAL_CREDITFIT_CALC",
                status="GRANTED",
                ip_address=request.remote_addr,
                user_agent=str(request.user_agent)
            )

        # IMPORTANT: return the result directly
        # This preserves compatibility with the old frontend.
        return jsonify(result)

    except (ValueError, TypeError, OverflowError):
        return jsonify({
            "success": False,
            "message": "Invalid input. Please check your form values."
        }), 400

    except Exception:
        app.logger.exception(
            "Error calculating CreditFit score"
        )

        return jsonify({
            "success": False,
            "message": "An unexpected error occurred."
        }), 500


# =========================================================
# CLEAR SAVED RESULT
# =========================================================

@app.route("/clear-result", methods=["GET", "POST"])
def clear_result():
    session.pop("creditFitResult", None)

    return jsonify({
        "success": True,
        "message": "Saved result cleared."
    })


# =========================================================
# SERVER TEST
# =========================================================

@app.route("/test")
def test():
    return "CreditFit360 server is running successfully!"


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    import socket
    import threading
    import time
    import webbrowser

    def is_port_in_use(p):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', p)) == 0

    def find_available_port(start_port=5000, max_attempts=20):
        p = start_port
        while p < start_port + max_attempts:
            if not is_port_in_use(p):
                return p
            p += 1
        return start_port

    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def open_browser_delayed(url, delay=1.0):
        def _open():
            time.sleep(delay)
            try:
                print(f"[*] Opening default web browser at {url} ...")
                webbrowser.open(url)
            except Exception as e:
                print(f"[!] Could not launch browser automatically: {e}")
        t = threading.Thread(target=_open, daemon=True)
        t.start()

    raw_port = int(os.environ.get("PORT", 5000))
    port = raw_port
    if is_port_in_use(port):
        print(f"[!] Port {port} is currently in use.")
        free_port = find_available_port(start_port=port + 1)
        print(f"[+] Automatically switching to available port: {free_port}")
        port = free_port

    local_ip = get_local_ip()
    target_url = f"http://localhost:{port}"

    print("=" * 64)
    print("           CREDITFIT 360 - LOCAL SERVER RUNNER           ")
    print("     Smart Credit Health, Reverse Underwriting & FinAI   ")
    print("=" * 64)
    print(f"  • Local Web URL:     {target_url}")
    print(f"  • Localhost IP:      http://127.0.0.1:{port}")
    print(f"  • Network / Mobile:  http://{local_ip}:{port}")
    print(f"  • Database:          {os.path.join(BASE_DIR, 'database.db')} (SQLite Active)")
    print(f"  • Privacy Standard:  RBI CEPC 2023-24 & DPDP Act 2023 Shield")
    print("-" * 64)
    print(f"  [i] Quick Demo Login: demo@creditfit360.com / Demo@123")
    print(f"  [i] Press CTRL + C anytime in this terminal to stop.")
    print("=" * 64)
    print()

    no_browser = os.environ.get("NO_BROWSER", "0").lower() in ("true", "1")
    if not no_browser:
        open_browser_delayed(target_url, delay=1.0)

    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1")
    try:
        app.run(
            host="0.0.0.0",
            port=port,
            debug=debug,
            use_reloader=False
        )
    except (KeyboardInterrupt, SystemExit):
        print("\n[+] CreditFit360 server stopped gracefully. Goodbye!")