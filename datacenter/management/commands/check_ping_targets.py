import re
import subprocess
import sys

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from datacenter.models import PingTarget


LATENCY_RE = re.compile(r"time[=<]\s*(\d+(?:\.\d+)?)\s*ms", re.IGNORECASE)


def _ping_command(host, timeout):
    if sys.platform.startswith("win"):
        return ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    return ["ping", "-c", "1", "-W", str(timeout), host]


def _latency_ms(output):
    match = LATENCY_RE.search(output)
    if not match:
        return None
    return max(1, round(float(match.group(1))))


def check_target(target, timeout=3):
    completed = subprocess.run(
        _ping_command(target.host, timeout),
        capture_output=True,
        text=True,
        timeout=timeout + 2,
        check=False,
    )
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part).strip()
    is_up = completed.returncode == 0
    return target.record_check(is_up=is_up, latency_ms=_latency_ms(output), output=output)


def _default_recipients():
    emails = getattr(settings, "MONITORING_ALERT_EMAILS", "")
    return [email.strip() for email in emails.split(",") if email.strip()]


def _send_alert(check):
    target = check.target
    recipients = target.alert_recipients or _default_recipients()
    if not recipients or not check.status_changed:
        return False

    if check.status == PingTarget.DOWN:
        subject = f"[OLKAA ALERT] {target.name} قطع شد"
        headline = "وضعیت سرویس قطع شد."
    else:
        subject = f"[OLKAA RECOVERY] {target.name} برگشت"
        headline = "وضعیت سرویس به حالت آنلاین برگشت."

    body = "\n".join(
        [
            headline,
            "",
            f"سرویس: {target.name}",
            f"Host/IP: {target.host}",
            f"نوع: {target.get_target_type_display()}",
            f"محیط: {target.get_environment_display()}",
            f"وضعیت: {check.get_status_display()}",
            f"تاخیر: {check.latency_ms or '-'} ms",
            f"تعداد خطای پیاپی: {target.failure_count}",
            f"مسئول: {target.support_owner or '-'}",
            f"راهنمای اقدام: {target.support_hint or '-'}",
            "",
            f"زمان: {timezone.localtime(check.created_at):%Y-%m-%d %H:%M:%S}",
        ]
    )
    sent = send_mail(subject, body, None, recipients, fail_silently=False)
    if sent:
        now = timezone.now()
        check.alert_sent_at = now
        check.save(update_fields=("alert_sent_at", "updated_at"))
        target.last_alert_sent_at = now
        target.save(update_fields=("last_alert_sent_at", "updated_at"))
    return bool(sent)


class Command(BaseCommand):
    help = "Ping active monitoring targets and store the latest status."

    def add_arguments(self, parser):
        parser.add_argument("--target", help="Check one host/name only.")
        parser.add_argument("--timeout", type=int, default=3)
        parser.add_argument("--no-email", action="store_true", help="Disable alert emails for this run.")

    def handle(self, *args, **options):
        queryset = PingTarget.objects.filter(is_active=True)
        if options["target"]:
            queryset = queryset.filter(host=options["target"]) | queryset.filter(name=options["target"])

        checked = 0
        for target in queryset.distinct():
            result = check_target(target, timeout=options["timeout"])
            if not options["no_email"]:
                try:
                    _send_alert(result)
                except Exception as error:
                    self.stderr.write(f"alert failed for {target.host}: {error}")
            checked += 1
            self.stdout.write(f"{target.host}: {result.status} {result.latency_ms or '-'}ms")

        self.stdout.write(self.style.SUCCESS(f"Checked {checked} target(s)."))
