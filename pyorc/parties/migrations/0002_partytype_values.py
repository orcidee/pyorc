from django.db import migrations
from django.utils.translation import gettext_lazy as _


def forward(apps, schema_editor):
    PartyType = apps.get_model("parties", "PartyType")
    order = 0
    for name, codename, table, avail in [
        (_("Jeu de rôle"), "roleplay", True, True),
        (_("Jeu de plateau"), "boardgame", True, False),
        (_("GN'Idee"), "gnidee", False, False),
        (_("JDR'idée"), "jdridee", False, False),
        (_("Figurines"), "figures", True, False),
        (_("Animation"), "animation", False, False),
        (_("Autre"), "other", False, False),
    ]:
        PartyType.objects.create(
            name=name,
            codename=codename,
            is_table_number_required=table,
            is_availability_required=avail,
            order=order,
        )
        order += 1


def reverse(apps, schema_editor):
    PartyType = apps.get_model("parties", "PartyType")
    PartyType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('parties', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, reverse)
    ]
