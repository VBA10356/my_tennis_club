from django.db import migrations, models
from django.utils.text import slugify


def populate_member_slugs(apps, schema_editor):
    Member = apps.get_model("members", "Member")
    database = schema_editor.connection.alias
    used_slugs = set()

    for member in Member.objects.using(database).order_by("pk").iterator():
        base_slug = slugify(member.slug or f"{member.firstName}-{member.lastName}")
        base_slug = base_slug[:50].rstrip("-") or f"member-{member.pk}"
        candidate = base_slug
        suffix = 2

        while candidate in used_slugs:
            suffix_text = f"-{suffix}"
            candidate = (
                f"{base_slug[:50 - len(suffix_text)].rstrip('-')}{suffix_text}"
            )
            suffix += 1

        if member.slug != candidate:
            Member.objects.using(database).filter(pk=member.pk).update(
                slug=candidate
            )
        used_slugs.add(candidate)


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0003_member_slug"),
    ]

    operations = [
        migrations.RunPython(
            populate_member_slugs,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="member",
            name="slug",
            field=models.SlugField(blank=True, max_length=50, unique=True),
        ),
    ]
