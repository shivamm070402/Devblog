from django.db import models
from django.contrib.auth.models import User
import math


# Emoji + gradient palette per category
CATEGORY_STYLES = {
    'system-design': ('🏗️', 'linear-gradient(135deg,#667eea,#764ba2)'),
    'technology':    ('💻', 'linear-gradient(135deg,#6c63ff,#48c6ef)'),
    'sports':        ('🏏', 'linear-gradient(135deg,#e74c3c,#f39c12)'),
    'health':        ('💚', 'linear-gradient(135deg,#2ecc71,#1abc9c)'),
    'travel':        ('✈️',  'linear-gradient(135deg,#2980b9,#6dd5fa)'),
}
DEFAULT_EMOJI    = '📝'
DEFAULT_GRADIENT = 'linear-gradient(135deg,#8e9eab,#eef2f3)'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title      = models.CharField(max_length=250)
    slug       = models.SlugField(max_length=250, unique_for_date='created_at')
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category   = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='posts')
    body       = models.TextField()
    image      = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True, null=True)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes  = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.title

    def get_excerpt(self, length=200):
        return self.body[:length] + '…' if len(self.body) > length else self.body

    @property
    def reading_time(self):
        """Average reading speed: 200 wpm."""
        word_count = len(self.body.split())
        return max(1, math.ceil(word_count / 200))

    @property
    def card_emoji(self):
        slug = self.category.slug if self.category else ''
        return CATEGORY_STYLES.get(slug, (DEFAULT_EMOJI, DEFAULT_GRADIENT))[0]

    @property
    def card_gradient(self):
        slug = self.category.slug if self.category else ''
        return CATEGORY_STYLES.get(slug, (DEFAULT_EMOJI, DEFAULT_GRADIENT))[1]

    @property
    def has_diagrams(self):
        return '```diagram' in self.body or '<svg' in self.body
