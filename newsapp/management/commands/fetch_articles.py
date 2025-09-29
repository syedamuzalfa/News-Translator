# newsapp/management/commands/fetch_articles.py

import time
from django.core.management.base import BaseCommand
from newsapp.models import Article
from newsapp.utils import get_article_links, get_article_content, translate_text, SECTIONS
from django.utils.timezone import now
from datetime import timedelta

# Delete older than 10 days
cutoff_date = now() - timedelta(days=3)
Article.objects.filter(created_at__lt=cutoff_date).delete()


class Command(BaseCommand):
    help = "Fetch and translate Dawn Editorial & Opinion articles"

    def handle(self, *args, **kwargs):
        for section_name, url in SECTIONS.items():
            self.stdout.write(self.style.NOTICE(f"📡 Fetching {section_name}..."))
            links = get_article_links(url)

            new_count = 0
            for link in links:
                # Skip if already saved
                if Article.objects.filter(url=link).exists():
                    continue

                article = get_article_content(link)
                if article and article["content"]:
                    try:
                        urdu_title = translate_text(article["title"])
                        urdu_content = translate_text(article["content"])

                        Article.objects.create(
                            section=section_name,
                            english_title=article["title"],
                            urdu_title=urdu_title,
                            english_content=article["content"],
                            urdu_content=urdu_content,
                            url=link
                        )
                        new_count += 1
                        self.stdout.write(self.style.SUCCESS(f"✅ Saved: {article['title']}"))

                        # be polite with Dawn server
                        time.sleep(1)

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"⚠️ Error saving {link}: {e}"))

            self.stdout.write(self.style.SUCCESS(
                f"🎉 {section_name}: {new_count} new articles added"
            ))
