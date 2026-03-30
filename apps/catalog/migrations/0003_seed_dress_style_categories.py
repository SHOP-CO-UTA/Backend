from django.db import migrations


def seed_dress_styles(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    rows = [
        ("Casual", "casual"),
        ("Formal", "formal"),
        ("Party", "party"),
        ("Gym", "gym"),
    ]
    for name, slug in rows:
        if not Category.objects.filter(slug=slug).exists():
            Category.objects.create(
                name=name,
                slug=slug,
                is_active=True,
                sort_order=0,
            )


def unseed_dress_styles(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Category.objects.filter(slug__in=["casual", "formal", "party", "gym"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_alter_category_options_remove_product_category_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_dress_styles, unseed_dress_styles),
    ]
