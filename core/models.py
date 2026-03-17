from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    """
    Profile extension for the default Django User model.
    Stores additional player-specific data.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    stars = models.IntegerField(default=0)
    # Add other profile fields here as needed (e.g. avatar, nickname)

    def __str__(self):
        return self.user.username

class Level(models.Model):
    """
    Represents a game level or stage (e.g. Level 1, Level 2).
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    required_stars = models.IntegerField(default=0)
    order = models.IntegerField(default=0) # For sorting levels

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Material(models.Model):
    """
    Category or type of learning material (e.g. Letter A, Letter B).
    """
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_locked = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} (Level: {self.level.name})"

class MaterialContent(models.Model):
    """
    The actual content data associated with a Material.
    """
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=50, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ], default='text')
    content_data = models.TextField() # Can store text, file paths, or JSON
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.material.title} - Content {self.order}"
