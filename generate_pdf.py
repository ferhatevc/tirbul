#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TırBul Yatırımcı Sunumu — Clean PDF Generator using Platypus"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, 
                                 TableStyle, PageBreak, KeepTogether)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import os

# Register Arial for Turkish unicode support
pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', '/System/Library/Fonts/Supplemental/Arial Italic.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf'))
registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic', boldItalic='Arial-BoldItalic')

PDF_PATH = '/Users/ferhatevci/.gemini/antigravity/scratch/tirbul/TirBul_Yatirimci_Sunumu.pdf'
W, H = landscape(A4)

# Colors
BG = HexColor('#0a0f1e')
PRIMARY = '#FF6B35'
PRIMARY_L = '#FFB347'
SUCCESS = '#10b981'
DANGER = '#ef4444'
INFO = '#6366f1'
TEXT = '#f0f0f0'
TEXT_S = '#9ca3af'
SURFACE = '#111827'
BORDER = '#1e293b'

# Styles
styles = {
    'title': ParagraphStyle('title', fontName='Arial-Bold', fontSize=32, 
                            textColor=HexColor(PRIMARY), alignment=TA_CENTER, spaceAfter=6),
    'h1': ParagraphStyle('h1', fontName='Arial-Bold', fontSize=24, 
                         textColor=HexColor(TEXT), spaceAfter=4, spaceBefore=0),
    'h1o': ParagraphStyle('h1o', fontName='Arial-Bold', fontSize=24, 
                          textColor=HexColor(PRIMARY), spaceAfter=12),
    'h2': ParagraphStyle('h2', fontName='Arial-Bold', fontSize=16, 
                         textColor=HexColor(TEXT), spaceAfter=8),
    'h3': ParagraphStyle('h3', fontName='Arial-Bold', fontSize=13, 
                         textColor=HexColor(TEXT), spaceAfter=6),
    'body': ParagraphStyle('body', fontName='Arial', fontSize=11, 
                           textColor=HexColor(TEXT_S), leading=16, spaceAfter=4),
    'center': ParagraphStyle('center', fontName='Arial', fontSize=12, 
                             textColor=HexColor(TEXT_S), alignment=TA_CENTER, leading=18),
    'tag': ParagraphStyle('tag', fontName='Arial-Bold', fontSize=9, 
                           textColor=HexColor(PRIMARY_L), alignment=TA_CENTER, spaceAfter=16),
    'stat_num': ParagraphStyle('stat_num', fontName='Arial-Bold', fontSize=28, 
                               textColor=HexColor(PRIMARY), alignment=TA_CENTER),
    'stat_lbl': ParagraphStyle('stat_lbl', fontName='Arial', fontSize=9, 
                               textColor=HexColor(TEXT_S), alignment=TA_CENTER),
    'small': ParagraphStyle('small', fontName='Arial', fontSize=9, 
                            textColor=HexColor(TEXT_S), leading=14),
    'quote': ParagraphStyle('quote', fontName='Arial-Italic', fontSize=10, 
                            textColor=HexColor(TEXT_S), leading=15, leftIndent=12,
                            borderWidth=2, borderColor=HexColor(PRIMARY), borderPadding=8),
    'footer': ParagraphStyle('footer', fontName='Arial', fontSize=6, 
                             textColor=HexColor('#333333'), alignment=TA_CENTER),
}

def bg_draw(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Subtle orb
    canvas.setFillColor(HexColor('#FF6B35'))
    canvas.setFillAlpha(0.04)
    canvas.circle(W - 50, H + 50, 250, fill=1, stroke=0)
    canvas.restoreState()

doc = SimpleDocTemplate(PDF_PATH, pagesize=landscape(A4),
                        leftMargin=50, rightMargin=50, topMargin=40, bottomMargin=30)

def make_table(data, col_widths=None, style_cmds=None):
    t = Table(data, colWidths=col_widths, hAlign='LEFT')
    base_style = [
        ('BACKGROUND', (0,0), (-1,0), HexColor('#151c2c')),
        ('TEXTCOLOR', (0,0), (-1,0), HexColor(TEXT_S)),
        ('TEXTCOLOR', (0,1), (-1,-1), HexColor(TEXT)),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,0), (-1,0), 8),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor(SURFACE), HexColor('#0d1320')]),
    ]
    if style_cmds:
        base_style.extend(style_cmds)
    t.setStyle(TableStyle(base_style))
    return t

