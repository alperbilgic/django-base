# Generated by Django 4.2.11 on 2024-04-15 12:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),
        ("common", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Buyable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("restored_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=64)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("ADP", "ADP"),
                            ("AED", "AED"),
                            ("AFA", "AFA"),
                            ("AFN", "AFN"),
                            ("ALK", "ALK"),
                            ("ALL", "ALL"),
                            ("AMD", "AMD"),
                            ("ANG", "ANG"),
                            ("AOA", "AOA"),
                            ("AOK", "AOK"),
                            ("AON", "AON"),
                            ("AOR", "AOR"),
                            ("ARA", "ARA"),
                            ("ARL", "ARL"),
                            ("ARM", "ARM"),
                            ("ARP", "ARP"),
                            ("ARS", "ARS"),
                            ("ATS", "ATS"),
                            ("AUD", "AUD"),
                            ("AWG", "AWG"),
                            ("AZM", "AZM"),
                            ("AZN", "AZN"),
                            ("BAD", "BAD"),
                            ("BAM", "BAM"),
                            ("BAN", "BAN"),
                            ("BBD", "BBD"),
                            ("BDT", "BDT"),
                            ("BEC", "BEC"),
                            ("BEF", "BEF"),
                            ("BEL", "BEL"),
                            ("BGL", "BGL"),
                            ("BGM", "BGM"),
                            ("BGN", "BGN"),
                            ("BGO", "BGO"),
                            ("BHD", "BHD"),
                            ("BIF", "BIF"),
                            ("BMD", "BMD"),
                            ("BND", "BND"),
                            ("BOB", "BOB"),
                            ("BOL", "BOL"),
                            ("BOP", "BOP"),
                            ("BOV", "BOV"),
                            ("BRB", "BRB"),
                            ("BRC", "BRC"),
                            ("BRE", "BRE"),
                            ("BRL", "BRL"),
                            ("BRN", "BRN"),
                            ("BRR", "BRR"),
                            ("BRZ", "BRZ"),
                            ("BSD", "BSD"),
                            ("BTN", "BTN"),
                            ("BUK", "BUK"),
                            ("BWP", "BWP"),
                            ("BYB", "BYB"),
                            ("BYN", "BYN"),
                            ("BYR", "BYR"),
                            ("BZD", "BZD"),
                            ("CAD", "CAD"),
                            ("CDF", "CDF"),
                            ("CHE", "CHE"),
                            ("CHF", "CHF"),
                            ("CHW", "CHW"),
                            ("CLE", "CLE"),
                            ("CLF", "CLF"),
                            ("CLP", "CLP"),
                            ("CNH", "CNH"),
                            ("CNX", "CNX"),
                            ("CNY", "CNY"),
                            ("COP", "COP"),
                            ("COU", "COU"),
                            ("CRC", "CRC"),
                            ("CSD", "CSD"),
                            ("CSK", "CSK"),
                            ("CUC", "CUC"),
                            ("CUP", "CUP"),
                            ("CVE", "CVE"),
                            ("CYP", "CYP"),
                            ("CZK", "CZK"),
                            ("DDM", "DDM"),
                            ("DEM", "DEM"),
                            ("DJF", "DJF"),
                            ("DKK", "DKK"),
                            ("DOP", "DOP"),
                            ("DZD", "DZD"),
                            ("ECS", "ECS"),
                            ("ECV", "ECV"),
                            ("EEK", "EEK"),
                            ("EGP", "EGP"),
                            ("ERN", "ERN"),
                            ("ESA", "ESA"),
                            ("ESB", "ESB"),
                            ("ESP", "ESP"),
                            ("ETB", "ETB"),
                            ("EUR", "EUR"),
                            ("FIM", "FIM"),
                            ("FJD", "FJD"),
                            ("FKP", "FKP"),
                            ("FRF", "FRF"),
                            ("GBP", "GBP"),
                            ("GEK", "GEK"),
                            ("GEL", "GEL"),
                            ("GHC", "GHC"),
                            ("GHS", "GHS"),
                            ("GIP", "GIP"),
                            ("GMD", "GMD"),
                            ("GNF", "GNF"),
                            ("GNS", "GNS"),
                            ("GQE", "GQE"),
                            ("GRD", "GRD"),
                            ("GTQ", "GTQ"),
                            ("GWE", "GWE"),
                            ("GWP", "GWP"),
                            ("GYD", "GYD"),
                            ("HKD", "HKD"),
                            ("HNL", "HNL"),
                            ("HRD", "HRD"),
                            ("HRK", "HRK"),
                            ("HTG", "HTG"),
                            ("HUF", "HUF"),
                            ("IDR", "IDR"),
                            ("IEP", "IEP"),
                            ("ILP", "ILP"),
                            ("ILR", "ILR"),
                            ("ILS", "ILS"),
                            ("IMP", "IMP"),
                            ("INR", "INR"),
                            ("IQD", "IQD"),
                            ("IRR", "IRR"),
                            ("ISJ", "ISJ"),
                            ("ISK", "ISK"),
                            ("ITL", "ITL"),
                            ("JMD", "JMD"),
                            ("JOD", "JOD"),
                            ("JPY", "JPY"),
                            ("KES", "KES"),
                            ("KGS", "KGS"),
                            ("KHR", "KHR"),
                            ("KMF", "KMF"),
                            ("KPW", "KPW"),
                            ("KRH", "KRH"),
                            ("KRO", "KRO"),
                            ("KRW", "KRW"),
                            ("KWD", "KWD"),
                            ("KYD", "KYD"),
                            ("KZT", "KZT"),
                            ("LAK", "LAK"),
                            ("LBP", "LBP"),
                            ("LKR", "LKR"),
                            ("LRD", "LRD"),
                            ("LSL", "LSL"),
                            ("LTL", "LTL"),
                            ("LTT", "LTT"),
                            ("LUC", "LUC"),
                            ("LUF", "LUF"),
                            ("LUL", "LUL"),
                            ("LVL", "LVL"),
                            ("LVR", "LVR"),
                            ("LYD", "LYD"),
                            ("MAD", "MAD"),
                            ("MAF", "MAF"),
                            ("MCF", "MCF"),
                            ("MDC", "MDC"),
                            ("MDL", "MDL"),
                            ("MGA", "MGA"),
                            ("MGF", "MGF"),
                            ("MKD", "MKD"),
                            ("MKN", "MKN"),
                            ("MLF", "MLF"),
                            ("MMK", "MMK"),
                            ("MNT", "MNT"),
                            ("MOP", "MOP"),
                            ("MRO", "MRO"),
                            ("MRU", "MRU"),
                            ("MTL", "MTL"),
                            ("MTP", "MTP"),
                            ("MUR", "MUR"),
                            ("MVP", "MVP"),
                            ("MVR", "MVR"),
                            ("MWK", "MWK"),
                            ("MXN", "MXN"),
                            ("MXP", "MXP"),
                            ("MXV", "MXV"),
                            ("MYR", "MYR"),
                            ("MZE", "MZE"),
                            ("MZM", "MZM"),
                            ("MZN", "MZN"),
                            ("NAD", "NAD"),
                            ("NGN", "NGN"),
                            ("NIC", "NIC"),
                            ("NIO", "NIO"),
                            ("NLG", "NLG"),
                            ("NOK", "NOK"),
                            ("NPR", "NPR"),
                            ("NZD", "NZD"),
                            ("OMR", "OMR"),
                            ("PAB", "PAB"),
                            ("PEI", "PEI"),
                            ("PEN", "PEN"),
                            ("PES", "PES"),
                            ("PGK", "PGK"),
                            ("PHP", "PHP"),
                            ("PKR", "PKR"),
                            ("PLN", "PLN"),
                            ("PLZ", "PLZ"),
                            ("PTE", "PTE"),
                            ("PYG", "PYG"),
                            ("QAR", "QAR"),
                            ("RHD", "RHD"),
                            ("ROL", "ROL"),
                            ("RON", "RON"),
                            ("RSD", "RSD"),
                            ("RUB", "RUB"),
                            ("RUR", "RUR"),
                            ("RWF", "RWF"),
                            ("SAR", "SAR"),
                            ("SBD", "SBD"),
                            ("SCR", "SCR"),
                            ("SDD", "SDD"),
                            ("SDG", "SDG"),
                            ("SDP", "SDP"),
                            ("SEK", "SEK"),
                            ("SGD", "SGD"),
                            ("SHP", "SHP"),
                            ("SIT", "SIT"),
                            ("SKK", "SKK"),
                            ("SLE", "SLE"),
                            ("SLL", "SLL"),
                            ("SOS", "SOS"),
                            ("SRD", "SRD"),
                            ("SRG", "SRG"),
                            ("SSP", "SSP"),
                            ("STD", "STD"),
                            ("STN", "STN"),
                            ("SUR", "SUR"),
                            ("SVC", "SVC"),
                            ("SYP", "SYP"),
                            ("SZL", "SZL"),
                            ("THB", "THB"),
                            ("TJR", "TJR"),
                            ("TJS", "TJS"),
                            ("TMM", "TMM"),
                            ("TMT", "TMT"),
                            ("TND", "TND"),
                            ("TOP", "TOP"),
                            ("TPE", "TPE"),
                            ("TRL", "TRL"),
                            ("TRY", "TRY"),
                            ("TTD", "TTD"),
                            ("TVD", "TVD"),
                            ("TWD", "TWD"),
                            ("TZS", "TZS"),
                            ("UAH", "UAH"),
                            ("UAK", "UAK"),
                            ("UGS", "UGS"),
                            ("UGX", "UGX"),
                            ("USD", "USD"),
                            ("USN", "USN"),
                            ("USS", "USS"),
                            ("UYI", "UYI"),
                            ("UYP", "UYP"),
                            ("UYU", "UYU"),
                            ("UYW", "UYW"),
                            ("UZS", "UZS"),
                            ("VEB", "VEB"),
                            ("VED", "VED"),
                            ("VEF", "VEF"),
                            ("VES", "VES"),
                            ("VND", "VND"),
                            ("VNN", "VNN"),
                            ("VUV", "VUV"),
                            ("WST", "WST"),
                            ("XAF", "XAF"),
                            ("XAG", "XAG"),
                            ("XAU", "XAU"),
                            ("XBA", "XBA"),
                            ("XBB", "XBB"),
                            ("XBC", "XBC"),
                            ("XBD", "XBD"),
                            ("XCD", "XCD"),
                            ("XDR", "XDR"),
                            ("XEU", "XEU"),
                            ("XFO", "XFO"),
                            ("XFU", "XFU"),
                            ("XOF", "XOF"),
                            ("XPD", "XPD"),
                            ("XPF", "XPF"),
                            ("XPT", "XPT"),
                            ("XRE", "XRE"),
                            ("XSU", "XSU"),
                            ("XTS", "XTS"),
                            ("XUA", "XUA"),
                            ("XXX", "XXX"),
                            ("YDD", "YDD"),
                            ("YER", "YER"),
                            ("YUD", "YUD"),
                            ("YUM", "YUM"),
                            ("YUN", "YUN"),
                            ("YUR", "YUR"),
                            ("ZAL", "ZAL"),
                            ("ZAR", "ZAR"),
                            ("ZMK", "ZMK"),
                            ("ZMW", "ZMW"),
                            ("ZRN", "ZRN"),
                            ("ZRZ", "ZRZ"),
                            ("ZWD", "ZWD"),
                            ("ZWL", "ZWL"),
                            ("ZWN", "ZWN"),
                            ("ZWR", "ZWR"),
                        ],
                        default="TRY",
                        max_length=8,
                    ),
                ),
                (
                    "period",
                    models.CharField(
                        choices=[
                            ("monthly", "Monthly"),
                            ("semi_annual", "Semi Annual"),
                            ("annual", "Annual"),
                        ],
                        default="monthly",
                        max_length=64,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("corporate_subscription", "Corporate Subscription"),
                            ("personal_subscription", "Personal Subscription"),
                            ("one_time_purchase", "One Time Purchase"),
                        ],
                        default="personal_subscription",
                        max_length=64,
                    ),
                ),
                (
                    "trial_days",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("created", utils.fields.DateTimeWithoutTZField(auto_now_add=True)),
                ("updated", utils.fields.DateTimeWithoutTZField(auto_now=True)),
                (
                    "deleted_at",
                    utils.fields.DateTimeWithoutTZField(blank=True, null=True),
                ),
                (
                    "description",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="described_buyables",
                        to="common.translation",
                    ),
                ),
                (
                    "special_offer_root",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"special_offer_root__isnull": True},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="special_offers",
                        to="payment.buyable",
                    ),
                ),
                (
                    "title",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="titled_buyables",
                        to="common.translation",
                    ),
                ),
            ],
            options={
                "db_table": "buyable",
            },
        ),
        migrations.CreateModel(
            name="Purchase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("restored_at", models.DateTimeField(blank=True, null=True)),
                (
                    "stored_payment_method_id",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("vendor", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "original_transaction_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created", utils.fields.DateTimeWithoutTZField(auto_now_add=True)),
                ("updated", utils.fields.DateTimeWithoutTZField(auto_now=True)),
                (
                    "deleted_at",
                    utils.fields.DateTimeWithoutTZField(blank=True, null=True),
                ),
            ],
            options={
                "db_table": "purchase",
            },
        ),
        migrations.CreateModel(
            name="PurchasedBuyable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("restored_at", models.DateTimeField(blank=True, null=True)),
                (
                    "quantity",
                    models.IntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                ("created", utils.fields.DateTimeWithoutTZField(auto_now_add=True)),
                ("updated", utils.fields.DateTimeWithoutTZField(auto_now=True)),
                (
                    "deleted_at",
                    utils.fields.DateTimeWithoutTZField(blank=True, null=True),
                ),
                (
                    "buyable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase_buyables",
                        to="payment.buyable",
                    ),
                ),
                (
                    "purchase",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase_buyables",
                        to="payment.purchase",
                    ),
                ),
            ],
            options={
                "db_table": "purchase_buyable",
            },
        ),
        migrations.AddField(
            model_name="purchase",
            name="buyables",
            field=models.ManyToManyField(
                related_name="purchases",
                through="payment.PurchasedBuyable",
                to="payment.buyable",
            ),
        ),
        migrations.AddField(
            model_name="purchase",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="purchases",
                to="user.user",
            ),
        ),
        migrations.CreateModel(
            name="PaymentTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("restored_at", models.DateTimeField(blank=True, null=True)),
                (
                    "list_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "charge_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "credit_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("payment_vendor", models.CharField(max_length=64)),
                ("payment_method", models.CharField(max_length=64)),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("ADP", "ADP"),
                            ("AED", "AED"),
                            ("AFA", "AFA"),
                            ("AFN", "AFN"),
                            ("ALK", "ALK"),
                            ("ALL", "ALL"),
                            ("AMD", "AMD"),
                            ("ANG", "ANG"),
                            ("AOA", "AOA"),
                            ("AOK", "AOK"),
                            ("AON", "AON"),
                            ("AOR", "AOR"),
                            ("ARA", "ARA"),
                            ("ARL", "ARL"),
                            ("ARM", "ARM"),
                            ("ARP", "ARP"),
                            ("ARS", "ARS"),
                            ("ATS", "ATS"),
                            ("AUD", "AUD"),
                            ("AWG", "AWG"),
                            ("AZM", "AZM"),
                            ("AZN", "AZN"),
                            ("BAD", "BAD"),
                            ("BAM", "BAM"),
                            ("BAN", "BAN"),
                            ("BBD", "BBD"),
                            ("BDT", "BDT"),
                            ("BEC", "BEC"),
                            ("BEF", "BEF"),
                            ("BEL", "BEL"),
                            ("BGL", "BGL"),
                            ("BGM", "BGM"),
                            ("BGN", "BGN"),
                            ("BGO", "BGO"),
                            ("BHD", "BHD"),
                            ("BIF", "BIF"),
                            ("BMD", "BMD"),
                            ("BND", "BND"),
                            ("BOB", "BOB"),
                            ("BOL", "BOL"),
                            ("BOP", "BOP"),
                            ("BOV", "BOV"),
                            ("BRB", "BRB"),
                            ("BRC", "BRC"),
                            ("BRE", "BRE"),
                            ("BRL", "BRL"),
                            ("BRN", "BRN"),
                            ("BRR", "BRR"),
                            ("BRZ", "BRZ"),
                            ("BSD", "BSD"),
                            ("BTN", "BTN"),
                            ("BUK", "BUK"),
                            ("BWP", "BWP"),
                            ("BYB", "BYB"),
                            ("BYN", "BYN"),
                            ("BYR", "BYR"),
                            ("BZD", "BZD"),
                            ("CAD", "CAD"),
                            ("CDF", "CDF"),
                            ("CHE", "CHE"),
                            ("CHF", "CHF"),
                            ("CHW", "CHW"),
                            ("CLE", "CLE"),
                            ("CLF", "CLF"),
                            ("CLP", "CLP"),
                            ("CNH", "CNH"),
                            ("CNX", "CNX"),
                            ("CNY", "CNY"),
                            ("COP", "COP"),
                            ("COU", "COU"),
                            ("CRC", "CRC"),
                            ("CSD", "CSD"),
                            ("CSK", "CSK"),
                            ("CUC", "CUC"),
                            ("CUP", "CUP"),
                            ("CVE", "CVE"),
                            ("CYP", "CYP"),
                            ("CZK", "CZK"),
                            ("DDM", "DDM"),
                            ("DEM", "DEM"),
                            ("DJF", "DJF"),
                            ("DKK", "DKK"),
                            ("DOP", "DOP"),
                            ("DZD", "DZD"),
                            ("ECS", "ECS"),
                            ("ECV", "ECV"),
                            ("EEK", "EEK"),
                            ("EGP", "EGP"),
                            ("ERN", "ERN"),
                            ("ESA", "ESA"),
                            ("ESB", "ESB"),
                            ("ESP", "ESP"),
                            ("ETB", "ETB"),
                            ("EUR", "EUR"),
                            ("FIM", "FIM"),
                            ("FJD", "FJD"),
                            ("FKP", "FKP"),
                            ("FRF", "FRF"),
                            ("GBP", "GBP"),
                            ("GEK", "GEK"),
                            ("GEL", "GEL"),
                            ("GHC", "GHC"),
                            ("GHS", "GHS"),
                            ("GIP", "GIP"),
                            ("GMD", "GMD"),
                            ("GNF", "GNF"),
                            ("GNS", "GNS"),
                            ("GQE", "GQE"),
                            ("GRD", "GRD"),
                            ("GTQ", "GTQ"),
                            ("GWE", "GWE"),
                            ("GWP", "GWP"),
                            ("GYD", "GYD"),
                            ("HKD", "HKD"),
                            ("HNL", "HNL"),
                            ("HRD", "HRD"),
                            ("HRK", "HRK"),
                            ("HTG", "HTG"),
                            ("HUF", "HUF"),
                            ("IDR", "IDR"),
                            ("IEP", "IEP"),
                            ("ILP", "ILP"),
                            ("ILR", "ILR"),
                            ("ILS", "ILS"),
                            ("IMP", "IMP"),
                            ("INR", "INR"),
                            ("IQD", "IQD"),
                            ("IRR", "IRR"),
                            ("ISJ", "ISJ"),
                            ("ISK", "ISK"),
                            ("ITL", "ITL"),
                            ("JMD", "JMD"),
                            ("JOD", "JOD"),
                            ("JPY", "JPY"),
                            ("KES", "KES"),
                            ("KGS", "KGS"),
                            ("KHR", "KHR"),
                            ("KMF", "KMF"),
                            ("KPW", "KPW"),
                            ("KRH", "KRH"),
                            ("KRO", "KRO"),
                            ("KRW", "KRW"),
                            ("KWD", "KWD"),
                            ("KYD", "KYD"),
                            ("KZT", "KZT"),
                            ("LAK", "LAK"),
                            ("LBP", "LBP"),
                            ("LKR", "LKR"),
                            ("LRD", "LRD"),
                            ("LSL", "LSL"),
                            ("LTL", "LTL"),
                            ("LTT", "LTT"),
                            ("LUC", "LUC"),
                            ("LUF", "LUF"),
                            ("LUL", "LUL"),
                            ("LVL", "LVL"),
                            ("LVR", "LVR"),
                            ("LYD", "LYD"),
                            ("MAD", "MAD"),
                            ("MAF", "MAF"),
                            ("MCF", "MCF"),
                            ("MDC", "MDC"),
                            ("MDL", "MDL"),
                            ("MGA", "MGA"),
                            ("MGF", "MGF"),
                            ("MKD", "MKD"),
                            ("MKN", "MKN"),
                            ("MLF", "MLF"),
                            ("MMK", "MMK"),
                            ("MNT", "MNT"),
                            ("MOP", "MOP"),
                            ("MRO", "MRO"),
                            ("MRU", "MRU"),
                            ("MTL", "MTL"),
                            ("MTP", "MTP"),
                            ("MUR", "MUR"),
                            ("MVP", "MVP"),
                            ("MVR", "MVR"),
                            ("MWK", "MWK"),
                            ("MXN", "MXN"),
                            ("MXP", "MXP"),
                            ("MXV", "MXV"),
                            ("MYR", "MYR"),
                            ("MZE", "MZE"),
                            ("MZM", "MZM"),
                            ("MZN", "MZN"),
                            ("NAD", "NAD"),
                            ("NGN", "NGN"),
                            ("NIC", "NIC"),
                            ("NIO", "NIO"),
                            ("NLG", "NLG"),
                            ("NOK", "NOK"),
                            ("NPR", "NPR"),
                            ("NZD", "NZD"),
                            ("OMR", "OMR"),
                            ("PAB", "PAB"),
                            ("PEI", "PEI"),
                            ("PEN", "PEN"),
                            ("PES", "PES"),
                            ("PGK", "PGK"),
                            ("PHP", "PHP"),
                            ("PKR", "PKR"),
                            ("PLN", "PLN"),
                            ("PLZ", "PLZ"),
                            ("PTE", "PTE"),
                            ("PYG", "PYG"),
                            ("QAR", "QAR"),
                            ("RHD", "RHD"),
                            ("ROL", "ROL"),
                            ("RON", "RON"),
                            ("RSD", "RSD"),
                            ("RUB", "RUB"),
                            ("RUR", "RUR"),
                            ("RWF", "RWF"),
                            ("SAR", "SAR"),
                            ("SBD", "SBD"),
                            ("SCR", "SCR"),
                            ("SDD", "SDD"),
                            ("SDG", "SDG"),
                            ("SDP", "SDP"),
                            ("SEK", "SEK"),
                            ("SGD", "SGD"),
                            ("SHP", "SHP"),
                            ("SIT", "SIT"),
                            ("SKK", "SKK"),
                            ("SLE", "SLE"),
                            ("SLL", "SLL"),
                            ("SOS", "SOS"),
                            ("SRD", "SRD"),
                            ("SRG", "SRG"),
                            ("SSP", "SSP"),
                            ("STD", "STD"),
                            ("STN", "STN"),
                            ("SUR", "SUR"),
                            ("SVC", "SVC"),
                            ("SYP", "SYP"),
                            ("SZL", "SZL"),
                            ("THB", "THB"),
                            ("TJR", "TJR"),
                            ("TJS", "TJS"),
                            ("TMM", "TMM"),
                            ("TMT", "TMT"),
                            ("TND", "TND"),
                            ("TOP", "TOP"),
                            ("TPE", "TPE"),
                            ("TRL", "TRL"),
                            ("TRY", "TRY"),
                            ("TTD", "TTD"),
                            ("TVD", "TVD"),
                            ("TWD", "TWD"),
                            ("TZS", "TZS"),
                            ("UAH", "UAH"),
                            ("UAK", "UAK"),
                            ("UGS", "UGS"),
                            ("UGX", "UGX"),
                            ("USD", "USD"),
                            ("USN", "USN"),
                            ("USS", "USS"),
                            ("UYI", "UYI"),
                            ("UYP", "UYP"),
                            ("UYU", "UYU"),
                            ("UYW", "UYW"),
                            ("UZS", "UZS"),
                            ("VEB", "VEB"),
                            ("VED", "VED"),
                            ("VEF", "VEF"),
                            ("VES", "VES"),
                            ("VND", "VND"),
                            ("VNN", "VNN"),
                            ("VUV", "VUV"),
                            ("WST", "WST"),
                            ("XAF", "XAF"),
                            ("XAG", "XAG"),
                            ("XAU", "XAU"),
                            ("XBA", "XBA"),
                            ("XBB", "XBB"),
                            ("XBC", "XBC"),
                            ("XBD", "XBD"),
                            ("XCD", "XCD"),
                            ("XDR", "XDR"),
                            ("XEU", "XEU"),
                            ("XFO", "XFO"),
                            ("XFU", "XFU"),
                            ("XOF", "XOF"),
                            ("XPD", "XPD"),
                            ("XPF", "XPF"),
                            ("XPT", "XPT"),
                            ("XRE", "XRE"),
                            ("XSU", "XSU"),
                            ("XTS", "XTS"),
                            ("XUA", "XUA"),
                            ("XXX", "XXX"),
                            ("YDD", "YDD"),
                            ("YER", "YER"),
                            ("YUD", "YUD"),
                            ("YUM", "YUM"),
                            ("YUN", "YUN"),
                            ("YUR", "YUR"),
                            ("ZAL", "ZAL"),
                            ("ZAR", "ZAR"),
                            ("ZMK", "ZMK"),
                            ("ZMW", "ZMW"),
                            ("ZRN", "ZRN"),
                            ("ZRZ", "ZRZ"),
                            ("ZWD", "ZWD"),
                            ("ZWL", "ZWL"),
                            ("ZWN", "ZWN"),
                            ("ZWR", "ZWR"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "tax_rate",
                    models.DecimalField(decimal_places=3, default=0, max_digits=5),
                ),
                ("payer_id", models.CharField(blank=True, max_length=255, null=True)),
                ("ip_address", models.CharField(blank=True, max_length=64)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("initial", "Initial"),
                            ("pending", "Pending"),
                            ("stale", "Stale"),
                            ("canceled", "Canceled"),
                            ("reverted", "Reverted"),
                            ("failed", "Failed"),
                            ("succeeded", "Succeeded"),
                        ],
                        default="initial",
                        max_length=32,
                    ),
                ),
                (
                    "transaction_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("receipt", models.JSONField(blank=True, null=True)),
                ("raw_product_data", models.JSONField()),
                ("created", utils.fields.DateTimeWithoutTZField(auto_now_add=True)),
                ("updated", utils.fields.DateTimeWithoutTZField(auto_now=True)),
                (
                    "deleted_at",
                    utils.fields.DateTimeWithoutTZField(blank=True, null=True),
                ),
                (
                    "purchase",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="payment_transactions",
                        to="payment.purchase",
                    ),
                ),
            ],
            options={
                "db_table": "payment_transaction",
            },
        ),
        migrations.AddConstraint(
            model_name="paymenttransaction",
            constraint=models.UniqueConstraint(
                condition=models.Q(("deleted_at__isnull", True)),
                fields=("payment_vendor", "transaction_id"),
                name="unique_payment_transaction_payment_vendor_key_transaction_id_if_not_deleted",
            ),
        ),
        migrations.AddConstraint(
            model_name="buyable",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("type", "one_time_purchase"),
                    models.Q(
                        models.Q(("type", "one_time_purchase"), _negated=True),
                        ("period__isnull", False),
                    ),
                    _connector="OR",
                ),
                name="subscription_period_not_null_constraint",
            ),
        ),
        migrations.AddConstraint(
            model_name="buyable",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("type", "one_time_purchase"),
                    models.Q(
                        models.Q(("type", "one_time_purchase"), _negated=True),
                        ("trial_days__isnull", False),
                    ),
                    _connector="OR",
                ),
                name="subscription_trial_days_not_null_constraint",
            ),
        ),
        migrations.AddConstraint(
            model_name="buyable",
            constraint=models.UniqueConstraint(
                condition=models.Q(("deleted_at__isnull", True)),
                fields=("name",),
                name="unique_buyable_name_key_if_not_deleted",
            ),
        ),
    ]
