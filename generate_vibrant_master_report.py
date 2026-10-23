"""
Script to generate the ultra-colorful, visually captivating Microsoft Word (.docx)
Executive Presentation Report for CreditFit 360.
Includes:
- Modern gradient-styled visual diagrams, flowcharts, and graphs (Matplotlib + Pillow)
- High-contrast, vibrant corporate color scheme (Navy, Electric Blue, Emerald, Purple, Amber, Crimson)
- Colorful executive callout boxes with solid left border strips
- Beautiful tables with dark gradient headers, zebra rows, and color-coded status badges
- Dedicated colorful card layouts for all 15 platform modules
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "static", "report_assets_vibrant")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Global plot styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8


# =============================================================================
# 1. GENERATE ULTRA-COLORFUL CHARTS & DIAGRAMS
# =============================================================================

def generate_vibrant_charts():
    print("[*] Generating high-contrast, vibrant charts and diagrams...")

    # --- Chart 1: Paradigm Comparison (Brokers vs CreditFit 360) ---
    fig, ax = plt.subplots(figsize=(10, 5.0), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')

    # Card 1: Traditional Brokers (Red/Coral theme)
    rect_left = patches.FancyBboxPatch((0.02, 0.05), 0.46, 0.88, boxstyle="round,pad=0.03",
                                       fc='#FFF1F2', ec='#F43F5E', lw=2.0)
    ax.add_patch(rect_left)
    # Header box for Left
    hdr_left = patches.FancyBboxPatch((0.04, 0.77), 0.42, 0.13, boxstyle="round,pad=0.02",
                                      fc='#E11D48', ec='#BE123C', lw=1.2)
    ax.add_patch(hdr_left)
    ax.text(0.25, 0.835, "TRADITIONAL PORTALS (BROKERS)\n(CRED, Paisabazaar, BankBazaar)", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF')
    
    left_points = [
        ("✖ Monetization:", "Lenders pay commissions to push high-interest debt"),
        ("✖ Black Box:", "Hides actual bank FOIR & underwriting algorithms"),
        ("✖ Hard Inquiries:", "Multiple loan applications damage CIBIL score"),
        ("✖ Rejection Penalty:", "Score drops 15–30 pts per failed bank inquiry"),
        ("✖ Bank Grievances:", "Silent on bank errors, wrong defaults & delays"),
        ("✖ MSME Blindspot:", "Ignores 63M small businesses without bureau history")
    ]
    for idx, (head, desc) in enumerate(left_points):
        y_pos = 0.69 - idx * 0.11
        ax.text(0.05, y_pos, head, fontsize=8.5, fontweight='bold', color='#9F1239', va='center')
        ax.text(0.05, y_pos - 0.045, desc, fontsize=8, color='#881337', va='center')

    # Card 2: CreditFit 360 (Emerald Green theme)
    rect_right = patches.FancyBboxPatch((0.52, 0.05), 0.46, 0.88, boxstyle="round,pad=0.03",
                                        fc='#F0FDF4', ec='#10B981', lw=2.0)
    ax.add_patch(rect_right)
    # Header box for Right
    hdr_right = patches.FancyBboxPatch((0.54, 0.77), 0.42, 0.13, boxstyle="round,pad=0.02",
                                       fc='#059669', ec='#047857', lw=1.2)
    ax.add_patch(hdr_right)
    ax.text(0.75, 0.835, "CREDITFIT 360™\n(BORROWER DEFENSE SYSTEM)", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF')

    right_points = [
        ("✔ 100% Borrower Aligned:", "Educates, optimizes, and protects the consumer"),
        ("✔ Reverse Underwriting:", "Tests FOIR, debt capacity, and bank policies upfront"),
        ("✔ Zero Hard Inquiries:", "Safe simulations protect your credit score completely"),
        ("✔ Restorative Advice:", "Tells you exact debt amount to pay to guarantee approval"),
        ("✔ RBI Statutory Penalty:", "Calculates ₹100/day compensation and generates notices"),
        ("✔ SME Cash-Flow Engine:", "Scores MSMEs using turnover, margins & supplier history")
    ]
    for idx, (head, desc) in enumerate(right_points):
        y_pos = 0.69 - idx * 0.11
        ax.text(0.55, y_pos, head, fontsize=8.5, fontweight='bold', color='#065F46', va='center')
        ax.text(0.55, y_pos - 0.045, desc, fontsize=8, color='#064E3B', va='center')

    plt.tight_layout()
    chart1_path = os.path.join(ASSETS_DIR, "paradigm_comparison_vibrant.png")
    plt.savefig(chart1_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    # --- Chart 2: Architecture & Data Flowchart (High-Contrast Colorful) ---
    fig, ax = plt.subplots(figsize=(10, 4.4), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')

    tiers = [
        ("CLIENT TIER\n(Responsive Bento UI)", 0.11, 0.50, '#E0F2FE', '#0284C7', '#0369A1'),
        ("API GATEWAY\n(Flask Core app.py)", 0.33, 0.50, '#EDE9FE', '#7C3AED', '#5B21B6'),
        ("INTELLIGENCE CORE\n(ai_engine.py)", 0.55, 0.74, '#FDF2F8', '#DB2777', '#9D174D'),
        ("DEFENSE ENGINES\n(Underwrite & RBI)", 0.55, 0.26, '#D1FAE5', '#059669', '#065F46'),
        ("PERSISTENCE & AUDIT\n(SQLite database.db)", 0.80, 0.50, '#FEF3C7', '#D97706', '#92400E')
    ]

    for label, x, y, bg, border, text_c in tiers:
        box = patches.FancyBboxPatch((x - 0.095, y - 0.17), 0.19, 0.34, boxstyle="round,pad=0.025",
                                    fc=bg, ec=border, lw=2.2)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=text_c)

    def draw_colored_arrow(x1, y1, x2, y2, color, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, arrowstyle="->", lw=2.0))
        if label:
            ax.text((x1 + x2)/2, (y1 + y2)/2 + 0.05, label, ha='center', fontsize=7.5, color=color, fontweight='bold')

    draw_colored_arrow(0.205, 0.50, 0.235, 0.50, '#0284C7', "RESTful JSON")
    draw_colored_arrow(0.425, 0.56, 0.455, 0.70, '#7C3AED', "Context Matrix")
    draw_colored_arrow(0.425, 0.44, 0.455, 0.30, '#059669', "Risk Formulas")
    draw_colored_arrow(0.645, 0.70, 0.705, 0.55, '#DB2777', "User Dossier")
    draw_colored_arrow(0.645, 0.30, 0.705, 0.45, '#D97706', "DPDP Audit")

    plt.tight_layout()
    chart2_path = os.path.join(ASSETS_DIR, "system_architecture_vibrant.png")
    plt.savefig(chart2_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    # --- Chart 3: Market Size & Opportunity (Vibrant Multi-Color Graphs) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax1.set_facecolor('#FFFFFF')
    ax2.set_facecolor('#FFFFFF')

    # Subplot 1: Bar chart with distinct vibrant colors
    categories = ['Retail\nBorrowers', 'Operating\nMSMEs', 'Unenforced\nRBI Claims', 'Rejection\nOpacity']
    values = [150, 63, 99, 68]
    bar_colors = ['#3B82F6', '#10B981', '#EF4444', '#F59E0B']
    bars = ax1.bar(categories, values, color=bar_colors, width=0.55, edgecolor='#0F172A', linewidth=1.2)
    ax1.set_title("Market Demographics & Borrower Pain Points", fontsize=11, fontweight='bold', color='#0F172A', pad=12)
    ax1.set_ylabel("Volume (Millions) / Percentage (%)", fontsize=8.5, fontweight='bold', color='#475569')
    for bar, val, cat in zip(bars, values, categories):
        suffix = "%" if ("%" in cat or val < 100) else "M"
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3.5, f"{val}{suffix}",
                 ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax1.set_ylim(0, 180)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Subplot 2: Donut Chart for $300B Gap
    labels = ['Credit Supplied\n($120 Billion)', 'Unmet Credit Gap\n($300 Billion)']
    sizes = [120, 300]
    donut_colors = ['#CBD5E1', '#F43F5E']
    explode = (0, 0.08)
    wedges, texts, autotexts = ax2.pie(sizes, explode=explode, labels=labels, colors=donut_colors, 
                                       autopct='%1.1f%%', startangle=140, pctdistance=0.75,
                                       wedgeprops=dict(width=0.45, edgecolor='#FFFFFF', linewidth=2))
    for t in texts:
        t.set_fontsize(8.5)
        t.set_fontweight('bold')
        t.set_color('#1E293B')
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight('bold')
        at.set_color('#FFFFFF')

    ax2.set_title("India $420B MSME Addressable Debt Market", fontsize=11, fontweight='bold', color='#0F172A', pad=12)

    plt.tight_layout()
    chart3_path = os.path.join(ASSETS_DIR, "market_opportunity_vibrant.png")
    plt.savefig(chart3_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    # --- Chart 4: FOIR Sanction Probability Matrix (Vibrant Zones) ---
    fig, ax = plt.subplots(figsize=(9.5, 4.2), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#FFFFFF')

    foir = np.linspace(15, 75, 120)
    prob = 100 / (1 + np.exp((foir - 48) / 4.2))

    ax.plot(foir, prob, color='#2563EB', lw=3.0, label='Tier-1 Bank Sanction Odds (%)', zorder=5)

    # Colorful Zones
    ax.axvspan(15, 38, alpha=0.35, color='#A7F3D0', label='Prime Zone (FOIR < 38%): High Approval Odds')
    ax.axvspan(38, 50, alpha=0.35, color='#FDE68A', label='Caution Zone (38%–50%): High Interest Rates')
    ax.axvspan(50, 75, alpha=0.35, color='#FECDD3', label='Rejection Zone (> 50%): Automated System Rejection')

    ax.axvline(50, color='#DC2626', linestyle='--', lw=2.0, label='RBI 50% Statutory Hard Ceiling')

    ax.set_title("Reverse Underwriting Matrix: FOIR Debt Load vs. Approval Probability", 
                 fontsize=11.5, fontweight='bold', color='#0F172A', pad=14)
    ax.set_xlabel("FOIR (Fixed Obligation to Income Ratio) %", fontsize=9.5, fontweight='bold', color='#334155')
    ax.set_ylabel("Simulated Bank Sanction Probability (%)", fontsize=9.5, fontweight='bold', color='#334155')

    ax.legend(loc='lower left', fontsize=8.5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.grid(True, linestyle=':', alpha=0.6, color='#94A3B8')
    ax.set_ylim(0, 105)
    ax.set_xlim(15, 75)

    plt.tight_layout()
    chart4_path = os.path.join(ASSETS_DIR, "foir_simulation_vibrant.png")
    plt.savefig(chart4_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    # --- Chart 5: RBI Statutory Compensation Timeline (Vibrant Compounding Graph) ---
    fig, ax = plt.subplots(figsize=(9.5, 4.0), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#FFFFFF')

    days = np.array([0, 15, 30, 45, 60, 90, 120])
    compensation = np.maximum(0, (days - 30) * 100)

    ax.plot(days, compensation, marker='s', markersize=7, color='#E11D48', lw=2.8, 
            label='Mandatory Legal Compensation (₹100/day delay)', zorder=5)

    ax.axvspan(0, 30, alpha=0.25, color='#A7F3D0', label='30-Day Mandatory Resolution Grace Period (No Penalty)')
    ax.axvspan(30, 120, alpha=0.25, color='#FECDD3', label='Compounding Statutory Penalty Window (RBI Mandate)')

    for d, c in zip(days, compensation):
        if d >= 30:
            ax.annotate(f"₹{c:,}", (d, c), textcoords="offset points", xytext=(0, 10),
                        ha='center', fontsize=9, fontweight='bold', color='#BE123C',
                        bbox=dict(boxstyle="round,pad=0.2", fc="#FFF1F2", ec="#F43F5E", lw=1))

    ax.set_title("RBI CEPC/2023-24 Legal Compensation Accrual Timeline", 
                 fontsize=11.5, fontweight='bold', color='#0F172A', pad=14)
    ax.set_xlabel("Days Elapsed Since Formal Grievance Lodged", fontsize=9.5, fontweight='bold', color='#334155')
    ax.set_ylabel("Legally Binding Compensation Payable (INR)", fontsize=9.5, fontweight='bold', color='#334155')

    ax.legend(loc='upper left', fontsize=8.5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.grid(True, linestyle=':', alpha=0.6, color='#94A3B8')

    plt.tight_layout()
    chart5_path = os.path.join(ASSETS_DIR, "rbi_penalty_vibrant.png")
    plt.savefig(chart5_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    # --- Chart 6: 7-Minute Demo Flowchart (7 Vibrant Chevrons) ---
    fig, ax = plt.subplots(figsize=(10.5, 3.6), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')

    stages = [
        ("Min 1", "The Hook\n& Problem", '#DBEAFE', '#2563EB', '#1E40AF'),
        ("Min 2", "1-Click Login\n& Dashboard", '#E0E7FF', '#4F46E5', '#3730A3'),
        ("Min 3", "Account\nAggregator AA", '#EDE9FE', '#7C3AED', '#5B21B6'),
        ("Min 4", "Reverse\nUnderwriting", '#FCE7F3', '#DB2777', '#9D174D'),
        ("Min 5", "RBI Penalty\nNotice Draft", '#FEE2E2', '#DC2626', '#991B1B'),
        ("Min 6", "Official A4\nDossier PDF", '#FEF3C7', '#D97706', '#92400E'),
        ("Min 7", "DPDP Erasure\n& Revenue", '#D1FAE5', '#059669', '#065F46')
    ]

    for idx, (time_lbl, stage_lbl, bg_c, border_c, text_c) in enumerate(stages):
        x = 0.035 + idx * 0.138
        y = 0.5
        box = patches.FancyBboxPatch((x, y - 0.32), 0.12, 0.64, boxstyle="round,pad=0.02",
                                    fc=bg_c, ec=border_c, lw=2.0)
        ax.add_patch(box)
        # Time badge
        time_badge = patches.FancyBboxPatch((x + 0.015, y + 0.14), 0.09, 0.12, boxstyle="round,pad=0.01",
                                           fc=border_c, ec=border_c)
        ax.add_patch(time_badge)
        ax.text(x + 0.06, y + 0.20, time_lbl, ha='center', va='center', fontsize=8, fontweight='bold', color='#FFFFFF')
        ax.text(x + 0.06, y - 0.08, stage_lbl, ha='center', va='center', fontsize=8, fontweight='bold', color=text_c)

        if idx < len(stages) - 1:
            ax.annotate('', xy=(x + 0.136, y), xytext=(x + 0.122, y),
                        arrowprops=dict(facecolor='#64748B', edgecolor='#64748B', arrowstyle="->", lw=1.6))

    plt.tight_layout()
    chart6_path = os.path.join(ASSETS_DIR, "presentation_flowchart_vibrant.png")
    plt.savefig(chart6_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    print("[+] All vibrant charts generated successfully!")
    return {
        "chart1": chart1_path,
        "chart2": chart2_path,
        "chart3": chart3_path,
        "chart4": chart4_path,
        "chart5": chart5_path,
        "chart6": chart6_path
    }


# =============================================================================
# 2. WORD DOCUMENT COLORFUL STYLING UTILITIES
# =============================================================================

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
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

def set_cell_left_border(cell, color_hex="2563EB", sz="36"):
    """Adds a thick colored left border like modern UI blockquotes."""
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color_hex}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

def set_table_borders_none(tbl):
    """Removes standard grid lines so custom backgrounds stand out."""
    tblPr = tbl._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="none"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
                <w:insideH w:val="none"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr[0].append(borders)


# =============================================================================
# 3. BUILD THE VIBRANT MASTER WORD DOCUMENT
# =============================================================================

def build_vibrant_docx(charts):
    print("[*] Assembling vibrant, colorful Microsoft Word (.docx) presentation...")
    doc = docx.Document()

    # Configure Margins
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    # Global Color Constants
    NAVY = RGBColor(15, 23, 42)
    WHITE = RGBColor(255, 255, 255)
    BLUE = RGBColor(37, 99, 235)
    CYAN = RGBColor(8, 145, 178)
    PURPLE = RGBColor(124, 58, 237)
    EMERALD = RGBColor(5, 150, 105)
    AMBER = RGBColor(217, 119, 6)
    ROSE = RGBColor(225, 29, 72)
    DARK_TEXT = RGBColor(30, 41, 59)
    SLATE = RGBColor(100, 116, 139)

    # ---------------------------------------------------------
    # HERO BANNER COVER (Vibrant Dark Navy & Cyan Card)
    # ---------------------------------------------------------
    hero_tbl = doc.add_table(rows=1, cols=1)
    hero_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hero_cell = hero_tbl.cell(0, 0)
    hero_cell.width = Inches(6.8)
    set_cell_background(hero_cell, "0B132B")  # Deep Midnight Navy
    set_cell_margins(hero_cell, top=260, bottom=260, left=240, right=240)
    set_cell_left_border(hero_cell, color_hex="06B6D4", sz="48")  # Cyan left bar

    hp = hero_cell.paragraphs[0]
    hp.paragraph_format.space_before = Pt(4)
    hp.paragraph_format.space_after = Pt(4)

    # Badge Pill
    r_badge = hp.add_run("⚡ INSTITUTIONAL CLIENT PRESENTATION & SYSTEM DOSSIER  |  VERSION 2.5\n")
    r_badge.font.name = "Arial"
    r_badge.font.size = Pt(9.5)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(56, 189, 248)  # Sky Cyan

    # Main Brand Title
    r_title = hp.add_run("CREDITFIT 360™\n")
    r_title.font.name = "Arial Black"
    r_title.font.size = Pt(28)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle
    r_sub = hp.add_run("The Borrower-First Financial Intelligence & Reverse Underwriting Operating System\n")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(253, 224, 71)  # Warm Gold Accent

    # Tagline
    r_desc = hp.add_run("Reverse Underwriting Matrix  •  RBI CEPC 2023-24 Statutory Defense  •  DPDP Act 2023 Shield")
    r_desc.font.name = "Calibri"
    r_desc.font.size = Pt(10)
    r_desc.font.italic = True
    r_desc.font.color.rgb = RGBColor(203, 213, 225)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Colorful Metadata Grid Table
    meta_tbl = doc.add_table(rows=2, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_cards = [
        ("🚀 PLATFORM STATUS", "Active Localhost Server (Port 5000 / Auto-Failover)", "EFF6FF", "1D4ED8"),
        ("⚡ 1-CLICK DEMO ACCESS", "demo@creditfit360.com  /  Demo@123 (OTP: 123456)", "F0FDF4", "047857"),
        ("🎯 PREPARED FOR", "Corporate Clients, Strategic Partners, Investors & Evaluators", "FAF5FF", "6D28D9"),
        ("🛡️ REGULATORY COMPLIANCE", "RBI CEPC/2023-24 (₹100/day) & DPDP Act 2023 Certified", "FEF2F2", "B91C1C")
    ]

    for idx, (head, val, bg, border_c) in enumerate(meta_cards):
        r_idx = idx // 2
        c_idx = idx % 2
        cell = meta_tbl.cell(r_idx, c_idx)
        cell.width = Inches(3.35)
        set_cell_background(cell, bg)
        set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
        set_cell_left_border(cell, color_hex=border_c, sz="30")

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r_h = p.add_run(f"{head}\n")
        r_h.font.bold = True
        r_h.font.size = Pt(8.5)
        r_h.font.color.rgb = RGBColor(int(border_c[:2], 16), int(border_c[2:4], 16), int(border_c[4:], 16))

        r_v = p.add_run(val)
        r_v.font.size = Pt(9)
        r_v.font.color.rgb = NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # Helper function for vibrant section headers
    def add_vibrant_section_header(num, title, color_hex="2563EB", text_rgb=BLUE):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.8)
        set_cell_background(cell, f"{color_hex}15")  # 15% tint
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        set_cell_left_border(cell, color_hex=color_hex, sz="40")

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r_num = p.add_run(f"SECTION {num:02d} — ")
        r_num.font.name = "Arial Black"
        r_num.font.size = Pt(12)
        r_num.font.bold = True
        r_num.font.color.rgb = text_rgb

        r_title = p.add_run(title.upper())
        r_title.font.name = "Arial"
        r_title.font.size = Pt(12)
        r_title.font.bold = True
        r_title.font.color.rgb = NAVY

        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    def add_vibrant_callout(text, title="KEY STRATEGIC TAKEAWAY", color_hex="2563EB", bg_hex="EFF6FF"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.8)
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
        set_cell_left_border(cell, color_hex=color_hex, sz="36")

        cp = cell.paragraphs[0]
        cp.paragraph_format.space_after = Pt(2)
        c_title = cp.add_run(f"📌 {title}: ")
        c_title.font.bold = True
        c_title.font.size = Pt(9.5)
        c_title.font.color.rgb = RGBColor(int(color_hex[:2], 16), int(color_hex[2:4], 16), int(color_hex[4:], 16))

        c_body = cp.add_run(text)
        c_body.font.size = Pt(9.5)
        c_body.font.color.rgb = NAVY

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_image_with_caption(img_path, caption):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.4))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(12)
        run_cap = p_cap.add_run(f"Figure: {caption}")
        run_cap.font.size = Pt(8.5)
        run_cap.font.bold = True
        run_cap.font.color.rgb = SLATE

    # =========================================================================
    # SECTION 1: THE REAL MARKET NEED & URGENCY
    # =========================================================================
    add_vibrant_section_header(1, "The Real Market Need, Market Size & Opportunity", "2563EB", BLUE)

    p = doc.add_paragraph()
    p.add_run(
        "Is there an actual need for CreditFit 360 in the market? The answer is an unequivocal YES. "
        "India's consumer and small business lending markets are experiencing exponential growth, yet the "
        "system remains plagued by severe information asymmetry. Existing fintech platforms (CRED, Paisabazaar, "
        "BankBazaar) operate as commercial brokers—they get paid commissions when users borrow more money. "
        "Consequently, there is no major platform exclusively defending the borrower."
    )

    add_image_with_caption(charts["chart1"], "Paradigm Comparison: Legacy Loan Brokers vs. CreditFit 360 Borrower Defense Suite")

    add_vibrant_callout(
        "CreditFit 360 transforms credit from a passive, score-checking gimmick into an actionable, "
        "reverse-engineered financial defense system with statutory enforcement rights under the Reserve Bank of India.",
        "THE PARADIGM SHIFT", "059669", "ECFDF5"
    )

    p2 = doc.add_paragraph()
    p2.add_run("The 4 Critical Market Inefficiencies Driving Unprecedented Demand:")
    p2.runs[0].font.bold = True
    p2.runs[0].font.color.rgb = NAVY

    inefficiencies = [
        ("1. The Credit Opacity Problem (68% Blind Rejections)",
         "Over 68% of Indian loan applicants who face rejection have no idea why. Banks do not evaluate credit score in a vacuum; they evaluate FOIR (Fixed Obligation to Income Ratio), credit mix, and inquiry velocity—metrics consumer apps never expose.", "2563EB"),

        ("2. The 'Hard Inquiry' Spiral of Death",
         "When a borrower faces rejection, they panic-apply to 3 or 4 other lenders in quick succession. Each application triggers a 'hard pull' on CIBIL/Experian, knocking 15–30 points off their score and locking them into subprime rates.", "DC2626"),

        ("3. The Unenforced RBI ₹100/Day Statutory Penalty (99% Unclaimed)",
         "Under RBI Master Direction CEPC/2023-24, banks and credit bureaus must resolve credit report errors within 30 days. If they fail, they are legally obligated to pay ₹100 per day of delay. Over 99% of Indian citizens are unaware of this statutory right.", "D97706"),

        ("4. The $300B MSME Credit Gap",
         "Over 63 million MSMEs face a $300B debt deficit because legacy bank underwriting looks for vintage bureau records rather than actual operating cash flow, GST returns, and supplier invoice regularities.", "7C3AED")
    ]

    for title, desc, col in inefficiencies:
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.cell(0, 0)
        c.width = Inches(6.8)
        set_cell_background(c, "F8FAFC")
        set_cell_margins(c, top=80, bottom=80, left=140, right=140)
        set_cell_left_border(c, color_hex=col, sz="28")

        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        rt = p.add_run(f"• {title}: ")
        rt.font.bold = True
        rt.font.size = Pt(9)
        rt.font.color.rgb = RGBColor(int(col[:2], 16), int(col[2:4], 16), int(col[4:], 16))

        rd = p.add_run(desc)
        rd.font.size = Pt(8.5)
        rd.font.color.rgb = DARK_TEXT

        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    add_image_with_caption(charts["chart3"], "Empirical Market Opportunity: Retail Borrowers, MSME Gap ($300B), and Unenforced Rights")

    # =========================================================================
    # SECTION 2: TARGET AUDIENCE & BUYER PERSONA MATRIX
    # =========================================================================
    add_vibrant_section_header(2, "Target Audience & Customer Segmentation Matrix", "059669", EMERALD)

    p = doc.add_paragraph()
    p.add_run(
        "CreditFit 360 solves distinct, urgent financial problems across a diverse, multi-billion-dollar audience spectrum:"
    )

    aud_table = doc.add_table(rows=7, cols=3)
    aud_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    aud_headers = ["Target Segment", "Specific Persona", "Why They Desperately Need CreditFit 360"]
    for j, h in enumerate(aud_headers):
        cell = aud_table.cell(0, j)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = WHITE

    aud_data = [
        ("1. Pre-Loan Retail Borrowers", "Salaried professionals planning Home, Auto, or Personal Loans", "Simulates approval odds beforehand with ZERO hard inquiries, locking in prime interest rates."),
        ("2. Loan Rejection Victims", "Borrowers rejected by banks in the last 90 days", "Diagnoses exact mathematical failure points (e.g. FOIR > 50%) and provides an actionable paydown roadmap."),
        ("3. Bank Error Dispute Victims", "Borrowers with wrong defaults, phantom loans, or bureau delays", "Computes statutory ₹100/day delay compensation and produces ready-to-dispatch legal grievance notices."),
        ("4. MSMEs & Sole Proprietors", "Small business owners, retailers, and GST traders", "Alternative multi-factor cash-flow credit scoring bypassing vintage balance-sheet constraints."),
        ("5. Loan DSAs & Agents", "Direct Selling Agents and loan intermediaries", "Generates verified institutional dossiers to pre-qualify leads and eliminate bank branch rejections."),
        ("6. CAs & Wealth Advisors", "Chartered Accountants and financial consultants", "Institutional A4 client dossiers and A/B scenario testing tools for professional debt advisory.")
    ]

    for i, row in enumerate(aud_data):
        for j, val in enumerate(row):
            cell = aud_table.cell(i + 1, j)
            bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = BLUE
            else:
                r.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # SECTION 3: SYSTEM ARCHITECTURE & ENGINEERING DESIGN
    # =========================================================================
    add_vibrant_section_header(3, "Platform Architecture & Engineering Design", "7C3AED", PURPLE)

    p = doc.add_paragraph()
    p.add_run(
        "CreditFit 360 is built using a resilient, decoupled web application stack designed for rapid local execution, "
        "fault tolerance, and enterprise data governance:"
    )

    add_image_with_caption(charts["chart2"], "End-to-End Enterprise Platform Architecture & Secure Data Flow")

    arch_bullets = [
        ("Application Server", "Python 3.10+, Flask 3.1+ RESTful server with cryptographic session security.", "2563EB"),
        ("Persistence Engine", "Zero-dependency, thread-safe SQLite database (database.db) managed via db.py.", "D97706"),
        ("AI & Math Intelligence", "ai_engine.py with proprietary reverse-underwriting matrices and legal dispute compilers.", "7C3AED"),
        ("Frontend System", "Neon-Bento glassmorphic CSS design system with @media print clean A4 PDF layouts.", "059669"),
        ("Dedicated Runner", "server.py with automated port-collision resolution, LAN discovery, and auto-browser launch.", "0891B2")
    ]

    for t, d, c in arch_bullets:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        rt = p.add_run(f"• {t}: ")
        rt.font.bold = True
        rt.font.size = Pt(9)
        rt.font.color.rgb = RGBColor(int(c[:2], 16), int(c[2:4], 16), int(c[4:], 16))
        rd = p.add_run(d)
        rd.font.size = Pt(9)
        rd.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # SECTION 4: EXHAUSTIVE FUNCTION-BY-FUNCTION COLORFUL CARDS (ALL 15 MODULES)
    # =========================================================================
    add_vibrant_section_header(4, "Exhaustive Function-by-Function Breakdown: Why It Exists & What It Does", "E11D48", ROSE)

    p = doc.add_paragraph()
    p.add_run(
        "Every single feature in CreditFit 360 was engineered to solve a specific financial inefficiency. "
        "Below is the complete functional breakdown of all 15 modules:"
    )

    modules_full = [
        {
            "num": "01",
            "name": "Enterprise Authentication & 1-Click Demo Portal",
            "route": "/",
            "theme_hex": "2563EB",
            "why": "Complex registration forms cause 60%+ drop-off. Evaluators and clients need instant access without creating throwaway email accounts.",
            "what": "Secure tabbed authentication with a preloaded 1-Click Demo Login button populated with verified demo credentials.",
            "engine": "Werkzeug scrypt password hashing, session secret encryption, and instant session seeding (demo@creditfit360.com / Demo@123).",
            "output": "Instant user session authentication, personalized dashboard greeting, and simulator access."
        },
        {
            "num": "02",
            "name": "Financial Intelligence Command Center",
            "route": "/dashboard",
            "theme_hex": "7C3AED",
            "why": "Borrowers are paralyzed by disconnected numbers. They need a single executive dashboard prioritizing their debt risks.",
            "what": "Displays dynamic 0–100 CreditFit Health Index, risk tiering (Prime/Near-Prime/Subprime), FOIR debt ratio, and active warning banners.",
            "engine": "Weighted index factoring FOIR debt burden (35%), credit utilization (25%), emergency runway (20%), and repayment track record (20%).",
            "output": "Executive command center with real-time risk alerts (e.g. 'FOIR exceeds 45% ceiling', 'Emergency runway under 3 months')."
        },
        {
            "num": "03",
            "name": "Personal CreditFit Assessment Wizard",
            "route": "/personal-credit",
            "theme_hex": "0891B2",
            "why": "Standard bank loan forms are intimidating and complex. A guided 4-step wizard captures institutional metrics without cognitive overload.",
            "what": "Step-by-step wizard capturing Basic Info, Monthly Living Cash Flows, Bureau Credit Limits, and Liquid Emergency Reserves.",
            "engine": "Calculates net disposable income, fixed debt obligations, credit utilization percentages, and emergency runway months.",
            "output": "Comprehensive personal credit profile automatically synced into database.db."
        },
        {
            "num": "04",
            "name": "India Stack Account Aggregator (AA) Auto-Fill Sandbox",
            "route": "/personal-credit (Modal)",
            "theme_hex": "059669",
            "why": "Manual data entry takes 10+ minutes and leads to typos and abandoned applications. Users demand instant automated bank data retrieval.",
            "what": "Simulates RBI-regulated Account Aggregator (FIP/FIU) frameworks (HDFC, SBI, ICICI) to pull verified salary, debt, and balance data in 3 seconds.",
            "engine": "OTP simulation ('123456') validating user consent and auto-populating 18 form fields across all 4 stages of the wizard.",
            "output": "Zero-friction 3-second auto-population of verified bank data demonstrating India Stack production readiness."
        },
        {
            "num": "05",
            "name": "SME CreditScore Multi-Factor Engine",
            "route": "/sme-credit-score",
            "theme_hex": "D97706",
            "why": "Over 63 million MSMEs lack audited balance sheets and get unfairly rejected by retail scoring algorithms.",
            "what": "Dedicated alternative underwriting engine for small businesses and sole proprietorships evaluating non-bureau cash-flow data.",
            "engine": "Multi-dimensional scoring model analyzing operational vintage, profit margin consistency, vendor invoice discipline, and working capital buffers.",
            "output": "SME Creditworthiness Score (0–100), operating stability rating, and recommended working capital limits."
        },
        {
            "num": "06",
            "name": "Reverse Underwriting Suite",
            "route": "/defense-suite (Tab 1)",
            "theme_hex": "E11D48",
            "why": "Applying blindly for a loan damages credit scores through hard inquiries. Borrowers must test bank approval odds BEFORE applying.",
            "what": "Stress-tests requested loan amount, proposed interest rate, and tenure against the applicant's existing debt-to-income limits.",
            "engine": "Evaluates resulting EMI against the standard 50% FOIR regulatory cap; models Tier-1 bank credit committee policies.",
            "output": "Exact approval odds and specific restorative instructions (e.g. 'Pay off ₹45,000 in credit card debt to bring FOIR below 50%')."
        },
        {
            "num": "07",
            "name": "RBI Statutory Penalty Enforcer & Legal Notice Generator",
            "route": "/defense-suite (Tab 2)",
            "theme_hex": "DC2626",
            "why": "Banks and credit bureaus routinely delay resolving credit report disputes for months. 99% of consumers do not know they are entitled to ₹100/day compensation.",
            "what": "Calculates mandatory statutory delay compensation under RBI Master Circular CEPC/2023-24 and generates a formal ready-to-dispatch legal grievance notice.",
            "engine": "Statutory calculation: Max(0, (Elapsed Days - 30) * ₹100/day); drafts legal notice citing Section 21 of the Credit Information Companies (Regulation) Act, 2005.",
            "output": "Total accrued statutory claim in INR, ready-to-print legal grievance notice, and dispute persistence in database.db."
        },
        {
            "num": "08",
            "name": "Institutional Loan Readiness Dossier & Verification ID",
            "route": "/dossier",
            "theme_hex": "2563EB",
            "why": "Borrowers walking into banks without structured documentation get unfavorable interest rates or delayed processing. They need an official, verified financial summary.",
            "what": "Executive financial dossier featuring a unique cryptographic verification ID (e.g. CF360-IND-202610-8921), max loan capacity, and bank pre-approval odds.",
            "engine": "Calculates maximum sanctionable loan under 50% FOIR ceiling over 60 months at prime interest rates.",
            "output": "Institutional dossier suitable for presentation to bank loan managers and NBFC credit officers."
        },
        {
            "num": "09",
            "name": "1-Click Clean A4 PDF Export",
            "route": "/dossier (Print Action)",
            "theme_hex": "059669",
            "why": "Converting web pages into client-ready documents usually results in broken layouts, cut-off tables, and visible website buttons.",
            "what": "High-fidelity, print-optimized A4 document rendering using dedicated @media print CSS rules.",
            "engine": "Automated CSS print engine that strips web navigation, buttons, and dark backgrounds, applying formal document typography and watermarks.",
            "output": "Flawless, institutional A4 PDF ready for formal bank submission or digital sharing."
        },
        {
            "num": "10",
            "name": "FitAI Financial Co-Pilot",
            "route": "/assistant",
            "theme_hex": "7C3AED",
            "why": "Borrowers need instant, personalized answers to complex financial questions without paying expensive advisory fees.",
            "what": "Natural language AI financial assistant that synchronizes with the user's active session data to deliver context-aware financial guidance.",
            "engine": "ai_engine.py contextual query engine with pre-programmed regulatory frameworks and prompt-chip accelerators.",
            "output": "Conversational, tailored financial advice directly addressing the user's FOIR, credit score, and debt capacity."
        },
        {
            "num": "11",
            "name": "MoneyMap Cash Flow Visualizer",
            "route": "/moneymap",
            "theme_hex": "0891B2",
            "why": "Most consumers do not understand where their monthly salary disappears, leading to accidental loan default risks.",
            "what": "Visualizes monthly income flow across Fixed EMIs, Essential Living Expenses, Discretionary Costs, and Net Liquid Surplus.",
            "engine": "Cash-flow allocation engine categorizing monthly debits into structured financial health buckets.",
            "output": "Clear visual breakdown highlighting overspending areas and liquid surplus available for loan repayment."
        },
        {
            "num": "12",
            "name": "Financial Decision Lab",
            "route": "/decision-lab",
            "theme_hex": "D97706",
            "why": "Borrowers face difficult financial dilemmas (e.g., prepay home loan vs. invest in mutual funds) and have no mathematical tools to compare outcomes.",
            "what": "A/B scenario testing engine that projects the 10-to-20-year net-wealth outcome of competing financial decisions.",
            "engine": "Compound interest and amortization calculation engine factoring inflation, interest savings, and investment returns.",
            "output": "Side-by-side comparison tables and graphs showing total wealth difference between options."
        },
        {
            "num": "13",
            "name": "What-If FinTwin 12-Month Simulator",
            "route": "/what-if-simulator",
            "theme_hex": "E11D48",
            "why": "Consumers hesitate to make financial moves because they cannot predict how it will affect their credit score.",
            "what": "Interactive digital twin simulator with sliders allowing users to simulate debt paydowns, card closures, or new credit to forecast score trajectory.",
            "engine": "Dynamic credit score simulation model projecting monthly score changes over a 12-month horizon.",
            "output": "Interactive score trajectory line chart showing projected score improvements based on simulated user actions."
        },
        {
            "num": "14",
            "name": "Wealth Path Milestone Planner",
            "route": "/wealth-path",
            "theme_hex": "059669",
            "why": "Borrowers need a structured, inflation-adjusted plan to accumulate down payments for home or business asset purchases.",
            "what": "Goal-based milestone planner that calculates required monthly SIP contributions to reach specific capital goals.",
            "engine": "Future-value capitalization formula with user-defined target date and expected annual rate of return.",
            "output": "Clear milestone roadmap with recommended monthly savings targets and timeline projections."
        },
        {
            "num": "15",
            "name": "DPDP Act 2023 Privacy & Governance Center",
            "route": "/privacy-consent-center",
            "theme_hex": "0F172A",
            "why": "Fintechs failing to comply with India's DPDP Act 2023 face statutory penalties up to ₹250 Crores. Users demand verifiable data control.",
            "what": "Enterprise data governance center featuring Section 6 consent audit trails, Section 12 data portability, and Section 12 Right to Erasure.",
            "engine": "Immutable SQLite consent table, automated JSON data exporter, and irreversible user-record purge API.",
            "output": "Verified consent audit log, downloadable JSON personal dossier, and verified 1-click complete data erasure."
        }
    ]

    for mod in modules_full:
        c_hex = mod["theme_hex"]
        tbl_mod = doc.add_table(rows=5, cols=2)
        tbl_mod.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Row 0: Full-Width Colored Header Bar
        cell_hdr = tbl_mod.cell(0, 0)
        cell_hdr.merge(tbl_mod.cell(0, 1))
        set_cell_background(cell_hdr, c_hex)
        set_cell_margins(cell_hdr, top=100, bottom=100, left=140, right=140)

        p_h = cell_hdr.paragraphs[0]
        p_h.paragraph_format.space_before = Pt(2)
        p_h.paragraph_format.space_after = Pt(2)
        r_mh = p_h.add_run(f"MODULE {mod['num']}: {mod['name'].upper()} ({mod['route']})")
        r_mh.font.name = "Arial Black"
        r_mh.font.size = Pt(9.5)
        r_mh.font.color.rgb = WHITE

        # Rows 1 to 4: Structured Info
        rows_data = [
            ("🎯 WHY IT IS NEEDED IN MARKET", mod["why"], "FFF1F2", "E11D48"),
            ("⚡ WHAT IT ACTUALLY DOES", mod["what"], "EFF6FF", "2563EB"),
            ("🔬 UNDERLYING ENGINE / FORMULA", mod["engine"], "F8FAFC", "475569"),
            ("🏆 TANGIBLE OUTPUT / VALUE", mod["output"], "F0FDF4", "059669")
        ]

        for r_i, (label, text, bg, border_c) in enumerate(rows_data):
            c0 = tbl_mod.cell(r_i + 1, 0)
            c1 = tbl_mod.cell(r_i + 1, 1)
            c0.width = Inches(2.2)
            c1.width = Inches(4.6)
            set_cell_background(c0, bg)
            set_cell_background(c1, "FFFFFF" if r_i % 2 == 0 else "F8FAFC")
            set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
            set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
            set_cell_left_border(c0, color_hex=border_c, sz="24")

            p0 = c0.paragraphs[0]
            p0.paragraph_format.space_before = Pt(2)
            p0.paragraph_format.space_after = Pt(2)
            r0 = p0.add_run(label)
            r0.font.bold = True
            r0.font.size = Pt(8)
            r0.font.color.rgb = RGBColor(int(border_c[:2], 16), int(border_c[2:4], 16), int(border_c[4:], 16))

            p1 = c1.paragraphs[0]
            p1.paragraph_format.space_before = Pt(2)
            p1.paragraph_format.space_after = Pt(2)
            r1 = p1.add_run(text)
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = DARK_TEXT

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Insert Visual FOIR & RBI Compounding Charts
    add_image_with_caption(charts["chart4"], "Reverse Underwriting Matrix: FOIR Sanction Probability Curves and Safe Ceilings")
    add_image_with_caption(charts["chart5"], "RBI Statutory Penalty Timeline: Compounding Delayed-Dispute Legal Claims (CEPC/2023-24)")

    # =========================================================================
    # SECTION 5: STEP-BY-STEP 7-MINUTE CLIENT PRESENTATION SCRIPT
    # =========================================================================
    add_vibrant_section_header(5, "Step-by-Step 7-Minute Live Client Presentation Script", "D97706", AMBER)

    p = doc.add_paragraph()
    p.add_run(
        "Follow this exact minute-by-minute script during your client pitch or investor demo to ensure a compelling, "
        "high-conversion presentation:"
    )

    add_image_with_caption(charts["chart6"], "7-Minute High-Impact Client Presentation Roadmap & Demonstration Stages")

    demo_steps = [
        ("Minute 1: The Hook & Market Problem",
         "What to Say: 'Good morning. In India today, over 150 million consumers and 60 million MSMEs interact with credit. But when they apply for a loan, they enter a total black box. Platforms like CRED or Paisabazaar are essentially loan distribution agents—they get paid when you borrow more. Nobody is in the borrower's corner. We created CreditFit 360 to be India's first Borrower Defense and Reverse-Underwriting Operating System.'",
         "Action on Screen: Open http://localhost:5000 in your browser; show the sleek landing page.", "2563EB"),

        ("Minute 2: 1-Click Sign-In & Command Dashboard",
         "What to Say: 'Let's enter the platform. We have built-in zero-friction access. With our 1-Click Demo Login, we instantly enter the Executive Dashboard. Rather than just showing a vanity 3-digit score, CreditFit 360 surfaces FOIR limits, emergency runway months, and predictive risk flags that bank credit managers actually evaluate.'",
         "Action on Screen: Click '⚡ 1-Click Demo Login'. Point to the dynamic Health Score gauge and active warning banners.", "4F46E5"),

        ("Minute 3: Account Aggregator (AA) Auto-Fill Sandbox",
         "What to Say: 'Normally, filling a 20-field financial form causes users to drop off. Watch this: we integrate with India's RBI Account Aggregator framework. The user chooses their bank, enters their mobile number, and confirms simulated OTP 123456. Instantly, our system securely pulls verified salary credits, existing EMIs, and liquid reserves, auto-filling all four stages of the underwriting engine in seconds.'",
         "Action on Screen: Navigate to 'Personal CreditFit' -> Click '🏦 Connect Bank via AA' -> Select Bank -> Click Send OTP -> Enter '123456' -> Click Verify & Auto-Fill.", "7C3AED"),

        ("Minute 4: Reverse Underwriting Engine",
         "What to Say: 'Here is where CreditFit 360 protects the consumer. Instead of submitting a loan application and triggering a score-damaging hard inquiry, our Reverse Underwriter stress-tests the applicant's profile against Tier-1 bank credit committee policies. If the FOIR is too high, it advises them on the exact amount of debt to pay off first to guarantee approval.'",
         "Action on Screen: Navigate to 'Defense & Approval' -> 'Reverse Underwriting'. Enter a loan amount (e.g. ₹25,00,000) and click 'Run Reverse Simulation'. Point to the odds and recommendations.", "DB2777"),

        ("Minute 5: RBI Statutory Compensation Enforcer",
         "What to Say: 'This is our standout regulatory defense feature. Under RBI Circular CEPC/2023-24, banks must resolve credit report disputes within 30 days. If they fail, they owe the borrower ₹100 per day. Here, the borrower enters their dispute date, and CreditFit 360 computes the statutory penalty and produces a ready-to-dispatch legal notice under Section 21 of the CIC Act.'",
         "Action on Screen: Click the 'Statutory Defense & RBI Notice' tab. Enter a past date (e.g., 60 days ago) and click 'Calculate Statutory Penalty'. Show the legal letter and claim amount.", "DC2626"),

        ("Minute 6: Official Loan Readiness Dossier & Clean PDF Export",
         "What to Say: 'When a borrower is ready to apply, they don't walk into a bank empty-handed. CreditFit 360 generates this Institutional Loan Readiness Dossier, complete with verification ID, FOIR stress metrics, and bank approval probabilities. With a single click, it prints into a clean, professional A4 PDF.'",
         "Action on Screen: Click '📑 Export Dossier (PDF)' in the navigation bar. Show the formal A4 layout. Click 'Print / Save as PDF' to demonstrate clean export.", "D97706"),

        ("Minute 7: DPDP Act Privacy Governance & Business Scalability",
         "What to Say: 'Finally, we take compliance seriously. Under India's Digital Personal Data Protection Act 2023, users can view their immutable consent audit trail, download their full data package, or execute the Right to Erasure to permanently purge their database records. As a business, CreditFit 360 monetizes via B2C subscriptions (₹399/yr), B2B SaaS licenses for CAs and Loan Agents (₹1,499/mo), and qualified lender referral payouts. Thank you.'",
         "Action on Screen: Navigate to '🛡️ DPDP Privacy Center'. Show the consent log and click 'Export My Personal Data (JSON)'. Conclude the presentation.", "059669")
    ]

    for title, speech, action, col_hex in demo_steps:
        tbl_s = doc.add_table(rows=2, cols=1)
        tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_top = tbl_s.cell(0, 0)
        c_bot = tbl_s.cell(1, 0)
        c_top.width = Inches(6.8)
        c_bot.width = Inches(6.8)

        set_cell_background(c_top, f"{col_hex}15")
        set_cell_background(c_bot, "FFFFFF")
        set_cell_margins(c_top, top=80, bottom=80, left=120, right=120)
        set_cell_margins(c_bot, top=80, bottom=80, left=120, right=120)
        set_cell_left_border(c_top, color_hex=col_hex, sz="30")
        set_cell_left_border(c_bot, color_hex=col_hex, sz="30")

        # Top Header
        p_th = c_top.paragraphs[0]
        p_th.paragraph_format.space_before = Pt(2)
        p_th.paragraph_format.space_after = Pt(2)
        r_th = p_th.add_run(f"▶ {title.upper()}")
        r_th.font.name = "Arial Black"
        r_th.font.size = Pt(9.5)
        r_th.font.color.rgb = RGBColor(int(col_hex[:2], 16), int(col_hex[2:4], 16), int(col_hex[4:], 16))

        # Bottom Body
        p_tb = c_bot.paragraphs[0]
        p_tb.paragraph_format.space_before = Pt(2)
        p_tb.paragraph_format.space_after = Pt(2)
        r_sp_lbl = p_tb.add_run("💬 WHAT TO SAY: ")
        r_sp_lbl.font.bold = True
        r_sp_lbl.font.size = Pt(8.5)
        r_sp_lbl.font.color.rgb = NAVY

        r_sp_txt = p_tb.add_run(f"{speech.replace('What to Say: ', '')}\n\n")
        r_sp_txt.font.size = Pt(8.5)
        r_sp_txt.font.color.rgb = DARK_TEXT

        r_ac_lbl = p_tb.add_run("👉 LIVE DEMO ACTION: ")
        r_ac_lbl.font.bold = True
        r_ac_lbl.font.size = Pt(8.5)
        r_ac_lbl.font.color.rgb = EMERALD

        r_ac_txt = p_tb.add_run(action.replace('Action on Screen: ', ''))
        r_ac_txt.font.size = Pt(8.5)
        r_ac_txt.font.bold = True
        r_ac_txt.font.color.rgb = NAVY

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # SECTION 6: COMMERCIAL MONETIZATION & BUSINESS SCALABILITY
    # =========================================================================
    add_vibrant_section_header(6, "Commercial Viability, Revenue Models & Business Scalability", "0D9488", CYAN)

    p = doc.add_paragraph()
    p.add_run(
        "CreditFit 360 features a diversified, highly lucrative revenue model spanning high-volume B2C subscriptions, "
        "recurring B2B professional SaaS, and high-ticket institutional lender referral fees:"
    )

    rev_table = doc.add_table(rows=4, cols=4)
    rev_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rev_headers = ["Revenue Stream", "Target Market", "Pricing Model", "Core Value Proposition"]
    for j, h in enumerate(rev_headers):
        cell = rev_table.cell(0, j)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = WHITE

    rev_data = [
        ("B2C Premium Defense", "Retail Borrowers & Salaried Individuals", "₹399/year or ₹49/month", "Auto-dispute letter generator, RBI statutory compensation tracker, unlimited What-If simulations."),
        ("B2B SaaS for CAs & DSAs", "Direct Selling Agents, Loan Brokers, Accounting Firms", "₹1,499/month per license", "Client loan readiness assessment dossiers, pre-qualification stress tests, rejection-prevention tools."),
        ("Pre-Underwritten Referral Marketplace", "Tier-2 & Tier-3 NBFCs and Digital Lenders", "1.0% – 1.8% of loan sanction value", "Routing pre-vetted applicants whose FOIR and credit profiles match exact lender underwriting criteria.")
    ]

    for i, row in enumerate(rev_data):
        for j, val in enumerate(row):
            cell = rev_table.cell(i + 1, j)
            bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=90, bottom=90, left=110, right=110)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = BLUE
            else:
                r.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # SECTION 7: TOUGH CLIENT Q&A AND OBJECTION DEFENSE
    # =========================================================================
    add_vibrant_section_header(7, "Tough Client Q&A and Objection Defense Guide", "E11D48", ROSE)

    qa_list = [
        ("Q1: How does CreditFit 360 differ from CRED or Paisabazaar?",
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
        r_q.font.size = Pt(9.5)
        r_q.font.color.rgb = BLUE

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(6)
        r_a = p_a.add_run(a)
        r_a.font.size = Pt(9)
        r_a.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SECTION 8: LOCALHOST OPERATIONS MANUAL
    # =========================================================================
    add_vibrant_section_header(8, "Production Local Server Operations Manual", "475569", SLATE)

    ops_steps = [
        ("One-Click Launch (Windows Explorer)", "Double-click 'run_server.bat' or 'start_localhost.bat' in the project folder. The script automatically verifies Python in PATH, installs dependencies, starts the server, and opens your default browser."),
        ("Terminal Command Launch", "Run 'python server.py' from PowerShell or Command Prompt. Optional flags include '--port 8080' (custom port) or '--no-browser' (headless mode)."),
        ("Automatic Port Collision Protection", "If port 5000 is occupied by another application, server.py automatically detects the conflict and binds to the next available port (e.g. 5001) without crashing."),
        ("LAN / Mobile Phone Testing", "server.py automatically identifies your machine's local Wi-Fi IP address (e.g., http://192.168.1.4:5000), allowing seamless multi-device testing from a smartphone on the same network.")
    ]

    for t, d in ops_steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(f"• {t}: ")
        r_t.font.bold = True
        r_t.font.size = Pt(9)
        r_t.font.color.rgb = NAVY

        r_d = p.add_run(d)
        r_d.font.size = Pt(9)
        r_d.font.color.rgb = DARK_TEXT

    # Save to disk as the Vibrant Edition (to prevent collision with open Word file)
    vibrant_docx_path = os.path.join(PROJECT_ROOT, "CreditFit_360_Master_Presentation_VIBRANT_EDITION.docx")
    doc.save(vibrant_docx_path)
    print(f"[+] Vibrant Master Document successfully saved at: {vibrant_docx_path}")

    # Also try to overwrite the original if not locked
    orig_path = os.path.join(PROJECT_ROOT, "CreditFit_360_Master_Client_Report.docx")
    try:
        doc.save(orig_path)
        print(f"[+] Also updated original file at: {orig_path}")
    except PermissionError:
        print("[!] Original file is open in MS Word. Saved vibrant edition as separate file.")

    return vibrant_docx_path


if __name__ == "__main__":
    charts = generate_vibrant_charts()
    docx_file = build_vibrant_docx(charts)
    print("All tasks finished successfully!")
