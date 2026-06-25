from django.core.management.base import BaseCommand

from accounting.models import Account, FiscalYear


ACCOUNTS = [
    ("1000", "دارایی‌ها", Account.ASSET, None),
    ("1100", "بانک و صندوق", Account.ASSET, "1000"),
    ("1200", "حساب‌های دریافتنی", Account.ASSET, "1000"),
    ("2000", "بدهی‌ها", Account.LIABILITY, None),
    ("2100", "حساب‌های پرداختنی", Account.LIABILITY, "2000"),
    ("3000", "سرمایه", Account.EQUITY, None),
    ("4000", "درآمدها", Account.INCOME, None),
    ("4100", "درآمد خدمات نرم‌افزار", Account.INCOME, "4000"),
    ("4200", "درآمد دیتاسنتر و شبکه", Account.INCOME, "4000"),
    ("4300", "درآمد CIP و هوانوردی", Account.INCOME, "4000"),
    ("5000", "هزینه‌ها", Account.EXPENSE, None),
    ("5100", "هزینه حقوق و دستمزد", Account.EXPENSE, "5000"),
    ("5200", "هزینه زیرساخت و دیتاسنتر", Account.EXPENSE, "5000"),
    ("5300", "هزینه اداری و عمومی", Account.EXPENSE, "5000"),
]


class Command(BaseCommand):
    help = "Create basic accounting chart of accounts for Olkaa."

    def handle(self, *args, **options):
        created = 0
        account_by_code = {}
        for code, name, account_type, parent_code in ACCOUNTS:
            parent = account_by_code.get(parent_code) if parent_code else None
            account, was_created = Account.objects.get_or_create(
                code=code,
                defaults={"name": name, "account_type": account_type, "parent": parent},
            )
            account_by_code[code] = account
            created += int(was_created)

        FiscalYear.objects.get_or_create(
            title="سال مالی ۱۴۰۵",
            defaults={"start_date": "2026-03-21", "end_date": "2027-03-20"},
        )
        self.stdout.write(self.style.SUCCESS(f"Accounting seed complete. Created {created} account(s)."))
