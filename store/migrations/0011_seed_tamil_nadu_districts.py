from decimal import Decimal

from django.db import migrations

from store.models import TAMIL_NADU_DISTRICTS


def seed_tamil_nadu_districts(apps, schema_editor):
    DistrictDeliveryCharge = apps.get_model("store", "DistrictDeliveryCharge")
    if DistrictDeliveryCharge.objects.exists():
        return
    DistrictDeliveryCharge.objects.bulk_create(
        [
            DistrictDeliveryCharge(name=name, charge=Decimal("50.00"), is_active=True)
            for name in TAMIL_NADU_DISTRICTS
        ],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_category_offer_percentage_category_price_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_tamil_nadu_districts, migrations.RunPython.noop),
    ]
