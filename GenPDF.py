__author__ = 'Administrator'
#coding:cp936

#for setup error:No module named _fontdata_enc_winansi
from reportlab.pdfbase import _fontdata_enc_winansi
from reportlab.pdfbase import _fontdata_enc_macroman
from reportlab.pdfbase import _fontdata_enc_standard
from reportlab.pdfbase import _fontdata_enc_symbol
from reportlab.pdfbase import _fontdata_enc_zapfdingbats
from reportlab.pdfbase import _fontdata_enc_pdfdoc
from reportlab.pdfbase import _fontdata_enc_macexpert
from reportlab.pdfbase import _fontdata_widths_courier
from reportlab.pdfbase import _fontdata_widths_courierbold
from reportlab.pdfbase import _fontdata_widths_courieroblique
from reportlab.pdfbase import _fontdata_widths_courierboldoblique
from reportlab.pdfbase import _fontdata_widths_helvetica
from reportlab.pdfbase import _fontdata_widths_helveticabold
from reportlab.pdfbase import _fontdata_widths_helveticaoblique
from reportlab.pdfbase import _fontdata_widths_helveticaboldoblique
from reportlab.pdfbase import _fontdata_widths_timesroman
from reportlab.pdfbase import _fontdata_widths_timesbold
from reportlab.pdfbase import _fontdata_widths_timesitalic
from reportlab.pdfbase import _fontdata_widths_timesbolditalic
from reportlab.pdfbase import _fontdata_widths_symbol
from reportlab.pdfbase import _fontdata_widths_zapfdingbats

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

MyFont = 'simsun.ttc'
MyFontName = 'song'

def my_convert(str):
    return str.decode('gb2312').encode('utf-8')

def GenPDF(filename, classified_product_list, Specified_Order):
    pdfmetrics.registerFont(TTFont(MyFontName, MyFont))
    elements = []
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename)
    styles['Title'].fontName = MyFontName
    elements.append(Paragraph(my_convert("清单"), styles['Title']))
    data = [
        [my_convert('货号'), my_convert('商品名称'), my_convert('颜色'), my_convert('尺码'), my_convert('数量'), my_convert('分配')]
    ]

    for prefix in Specified_Order:
        for product in classified_product_list[prefix]:
            temp = []
            temp.append(product['ProductNum'])
            temp.append(product['ProductName'])
            str = product['Property'].split('|')
            temp.append(str[1])
            temp.append(str[0])
            temp.append(product['Quantity'])
            temp.append(product['DistributionStr'])
            data.append(temp)

    table = Table(
        data=data,
        colWidths=[
            2.75 * cm, 7.5 * cm, 2.75 * cm, 2.5 * cm, 1.0 * cm, 2.5 * cm
        ]
    )
    table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), MyFontName),
        ('ALIGN', (0,0), (5,0), 'CENTER'),
        ('ALIGN', (0,1), (1,-1), 'LEFT'),
        ('ALIGN', (2,1), (5,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)

