from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone


LANGUAGES = {
    "fa": {
        "path": "",
        "dir": "rtl",
        "name": "فارسی",
        "title": "فاوا ایمن الکا | نرم افزار، هوانوردی، دیتاسنتر و تشریفات",
        "description": "فاوا ایمن الکا ارائه دهنده راهکارهای نرم افزاری، خدمات دیتاسنتر، اینترنت اختصاصی، اجاره IP و سرویس Home Check-in و CIP Express است.",
        "brand": "فاوا ایمن الکا",
        "hero": "سامانه یکپارچه فاوا ایمن الکا برای نرم افزار، عملیات و زیرساخت.",
        "lead": "یک هسته مشترک برای مدیریت مشتریان، امور مالی، خدمات دیتاسنتر، سامانه های هوانوردی و سرویس اختصاصی Home Check-in و CIP Express.",
        "nav": ["راهکارها", "CIP Express", "دیتاسنتر", "مشتریان", "دفاتر", "تماس"],
        "cta_primary": "مشاهده راهکارها",
        "cta_secondary": "سرویس اختصاصی",
        "employee": "ثبت نام کارمند",
        "solutions_title": "یک اکوسیستم برای نرم افزار، عملیات و زیرساخت",
        "solutions_text": "محصولات و خدمات فاوا ایمن الکا برای کسب و کارهایی طراحی شده که به اتصال دقیق میان مشتری، عملیات، مالی و شبکه نیاز دارند.",
        "signature_title": "Home Check-in & CIP Express",
        "signature_text": "پذیرش و تشریفات کامل مسافر از منزل یا هتل تا لحظه نشستن روی صندلی هواپیما؛ تجربه ای یکپارچه، بدون صف و بدون دغدغه.",
        "datacenter_title": "خدمات دیتاسنتر و شبکه",
        "datacenter_text": "زیرساخت قابل اتکا برای سازمان هایی که پایداری سرویس و کیفیت اتصال برایشان حیاتی است.",
        "clients_title": "همکاری با مجموعه های هوانوردی، دولتی، گردشگری و صنعتی",
        "clients_text": "نمونه ای از حوزه هایی که فاوا ایمن الکا در آن ها تجربه اجرای پروژه، پشتیبانی و توسعه راهکار دارد.",
        "contact_title": "آماده همکاری با شما هستیم",
        "contact_text": "برای دریافت دمو، بررسی نیاز سازمان یا شروع مذاکره درباره پروژه های نرم افزاری و زیرساختی با ما در ارتباط باشید.",
        "copyright": "© ۱۴۰۵ فاوا ایمن الکا",
        "offices": "تهران · کیش · فرودگاه امام",
    },
    "en": {
        "path": "en/",
        "dir": "ltr",
        "name": "English",
        "title": "Fava Emen Olka | Software, Aviation, Datacenter and CIP Services",
        "description": "Fava Emen Olka provides software platforms, aviation systems, datacenter services, dedicated internet, IPv4 leasing, Home Check-in and CIP Express services.",
        "brand": "Fava Emen Olka",
        "hero": "Integrated software, operations and infrastructure for organizations that need speed, accuracy and trust.",
        "lead": "A shared operating core for customer management, finance, datacenter services, aviation systems, Home Check-in and CIP Express.",
        "nav": ["Solutions", "CIP Express", "Datacenter", "Clients", "Offices", "Contact"],
        "cta_primary": "View solutions",
        "cta_secondary": "Signature service",
        "employee": "Employee signup",
        "solutions_title": "One ecosystem for software, operations and infrastructure",
        "solutions_text": "Fava Emen Olka products are designed for teams that need a precise connection between customers, operations, finance and network services.",
        "signature_title": "Home Check-in & CIP Express",
        "signature_text": "Complete passenger check-in and hospitality from home or hotel to the aircraft seat, without queues and operational friction.",
        "datacenter_title": "Datacenter and network services",
        "datacenter_text": "Reliable infrastructure for organizations where service availability and connectivity quality are mission critical.",
        "clients_title": "Trusted by aviation, public-sector, tourism and industrial organizations",
        "clients_text": "We deliver implementation, support and product development across aviation, hospitality, datacenter and enterprise operations.",
        "contact_title": "Ready to work with you",
        "contact_text": "Contact us for a demo, organizational needs assessment, or a conversation about software and infrastructure projects.",
        "copyright": "© 2026 Fava Emen Olka",
        "offices": "Tehran · Kish · Imam Khomeini Airport",
    },
    "ar": {
        "path": "ar/",
        "dir": "rtl",
        "name": "العربية",
        "title": "فاوا إمن أولكا | البرمجيات والطيران ومراكز البيانات وخدمات CIP",
        "description": "تقدم فاوا إمن أولكا منصات برمجية، أنظمة طيران، خدمات مراكز البيانات، إنترنت مخصص، تأجير IPv4 وخدمات Home Check-in وCIP Express.",
        "brand": "فاوا إمن أولكا",
        "hero": "منظومة متكاملة للبرمجيات والعمليات والبنية التحتية للمؤسسات التي تحتاج إلى الدقة والسرعة والأمان.",
        "lead": "نواة تشغيلية مشتركة لإدارة العملاء، المالية، خدمات مراكز البيانات، أنظمة الطيران، Home Check-in وCIP Express.",
        "nav": ["الحلول", "CIP Express", "مركز البيانات", "العملاء", "المكاتب", "اتصل بنا"],
        "cta_primary": "عرض الحلول",
        "cta_secondary": "الخدمة المميزة",
        "employee": "تسجيل الموظف",
        "solutions_title": "منظومة واحدة للبرمجيات والعمليات والبنية التحتية",
        "solutions_text": "صممت منتجات وخدمات فاوا إمن أولكا للمؤسسات التي تحتاج إلى ربط دقيق بين العملاء والعمليات والمالية والشبكات.",
        "signature_title": "Home Check-in & CIP Express",
        "signature_text": "خدمة استقبال وتشريفات كاملة للمسافر من المنزل أو الفندق حتى مقعد الطائرة، بدون طوابير وبأقل احتكاك تشغيلي.",
        "datacenter_title": "خدمات مراكز البيانات والشبكات",
        "datacenter_text": "بنية تحتية موثوقة للمؤسسات التي تعتمد على استقرار الخدمة وجودة الاتصال.",
        "clients_title": "ثقة قطاعات الطيران والحكومة والسياحة والصناعة",
        "clients_text": "نقدم التنفيذ والدعم وتطوير الحلول في الطيران والضيافة ومراكز البيانات والعمليات المؤسسية.",
        "contact_title": "جاهزون للتعاون معكم",
        "contact_text": "تواصلوا معنا للحصول على عرض توضيحي أو دراسة احتياجات المؤسسة أو بدء نقاش حول مشاريع البرمجيات والبنية التحتية.",
        "copyright": "© 2026 فاوا إمن أولكا",
        "offices": "طهران · كيش · مطار الإمام الخميني",
    },
}

