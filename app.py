import streamlit as st
from fpdf import FPDF
import pandas as pd
from datetime import datetime

# Page Configuration (Light Mode / Wide Layout)
st.set_page_config(
    page_title="JSP DataClean PDF & Excel Tools",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional Light Mode CSS Styling (Clean White & High Contrast)
st.markdown("""
    <style>
    /* Safe Clean White Background */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    /* Custom Text Areas for optimal light contrast */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-family: monospace !important;
        font-size: 14px !important;
    }
    .stTextArea textarea:focus {
        border-color: #16a34a !important;
        box-shadow: 0 0 8px rgba(22, 163, 74, 0.2) !important;
    }

    /* High-impact Action Button */
    .stButton button {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
        border: 1px solid #16a34a;
        width: 100%;
        padding: 11px;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        border-color: #15803d;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'uses_left' not in st.session_state:
    st.session_state.uses_left = 2
if 'plan_type' not in st.session_state:
    st.session_state.plan_type = "Free"
if 'quota_left' not in st.session_state:
    st.session_state.quota_left = 0
if 'run_clicked' not in st.session_state:
    st.session_state.run_clicked = False

# JSP Corporate Header (Light Clean Mode Container)
st.markdown("""
    <div style="display: flex; align-items: center; background: #ffffff; padding: 20px 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div style="background: #0f172a; color: #ffffff; font-weight: 900; padding: 12px 18px; border-radius: 8px; font-size: 20px; margin-right: 20px; letter-spacing: 1.5px; display: flex; align-items: center; gap: 8px;">
            <span style="color: #22c55e;">●</span> JSP
        </div>
        <div>
            <div style="font-size: 22px; font-weight: 800; color: #0f172a; letter-spacing: 0.8px;">JSP TECHNOLOGY</div>
            <div style="font-size: 14px; color: #64748b; margin-top: 3px;">DataClean Utility Suite &bull; Global Professional Solutions</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("Clean text lists, remove duplicates, instantly format data, and export professional reports in **PDF** or **Excel**.")

# License & Plans Section (Using 100% Native Streamlit components)
with st.expander("🔑 JSP Plans & License Activation", expanded=(st.session_state.plan_type == "Free" and st.session_state.uses_left <= 0)):
    if st.session_state.plan_type != "Free":
        st.success(f"✅ **Active Plan: {st.session_state.plan_type}** | Operations Left: {st.session_state.quota_left}")
    else:
        st.info(f"💡 **Free Plan:** {st.session_state.uses_left} free uses remaining (Max 50 lines / 10,000 characters).")
        st.markdown("Need more power? Choose an option below:")
        st.markdown("- ☕ **Coffee Pass ($3):** 5 immediate operations (No subscription).")
        st.markdown("- 📅 **Monthly Pro ($9):** 20 operations/month.")
        st.markdown("- ⭐ **Annual Pro ($49):** 50 operations/month.")
        
        license_input = st.text_input("Enter License Key / Coffee Pass Code:", type="password", placeholder="Ex: JSP-COFFEE-XXXX")
        if st.button("Activate Code / Refill"):
            key = license_input.strip().upper()
            if key.startswith("JSP-COFFEE"):
                if st.session_state.plan_type == "Free":
                    st.session_state.plan_type = "Coffee Pass (5 Ops)"
                    st.session_state.quota_left = 5
                else:
                    st.session_state.quota_left += 5
                st.success("☕ Coffee Pass activated/refilled successfully (+5 operations added)!")
                st.rerun()
            elif key.startswith("JSP-MONTHLY"):
                st.session_state.plan_type = "Monthly Pro"
                st.session_state.quota_left = 20
                st.success("📅 Monthly Pro activated! 20 operations available.")
                st.rerun()
            elif key.startswith("JSP-ANNUAL"):
                st.session_state.plan_type = "Annual Pro"
                st.session_state.quota_left = 50
                st.success("⭐ Annual Pro activated! 50 operations available.")
                st.rerun()
            else:
                st.error("Invalid key. Please check your JSP Technology purchase receipt.")

st.markdown("---")

# Data Input Section
st.subheader("1. Paste your raw data or text below:")
raw_input_text = st.text_area(
    "Raw Data Input",
    height=180,
    placeholder="Paste your messy lists, emails, numbers, or unformatted text here...",
    label_visibility="collapsed"
)

# Cleaning Options (Filters)
st.subheader("2. Select Cleaning Options:")
col1, col2 = st.columns(2)
with col1:
    remove_dups = st.checkbox("Remove Duplicate Lines", value=True)
    remove_empty = st.checkbox("Remove Empty Lines", value=True)
with col2:
    trim_spaces = st.checkbox("Trim Extra Spaces", value=True)
    sort_alpha = st.checkbox("Sort Alphabetically", value=False)

st.markdown("---")

# Explicit Execution Button
run_button = st.button("⚡ Run Data Cleaning & Formatting")

if run_button:
    st.session_state.run_clicked = True

# Text Processing Function
def clean_text(text, dups, empty, trim, sort):
    if not text:
        return ""
    lines = text.splitlines()
    
    if trim:
        lines = [line.strip() for line in lines]
    if empty:
        lines = [line for line in lines if line != ""]
    if dups:
        seen = set()
        unique_lines = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        lines = unique_lines
    if sort:
        lines.sort()
        
    return "\n".join(lines)

# Processing and Result Display
if st.session_state.run_clicked:
    if not raw_input_text:
        st.warning("⚠️ Please paste some text into the box above before running.")
    else:
        lines_count = len(raw_input_text.splitlines())
        chars_count = len(raw_input_text)
        
        limit_exceeded = False
        error_message = ""
        
        if st.session_state.plan_type == "Free":
            if lines_count > 50:
                limit_exceeded = True
                error_message = f"⚠️ **Free Plan Limit Exceeded:** Your text has {lines_count} lines (maximum is 50). Get a **Coffee Pass ($3)** above to unlock larger batches."
            elif chars_count > 10000:
                limit_exceeded = True
                error_message = f"⚠️ **Free Plan Limit Exceeded:** Character limit of 10,000 reached."
            elif st.session_state.uses_left <= 0:
                limit_exceeded = True
                error_message = "🔒 **Free Limit Reached:** You have used your 2 free runs. Support our development by getting a **Coffee Pass ($3)** above!"
        else:
            if st.session_state.quota_left <= 0:
                limit_exceeded = True
                error_message = f"🔒 **Plan Quota Exhausted:** Your operations on the {st.session_state.plan_type} plan have ended. Enter a new Coffee Pass key above to refill instantly!"

        if limit_exceeded:
            st.error(error_message)
        else:
            processed_text = clean_text(raw_input_text, remove_dups, remove_empty, trim_spaces, sort_alpha)

            st.subheader("3. Cleaned Results Preview:")
            st.text_area("Processed Result", value=processed_text, height=180, label_visibility="collapsed")
            
            original_lines = len(raw_input_text.splitlines())
            final_lines = len(processed_text.splitlines()) if processed_text else 0
            st.caption(f"📊 Statistics: {original_lines} original lines processed -> {final_lines} clean lines ready.")

            if st.session_state.plan_type == "Free" and st.session_state.uses_left > 0:
                st.session_state.uses_left -= 1
            elif st.session_state.plan_type != "Free" and st.session_state.quota_left > 0:
                st.session_state.quota_left -= 1

            # Professional PDF Generation
            class PDF(FPDF):
                def header(self):
                    self.set_fill_color(15, 23, 42)
                    self.rect(10, 10, 15, 15, 'F')
                    self.set_font('Arial', 'B', 10)
                    self.set_text_color(34, 197, 94)
                    self.set_xy(10, 13.5)
                    self.cell(15, 8, 'JSP', 0, 0, 'C')

                    self.set_xy(28, 10)
                    self.set_font('Arial', 'B', 13)
                    self.set_text_color(15, 23, 42)
                    self.cell(100, 6, 'JSP TECHNOLOGY', 0, 1, 'L')
                    
                    self.set_xy(28, 16)
                    self.set_font('Arial', '', 8)
                    self.set_text_color(100, 116, 139)
                    self.cell(100, 4, 'DataClean Utility Suite | Certified Clean Report', 0, 1, 'L')
                    
                    self.set_draw_color(203, 213, 225)
                    self.set_line_width(0.6)
                    self.line(10, 28, 200, 28)
                    self.ln(12)

                def footer(self):
                    self.set_y(-20)
                    self.set_draw_color(203, 213, 225)
                    self.set_line_width(0.4)
                    self.line(10, 277, 200, 277)
                    
                    self.set_y(-15)
                    self.set_font('Arial', 'B', 8)
                    self.set_text_color(100, 116, 139)
                    self.cell(0, 5, 'Powered by JSP Technology - Global Digital Solutions', 0, 1, 'C')
                    
                    self.set_font('Arial', '', 7)
                    self.set_text_color(148, 163, 184)
                    self.cell(0, 4, f'Page {self.page_no()} | Secure Client-Side Processing', 0, 0, 'C')

            def create_pdf(text_content):
                pdf = PDF()
                pdf.add_page()
                
                pdf.set_font("Arial", 'B', 11)
                pdf.set_text_color(15, 23, 42)
                pdf.cell(0, 8, 'Processed Clean Data:', 0, 1, 'L')
                pdf.ln(2)

                pdf.set_font("Arial", size=9.5)
                pdf.set_text_color(51, 65, 85)
                
                safe_text = text_content.encode('latin-1', 'replace').decode('latin-1')
                for line in safe_text.splitlines():
                    if pdf.get_y() > 260:
                        pdf.add_page()
                    pdf.cell(0, 6.5, line, ln=True)
                    
                return bytes(pdf.output())

            def create_excel(text_content):
                lines = text_content.splitlines() if text_content else []
                df = pd.DataFrame(lines, columns=["Cleaned Data"])
                
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='JSP Clean Data')
                return output.getvalue()

            pdf_data = create_pdf(processed_text)
            excel_data = create_excel(processed_text)

            st.markdown("---")
            st.subheader("4. Export Clean Reports:")
            
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_data,
                    file_name="jsp_clean_report.pdf",
                    mime="application/pdf"
                )

            with col_dl2:
                st.download_button(
                    label="📊 Download Excel Spreadsheet",
                    data=excel_data,
                    file_name="jsp_clean_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# Final Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 12px;'>JSP DataClean PDF & Excel Tools &bull; Powered by JSP Technology &bull; Secure Client-Side Processing</p>", unsafe_allow_html=True)
