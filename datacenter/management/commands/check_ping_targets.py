import re
import subprocess
import sys

from django.core.management.base import BaseCommand

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


class Command(BaseCommand):
    help = "Ping active monitoring targets and store the latest status."

    def add_arguments(self, parser):
        parser.add_argument("--target", help="Check one host/name only.")
        parser.add_argument("--timeout", type=int, default=3)

    def handle(self, *args, **options):
        queryset = PingTarget.objects.filter(is_active=True)
        if options["target"]:
            queryset = queryset.filter(host=options["target"]) | queryset.filter(name=options["target"])

        checked = 0
        for target in queryset.distinct():
            result = check_target(target, timeout=options["timeout"])
            checked += 1
            self.stdout.write(f"{target.host}: {result.status} {result.latency_ms or '-'}ms")

        self.stdout.write(self.style.SUCCESS(f"Checked {checked} target(s)."))
