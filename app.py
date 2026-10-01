import streamlit as st
from fpdf import FPDF
import re

# Configuração da Página (Modo Escuro / Wide Layout)
st.set_page_config(
    page_title="JSP DataClean PDF Tools",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS Personalizada para o Modo Escuro Padrão JSP
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
    }
    .stButton button:hover {
        background-color: #2ea043;
    }
    </style>
""", unsafe_allow_html=True)

# Título Principal com a Marca JSP
st.title("⚡ JSP DataClean PDF Tools")
st.markdown("Clean messy text lists, remove duplicates, format data, and instantly export professional clean reports to **PDF**. Free, fast, and 100% private.")

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

# Processar os dados se houver input
processed_text = clean_text(raw_input_text, remove_dups, remove_empty, trim_spaces, sort_alpha)

if raw_input_text:
    st.markdown("---")
    st.subheader("3. Cleaned Results Preview:")
    st.text_area("Result Output", value=processed_text, height=180, label_visibility="collapsed")
    
    # Métricas rápidas
    original_lines = len(raw_input_text.splitlines())
    final_lines = len(processed_text.splitlines()) if processed_text else 0
    st.caption(f"📊 Stats: {original_lines} original lines processed -> {final_lines} clean lines ready.")

    # Geração do PDF com Branding Profissional da JSP Technology
    class PDF(FPDF):
        def header(self):
            # Título da Marca e Estilo Corporativo
            self.set_font('Arial', 'B', 14)
            self.set_text_color(33, 37, 41)
            self.cell(0, 10, 'JSP TECHNOLOGY | DataClean Report', 0, 1, 'L')
            
            # Subtítulo / Chamada de Mídia Global
            self.set_font('Arial', 'I', 8)
            self.set_text_color(108, 117, 125)
            self.cell(0, 4, 'Professional Data Extraction & Utility Suite - jsp-dataclean.streamlit.app', 0, 1, 'L')
            
            # Linha divisoria elegante
            self.set_draw_color(200, 200, 200)
            self.set_line_width(0.5)
            self.line(10, 25, 200, 25)
            self.ln(10)

        def footer(self):
            self.set_y(-20)
            # Linha divisória do rodapé
            self.set_draw_color(220, 220, 220)
            self.line(10, 277, 200, 277)
            
            # Informações institucionais e de mídia no rodapé
            self.set_y(-15)
            self.set_font('Arial', 'B', 8)
            self.set_text_color(80, 80, 80)
            self.cell(0, 5, 'Powered by JSP Technology - Global Digital Solutions', 0, 1, 'C')
            
            self.set_font('Arial', '', 7)
            self.set_text_color(130, 130, 130)
            self.cell(0, 4, f'Page {self.page_no()} | Secure Client-Side Processing', 0, 0, 'C')

    def create_pdf(text_content):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(40, 40, 40)
        
        safe_text = text_content.encode('latin-1', 'replace').decode('latin-1')
        for line in safe_text.splitlines():
            pdf.cell(0, 7, line, ln=True)
            
        return bytes(pdf.output())

    pdf_data = create_pdf(processed_text)

    st.markdown("---")
    st.subheader("4. Download Clean Report:")
    st.download_button(
        label="📥 Download Clean Report as PDF",
        data=pdf_data,
        file_name="jsp_clean_report.pdf",
        mime="application/pdf"
    )

# Bloco de Rodapé / Identidade da Marca na Interface
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e; font-size: 12px;'>JSP DataClean PDF Tools • Powered by JSP Technology • 100% Client-Side Privacy</p>", unsafe_allow_html=True)
