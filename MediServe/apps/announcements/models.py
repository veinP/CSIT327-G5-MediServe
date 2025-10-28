from django.db import models

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tblannouncements'
        managed = True  # Changed to True to allow Django migrations

    def __str__(self):
        return self.title