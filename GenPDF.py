__author__ = 'Administrator'
#coding:cp936

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

MyFont = 'simsun.ttc'
MyFontName = 'song'

def GenPDF(filename, classified_product_list, Specified_Order):
    pdfmetrics.registerFont(TTFont(MyFontName, MyFont))
    elements = []
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename)
    styles['Title'].fontName = MyFontName
    elements.append(Paragraph("清单", styles['Title']))
    data = [
        ['货号', '商品名称', '颜色', '尺码', '数量']
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
            data.append(temp)

    table = Table(
        data=data,
        colWidths=[
            2.75 * cm, 10.0 * cm, 2.75 * cm, 2.5 * cm, 1.0 * cm
        ]
    )
    table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), MyFontName),
        ('ALIGN', (0,0), (4,0), 'CENTER'),
        ('ALIGN', (0,1), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)

