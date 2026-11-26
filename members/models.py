from django.db import models
from django.utils.text import slugify

# Create your models here.
class Member(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    heroName = models.CharField(max_length=255, null = True)
    movie_year = models.IntegerField(null = True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

    def save(self, *args, **kwargs):
        base_slug = slugify(self.slug or f"{self.firstName}-{self.lastName}") or "member"
        max_length = self._meta.get_field("slug").max_length
        base_slug = base_slug[:max_length].rstrip("-") or "member"
        candidate = base_slug
        suffix = 2
        members = type(self)._default_manager.using(self._state.db or "default")
        existing = members.filter(slug=candidate)
        if self.pk:
            existing = existing.exclude(pk=self.pk)

        while existing.exists():
            suffix_text = f"-{suffix}"
            candidate = (
                f"{base_slug[:max_length - len(suffix_text)].rstrip('-')}{suffix_text}"
            )
            suffix += 1
            existing = members.filter(slug=candidate)
            if self.pk:
                existing = existing.exclude(pk=self.pk)

        self.slug = candidate
        super().save(*args, **kwargs)