import io

from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle


def generate_pdf(news):
    buffer = io.BytesIO()

    pdfmetrics.registerFont(TTFont('8483', f'{settings.BASE_DIR}/static/fonts/8483.ttf', 'utf-8'))
    style = ParagraphStyle(
        name='Normal',
        fontName='8483',
        fontSize=14,
    )
    style_red = ParagraphStyle(
        name='Normal',
        fontName='8483',
        fontSize=16,
        textColor="red"
    )
    style_green = ParagraphStyle(
        name='Normal',
        fontName='8483',
        fontSize=16,
        textColor="green"
    )
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    story = []
    for news_check in news:
        story.append(Paragraph(f"{news_check.title.upper()} ({news_check.user.username})", style))
        if news_check.is_fake:
            story.append(Paragraph("ФЕЙК", style_red))
        else:
            story.append(Paragraph("НЕ ФЕЙК", style_green))
        story.append(Paragraph(f"{news_check.body}<br /> <br />", style))

    doc.build(story)

    buffer.seek(0)
    return buffer

