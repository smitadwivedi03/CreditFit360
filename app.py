from flask import Flask, render_template, request, jsonify, session, redirect
from ai_engine import process_assistant_query

app = Flask(__name__)
app.secret_key = "creditfit360-secret-key"



# =========================================================
# HOME / LOGIN
# =========================================================

@app.route("/")
def login():
    return render_template("login.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():
    result = session.get("creditFitResult")
    return render_template("dashboard.html", result=result)


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
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


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
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )