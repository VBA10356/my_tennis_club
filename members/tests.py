from django.test import TestCase
from django.urls import reverse

from .models import Member


class MemberListImageTests(TestCase):
    def test_member_without_image_shows_fallback(self):
        Member.objects.create(firstName="No", lastName="Image")

        response = self.client.get(reverse("members"))

        self.assertContains(response, "No image provided")

    def test_member_with_image_shows_image(self):
        Member.objects.create(
            firstName="Has",
            lastName="Image",
            image="member_images/hero.jpg",
        )

        response = self.client.get(reverse("members"))

        self.assertContains(
            response,
            '<img class="member-image" src="/media/member_images/hero.jpg"',
            html=False,
        )