def stat_card(num, label):
    data = [[Paragraph(num, styles['stat_num'])], [Paragraph(label, styles['stat_lbl'])]]
    t = Table(data, colWidths=[170])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor(SURFACE)),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def card_table(cards, col_w=None):
    """cards = list of (icon, title, desc) or table cells"""
    data = [cards]
    cw = col_w or [170] * len(cards)
    t = Table(data, colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor(SURFACE)),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, HexColor(BORDER)),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return t

P = lambda text, style='body': Paragraph(text, styles[style])
S = lambda h=12: Spacer(1, h)

elements = []

# ============ SLIDE 1: COVER ============
elements.append(S(60))
elements.append(P("Yatırımcı Sunumu — Haziran 2026", 'tag'))
elements.append(P("TırBul", 'title'))
elements.append(S(8))
elements.append(P("Türkiye'nin İlk<br/><b>Güvenli Taşımacılık Platformu</b>", 'center'))
elements.append(S(24))
elements.append(P("Otomatik Sigorta&nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;Doğrulanmış Şoförler&nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;Fotoğraflı Teslimat", 'center'))
elements.append(S(40))
elements.append(P(f'Yatırım Talebi: <font color="{PRIMARY}"><b>$25.000</b></font>', 'center'))
elements.append(S(8))
elements.append(P("Slayt 1/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 2: PROBLEM ============
elements.append(P("SORUN", 'tag'))
elements.append(P("Anadolu'da Her Sanayicinin Yaşadığı", 'h1'))
elements.append(P("3 Büyük Sorun", 'h1o'))
elements.append(S(8))

problems = [
    ("01", '"Güvenilir tırcı bulamıyorum"', "Yükü kime vereceğini bilemiyor. Geçmişi, belgesi belirsiz. Her seferinde risk alıyor."),
    ("02", '"Tırcılar sigorta yaptırmıyor"', "Hasar olduğunda tüm zarar sanayicinin üstünde. Sigorta yaptırmak ayrı bir iş ve maliyet."),
    ("03", '"Değnekçiler komisyon yiyor"', "Aracılar gereksiz komisyon alıyor. Şeffaflık yok, fiyatlar şişirilmiş, katma değer sıfır."),
]
for num, title, desc in problems:
    row = [[Paragraph(f'<b><font color="{DANGER}" size="14">{num}</font></b>', styles['center']),
            Paragraph(f'<b><font color="{TEXT}">{title}</font></b><br/><font color="{TEXT_S}" size="9">{desc}</font>', styles['body'])]]
    t = Table(row, colWidths=[50, W-150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#120d0d')),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#2d1515')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    elements.append(S(6))

elements.append(S(8))
elements.append(P(f'<i><font color="{TEXT_S}">"Bu sorun sadece Sivas\'a özel değil. Türkiye\'de karayolu taşımacılığının %90\'ında aynı sorun var. Ama kimse Anadolu\'dan başlamıyor."</font></i>', 'body'))
elements.append(P("Slayt 2/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 3: MARKET ============
elements.append(P("PAZAR BÜYÜKLÜĞÜ", 'tag'))
elements.append(P("Devasa Bir Pazar,", 'h1'))
elements.append(P("Kimsenin Girmediği Alan", 'h1o'))
elements.append(S(8))

# 3 stat cards
stat_row = [[stat_card("$100B", "Türkiye Lojistik Pazarı"),
             stat_card("%90", "Karayolu Taşımacılığı"),
             stat_card("<%5", "Dijitalleşme Oranı")]]
st = Table(stat_row, colWidths=[230, 230, 230])
st.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),
                         ('VALIGN', (0,0), (-1,-1), 'TOP'),
                         ('LEFTPADDING', (0,0), (-1,-1), 5),
                         ('RIGHTPADDING', (0,0), (-1,-1), 5)]))
elements.append(st)
elements.append(S(16))

# Two columns
col_data = [[
    Paragraph(f'<b><font color="{TEXT}" size="13">Sivas Başlangıç Pazarı</font></b><br/><br/>'
              f'<font color="{TEXT_S}">• OSB: 370+ firma, %99 doluluk<br/>'
              f'• 2024 ihracatı: $82M (%17 büyüme)<br/>'
              f'• Yılda 30+ yeni fabrika<br/>'
              f'• Tahmini nakliye hacmi: 500M+ ₺/yıl</font>', styles['body']),
    Paragraph(f'<b><font color="{TEXT}" size="13">Genişleme Yol Haritası</font></b><br/><br/>'
              f'<font color="{TEXT_S}">• 1. Yıl: Sivas + çevre → ~500M₺<br/>'
              f'• 2. Yıl: İç Anadolu → ~5 Milyar₺<br/>'
              f'• 3. Yıl: Türkiye geneli → ~50+ Milyar₺</font>', styles['body']),
]]
ct = Table(col_data, colWidths=[340, 340])
ct.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),
                         ('LEFTPADDING', (0,0), (-1,-1), 10)]))
