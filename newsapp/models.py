from django.db import models

class Article(models.Model):
    section = models.CharField(max_length=50)
    english_title = models.TextField()
    urdu_title = models.TextField()
    english_content = models.TextField()
    urdu_content = models.TextField()
    url = models.URLField(unique=True)   # ✅ this is required for checking duplicates
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.english_title
