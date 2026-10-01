import streamlit as st
from fpdf import FPDF
import pandas as pd
from datetime import datetime, timedelta
import re

# Configuração da Página (Modo Escuro / Wide Layout)
st.set_page_config(
    page_title="JSP DataClean PDF & Excel Tools",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS Personalizada para o Padrão Visual JSP Technology
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextArea textarea {
        background-color: #1a1c24;
        color: #ffffff;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    .stButton button {
        background-color: #238636;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 10px;
    }
    .stButton button:hover {
        background-color: #2ea043;
    }
    .stAlert {
        background-color: #1a1c24;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização do Estado da Sessão para Controle de Cotas
if 'uses_left' not in st.session_state:
    st.session_state.uses_left = 2
if 'plan_type' not in st.session_state:
    st.session_state.plan_type = "Free"
if 'quota_left' not in st.session_state:
    st.session_state.quota_left = 0

# Cabeçalho Visual Corporativo JSP na Página Principal
st.markdown("""
    <div style="display: flex; align-items: center; background-color: #1a1c24; padding: 16px 20px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 25px;">
        <div style="background-color: #0f172a; color: #ffffff; font-weight: bold; padding: 10px 16px; border-radius: 6px; font-size: 18px; margin-right: 18px; letter-spacing: 1px;">JSP</div>
        <div>
            <div style="font-size: 20px; font-weight: bold; color: #ffffff; letter-spacing: 0.5px;">JSP TECHNOLOGY</div>
            <div style="font-size: 12px; color: #8b949e; margin-top: 2px;">DataClean Utility Suite &bull; Global Professional Solutions</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("Clean messy text lists, remove duplicates, format data, and instantly export professional clean reports to **PDF** or **Excel**. Free, fast, and 100% private.")

# Seção de Ativação / Planos (Incluindo o Coffee Pass)
with st.expander("🔑 JSP Technology Plans & License Activation", expanded=(st.session_state.plan_type == "Free" and st.session_state.uses_left <= 0)):
    if st.session_state.plan_type != "Free":
        st.success(f"✅ **Active Plan: {st.session_state.plan_type}** | Operations Remaining: {st.session_state.quota_left}")
    else:
        st.info(f"💡 **Free Tier:** {st.session_state.uses_left} free uses remaining (Max 50 lines / 10,000 chars).")
        st.markdown("""
            *☕ **Coffee Pass ($3):** 5 instant operations (No subscription).*  
            *📅 **Monthly Pro ($9):** 20 operations/month.*  
            *⭐ **Annual Pro ($49):** 50 operations/month.*  
        """)
        
        license_input = st.text_input("Enter your JSP License Key / Coffee Pass Code:", type="password", placeholder="JSP-COFFEE-XXXX or JSP-PRO-XXXX")
        if st.button("Activate Code"):
            key = license_input.strip().upper()
            if key.startswith("JSP-COFFEE"):
                st.session_state.plan_type = "Coffee Pass (5 Ops)"
                st.session_state.quota_left = 5
                st.success("☕ Coffee Pass activated! Enjoy 5 batch operations.")
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
                st.error("Invalid key. Please check your purchase receipt from JSP Technology.")

st.markdown("---")

# Área de Entrada de Dados
st.subheader("1. Paste Your Raw Data / Text Below:")
raw_input_text = st.text_area(
    "Raw Data Input",
    height=180,
    placeholder="Paste your messy lists, emails, numbers, or unformatted text here...",
    label_visibility="collapsed"
)

# Opções de Limpeza (Filtros)
st.subheader("2. Select Cleaning Options:")
col1, col2 = st.columns(2)
with col1:
    remove_dups = st.checkbox("Remove Duplicate Lines", value=True)
    remove_empty = st.checkbox("Remove Empty Lines", value=True)
with col2:
    trim_spaces = st.checkbox("Trim Extra Spaces", value=True)
    sort_alpha = st.checkbox("Sort Alphabetically", value=False)

# Função de Processamento do Texto
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

# Validação de Limites de Conteúdo e Acessos
if raw_input_text:
    lines_count = len(raw_input_text.splitlines())
    chars_count = len(raw_input_text)
    
    limit_exceeded = False
    error_message = ""
    
    # Se estiver no plano Free, aplica restrições estritas de tamanho e número de usos
    if st.session_state.plan_type == "Free":
        if lines_count > 50:
            limit_exceeded = True
            error_message = f"⚠️ **Free Tier Limit Exceeded:** Your input has {lines_count} lines (max 50). Get a **Coffee Pass** or Pro plan above for unlimited batch processing."
        elif chars_count > 10000:
            limit_exceeded = True
            error_message = f"⚠️ **Free Tier Limit Exceeded:** Character limit (10,000) reached."
        elif st.session_state.uses_left <= 0:
            limit_exceeded = True
            error_message = "🔒 **Free Trial Limit Reached:** You have used your 2 free sessions. Support our development by grabbing a **Coffee Pass ($3)** or a Pro plan above!"
    else:
        # Se for plano pago (Coffee, Monthly, Annual), valida se ainda tem cota de operações
        if st.session_state.quota_left <= 0:
            limit_exceeded = True
            error_message = f"🔒 **Plan Quota Exhausted:** You have used all operations in your {st.session_state.plan_type}. Please renew your pass."

    if limit_exceeded:
        st.markdown("---")
        st.error(error_message)
    else:
        processed_text = clean_text(raw_input_text, remove_dups, remove_empty, trim_spaces, sort_alpha)

        st.markdown("---")
        st.subheader("3. Cleaned Results Preview:")
        st.text_area("Result Output", value=processed_text, height=180, label_visibility="collapsed")
        
        original_lines = len(raw_input_text.splitlines())
        final_lines = len(processed_text.splitlines()) if processed_text else 0
        st.caption(f"📊 Stats: {original_lines} original lines processed -> {final_lines} clean lines ready.")

        # Geração do PDF com Branding Profissional e Logo Estilizada
        class PDF(FPDF):
            def header(self):
                self.set_fill_color(15, 23, 42)
                self.rect(10, 10, 15, 15, 'F')
                self.set_font('Arial', 'B', 10)
                self.set_text_color(255, 255, 255)
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
                
                self.set_draw_color(226, 232, 240)
                self.set_line_width(0.6)
                self.line(10, 28, 200, 28)
                self.ln(12)

            def footer(self):
                self.set_y(-20)
                self.set_draw_color(226, 232, 240)
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
            pdf.cell(0, 8, 'Processed Clean Data Output:', 0, 1, 'L')
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
            if st.download_button(
                label="📥 Download PDF Report",
                data=pdf_data,
                file_name="jsp_clean_report.pdf",
                mime="application/pdf"
            ):
                # Desconta o uso dependendo do plano ativo
                if st.session_state.plan_type == "Free" and st.session_state.uses_left > 0:
                    st.session_state.uses_left -= 1
                elif st.session_state.plan_type != "Free" and st.session_state.quota_left > 0:
                    st.session_state.quota_left -= 1

        with col_dl2:
            if st.download_button(
                label="📊 Download Excel Spreadsheet",
                data=excel_data,
                file_name="jsp_clean_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ):
                if st.session_state.plan_type == "Free" and st.session_state.uses_left > 0:
                    st.session_state.uses_left -= 1
                elif st.session_state.plan_type != "Free" and st.session_state.quota_left > 0:
                    st.session_state.quota_left -= 1

# Bloco de Rodapé / Identidade da Marca na Interface
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e; font-size: 12px;'>JSP DataClean PDF & Excel Tools • Powered by JSP Technology • 100% Client-Side Privacy</p>", unsafe_allow_html=True)
