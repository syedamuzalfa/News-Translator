from django.shortcuts import render
from .models import Article
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from .models import Article

# def home(request):
#     articles = Article.objects.order_by("-created_at")[:20]
#     return render(request, "newsapp/home.html", {"articles": articles})



from datetime import timedelta
from django.utils.timezone import now


def home(request):
    today = now().date()

    editorials = Article.objects.filter(
        section="Editorial", created_at__date=today
    ).order_by("-created_at")

    opinions = Article.objects.filter(
        section="Opinion", created_at__date=today
    ).order_by("-created_at")

    return render(request, "newsapp/home.html", {
        "editorials": editorials,
        "opinions": opinions,
    })


def archive(request):
    yesterday = now().date() - timedelta(days=1)

    editorials = Article.objects.filter(
        section="Editorial", created_at__date=yesterday
    ).order_by("-created_at")

    opinions = Article.objects.filter(
        section="Opinion", created_at__date=yesterday
    ).order_by("-created_at")

    return render(request, "newsapp/archive.html", {
        "editorials": editorials,
        "opinions": opinions,
    })



# Register Urdu font (Noto Nastaliq or a similar Unicode font)
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))  # For Urdu justification

def download_pdf(request, article_id):
    article = Article.objects.get(id=article_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{article.english_title[:50]}.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    # Custom styles
    english_style = ParagraphStyle(
        "English",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        alignment=TA_JUSTIFY,
    )

    urdu_style = ParagraphStyle(
        "Urdu",
        parent=styles["Normal"],
        fontName="HeiseiMin-W3",
        fontSize=14,
        leading=18,
        alignment=TA_JUSTIFY,
    )

    story = []
    story.append(Paragraph(f"<b>{article.english_title}</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(article.english_content.replace("\n", "<br/>"), english_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>{article.urdu_title}</b>", urdu_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(article.urdu_content.replace("\n", "<br/>"), urdu_style))

    doc.build(story)
    return response
