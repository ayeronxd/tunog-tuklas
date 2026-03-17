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
    
    # Coordinates for rendering on the map (percentages)
    pos_top = models.IntegerField(default=50, help_text="Y coordinate percentage (0-100)")
    pos_left = models.IntegerField(default=50, help_text="X coordinate percentage (0-100)")

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

class UserLevelProgress(models.Model):
    """
    Tracks a specific user's progress and stars for a specific level.
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='progress')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    
    is_unlocked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    stars_earned = models.IntegerField(default=0, help_text="Max 5 stars per level")

    class Meta:
        unique_together = ('account', 'level') # A user can only have one progress record per level

    def __str__(self):
        return f"{self.account.user.username} - {self.level.name} ({self.stars_earned} Stars)"
