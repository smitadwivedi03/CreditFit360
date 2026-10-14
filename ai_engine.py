"""
CreditFit360 - AI Financial Intelligence & Co-Pilot Engine
Provides domain-expert financial reasoning, scenario evaluation, CIBIL/Credit score advice,
FOIR/DTI loan affordability calculation, dispute letter generation, and debt payoff optimization.
Supports optional external LLM integration (Gemini/OpenAI) with high-fidelity deterministic fallback.
"""

import os
import re
import json
import math
from typing import Dict, Any, List, Optional

def _calculate_loan_capacity(monthly_income: float, existing_emi: float, max_foir: float = 0.50, interest_rate_pa: float = 10.5, tenure_years: int = 5) -> Dict[str, Any]:
    """Calculates maximum safe borrowing capacity based on FOIR (Fixed Obligation to Income Ratio)."""
    max_total_emi = monthly_income * max_foir
    available_emi = max(0.0, max_total_emi - existing_emi)
    
    # EMI formula: EMI = [P * r * (1+r)^n] / [(1+r)^n - 1]
    # Solving for Principal: P = EMI * [(1+r)^n - 1] / [r * (1+r)^n]
    monthly_rate = (interest_rate_pa / 100.0) / 12.0
    tenure_months = tenure_years * 12
    
    if monthly_rate > 0 and tenure_months > 0:
        factor = math.pow(1 + monthly_rate, tenure_months)
        loan_capacity = available_emi * (factor - 1) / (monthly_rate * factor)
    else:
        loan_capacity = available_emi * tenure_months
        
    return {
        "max_total_emi": round(max_total_emi, 2),
        "available_emi": round(available_emi, 2),
        "estimated_principal": round(loan_capacity, 2),
        "assumed_rate": interest_rate_pa,
        "assumed_tenure_years": tenure_years,
        "current_foir_pct": round((existing_emi / monthly_income * 100.0) if monthly_income > 0 else 0.0, 1)
    }

def _calculate_utilization_targets(outstanding: float, limit: float) -> Dict[str, Any]:
    """Calculates paydown amounts to hit 30% and 10% credit card utilization."""
    current_ratio = (outstanding / limit * 100.0) if limit > 0 else 0.0
    target_30_balance = limit * 0.30
    target_10_balance = limit * 0.10
    
    pay_for_30 = max(0.0, outstanding - target_30_balance)
    pay_for_10 = max(0.0, outstanding - target_10_balance)
    
    return {
        "current_ratio": round(current_ratio, 1),
        "target_30_paydown": round(pay_for_30, 2),
        "target_10_paydown": round(pay_for_10, 2),
        "target_30_balance": round(target_30_balance, 2),
        "target_10_balance": round(target_10_balance, 2)
    }

def generate_dispute_letter(user_name: str, account_no: str = "", bureau_name: str = "TransUnion CIBIL", error_details: str = "") -> str:
    """Generates a legally structured Credit Bureau Dispute Letter."""
    clean_name = user_name if user_name else "[Your Full Name]"
    clean_acc = account_no if account_no else "[Account / Loan Number]"
    clean_error = error_details if error_details else "an account reported as 'Overdue / 30-day Late' which was paid in full on time"
    
    return f"""### 📝 Formal Credit Bureau Dispute Notice

**Date:** `[Current Date]`  
**To:** Dispute Resolution Cell, {bureau_name} Limited  
**Subject:** Formal Dispute Regarding Inaccurate Information in Credit Information Report (CIR)  

---

**Complainant Information:**
- **Full Legal Name:** {clean_name}
- **PAN / Identification No:** `[Enter PAN Card Number]`
- **Date of Birth:** `[DD/MM/YYYY]`
- **Registered Mobile & Email:** `[Mobile / Email]`
- **Disputed Account / Loan No:** `{clean_acc}`

---

**Statement of Dispute:**
I am writing to formally request an investigation into an inaccurate entry appearing on my recent Credit Report. Specifically:
> **Reported Discrepancy:** {clean_error}

**Factual Position:**
1. I have consistently maintained timely payments toward the aforementioned account.
2. The reporting creditor has either misreported payment dates or failed to update the 'NOC / Closed' or 'Standard / Paid-in-Full' status.
3. This inaccurate mark is depressing my credit score without legitimate grounds and causing unwarranted credit prejudice.

**Requested Action:**
Pursuant to Section 21(3) of the Credit Information Companies (Regulation) Act (CICRA), 2005:
- Please initiate an expedited dispute verification with the reporting lender.
- Update or purge the erroneous mark within the statutory 30-day timeline.
- Issue an updated Credit Information Report reflecting my corrected score.

**Enclosures:**
1. Self-attested copy of PAN Card & Aadhaar / Passport for identity verification.
2. Bank statement showing timely debit / EMI clearance.
3. No Dues Certificate (NDC) or Lender Statement of Account.

Sincerely,  
**{clean_name}**  
*(Dispute Reference Ticket: To be filed online at the {bureau_name} Consumer Dispute Portal)*"""

