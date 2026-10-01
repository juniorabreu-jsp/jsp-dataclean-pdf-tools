import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """ Canvas customizado para adicionar número de páginas e rodapé profissional em todas as folhas """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Linha fina de rodapé
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 40, A4[0] - 40, 40)
        
        # Texto de rodapé
        footer_text = f"JSP Technology — Soluções Digitais | Página {self._pageNumber} de {page_count}"
        self.drawString(40, 28, footer_text)
        
        self.restoreState()

def gerar_pdf_jsp(nome_arquivo="relatorio_jsp_technology.pdf"):
    # Configuração do documento (Margens confortáveis de 40pt)
    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=50
    )
    
    story = []
    
    # Estilos tipográficos
    styles = getSampleStyleSheet()
    
    # Paleta de Cores Profissional
    primary_color = colors.HexColor("#0F172A")  # Azul escuro / Grafite profundo
    accent_color = colors.HexColor("#10B981")   # Verde digital moderno
    text_color = colors.HexColor("#334155")     # Cinza texto suave
    card_bg = colors.HexColor("#F8FAFC")        # Fundo leve para blocos
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=accent_color,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_color,
        spaceAfter=8
    )
    
    # --- CABEÇALHO / MARCA EM EVIDÊNCIA ---
    header_data = [
        [
            Paragraph("<b>JSP</b><font color='#10B981'><b>.</b></font><b>Technology</b>", ParagraphStyle('Brand', fontName='Helvetica-Bold', fontSize=16, leading=18, textColor=primary_color)),
            Paragraph("<b>RELATÓRIO TÉCNICO & EXECUTIVO</b><br/><font size=8 color='#718096'>Padrão de Qualidade SaaS 2026</font>", ParagraphStyle('Meta', fontName='Helvetica', fontSize=9, leading=12, alignment=2, textColor=text_color))
        ]
    ]
    
    header_table = Table(header_data, colWidths=[250, 265])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (-1,-1), 1.5, primary_color),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 15))
    
    # --- TÍTULO DO DOCUMENTO ---
    story.append(Paragraph("Sumário Executivo e Diretrizes do Projeto", title_style))
    story.append(Paragraph("Documentação gerada automaticamente com base na nova identidade visual unificada.", subtitle_style))
    story.append(Spacer(1, 5))
    
    # --- BLOCO DE DESTAQUE (CARD) ---
    intro_text = (
        "Este documento consolida as especificações operacionais e os parâmetros de desenvolvimento "
        "adotados pela <b>JSP Technology</b>. O layout foi rigorosamente desenhado para assegurar um "
        "conforto visual ideal (evitando fadiga ocular), mantendo a marca corporativa em evidência de "
        "forma sóbria, elegante e profissional."
    )
    
    card_table = Table([[Paragraph(intro_text, body_style)]], colWidths=[515])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), card_bg),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LINELEFT', (0,0), (-1,-1), 3.0, accent_color),
    ]))
    
    story.append(card_table)
    story.append(Spacer(1, 15))
    
    # --- SEÇÃO 1 ---
    story.append(Paragraph("1. Diretrizes de Usabilidade e Conforto Visual", h1_style))
    story.append(Paragraph(
        "Para garantir que relatórios extensos não sejam exaustivos à leitura, empregamos uma paleta "
        "composta por fundos neutros limpos, tipografia em cinza carvão de alta legibilidade (evitando o "
        "preto puro contrastante excessivo) e acentos focados nas cores institucionais da marca.",
        body_style
    ))
    
    # --- SEÇÃO 2 ---
    story.append(Paragraph("2. Parâmetros Técnicos e Arquitetura", h1_style))
    
    # Tabela de dados estruturados limpa
    table_data = [
        [Paragraph("<b>Componente</b>", body_style), Paragraph("<b>Especificação Técnica</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("Identidade Visual", body_style), Paragraph("SaaS Moderno / Flat Minimalista", body_style), Paragraph("<font color='#10B981'><b>Ativo</b></font>", body_style)],
        [Paragraph("Geração de Relatórios", body_style), Paragraph("ReportLab Core com Canvas Dinâmico", body_style), Paragraph("<font color='#10B981'><b>Homologado</b></font>", body_style)],
        [Paragraph("Segurança & Licenciamento", body_style), Paragraph("Estrutura Portable / Módulo HWID", body_style), Paragraph("<font color='#10B981'><b>Operacional</b></font>", body_style)],
    ]
    
    t = Table(table_data, colWidths=[130, 265, 120])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('TEXTCOLOR', (0,0), (-1,0), primary_color),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 15))
    
    # --- SEÇÃO 3 ---
    story.append(Paragraph("3. Considerações Finais", h1_style))
    story.append(Paragraph(
        "A consistência visual reforça o posicionamento de mercado da JSP Technology como referência em "
        "soluções digitais de alta performance. Este modelo de PDF pode ser integrado diretamente às "
        "suas aplicações em Streamlit ou scripts de automação.",
        body_style
    ))

    # Construir PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF gerado com sucesso: {nome_arquivo}")

if __name__ == "__main__":
    gerar_pdf_jsp()
