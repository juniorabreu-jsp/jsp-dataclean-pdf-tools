import streamlit as st
from fpdf import FPDF
import pandas as pd
from datetime import datetime
import urllib.parse
import uuid

# Page Configuration (Clean Light Mode & Professional Layout)
st.set_page_config(
    page_title="JSP DataClean | Professional Data Formatting & Export Suite",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional Light Mode CSS Styling (Clean White & High Contrast Corporate Look)
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        font-family: monospace !important;
        font-size: 14px !important;
        padding: 12px !important;
    }
    .stTextArea textarea:focus {
        border-color: #16a34a !important;
        box-shadow: 0 0 10px rgba(22, 163, 74, 0.2) !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: white !important;
        border-radius: 10px;
        font-weight: 700;
        border: none;
        width: 100%;
        padding: 12px;
        font-size: 15px;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.25);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        box-shadow: 0 6px 16px rgba(22, 163, 74, 0.35);
        transform: translateY(-1px);
    }
    
    .guide-box {
        background: #ffffff;
        border-left: 4px solid #16a34a;
        padding: 16px 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        color: #334155;
        font-size: 14px;
        line-height: 1.5;
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
if 'generated_keys_db' not in st.session_state:
    st.session_state.generated_keys_db = {
        "JSP-COFFEE-TEST": {"plan": "Coffee Pass (5 Ops)", "used": False, "ops": 5, "created_at": "2026-03-04"},
        "JSP-LIFETIME-MASTER": {"plan": "Vitalícia / Permanente", "used": False, "ops": 999999, "created_at": "2026-03-04"}
    }
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

# Detecta se o usuário acessou o painel digitando /painel no final do endereço
try:
    # Tenta ler a rota atual do navegador no Streamlit moderno
    current_path = st.context.headers.get("Sec-Fetch-Site", "") # fallback seguro
    # Verificação alternativa via URL query string ou se o componente de navegação interna foi acionado
    is_painel_route = False
except Exception:
    is_painel_route = False

# Forma alternativa e 100% funcional no Streamlit para alternar via URL hash ou query param robusto
query_params = st.query_params
# Se a URL contiver ?painel=true ou ?admin=true
is_admin_mode = query_params.get("painel") == "true" or query_params.get("admin") == "true"

# Se não estiver no modo admin por parâmetro, permitimos alternar digitando uma senha rápida ou exibindo a visão normal
# Vamos colocar um atalho invisível ou direto:
if is_admin_mode:
    st.markdown("## 🔐 JSP Technology - Master Admin Panel")
    st.markdown("Painel administrativo restrito. Gere chaves vitalícias, gerencie planos e configure alertas de vendas.")
    
    if not st.session_state.admin_logged:
        admin_pass = st.text_input("Digite a Senha Master do Admin:", type="password", placeholder="Senha padrão: jsp2026admin")
        if st.button("Entrar no Painel"):
            if admin_pass == "jsp2026admin":
                st.session_state.admin_logged = True
                st.success("🔓 Acesso administrativo liberado!")
                st.rerun()
            else:
                st.error("❌ Senha master incorreta.")
    else:
        st.success("✅ Autenticado como Administrador Master")
        if st.button("Sair / Fechar Painel Admin"):
            st.session_state.admin_logged = False
            st.rerun()
            
        st.markdown("---")
        
        # TAB 1: Key Generator (Com opção Vitalícia)
        st.markdown("### 🔑 1. Gerar Nova Chave de Licença")
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            plan_selection = st.selectbox("Selecione o Plano:", ["Coffee Pass (5 Ops)", "Monthly Pro", "Annual Pro", "Vitalícia / Permanente"])
        with col_k2:
            custom_code_prefix = st.selectbox("Prefixo da Chave:", ["JSP-COFFEE", "JSP-MONTHLY", "JSP-ANNUAL", "JSP-LIFETIME"])
            
        if st.button("⚡ Gerar Chave Segura"):
            unique_suffix = str(uuid.uuid4())[:6].upper()
            new_key = f"{custom_code_prefix}-{unique_suffix}"
            
            if "Coffee" in plan_selection:
                ops_count = 5
            elif "Monthly" in plan_selection:
                ops_count = 20
            elif "Annual" in plan_selection:
                ops_count = 50
            else: # Vitalícia
                ops_count = 999999
            
            st.session_state.generated_keys_db[new_key] = {
                "plan": plan_selection,
                "used": False,
                "ops": ops_count,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.success(f"🎉 Chave gerada com sucesso: **`{new_key}`** ({plan_selection})")
            if "Vitalícia" in plan_selection:
                st.info("🌟 Chave vitalícia criada! Utilize para você ou envie para quem desejar acesso permanente.")
            else:
                st.info(f"Copie esta chave e envie para o seu cliente.")

        st.markdown("### 📋 Banco de Dados de Licenças")
        if st.session_state.generated_keys_db:
            df_keys = pd.DataFrame([
                {"Key": k, "Plan": v["plan"], "Operations": v["ops"], "Status": "Usada" if v["used"] else "Disponível", "Created": v["created_at"]}
                for k, v in st.session_state.generated_keys_db.items()
            ])
            st.dataframe(df_keys, use_container_width=True)
        else:
            st.info("Nenhuma chave gerada ainda.")

        st.markdown("---")
        
        # TAB 2: WhatsApp & Email Alert Simulator / Config
        st.markdown("### 📱 2. Configuração de Alertas de Vendas (WhatsApp & E-mail)")
        with st.form("alert_config_form"):
            admin_whatsapp = st.text_input("Seu Número do WhatsApp (com DDI e DDD):", value="5585920025390")
            admin_email = st.text_input("Seu E-mail de Notificação:", value="contato@jsptechnology.com")
            test_buyer_email = st.text_input("Simular E-mail do Comprador:", value="cliente@exemplo.com")
            test_plan_bought = st.selectbox("Simular Plano Adquirido:", ["Coffee Pass ($3)", "Monthly Pro ($9)", "Annual Pro ($49)", "Vitalícia / Permanente"])
            test_generated_key = st.text_input("Simular Chave Gerada para o Cliente:", value="JSP-LIFETIME-A1B2C3")
            
            submit_alert_test = st.form_submit_button("🔔 Simular / Disparar Alerta para o WhatsApp")
            
            if submit_alert_test:
                alert_msg = (
                    f"🚀 *Nova Venda Aprovada - JSP DataClean!*\n\n"
                    f"• *Plano Escolhido:* {test_plan_bought}\n"
                    f"• *Chave Gerada:* `{test_generated_key}`\n"
                    f"• *Comprador:* {test_buyer_email}\n"
                    f"• *Data:* {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                    f"🔐 *Acesso ao Painel Admin:*\n"
                    f"• Link: http://localhost:8501/?painel=true\n"
                    f"• Senha Master: `jsp2026admin`"
                )
                
                encoded_msg = urllib.parse.quote(alert_msg)
                wa_url = f"https://api.whatsapp.com/send?phone={admin_whatsapp}&text={encoded_msg}"
                
                st.success("✅ Alerta estruturado com sucesso!")
                st.markdown(f"👉 **[Clique aqui para disparar o Alerta no seu WhatsApp]({wa_url})**")
                st.info(f"📧 E-mail de notificação enviado para: **{admin_email}**")

# ==========================================
# CLIENT APP VIEW (VISÃO NORMAL DO CLIENTE)
# ==========================================
else:
    # JSP Commercial Corporate Header
    st.markdown("""
        <div style="display: flex; align-items: center; background: #ffffff; padding: 22px 26px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04);">
            <div style="background: #0f172a; color: #ffffff; font-weight: 900; padding: 14px 20px; border-radius: 10px; font-size: 22px; margin-right: 20px; letter-spacing: 1.5px; display: flex; align-items: center; gap: 8px;">
                <span style="color: #22c55e;">●</span> JSP
            </div>
            <div>
                <div style="font-size: 24px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">JSP TECHNOLOGY</div>
                <div style="font-size: 14px; color: #64748b; margin-top: 3px; font-weight: 500;">DataClean Utility Suite &bull; Enterprise-Grade Data Processing & Export</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Self-Explanatory Step 1 Guide Banner
    st.markdown("""
        <div class="guide-box">
            <strong>💡 How it works in 3 simple steps:</strong><br>
            1️⃣ <b>Paste your messy lists, raw leads, or unformatted text</b> into the box below.<br>
            2️⃣ <b>Select your cleaning rules</b> (remove duplicates, trim spaces, sort alphabetically).<br>
            3️⃣ <b>Run & Export</b> instantly as a polished PDF Report or clean Excel Spreadsheet!<br><br>
            <span style="color: #16a34a; font-size: 13px;">🕒 <b>Delivery Notice:</b> License keys and manual orders are processed within 24 hours due to time zone differences.</span>
        </div>
    """, unsafe_allow_html=True)

    # License & Commercial Upgrade Section
    with st.expander("🚀 Upgrade & License Activation (Coffee Pass / Pro / Lifetime)", expanded=(st.session_state.plan_type == "Free" and st.session_state.uses_left <= 0)):
        if st.session_state.plan_type != "Free":
            st.success(f"✨ **Active Enterprise Tier: {st.session_state.plan_type}** | Operations Remaining: {st.session_state.quota_left}")
        else:
            st.info(f"🌟 **Free Trial Status:** {st.session_state.uses_left} free runs remaining (Up to 50 lines per run).")
            st.markdown("### Unlock Unlimited Power & Professional Reports:")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.markdown("**☕ Coffee Pass**\n- $3 one-time\n- 5 Operations\n- No subscription")
            with col_p2:
                st.markdown("**📅 Monthly Pro**\n- $9 / month\n- 20 Ops / month\n- Priority support")
            with col_p3:
                st.markdown("**⭐ Annual Pro**\n- $49 / year\n- 50 Ops / month\n- Max productivity")
                
            st.markdown("<br>", unsafe_allow_html=True)
            license_input = st.text_input("Enter your License Key or Coffee Pass Code:", type="password", placeholder="Ex: JSP-COFFEE-XXXX or JSP-LIFETIME-XXXX")
            if st.button("Activate License Key"):
                key = license_input.strip().upper()
                
                if key in st.session_state.generated_keys_db:
                    key_data = st.session_state.generated_keys_db[key]
                    st.session_state.plan_type = key_data["plan"]
                    st.session_state.quota_left += key_data["ops"]
                    key_data["used"] = True
                    st.success(f"🎉 License successfully activated! +{key_data['ops']} operations added to your account.")
                    st.rerun()
                else:
                    st.error("❌ Invalid license key or already expired. Please verify your code received from JSP Technology support.")

    st.markdown("---")

    # Data Input Section
    st.markdown("### 📥 Step 1: Input Your Raw Data")
    raw_input_text = st.text_area(
        "Data Input",
        height=170,
        placeholder="Paste raw leads, emails, phone numbers, or unformatted text items here (one per line)...",
        label_visibility="collapsed"
    )

    # Cleaning Options (Filters)
    st.markdown("### ⚙️ Step 2: Configure Cleaning Filters")
    col1, col2 = st.columns(2)
    with col1:
        remove_dups = st.checkbox("Remove Duplicate Lines (De-duplication)", value=True)
        remove_empty = st.checkbox("Remove Empty Lines (Clean layout)", value=True)
    with col2:
        trim_spaces = st.checkbox("Trim Extra Whitespaces (Clean padding)", value=True)
        sort_alpha = st.checkbox("Sort Alphabetically (A to Z)", value=False)

    st.markdown("---")

    # Explicit Commercial Execution Button
    run_button = st.button("⚡ Run Instant Data Cleaning & Formatting")

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
            st.warning("⚠️ Please paste your raw data into the text box above before running the cleaner.")
        else:
            lines_count = len(raw_input_text.splitlines())
            chars_count = len(raw_input_text)
            
            limit_exceeded = False
            error_message = ""
            
            if st.session_state.plan_type == "Free":
                if lines_count > 50:
                    limit_exceeded = True
                    error_message = f"🔒 **Free Tier Limit Reached:** Your input has {lines_count} lines (maximum allowed on Free tier is 50). Unlock a **Coffee Pass ($3)** above to process large enterprise datasets instantly!"
                elif chars_count > 10000:
                    limit_exceeded = True
                    error_message = f"🔒 **Free Tier Character Limit Reached:** Maximum of 10,000 characters exceeded."
                elif st.session_state.uses_left <= 0:
                    limit_exceeded = True
                    error_message = "🔒 **Free Trial Completed:** You've used your 2 complimentary runs. Support JSP Technology by grabbing a quick **Coffee Pass ($3)** above!"
            else:
                if st.session_state.quota_left <= 0 and st.session_state.plan_type != "Vitalícia / Permanente":
                    limit_exceeded = True
                    error_message = f"🔒 **Quota Exhausted:** Your operations for the {st.session_state.plan_type} plan have ended. Enter a new refill code above to continue working without interruption."

            if limit_exceeded:
                st.error(error_message)
            else:
                processed_text = clean_text(raw_input_text, remove_dups, remove_empty, trim_spaces, sort_alpha)

                st.markdown("### ✨ Step 3: Review Cleaned Results & Export")
                st.text_area("Processed Output", value=processed_text, height=170, label_visibility="collapsed")
                
                original_lines = len(raw_input_text.splitlines())
                final_lines = len(processed_text.splitlines()) if processed_text else 0
                st.caption(f"📊 **Performance Metrics:** {original_lines} raw lines processed &bull; {final_lines} clean items ready for export.")

                if st.session_state.plan_type == "Free" and st.session_state.uses_left > 0:
                    st.session_state.uses_left -= 1
                elif st.session_state.plan_type != "Free" and st.session_state.quota_left > 0 and st.session_state.plan_type != "Vitalícia / Permanente":
                    st.session_state.quota_left -= 1

                # Professional PDF Generator
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
                    pdf.cell(0, 8, 'Certified Clean Data Report:', 0, 1, 'L')
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
                    df = pd.DataFrame(lines, columns=["Cleaned Data Items"])
                    
                    from io import BytesIO
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='JSP Clean Data')
                    return output.getvalue()

                pdf_data = create_pdf(processed_text)
                excel_data = create_excel(processed_text)

                st.markdown("---")
                
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        label="📥 Download Official PDF Report",
                        data=pdf_data,
                        file_name="jsp_clean_report.pdf",
                        mime="application/pdf"
                    )

                with col_dl2:
                    st.download_button(
                        label="📊 Download Excel Spreadsheet (.xlsx)",
                        data=excel_data,
                        file_name="jsp_clean_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    # Professional Commercial Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 12px; font-weight: 500;'>JSP DataClean Utility Suite &bull; Powered by JSP Technology &bull; Secure Enterprise Data Solutions</p>", unsafe_allow_html=True)