def process_assistant_query(query: str, session_data: Optional[Dict[str, Any]] = None, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    Core intelligent router that inspects user profile data, classifies intent,
    and returns rich markdown responses with metrics and follow-up suggestions.
    """
    q = (query or "").strip().lower()
    profile = session_data or {}
    
    # Extract baseline profile metrics with safe defaults
    income = float(profile.get("monthly_income") or profile.get("income") or 0.0)
    existing_emi = float(profile.get("existing_emi") or 0.0)
    expenses = float(profile.get("household_expenses") or profile.get("essential_expenses") or 0.0)
    score = float(profile.get("credit_score") or profile.get("total_score") or profile.get("score") or 0.0)
    credit_limit = float(profile.get("credit_limit") or 0.0)
    credit_out = float(profile.get("credit_outstanding") or 0.0)
    emergency_fund = float(profile.get("emergency_fund") or profile.get("current_savings") or 0.0)
    missed_payments = int(profile.get("missed_payments") or 0)
    active_loans = int(profile.get("active_loans") or 0)
    full_name = str(profile.get("full_name") or "Valued Member").strip()
    
    # Calculated profile attributes
    foir = (existing_emi / income * 100.0) if income > 0 else 0.0
    utilization = (credit_out / credit_limit * 100.0) if credit_limit > 0 else (100.0 if credit_out > 0 else 0.0)
    monthly_balance = income - existing_emi - expenses
    emergency_months = (emergency_fund / expenses) if expenses > 0 else 0.0
    
    # -------------------------------------------------------------
    # INTENT CLASSIFICATION & DISPATCH
    # -------------------------------------------------------------
    
    # 1. DISPUTE / ERROR / CIBIL CORRECTION
    if any(k in q for k in ["dispute", "cibil error", "wrong entry", "incorrect mark", "remove late payment", "dispute letter", "draft letter", "rectify"]):
        reply = generate_dispute_letter(
            user_name=full_name if full_name != "Valued Member" else "Account Holder",
            error_details="Late payment / overdue reporting on account that was resolved or incorrectly stamped."
        )
        return {
            "reply": reply,
            "action_type": "dispute_letter",
            "suggested_prompts": [
                "How do I submit this dispute on the CIBIL portal?",
                "How long does CIBIL take to update a resolved dispute?",
                "What documents do I need to attach with my dispute?"
            ],
            "metrics": {
                "score": score if score > 0 else "Not set",
                "dispute_type": "Official CIBIL / Experian Format"
            }
        }
        
    # 2. SCORE BOOST / IMPROVEMENT / 30-60-90 DAY PLAN
    if any(k in q for k in ["raise score", "improve score", "boost score", "increase cibil", "how to improve", "90 day", "score plan", "30 day", "raise cibil", "cibil booster"]):
        util_info = _calculate_utilization_targets(credit_out, credit_limit)
        
        reply = f"""### 🚀 Tailored 90-Day Credit Score Acceleration Plan

Based on your financial parameters, here is your high-impact action roadmap:

#### 📊 Current Health Snapshot
- **Current Score:** **{int(score) if score > 0 else '710 (Baseline Estimate)'}**
- **Credit Utilization:** **{round(utilization, 1)}%** *(Target: < 30%, Optimal: < 10%)*
- **EMI Burden (FOIR):** **{round(foir, 1)}%** of monthly income

---

#### 🗓️ Phase 1: Days 1 – 30 (Rapid Ratio Correction)
1. **Target Credit Card Utilization:**
   - Your current outstanding is **₹{credit_out:,.0f}** against a limit of **₹{credit_limit:,.0f}**.
   - {"🔴 *High Alert:* Pay down **₹{:,.0f}** immediately to bring utilization under 30%." .format(util_info['target_30_paydown']) if util_info['target_30_paydown'] > 0 else "🟢 Your utilization is already in a healthy zone below 30%!"}
   - **Pro Tip:** Make payments 3-5 days *before* the statement generation date so the reported balance to CIBIL is low.

#### 🗓️ Phase 2: Days 31 – 60 (Payment Discipline & Inquiries Freeze)
2. **Zero Hard Enquiries:**
   - Avoid applying for new personal loans or credit cards. Every hard inquiry can ding your score by 5–10 points.
   - {"You have reported " + str(missed_payments) + " missed payment(s). Maintain a strict zero-default streak for 6 straight months to recover payment history weight (35% of total score)." if missed_payments > 0 else "Zero missed payments detected. Continue automating auto-debits to protect this spotless streak."}

#### 🗓️ Phase 3: Days 61 – 90 (Credit Mix & Limit Expansion)
3. **Request a Soft Credit Limit Increase:**
   - Call your credit card issuer to request a credit limit hike without a hard credit pull.
   - Example: Increasing limit from ₹{credit_limit:,.0f} to ₹{credit_limit * 1.5:,.0f} automatically cuts your utilization by 33%!
4. **Mix of Credit:**
   - Maintain a balanced portfolio of secured (auto/home) and unsecured (credit card/personal) credit.

> **💡 Expected Impact:** Implementing these steps typically yields a **+30 to +65 point rebound** over 3 to 6 reporting cycles."""

        return {
            "reply": reply,
            "action_type": "score_boost",
            "suggested_prompts": [
                "How does paying before statement date help?",
                "Can I afford a new loan right now?",
                "Explain the Snowball vs Avalanche debt strategy"
            ],
            "metrics": {
                "score": score,
                "utilization": round(utilization, 1),
                "target_paydown_30": util_info["target_30_paydown"]
            }
        }
        
    # 3. LOAN AFFORDABILITY / BORROWING CAPACITY / CAN I AFFORD
    if any(k in q for k in ["loan", "afford", "borrow", "eligibility", "home loan", "car loan", "personal loan", "emi capacity", "how much loan", "take a loan"]):
        cap = _calculate_loan_capacity(income if income > 0 else 75000.0, existing_emi)
        
        reply = f"""### 🏦 Loan Affordability & Borrowing Capacity Analysis

Here is the exact lending diagnostic based on your cash flow:

| Metric | Your Financial Value | Recommended Standard |
| :--- | :--- | :--- |
| **Monthly Income** | **₹{income:,.0f}** | Stable cash flow |
| **Current EMI Outflow** | **₹{existing_emi:,.0f}** | `{round(foir, 1)}%` of income |
| **Max Safe EMI Limit (50% FOIR)** | **₹{cap['max_total_emi']:,.0f}** | Hard bank ceiling |
| **Available Fresh EMI Capacity** | **₹{cap['available_emi']:,.0f} / mo** | Net head-room for new loans |

---

#### 💡 Estimated Borrowing Capacity (Assuming 10.5% p.a. interest):
- **3-Year Loan (Personal):** Up to **₹{cap['available_emi'] * 29.5:,.0f}**
- **5-Year Loan (Car / Term):** Up to **₹{cap['estimated_principal']:,.0f}**
- **15-Year Loan (Home Loan @ 8.75%):** Up to **₹{cap['available_emi'] * 102.0:,.0f}**

#### ⚠️ Risk Verdict:
{"🟢 **Strong Approval Position:** Your FOIR is below 35%. Tier-1 banks will offer competitive interest rates." if foir < 35 else ("🟡 **Moderate Risk:** Your EMI burden is between 35% - 50%. Lenders may scrutinize bank statements." if foir <= 50 else "🔴 **High Debt Stress:** Your existing EMIs exceed 50% of your income. Taking an additional loan is strictly ill-advised.")}

**Recommendations:**
- If applying for a major loan, pay off your credit card balances first to reduce obligations.
- Adding an earning co-applicant (spouse/parent) can boost approval capacity by 40-70%."""

        return {
            "reply": reply,
            "action_type": "loan_capacity",
            "suggested_prompts": [
                "How do I reduce my current EMI burden?",
                "What is the difference between FOIR and DTI?",
                "How can I raise my score before applying for a loan?"
            ],
            "metrics": {
                "available_emi": cap["available_emi"],
                "estimated_loan": cap["estimated_principal"],
                "foir_pct": cap["current_foir_pct"]
            }
        }

    # 4. CREDIT UTILIZATION & CARD BALANCE
    if any(k in q for k in ["utilization", "utilisation", "credit card", "credit limit", "outstanding balance", "30% rule", "card limit"]):
        util_info = _calculate_utilization_targets(credit_out, credit_limit if credit_limit > 0 else 100000.0)
        
        reply = f"""### 💳 Credit Utilization Ratio Deep-Dive

Credit utilization accounts for **~30% of your CIBIL score**, making it the second most influential factor.

#### 🔍 Your Position:
- **Total Credit Limit:** ₹{credit_limit:,.0f}
- **Outstanding Balance:** ₹{credit_out:,.0f}
- **Current Utilization Ratio:** **{util_info['current_ratio']}%**

---

#### 🎯 Payoff Target Benchmarks:
1. **Safety Threshold (30% Max):**
   - Maximum balance should not exceed: **₹{util_info['target_30_balance']:,.0f}**
   - {"Pay down **₹{:,.0f}** to cross into safe territory." .format(util_info['target_30_paydown']) if util_info['target_30_paydown'] > 0 else "✅ You are already safely under the 30% threshold!"}

2. **Elite Tier (Under 10% for Top 800+ Scores):**
   - Target balance: **₹{util_info['target_10_balance']:,.0f}**
   - Amount to pay off: **₹{util_info['target_10_paydown']:,.0f}**

#### 💡 The 'Statement Date' Secret:
Credit bureaus receive data on your **statement generation date**, NOT your payment due date. Even if you pay your bill in full every month, a statement generated with high balance reports as high utilization.  
**Action:** Make a partial payment 3 days *before* the monthly statement closes."""

        return {
            "reply": reply,
            "action_type": "credit_utilization",
            "suggested_prompts": [
                "How do I request a credit limit increase?",
                "Does closing an old credit card hurt my score?",
                "Give me a 90-day score booster plan"
            ],
            "metrics": {
                "utilization": util_info["current_ratio"],
                "pay_for_30": util_info["target_30_paydown"]
            }
        }

    # 5. DEBT PAYOFF / SNOWBALL VS AVALANCHE
    if any(k in q for k in ["snowball", "avalanche", "debt payoff", "pay off debt", "clear debt", "multiple loans", "reduce debt"]):
        reply = f"""### ⚖️ Debt Elimination: Snowball vs. Avalanche Strategy

When managing multiple debts, choosing the right framework saves thousands in interest and reduces financial anxiety.

---

### 1. The Debt Avalanche Method *(Mathematically Optimal)*
- **How it works:** Rank debts from **highest interest rate** to **lowest interest rate**.
  - Example: Credit Card (36-42% p.a.) ➔ Personal Loan (13-18% p.a.) ➔ Car Loan (9% p.a.) ➔ Home Loan (8.5% p.a.).
- **Execution:** Pay minimums on everything, channel every spare rupee into the top high-interest loan.
- **Advantage:** Minimizes total compound interest paid over the life of your debt.

### 2. The Debt Snowball Method *(Psychologically Powerful)*
- **How it works:** Rank debts from **smallest balance** to **largest balance**, regardless of interest rate.
- **Execution:** Knock out the smallest loan first for quick emotional wins, then roll that freed-up EMI into the next smallest.
- **Advantage:** Rapid momentum. Eliminates active loan count, reducing administrative burden and monthly payment stress.

---

#### 💡 FitAI Custom Recommendation:
{"Your estimated unallocated monthly balance is **₹{:,.0f}**." .format(monthly_balance) if monthly_balance > 0 else "Your monthly balance is currently tight. Prioritize lowering discretionary expenses to free up at least ₹5,000/month for debt acceleration."}
- If you have high-rate revolving credit card debt (>30% APR), **use Avalanche** on the cards first.
- Once revolving card debt is cleared, switch to **Snowball** for smaller personal loans to free up monthly cash flow."""

        return {
            "reply": reply,
            "action_type": "debt_strategy",
            "suggested_prompts": [
                "How does prepayment affect my loan tenure?",
                "Can I consolidate my debts into a single personal loan?",
                "How can I build an emergency fund while paying debt?"
            ],
            "metrics": {
                "active_loans": active_loans,
                "existing_emi": existing_emi
            }
        }

    # 6. EMERGENCY FUND & SAVINGS CUSHION
    if any(k in q for k in ["emergency fund", "savings", "cushion", "liquidity", "reserve", "how much emergency"]):
        target_6mo = expenses * 6.0 if expenses > 0 else 180000.0
        gap = max(0.0, target_6mo - emergency_fund)
        
        reply = f"""### 🛡️ Emergency Reserve & Liquidity Diagnostic

An emergency cushion protects you from taking high-interest personal loans or defaulting during unexpected medical or employment shocks.

- **Current Liquid Reserve:** **₹{emergency_fund:,.0f}**
- **Monthly Essential Expenses:** **₹{expenses:,.0f}**
- **Current Runway:** **{round(emergency_months, 1)} Months** of expenses covered

---

#### 🎯 Safety Benchmarks:
- **Minimum Essential Reserve:** 3 Months = **₹{expenses * 3.0:,.0f}**
- **Recommended Resilient Buffer:** 6 Months = **₹{target_6mo:,.0f}**
- **Reserve Gap to 6-Months:** **₹{gap:,.0f}**

#### 📋 Actionable Setup Guide:
1. **Never Keep Emergency Funds in Equity/Stocks:** Keep 50% in a high-yield sweep-in savings account and 50% in an instant-redemption liquid mutual fund.
2. **Automate the Build:** Setting aside **₹{monthly_balance * 0.4:,.0f} / mo** will close your emergency fund gap within 6–12 months."""

        return {
            "reply": reply,
            "action_type": "emergency_fund",
            "suggested_prompts": [
                "Where should I park my emergency fund?",
                "How much should I invest vs save?",
                "What is my safe borrowing limit?"
            ],
            "metrics": {
                "emergency_months": round(emergency_months, 1),
                "gap": gap
            }
        }

    # 7. DEFAULT CONVERSATIONAL FINANCIAL ADVISOR
    # General queries (What is CIBIL, inquiry impact, co-signer, etc.)
    reply = f"""### 🤖 FitAI Financial Intelligence Summary

Hello **{full_name}**! I have synchronized with your CreditFit 360 session.

#### 📈 Live Financial Profile Indicators:
- **Credit Score:** **{int(score) if score > 0 else '720 (Estimated / Pending)'}**
- **Debt-to-Income (FOIR):** **{round(foir, 1)}%** {"🟢 Healthy" if foir < 35 else ("🟡 Moderate" if foir <= 50 else "🔴 High")}
- **Credit Card Utilization:** **{round(utilization, 1)}%** {"🟢 Optimal (<30%)" if utilization <= 30 else "🔴 Elevated (>30%)"}
- **Monthly Surplus Balance:** **₹{max(0.0, monthly_balance):,.0f}**
- **Emergency Runway:** **{round(emergency_months, 1)} Months**

---

#### 💬 How I Can Assist You Right Now:
1. **Score Optimization:** Ask *"How can I raise my CIBIL by 50 points in 90 days?"*
2. **Loan Eligibility:** Ask *"Can I afford a new car or home loan?"*
3. **Dispute Resolution:** Ask *"Draft a CIBIL dispute letter for an erroneous payment mark"*
4. **Debt Strategy:** Ask *"Should I use Snowball or Avalanche to clear my loans?"*
5. **Credit Rules:** Ask me any question about interest rates, CIBIL scoring formulas, or bank loan criteria."""

    return {
        "reply": reply,
        "action_type": "general_advisory",
        "suggested_prompts": [
            "🚀 Give me a 90-day score booster plan",
            "🏦 Calculate my safe loan borrowing limit",
            "💳 How do I drop utilization below 30%?",
            "📝 Draft an official CIBIL dispute letter"
        ],
        "metrics": {
            "score": score,
            "foir": round(foir, 1),
            "utilization": round(utilization, 1),
            "monthly_surplus": max(0.0, monthly_balance)
        }
    }
