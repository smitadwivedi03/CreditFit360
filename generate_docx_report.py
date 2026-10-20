"""
Generates the comprehensive executive Microsoft Word (.docx) document
for CreditFit 360: Full Platform Report & Client Presentation Guide.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets the background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    """Sets inner padding for a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def create_document():
    doc = docx.Document()

    # Page Margins: 1 inch on all sides
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles Setup
    NAVY = RGBColor(15, 23, 42)
    BLUE = RGBColor(37, 99, 235)
    SLATE = RGBColor(71, 85, 105)
    DARK_TEXT = RGBColor(30, 41, 59)
    GREEN = RGBColor(5, 150, 105)

    # =========================================================================
    # COVER / HEADER BANNER
    # =========================================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(4)
    run_brand = title_p.add_run("CREDITFIT 360™")
    run_brand.font.name = "Arial"
    run_brand.font.size = Pt(28)
    run_brand.font.bold = True
    run_brand.font.color.rgb = BLUE

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(18)
    run_sub = sub_p.add_run("Executive Master System Report & Client Presentation Dossier")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(16)
    run_sub.font.bold = True
    run_sub.font.color.rgb = NAVY

    tag_p = doc.add_paragraph()
    tag_p.paragraph_format.space_before = Pt(0)
    tag_p.paragraph_format.space_after = Pt(28)
    run_tag = tag_p.add_run("Borrower-First Defense Architecture | Reverse Underwriting | RBI CEPC 2023-24 & DPDP Act 2023 Compliant")
    run_tag.font.name = "Calibri"
    run_tag.font.size = Pt(11)
    run_tag.font.italic = True
    run_tag.font.color.rgb = SLATE

    # Meta Table Box
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Platform Version", "2.5 Enterprise Edition (Neon-Bento Architecture)"),
        ("Prepared For", "Corporate Clients, Strategic Fintech Partners, Investors, Academic Evaluators"),
        ("Production Status", "Active Production-Ready Localhost Server (Port 5000 / Auto-Failover)"),
        ("Document Classification", "CONFIDENTIAL & PROPRIETARY — SYSTEM AUDIT & PRESENTATION DOSSIER")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0)
        set_cell_margins(c1)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = NAVY

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(24)

    # Helper function for section headings
    def add_section_header(num, title):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(22)
        h.paragraph_format.space_after = Pt(6)
        r_num = h.add_run(f"SECTION {num:02d} — ")
        r_num.font.name = "Arial"
        r_num.font.size = Pt(13)
        r_num.font.bold = True
        r_num.font.color.rgb = BLUE

        r_title = h.add_run(title.upper())
        r_title.font.name = "Arial"
        r_title.font.size = Pt(13)
        r_title.font.bold = True
        r_title.font.color.rgb = NAVY

        # Subtle divider
        div = doc.add_paragraph()
        div.paragraph_format.space_before = Pt(0)
        div.paragraph_format.space_after = Pt(12)
        r_div = div.add_run("―" * 58)
        r_div.font.color.rgb = RGBColor(226, 232, 240)

    def add_callout(text, title="KEY STRATEGIC TAKEAWAY"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "EFF6FF")
        set_cell_margins(cell, top=160, bottom=160, left=200, right=200)

        cp = cell.paragraphs[0]
        cp.paragraph_format.space_after = Pt(4)
        c_title = cp.add_run(f"📌 {title}: ")
        c_title.font.bold = True
        c_title.font.size = Pt(10)
        c_title.font.color.rgb = BLUE

        c_body = cp.add_run(text)
        c_body.font.size = Pt(10)
        c_body.font.color.rgb = NAVY

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY & MARKET OPPORTUNITY
    # =========================================================================
    add_section_header(1, "Executive Summary & Market Opportunity")

    p = doc.add_paragraph()
    p.add_run(
        "CreditFit 360 is India's first borrower-aligned financial intelligence, reverse underwriting, and statutory "
        "defense operating system. In the contemporary Indian financial technology ecosystem, retail and enterprise "
        "borrowers navigate an asymmetrical relationship with credit institutions. Existing fintech portals—such as "
        "CRED, Paisabazaar, and BankBazaar—operate predominantly as loan distribution agents. Their core monetization "
        "relies upon receiving commissions from banks and non-banking financial companies (NBFCs) for selling debt products."
    )

    p2 = doc.add_paragraph()
    p2.add_run(
        "Because these legacy platforms are commercially aligned with the lenders, they cannot and do not advocate for the borrower. "
        "They present borrowers with a simple, three-digit credit score (e.g., 720 on CIBIL), while obscuring the true mathematical "
        "underwriting algorithms that banks use to sanction or reject credit."
    )

    add_callout(
        "CreditFit 360 eliminates this credit asymmetry. It sits exclusively on the borrower's side of the table: reverse-underwriting "
        "loan readiness before applications are made, stress-testing debt-to-income limits (FOIR), and enforcing statutory compensation "
        "under RBI master directions.",
        "THE PARADIGM SHIFT"
    )

    # Market Comparison Table
    comp_table = doc.add_table(rows=6, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Evaluation Metric", "Legacy Portals (CRED / Paisabazaar)", "CreditFit 360 Enterprise Suite"]
    for j, h in enumerate(headers):
        cell = comp_table.cell(0, j)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    comp_rows = [
        ("Alignment", "Lender-Centric (Affiliate Commission)", "Borrower-Centric (Independent Defense)"),
        ("Loan Application Process", "Pushes multiple applications (Hard Inquiries)", "Reverse-underwrites first (Zero Inquiries)"),
        ("Underwriting Logic", "Hidden Black Box (Single 3-digit score)", "Transparent FOIR, DTI & Multi-Bank Fitment Matrix"),
        ("Statutory Rights Protection", "Silent on bank errors & delays", "Enforces RBI CEPC 2023-24 ₹100/day penalty"),
        ("Data Sovereignty & Privacy", "Monetizes and distributes borrower lead data", "DPDP Act 2023 compliant with Right to Erasure")
    ]

    for i, row in enumerate(comp_rows):
        for j, val in enumerate(row):
            cell = comp_table.cell(i + 1, j)
            bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
            set_cell_background(cell, bg)
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY
            elif j == 2:
                r.font.color.rgb = BLUE
                r.font.bold = True
            else:
                r.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # SECTION 2: THE 4 CORE FINANCIAL PROBLEMS SOLVED
    # =========================================================================
    add_section_header(2, "The Core Industry Problems Solved by CreditFit 360")

    problems = [
        ("1. The Credit Opacity & Underwriting Rejection Crisis",
         "Over 65% of formal retail loan applications in India face rejection because consumers only review their raw CIBIL or Experian score. Lenders, however, evaluate Debt-to-Income (Fixed Obligation to Income Ratio - FOIR), inquiry velocity, and debt-service capacity. CreditFit 360 demystifies this underwriting logic, providing users with actionable pre-qualification metrics."),
        
        ("2. The 'Hard Inquiry' Compounding Trap",
         "When an applicant is rejected by a lender, they often apply impulsively to several alternative banks. Each formal application triggers a 'Hard Search' on the borrower's credit bureau file. Multiple hard inquiries in rapid succession degrade the credit score by 15 to 35 points, trapping the borrower in subprime status. CreditFit 360 executes high-fidelity simulated stress-testing with zero bureau inquiries."),

        ("3. Unenforced RBI Statutory Rights (₹100/Day Penalty Circular)",
         "Under RBI Master Direction CEPC/2023-24, Credit Information Companies (CIBIL, Experian, CRIF, Equifax) and lenders must resolve credit grievance errors within 30 days. Beyond 30 days, they must pay the borrower ₹100 per day of delay. Less than 1% of Indian consumers are aware of this right. CreditFit 360 automates statutory delay calculations and generates formal legal demand notices under Section 21 of the CIC Act."),

        ("4. The MSME Credit Exclusion Gap",
         "India's 63 million Micro, Small, and Medium Enterprises face a credit shortfall exceeding $300 billion. Traditional retail scores penalize business owners who reinvest cash flow into inventory rather than personal credit products. CreditFit 360 introduces a multi-factor SME scoring engine that evaluates operational vintage, operating profit margin consistency, vendor payment discipline, and cash buffer runways.")
    ]

    for title, desc in problems:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(title)
        r_t.font.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = NAVY

        p_d = doc.add_paragraph()
        p_d.paragraph_format.space_after = Pt(8)
        r_d = p_d.add_run(desc)
        r_d.font.size = Pt(10)
        r_d.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SECTION 3: COMPLETE PLATFORM MODULES (ALL 15 FEATURES)
    # =========================================================================
    add_section_header(3, "Exhaustive Operational Guide to All 15 Platform Modules")

    modules = [
        ("1. Secure Authentication & Demo Gateway", "/", "login.html",
         "Features role-based access control, cryptographic password hashing (scrypt with salt), and an instant '1-Click Demo Login' preloaded with demo@creditfit360.com / Demo@123. Allows prospective clients to test features without forced manual data entry."),
        
        ("2. Executive Command Dashboard", "/dashboard", "dashboard.html",
         "The central financial intelligence cockpit. Displays personalized greeting, live CreditFit 0-100 gauge, FOIR alerts, emergency runway meters, and direct links to print the institutional loan dossier."),

        ("3. Personal CreditFit Scoring Engine", "/personal-credit", "personal_credit.html",
         "A structured 4-step wizard capturing demographics, income, obligations, revolving debt, and liquid reserves. Integrates the RBI Account Aggregator (AA) Auto-Fill pipeline to pull bank figures directly via simulated OTP 123456."),

        ("4. SME CreditScore Engine", "/sme-credit-score", "sme_credit_score.html",
         "Specialized assessment framework for sole proprietorships and MSMEs. Scores operational longevity, profit margins, supplier payment discipline, and liquid cash buffers."),

        ("5. Institutional Loan Readiness Dossier", "/dossier", "dossier.html",
         "Executive, print-ready formal document. Generates an official reference ID (e.g., CF360-IND-202610-XXXX), computes the maximum sanctionable loan under a 50% FOIR ceiling, maps pre-approval odds across Tier-1 banks (SBI, HDFC, ICICI, Kotak), and outputs a pristine A4 PDF."),

        ("6. Reverse Underwriting Engine", "/defense-suite", "defense_suite.html",
         "Stress-tests applicant loan requests against real-world credit committee rules. Simulates maximum allowable EMI and surfaces corrective recommendations (e.g. 'Pay down ₹35,000 in credit card debt to drop FOIR below 40%')."),

        ("7. RBI Statutory Penalty Enforcer", "/defense-suite (Tab 2)", "defense_suite.html",
         "Calculates mandatory delay compensation under RBI Master Direction CEPC/2023-24 (Days Delayed beyond 30 × ₹100/day). Auto-generates a ready-to-serve formal legal notice under Section 21 of the CIC Act 2005."),

        ("8. FitAI Financial Co-Pilot", "/assistant", "assistant.html",
         "Context-aware AI financial assistant. Synchronizes in real time with active session indicators (FOIR, credit score, monthly surplus) to provide customized advice and quick-prompt chips."),

        ("9. MoneyMap Cash Flow Visualizer", "/moneymap", "moneymap.html",
         "Interactive income allocation simulator. Categorizes monthly cash flow into fixed obligations, living expenses, investments, and discretionary buffer."),

        ("10. Decision Lab (A/B Simulator)", "/decision-lab", "decision_lab.html",
         "Comparative financial scenario analysis. Evaluates trade-offs such as prepaying a home loan vs. investing the equivalent surplus into an equity index fund."),

        ("11. Wealth Path Milestone Planner", "/wealth-path", "wealth_path.html",
         "Long-term goal and asset acquisition roadmap. Adjusts for annual inflation and compounding growth to calculate monthly savings requirements."),

        ("12. What-If FinTwin Simulator", "/what-if-simulator", "what_if_simulator.html",
         "Digital twin sandbox. Allows borrowers to drag sliders representing debt payoffs, new credit cards, or credit line closures to preview projected score trajectories."),

        ("13. DPDP Act 2023 Privacy Center", "/privacy-consent-center", "privacy_center.html",
         "Regulatory governance dashboard. Displays an immutable audit trail of all consent events (Section 6), provides one-click JSON data portability, and enables irreversible data erasure (Section 12 Right to be Forgotten)."),

        ("14. System Settings & Profile", "/settings", "settings.html",
         "User profile administration, notification configurations, security options, and quick access to data privacy controls."),

        ("15. Legal Disclaimers & Institutional Information", "/about & /disclaimer", "about.html",
         "Clear declarations affirming that CreditFit 360 acts as an analytical technology platform and financial literacy engine, compliant with applicable regulatory guidelines.")
    ]

    for name, route, tpl, desc in modules:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(1)
        r_n = p.add_run(name)
        r_n.font.bold = True
        r_n.font.size = Pt(10.5)
        r_n.font.color.rgb = NAVY

        r_rt = p.add_run(f" | Route: {route} ({tpl})")
        r_rt.font.size = Pt(9.5)
        r_rt.font.color.rgb = BLUE

        p_d = doc.add_paragraph()
        p_d.paragraph_format.space_before = Pt(0)
        p_d.paragraph_format.space_after = Pt(6)
        r_d = p_d.add_run(desc)
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SECTION 4: THE 7-MINUTE CLIENT PRESENTATION SCRIPT
    # =========================================================================
    add_section_header(4, "The 7-Minute Live Client Presentation Script (Word-for-Word)")

    p_intro = doc.add_paragraph()
    p_intro.add_run(
        "When pitching CreditFit 360 to an enterprise client, banking partner, or investor jury, "
        "use this high-impact, seven-minute structured walkthrough. It transitions logically from the market problem "
        "to a live interactive demonstration, concluding with regulatory compliance and revenue models."
    )

    pitch_steps = [
        ("Minute 1: The Hook & Market Asymmetry",
         "Action: Stand confidently, address the client, and open with the market gap.\n"
         "Dialogue: 'Good morning. In India today, over 150 million consumers and 60 million MSMEs interact with the credit system. "
         "Yet, when they apply for a loan, they enter a complete black box. Platforms like CRED or Paisabazaar are essentially loan distribution agents—they "
         "get paid when you borrow more. Nobody is in the borrower's corner. We built CreditFit 360 to be the first Borrower Defense and Reverse Underwriting Suite in India.'"),

        ("Minute 2: Portal Sign-In & Dashboard Cockpit",
         "Action: Launch the browser at http://localhost:5000 and click '⚡ 1-Click Demo Login'.\n"
         "Dialogue: 'Let’s open the platform. On the landing page, notice our authentication system supports full registration and login. "
         "For this demonstration, I will click 1-Click Demo Login. Instantly, we enter the Executive Dashboard. Rather than just displaying a vanity three-digit score, "
         "CreditFit 360 immediately surfaces debt-to-income limits (FOIR), cash runway months, and predictive wealth trajectories.'"),

        ("Minute 3: India Stack Account Aggregator (AA) Fast-Track",
         "Action: Navigate to 'Personal CreditFit' and click the blue 'Connect Bank via AA' button.\n"
         "Dialogue: 'Normally, filling a 20-field financial questionnaire leads to high friction and user drop-off. Watch this: We leverage India’s RBI Account Aggregator framework. "
         "The borrower selects their bank, enters their mobile number, and confirms the simulated OTP 123456. Within seconds, verified salary credits, existing loan EMIs, and liquid "
         "balances are securely ingested and populated across the entire four-step underwriting engine.'"),

        ("Minute 4: Reverse Underwriting (Protecting the Score)",
         "Action: Click 'Calculate Score' and navigate to 'Defense Suite' -> 'Reverse Underwriter'.\n"
         "Dialogue: 'Here is where CreditFit 360 protects the consumer. Instead of applying blind and risking a hard inquiry that damages their CIBIL score, our Reverse Underwriter "
         "simulates bank credit committee policies. If the applicant’s FOIR exceeds 50%, the system flags the exact risk and advises them on how much debt to prepay before applying.'"),

        ("Minute 5: RBI Statutory Compensation Enforcer (The Shock & Awe Feature)",
         "Action: Click the 'Statutory Defense & RBI Notice' tab.\n"
         "Dialogue: 'This is our standout regulatory innovation. Under RBI Circular CEPC/2023-24, lenders and credit bureaus must resolve disputes within 30 days or pay the borrower "
         "₹100 per day of delay. Less than one percent of consumers know this right exists. CreditFit 360 computes the statutory penalty and automatically drafts a formal legal notice "
         "ready to serve under Section 21 of the CIC Act.'"),

        ("Minute 6: Generating the Institutional Loan Dossier (PDF)",
         "Action: Click '📑 Export Dossier (PDF)' in the topbar and demonstrate the print view.\n"
         "Dialogue: 'When a borrower is ready to apply, they don't walk into a bank empty-handed. CreditFit 360 compiles this Institutional Loan Readiness Dossier. It features a digital "
         "verification ID, FOIR stress metrics, max sanctionable loan limits, and approval odds across SBI, HDFC, ICICI, and Kotak. One click on Print Dossier generates a clean, professional A4 PDF.'"),

        ("Minute 7: DPDP Act 2023 Compliance & Monetization",
         "Action: Navigate to 'DPDP Privacy Center' and summarize commercial viability.\n"
         "Dialogue: 'Finally, compliance is foundational. Under India’s DPDP Act 2023, users can view their immutable consent audit trail, download their full data package, or execute the "
         "Right to Erasure to permanently purge their database records. With revenue models spanning B2C defense subscriptions, B2B SaaS for CAs and loan agents, and pre-underwritten NBFC referrals, "
         "CreditFit 360 is an enterprise-grade fintech platform ready for market deployment. Thank you.'")
    ]

    for title, content in pitch_steps:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)
        r_st = p_t.add_run(title)
        r_st.font.bold = True
        r_st.font.size = Pt(10.5)
        r_st.font.color.rgb = BLUE

        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(0)
        p_c.paragraph_format.space_after = Pt(6)
        r_sc = p_c.add_run(content)
        r_sc.font.size = Pt(9.5)
        r_sc.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SECTION 5: COMMERCIAL VIABILITY & MONETIZATION
    # =========================================================================
    add_section_header(5, "Commercial Viability, Revenue Models & Business Scalability")

    p = doc.add_paragraph()
    p.add_run(
        "CreditFit 360 is architected for diversified commercial revenue streams across retail (B2C), "
        "professional intermediaries (B2B SaaS), and institutional lender marketplaces (B2B2C):"
    )

    rev_table = doc.add_table(rows=4, cols=4)
    rev_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rev_headers = ["Revenue Stream", "Target Market", "Pricing Model", "Core Value Proposition"]
    for j, h in enumerate(rev_headers):
        cell = rev_table.cell(0, j)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    rev_data = [
        ("B2C Premium Defense", "Retail Borrowers & Salaried Professionals", "₹399/year or ₹49/month", "Auto-dispute letter generator, RBI statutory compensation tracker, unlimited What-If simulations."),
        ("B2B SaaS for CAs & DSAs", "Direct Selling Agents, Loan Brokers, Accounting Firms", "₹1,499/month per license", "Client loan readiness assessment dossiers, pre-qualification stress tests, rejection-prevention tools."),
        ("Pre-Underwritten Referral Marketplace", "Tier-2 & Tier-3 NBFCs and Digital Lenders", "1.0% – 1.8% of loan sanction value", "Routing pre-vetted applicants whose FOIR and credit profiles match exact lender underwriting criteria.")
    ]

    for i, row in enumerate(rev_data):
        for j, val in enumerate(row):
            cell = rev_table.cell(i + 1, j)
            bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
            set_cell_background(cell, bg)
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY
            else:
                r.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # SECTION 6: CLIENT OBJECTION HANDLING & INVESTOR Q&A
    # =========================================================================
    add_section_header(6, "Client Objection Handling & Investor Q&A Guide")

    qa_list = [
        ("Q1: How is CreditFit 360 different from CRED or Paisabazaar?",
         "Answer: CRED and Paisabazaar are essentially credit distribution marketplaces. They monetize through lender affiliate commissions—they get paid when a user borrows more money. As a result, they cannot act as a neutral advocate for the borrower. CreditFit 360 is borrower-aligned: it helps users reduce debt obligations, reverse-underwrite loan readiness without hard inquiries, and enforce statutory penalty claims against non-compliant banks."),

        ("Q2: Is CreditFit 360 an authorized credit bureau like CIBIL?",
         "Answer: No, and that is our explicit competitive advantage. Credit bureaus are historical data repositories that record past repayment behavior. CreditFit 360 is an analytical decision-support and defense platform. We ingest bureau data and bank statements via the Account Aggregator framework to evaluate real debt capacity and simulate institutional underwriting criteria."),

        ("Q3: What happens if a bank ignores the RBI statutory penalty notice?",
         "Answer: The ₹100 per day penalty is not an informal request; it is legally binding under RBI Master Direction CEPC/2023-24. If a lender fails to remediate the credit error or pay compensation within 30 days of the notice generated by CreditFit 360, the borrower escalates the complaint to the RBI Banking Ombudsman (CMS Portal). Lenders face formal regulatory penalties and audit citations for unresolved ombudsman complaints."),

        ("Q4: How does CreditFit 360 comply with India's new data privacy laws?",
         "Answer: CreditFit 360 was built specifically around the Digital Personal Data Protection (DPDP) Act 2023. We maintain an immutable Section 6 consent audit log recording every data access event with timestamps and IP addresses. We fulfill Section 12 Data Portability with instant JSON data exports, and enable users to execute the Right to Erasure, which permanently and irreversibly purges all personal records from our database.")
    ]

    for q, a in qa_list:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q)
        r_q.font.bold = True
        r_q.font.size = Pt(10)
        r_q.font.color.rgb = NAVY

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(6)
        r_a = p_a.add_run(a)
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SECTION 7: PRODUCTION LOCAL SERVER OPERATIONS
    # =========================================================================
    add_section_header(7, "Production Local Server Operations Manual")

    p = doc.add_paragraph()
    p.add_run(
        "CreditFit 360 includes a dedicated localhost server runner configured for production stability, "
        "automatic port conflict resolution, and local network accessibility:"
    )

    ops_steps = [
        ("One-Click Launch (Windows Explorer)", "Double-click 'run_server.bat' or 'start_localhost.bat' in the project folder. The script automatically verifies Python in PATH, installs dependencies, starts the server, and opens your default browser."),
        ("Terminal Command Launch", "Run 'python server.py' from PowerShell or Command Prompt. Optional flags include '--port 8080' (custom port) or '--no-browser' (headless mode)."),
        ("Automatic Port Collision Protection", "If port 5000 is occupied by another application, server.py automatically detects the conflict and binds to the next available port (e.g. 5001) without crashing."),
        ("LAN / Mobile Phone Testing", "server.py automatically identifies your machine's local Wi-Fi IP address (e.g., http://192.168.1.4:5000), allowing seamless multi-device testing from a smartphone on the same network.")
    ]

    for t, d in ops_steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(f"• {t}: ")
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = NAVY

        r_d = p.add_run(d)
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = DARK_TEXT

    # Output path
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CreditFit_360_Master_Client_Report.docx")
    doc.save(output_path)
    print(f"Document saved successfully at: {output_path}")

if __name__ == "__main__":
    create_document()