COMMON = {
    "sections": ["solutions", "signature", "datacenter", "clients", "offices", "contact"],
    "meta": [("DOMAIN", "olkaa.ir"), ("OFFICES", None), ("IPV4 POOL", "64,000")],
    "solutions": [
        ("AVIATION", {"fa": "نرم افزار هوانوردی", "en": "Aviation software", "ar": "برمجيات الطيران"}),
        ("ACCOUNTING", {"fa": "نرم افزار حسابداری", "en": "Accounting software", "ar": "برمجيات المحاسبة"}),
        ("RMS", {"fa": "سامانه مدیریت درآمد", "en": "Revenue management", "ar": "إدارة الإيرادات"}),
        ("HOSPITALITY", {"fa": "نرم افزار هتل داری", "en": "Hospitality software", "ar": "برمجيات الفنادق"}),
    ],
    "solution_text": {
        "fa": "طراحی، استقرار و پشتیبانی راهکارهای عملیاتی برای سازمان های حساس به کیفیت سرویس.",
        "en": "Design, deployment and support for operational platforms where service quality matters.",
        "ar": "تصميم وتنفيذ ودعم حلول تشغيلية للمؤسسات التي تعتمد على جودة الخدمة.",
    },
    "steps": {
        "fa": ["پذیرش در محل", "تحویل و پلمب بار", "ترانسفر اختصاصی", "Fast Track", "لانژ اختصاصی CIP", "بدرقه تا هواپیما"],
        "en": ["On-site check-in", "Baggage sealing", "Private transfer", "Fast Track", "CIP lounge", "Aircraft escort"],
        "ar": ["تسجيل من الموقع", "استلام وختم الأمتعة", "نقل خاص", "مسار سريع", "صالة CIP", "مرافقة إلى الطائرة"],
    },
    "clients": {
        "fa": ["هوانوردی و فرودگاهی", "دولتی و سازمانی", "گردشگری و هتل داری", "صنعتی و خصوصی"],
        "en": ["Aviation and airports", "Public and enterprise", "Tourism and hospitality", "Industrial and private sector"],
        "ar": ["الطيران والمطارات", "القطاع الحكومي والمؤسسي", "السياحة والضيافة", "الصناعة والقطاع الخاص"],
    },
}


def _absolute(request, path):
    return request.build_absolute_uri(path)


def home(request, lang="fa"):
    content = LANGUAGES.get(lang, LANGUAGES["fa"])
    nav_pairs = list(zip(COMMON["sections"], content["nav"]))
    alternates = {
        code: _absolute(request, "/" + data["path"])
        for code, data in LANGUAGES.items()
    }
    canonical = alternates[lang]
    return render(
        request,
        "website/home_multilang.html",
        {
            "lang": lang,
            "content": content,
            "common": COMMON,
            "nav_pairs": nav_pairs,
            "canonical": canonical,
            "alternates": alternates,
        },
    )


def robots_txt(request):
    body = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /portal/",
            f"Sitemap: {request.build_absolute_uri(reverse('website:sitemap'))}",
            "",
        ]
    )
    return HttpResponse(body, content_type="text/plain")


def sitemap_xml(request):
    urls = [
        (code, request.build_absolute_uri("/" + data["path"]))
        for code, data in LANGUAGES.items()
    ]
    today = timezone.localdate().isoformat()
    items = []
    for _code, url in urls:
        links = "".join(
            f'<xhtml:link rel="alternate" hreflang="{alt_code}" href="{alt_url}" />'
            for alt_code, alt_url in urls
        )
        links += f'<xhtml:link rel="alternate" hreflang="x-default" href="{urls[0][1]}" />'
        items.append(
            "<url>"
            f"<loc>{url}</loc>"
            f"<lastmod>{today}</lastmod>"
            "<changefreq>weekly</changefreq>"
            "<priority>0.8</priority>"
            f"{links}"
            "</url>"
        )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        + "".join(items)
        + "</urlset>"
    )
    return HttpResponse(body, content_type="application/xml")
