from django.db import models

# Blog Post model
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Blog Comment model
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

    def is_parent(self):
        return self.parent is None

# Video feature model (Tech, Conspiracy, Personal)
class Video(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Tech of the Week'),
        ('conspiracy', 'Conspiracy Spotlight'),
        ('personal', 'Personal Projects'),
    ]

    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

    def save(self, *args, **kwargs):
        if 'youtu.be/' in self.youtube_url:
            self.youtube_url = self.youtube_url.replace(
                'https://youtu.be/', 'https://www.youtube-nocookie.com/embed/'
            )
        elif 'watch?v=' in self.youtube_url:
            video_id = self.youtube_url.split('watch?v=')[1].split('&')[0]
            self.youtube_url = f'https://www.youtube-nocookie.com/embed/{video_id}'
        super().save(*args, **kwargs)

# Conspiracy Vault content model
class VaultLink(models.Model):
    CATEGORY_CHOICES = [
        ('ufo', 'UFOs / UAPs'),
        ('cia', 'CIA & Surveillance'),
        ('psyops', 'Psychological Ops'),
        ('censorship', 'Censorship & Big Tech'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    download = models.FileField(upload_to='vault_downloads/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