elements.append(ct)
elements.append(P("Slayt 3/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 4: SOLUTION ============
elements.append(P("ÇÖZÜM", 'tag'))
elements.append(P("TırBul = Eşleştirme +", 'h1'))
elements.append(P("Güvenli Taşımacılık Garantisi", 'h1o'))
elements.append(S(6))

features = [
    ("01", "Otomatik Sigorta", "Her taşımaya sigorta dahil. Sanayici ayrıca uğraşmıyor. Tek tıkla sigortalı taşıma."),
    ("02", "Şoför Doğrulama + Rozet", "3 katmanlı doğrulama. Rozet sistemi: Bronz → Gümüş → Altın → Elmas"),
    ("03", "Fotoğraflı Teslimat", "Yükleme ve teslimde fotoğraf kanıtı + GPS kaydı. Hasar anlaşmazlığı tarih olur."),
    ("04", "Şeffaf Fiyat", "Değnekçiye komisyon yok. Fiyatı yük sahibi belirler, nakliyeci teklif verir."),
]
for i in range(0, 4, 2):
    row = []
    for j in range(2):
        f = features[i+j]
        row.append(Paragraph(f'<b><font color="{PRIMARY}" size="12">{f[0]}</font></b><br/>'
                             f'<b><font color="{TEXT}" size="11">{f[1]}</font></b><br/>'
                             f'<font color="{TEXT_S}" size="9">{f[2]}</font>', styles['body']))
    ft = Table([row], colWidths=[340, 340])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor(SURFACE)),
        ('BOX', (0,0), (0,0), 0.5, HexColor(BORDER)),
        ('BOX', (1,0), (1,0), 0.5, HexColor(BORDER)),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(ft)
    elements.append(S(6))

elements.append(S(8))
elements.append(P(f'<para alignment="center"><b><font color="{TEXT}">Tek cümleyle:</font></b> <font color="{TEXT_S}">Sanayici</font> <font color="{PRIMARY}"><b>"yük ver"</b></font> <font color="{TEXT_S}">der, gerisini biz yaparız.</font></para>', 'center'))
elements.append(P("Slayt 4/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 5: PRODUCT READY ============
elements.append(P("ÜRÜN DURUMU", 'tag'))
elements.append(P("Bu Bir Fikir Değil,", 'h1'))
elements.append(P("Ürün Hazır ve Çalışıyor", 'h1o'))
elements.append(P(f'<font color="{TEXT_S}">Yatırım istemeden ÖNCE platformu geliştirdik. Çalışan demo mevcuttur.</font>', 'body'))
elements.append(S(10))

modules = [
    ("01", "Ana Sayfa", "Arama, istatistik, özellikler"),
    ("02", "Kayıt / Giriş", "Yük sahibi & nakliyeci"),
    ("03", "Yük Sahibi Paneli", "İlan verme, teklif yönetimi"),
    ("04", "Nakliyeci Paneli", "Yük arama, teklif, profil"),
    ("05", "Sigorta Sistemi", "3 teminat, otomatik hesaplama"),
    ("06", "Rozet Sistemi", "Bronz → Gümüş → Altın → Elmas"),
]
for i in range(0, 6, 3):
    row = []
    for j in range(3):
        m = modules[i+j]
        row.append(Paragraph(f'<para alignment="center"><b><font color="{PRIMARY}" size="14">{m[0]}</font></b><br/>'
                             f'<b><font color="{TEXT}" size="11">{m[1]}</font></b><br/>'
                             f'<font color="{TEXT_S}" size="8">{m[2]}</font><br/><br/>'
                             f'<font color="{SUCCESS}" size="8"><b>Hazır</b></font></para>', styles['center']))
    mt = Table([row], colWidths=[220, 220, 220])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor(SURFACE)),
        ('BOX', (0,0), (0,0), 0.5, HexColor(BORDER)),
        ('BOX', (1,0), (1,0), 0.5, HexColor(BORDER)),
        ('BOX', (2,0), (2,0), 0.5, HexColor(BORDER)),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(mt)
    elements.append(S(8))

elements.append(P("Slayt 5/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 6: COMPETITORS ============
elements.append(P("REKABET AVANTAJI", 'tag'))
elements.append(P("Rakipler Ne Yapıyor,", 'h1'))
elements.append(P("Biz Ne Farklı Yapıyoruz?", 'h1o'))
elements.append(S(6))

comp_data = [
    ['Özellik', 'Değnekçi', 'Tırport ($2M)', 'Kamion ($2.5M)', 'TırBul ($25K)'],
    ['Yük eşleştirme', 'Var', 'Var', 'Var', 'Var'],
    ['Otomatik sigorta', 'Yok', 'Yok', 'Yok', 'Var'],
    ['Şoför doğrulama + rozet', 'Yok', 'Kısmen', 'Kısmen', 'Var'],
    ['Fotoğraflı teslimat', 'Yok', 'Yok', 'Yok', 'Var'],
    ['GPS takip', 'Yok', 'Var', 'Var', 'Var'],
    ['Anadolu odağı', 'Var', 'Yok', 'Yok', 'Var'],
    ['KOBİ dostu', 'Kısmen', 'Yok', 'Yok', 'Var'],
]
cw = [180, 110, 130, 130, 130]
comp_style = [
    ('TEXTCOLOR', (4,0), (4,0), HexColor(PRIMARY)),
    ('FONTNAME', (4,0), (4,-1), 'Arial-Bold'),
    ('BACKGROUND', (0,2), (-1,4), HexColor('#120e08')),
    ('FONTNAME', (0,2), (0,4), 'Arial-Bold'),
]
# Color the check/cross marks
for row_i in range(1, len(comp_data)):
    for col_j in range(1, 5):
        val = comp_data[row_i][col_j]
        if val == 'Var':
            comp_style.append(('TEXTCOLOR', (col_j, row_i), (col_j, row_i), HexColor(SUCCESS)))
        elif val == 'Yok':
            comp_style.append(('TEXTCOLOR', (col_j, row_i), (col_j, row_i), HexColor(DANGER)))
        elif val == 'Kısmen':
            comp_style.append(('TEXTCOLOR', (col_j, row_i), (col_j, row_i), HexColor('#f59e0b')))

elements.append(make_table(comp_data, cw, comp_style))
elements.append(S(12))
elements.append(P(f'<i><font color="{TEXT_S}">"Rakipler milyonlarca dolar harcadı ama kimse sigorta + doğrulama + fotoğraflı teslimat paketini sunmuyor. Ve kimse Anadolu\'ya odaklanmıyor."</font></i>', 'body'))
elements.append(P("Slayt 6/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 7: REVENUE ============
elements.append(P("GELİR MODELİ", 'tag'))
elements.append(P(f'Para <font color="{PRIMARY}">Nereden Gelecek?</font>', 'h1'))
elements.append(S(10))

rev_row = []
rev_items = [("01", "Hizmet Bedeli", "%4", "Her taşımadan", PRIMARY),
             ("02", "Sigorta Kom.", "%20-30", "Toplu anlaşma farkı", SUCCESS),
             ("03", "Premium", "₺500-2K", "Aylık üyelik", INFO),
             ("04", "Reklam", "Ek", "Sektör reklamları", '#f59e0b')]
for num, title, amount, desc, color in rev_items:
    rev_row.append(Paragraph(f'<para alignment="center"><b><font color="{PRIMARY}" size="12">{num}</font></b><br/>'
                             f'<b><font color="{TEXT}" size="10">{title}</font></b><br/>'
                             f'<font color="{color}" size="20"><b>{amount}</b></font><br/>'
                             f'<font color="{TEXT_S}" size="8">{desc}</font></para>', styles['center']))
rt = Table([rev_row], colWidths=[168, 168, 168, 168])
rt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(SURFACE)),
    ('BOX', (0,0), (0,0), 0.5, HexColor(BORDER)),
    ('BOX', (1,0), (1,0), 0.5, HexColor(BORDER)),
    ('BOX', (2,0), (2,0), 0.5, HexColor(BORDER)),
    ('BOX', (3,0), (3,0), 0.5, HexColor(BORDER)),
    ('TOPPADDING', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
elements.append(rt)
elements.append(S(16))

# Example calc
calc_data = [['Taşıma Bedeli', '→', 'Hizmet (%4)', '+', 'Sigorta Kom.', '=', 'Platform Geliri'],
             ['₺30.000', '', '₺1.200', '', '₺400', '', '₺1.600']]
calc_style = [
    ('TEXTCOLOR', (0,0), (-1,0), HexColor(TEXT_S)),
    ('TEXTCOLOR', (0,1), (0,1), HexColor(TEXT)),
    ('TEXTCOLOR', (1,0), (-1,-1), HexColor(TEXT_S)),
    ('TEXTCOLOR', (2,1), (2,1), HexColor(PRIMARY)),
    ('TEXTCOLOR', (3,0), (3,-1), HexColor(TEXT_S)),
    ('TEXTCOLOR', (4,1), (4,1), HexColor(SUCCESS)),
    ('TEXTCOLOR', (5,0), (5,-1), HexColor(TEXT_S)),
    ('TEXTCOLOR', (6,1), (6,1), HexColor(PRIMARY_L)),
    ('FONTNAME', (0,1), (-1,1), 'Arial-Bold'),
    ('FONTSIZE', (0,1), (-1,1), 14),
    ('BACKGROUND', (0,0), (-1,-1), HexColor('#120e08')),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor('#2a1508')),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
]
ct2 = Table(calc_data, colWidths=[105, 30, 105, 30, 105, 30, 120])
ct2.setStyle(TableStyle(calc_style + [
    ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('FONTNAME', (0,0), (-1,0), 'Arial'), ('FONTSIZE', (0,0), (-1,0), 8),
]))
elements.append(P(f'<para alignment="center"><b><font color="{TEXT}">Örnek Hesap: 30.000₺ Taşıma</font></b></para>', 'center'))
elements.append(S(4))
elements.append(ct2)
elements.append(P("Slayt 7/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 8: PROJECTIONS ============
elements.append(P("12 AYLIK PROJEKSİYON", 'tag'))
elements.append(P("Ayda 200 Eşleşme ile", 'h1'))
elements.append(P("Aylık 290.000₺ Gelir", 'h1o'))
elements.append(S(6))

proj_data = [
    ['', 'Hizmet Bedeli', 'Sigorta Kom.', 'Premium', 'TOPLAM'],
    ['Gelir', '200.000₺', '60.000₺', '30.000₺', '290.000₺'],
]
proj_style = [('TEXTCOLOR', (4,1), (4,1), HexColor(SUCCESS)),
              ('FONTNAME', (4,1), (4,1), 'Arial-Bold'),
              ('FONTSIZE', (4,1), (4,1), 12)]
elements.append(P(f'<b><font color="{SUCCESS}">Gelirler</font></b>', 'h3'))
elements.append(make_table(proj_data, [100, 140, 140, 140, 160], proj_style))
elements.append(S(10))

exp_data = [
    ['', 'Sigorta Primleri', 'Personel', 'İşletme', 'Pazarlama', 'TOPLAM'],
    ['Gider', '80.000₺', '60.000₺', '25.000₺', '20.000₺', '185.000₺'],
]
exp_style = [('TEXTCOLOR', (5,1), (5,1), HexColor(DANGER)),
             ('FONTNAME', (5,1), (5,1), 'Arial-Bold')]
elements.append(P(f'<b><font color="{DANGER}">Giderler</font></b>', 'h3'))
elements.append(make_table(exp_data, [80, 120, 120, 110, 110, 140], exp_style))
elements.append(S(16))

# Net result
net_row = [[
    Paragraph(f'<para alignment="center"><font color="{PRIMARY}" size="22"><b>290K₺</b></font><br/><font color="{TEXT_S}" size="8">Aylık Gelir</font></para>', styles['center']),
    Paragraph(f'<para alignment="center"><font color="{DANGER}" size="22"><b>185K₺</b></font><br/><font color="{TEXT_S}" size="8">Aylık Gider</font></para>', styles['center']),
    Paragraph(f'<para alignment="center"><font color="{SUCCESS}" size="22"><b>105K₺</b></font><br/><font color="{TEXT_S}" size="8">Aylık Net Kâr (~$3.000)</font></para>', styles['center']),
]]
nt = Table(net_row, colWidths=[220, 220, 220])
nt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor('#120e08')),
    ('BOX', (0,0), (-1,-1), 1, HexColor(PRIMARY)),
    ('TOPPADDING', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
]))
elements.append(nt)
elements.append(P("Slayt 8/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 9: INVESTMENT ============
elements.append(P("YATIRIM TALEBİ", 'tag'))
elements.append(P(f'<font color="{PRIMARY}">25.000$</font> ile 12 Ayda Kâra Geçiş', 'h1'))
elements.append(S(12))

inv_data = [
    ['Kalem', 'Tutar', 'Oran', 'Açıklama'],
    ['Ürün Geliştirme', '$7.500', '%30', 'Backend, mobil uygulama, sunucu, SMS altyapısı'],
    ['Pazarlama', '$6.250', '%25', 'Saha ekibi, broşür, dijital reklam, etkinlikler'],
    ['İşletme Giderleri', '$5.000', '%20', 'Hosting, domain, API maliyetleri, ofis'],
    ['Yasal + Sigorta', '$3.750', '%15', 'Şirket kurulumu, R1 belgesi, avukat'],
    ['Yedek Fon', '$2.500', '%10', 'Beklenmedik durumlar'],
]
elements.append(make_table(inv_data, [140, 100, 80, 350]))
elements.append(S(16))

# Timeline
tl_data = [
    ['Q1 — Ay 1-3', 'Q2 — Ay 4-6', 'Q3 — Ay 7-9', 'Q4 — Ay 10-12'],
    [Paragraph(f'<font color="{TEXT_S}" size="9">Şirket kurulumu<br/>Mobil uygulama<br/>İlk 100 kullanıcı</font>', styles['small']),
     Paragraph(f'<font color="{TEXT_S}" size="9">500 kullanıcı<br/>50+ eşleşme/ay<br/>İlk gelirler</font>', styles['small']),
     Paragraph(f'<font color="{TEXT_S}" size="9">1.000 kullanıcı<br/>150+ eşleşme/ay<br/>Başabaş noktası</font>', styles['small']),
     Paragraph(f'<font color="{TEXT_S}" size="9">2.000+ kullanıcı<br/>200+ eşleşme/ay<br/><b><font color="{SUCCESS}">Kâra geçiş</font></b></font>', styles['small'])],
]
tlt = Table(tl_data, colWidths=[168, 168, 168, 168])
tlt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(SURFACE)),
    ('BOX', (0,0), (0,-1), 0.5, HexColor(BORDER)),
    ('BOX', (1,0), (1,-1), 0.5, HexColor(BORDER)),
    ('BOX', (2,0), (2,-1), 0.5, HexColor(BORDER)),
    ('BOX', (3,0), (3,-1), 0.5, HexColor(BORDER)),
    ('TEXTCOLOR', (0,0), (0,0), HexColor(PRIMARY)),
    ('TEXTCOLOR', (1,0), (1,0), HexColor(INFO)),
    ('TEXTCOLOR', (2,0), (2,0), HexColor('#f59e0b')),
    ('TEXTCOLOR', (3,0), (3,0), HexColor(SUCCESS)),
    ('FONTNAME', (0,0), (-1,0), 'Arial-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 10),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 12),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
]))
elements.append(tlt)
elements.append(P("Slayt 9/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 10: ROI ============
elements.append(P("YATIRIMCI GETİRİSİ", 'tag'))
elements.append(P(f'25.000$ Yatırıma <font color="{PRIMARY}">Ne Kazandırır?</font>', 'h1'))
elements.append(S(12))

scenarios = [
    ("Senaryo A", "Hisse Ortaklığı", "%20", "$25K → %20 hisse\n2. yılda şirket değeri\n$500K+ (4x getiri)", PRIMARY),
    ("Senaryo B — ÖNERİLEN", "Kâr Payı", "%25", "Net kârın %25'i (1. yıl)\nArdından %15 süresiz\nYıllık $5.000+ pasif gelir", SUCCESS),
    ("Senaryo C", "Borç + Bonus", "$28K+", "$25K geri ödeme\n+ kâr payı bonusu\n2 yılda $28K+ toplam", INFO),
]
sc_row = []
for tag_t, title, amount, desc, color in scenarios:
    sc_row.append(Paragraph(
        f'<para alignment="center">'
        f'<font color="{color}" size="7"><b>{tag_t.upper()}</b></font><br/><br/>'
        f'<b><font color="{TEXT}" size="12">{title}</font></b><br/><br/>'
        f'<font color="{color}" size="24"><b>{amount}</b></font><br/><br/>'
        f'<font color="{TEXT_S}" size="9">{desc.replace(chr(10), "<br/>")}</font></para>', styles['center']))

sct = Table([sc_row], colWidths=[220, 220, 220])
sct.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(SURFACE)),
    ('BOX', (0,0), (0,0), 1, HexColor(PRIMARY)),
    ('BOX', (1,0), (1,0), 1, HexColor(SUCCESS)),
    ('BOX', (2,0), (2,0), 1, HexColor(INFO)),
    ('TOPPADDING', (0,0), (-1,-1), 18),
    ('BOTTOMPADDING', (0,0), (-1,-1), 18),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
elements.append(sct)
elements.append(S(14))
elements.append(P(f'<para alignment="center"><font color="{TEXT_S}">• Tırport </font><b><font color="{TEXT}">$2M</font></b><font color="{TEXT_S}"> yatırım aldı — biz </font><b><font color="{PRIMARY}">$25K</font></b><font color="{TEXT_S}"> ile aynı pazarda, daha güçlü ürünle yarışıyoruz.</font></para>', 'center'))
elements.append(P("Slayt 10/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 11: WHY US ============
elements.append(P("NEDEN BU İŞ OLUR?", 'tag'))
elements.append(P(f'Bu İşi <font color="{PRIMARY}">Yapabilecek Konumdayız</font>', 'h1'))
elements.append(S(10))

why_data = [
    ['#', 'Güçlü Yön', 'Açıklama'],
    ['1', 'Problem Gerçek ve Acil', 'Uydurulmuş değil. Her sanayici, her nakliyeci yaşıyor.'],
    ['2', 'Ürün Hazır', 'Fikir aşamasını geçtik. Platform kodlandı, çalışıyor, demo var.'],
    ['3', 'Saha Avantajımız Var', "Sivas'ta sanayiciyi, nakliyeciyi tanıyoruz. Güven ağımız var."],
    ['4', 'Rakipler Buraya Bakmıyor', "Hepsi İstanbul odaklı. Anadolu'yu kimse dijitalleştirmedi."],
    ['5', 'Küçük Yatırımla Kâra Geçeriz', '$25K ile 12 ayda kârlı. Somut, ölçülebilir, test edilebilir.'],
]
why_style = [
    ('TEXTCOLOR', (0,1), (0,-1), HexColor(PRIMARY)),
    ('FONTNAME', (0,1), (0,-1), 'Arial-Bold'),
    ('FONTNAME', (1,1), (1,-1), 'Arial-Bold'),
]
elements.append(make_table(why_data, [40, 200, 420], why_style))
elements.append(S(14))

# Founder
founder_data = [[
    Paragraph(f'<para alignment="center"><font size="16"><b>TırBul</b></font><br/><br/>'
              f'<b><font color="{TEXT}" size="16">Ferhat Evci</font></b><br/>'
              f'<font color="{PRIMARY}" size="10"><b>Kurucu & CEO</b></font></para>', styles['center']),
    Paragraph(f'<font color="{TEXT_S}" size="10">'
              f'• Sivas\'ta sanayi esnafı<br/>'
              f'• Sahayı bilen girişimci<br/>'
              f'• Hırdavat sektörü deneyimi<br/>'
              f'• Yerel güven ağı<br/>'
              f'• Dijital ürün geliştirme yetkinliği<br/>'
              f'• E-ticaret deneyimi</font>', styles['body']),
]]
ft2 = Table(founder_data, colWidths=[220, 350])
ft2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor(SURFACE)),
    ('BOX', (0,0), (-1,-1), 0.5, HexColor('#2a1508')),
    ('TOPPADDING', (0,0), (-1,-1), 16),
    ('BOTTOMPADDING', (0,0), (-1,-1), 16),
    ('LEFTPADDING', (0,0), (-1,-1), 16),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
elements.append(ft2)
elements.append(P("Slayt 11/12", 'footer'))
elements.append(PageBreak())

# ============ SLIDE 12: CTA ============
elements.append(S(50))
elements.append(P("TırBul", 'title'))
elements.append(S(8))

ts = ParagraphStyle('bigtitle', fontName='Arial-Bold', fontSize=36, textColor=HexColor(PRIMARY), alignment=TA_CENTER)
elements.append(Paragraph("Birlikte Büyüyelim", ts))
elements.append(S(12))
elements.append(P("Sorun gerçek. Ürün hazır. Pazar devasa.<br/>Tek eksik: harekete geçmek.", 'center'))
elements.append(S(20))

cta_row = [[
    Paragraph(f'<para alignment="center"><font color="{PRIMARY}" size="18"><b>$25.000</b></font><br/><font color="{TEXT_S}" size="8">Yatırım</font></para>', styles['center']),
    Paragraph(f'<para alignment="center"><font color="{TEXT}" size="18"><b>12 Ay</b></font><br/><font color="{TEXT_S}" size="8">Kâra Geçiş</font></para>', styles['center']),
    Paragraph(f'<para alignment="center"><font color="{SUCCESS}" size="18"><b>4x</b></font><br/><font color="{TEXT_S}" size="8">Getiri Potansiyeli</font></para>', styles['center']),
]]
ctat = Table(cta_row, colWidths=[200, 200, 200])
ctat.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor('#120e08')),
    ('BOX', (0,0), (-1,-1), 1, HexColor(PRIMARY)),
    ('TOPPADDING', (0,0), (-1,-1), 16),
    ('BOTTOMPADDING', (0,0), (-1,-1), 16),
]))
elements.append(ctat)
elements.append(S(20))
elements.append(P(f'<b><font color="{TEXT}" size="14">TırBul</font></b><font color="{TEXT_S}" size="12"> — Güvenle taşı, güvenle teslim al.</font>', 'center'))
elements.append(S(8))
elements.append(P(f'<font color="{TEXT_S}">📞 Ferhat Evci  |  Sivas, Türkiye</font>', 'center'))
elements.append(P("Slayt 12/12", 'footer'))

# BUILD
doc.build(elements, onFirstPage=bg_draw, onLaterPages=bg_draw)
size = os.path.getsize(PDF_PATH)
print(f"✅ PDF başarıyla oluşturuldu!")
print(f"📄 Dosya: {PDF_PATH}")
print(f"📊 Boyut: {size / 1024:.0f} KB | 12 slayt")
