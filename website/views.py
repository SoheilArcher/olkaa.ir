from django.http import Http404, HttpResponse
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
        "about_label": "درباره الکا",
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
        "about_label": "About",
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
        "about_label": "عن الشركة",
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

ABOUT_CONTENT = {
    "title": "درباره فاوا ایمن الکا | سایت رسمی olkaa.ir",
    "description": "فاوا ایمن الکا یک شرکت فناوری در حوزه نرم افزار سازمانی، شبکه، دیتاسنتر، اینترنت اختصاصی، هوانوردی و سرویس های CIP است. olkaa.ir سایت رسمی فاوا ایمن الکا است.",
    "headline": "فاوا ایمن الکا، شرکت فناوری برای نرم افزار، شبکه و عملیات حساس",
    "lead": "فاوا ایمن الکا با تمرکز بر راهکارهای نرم افزاری، خدمات دیتاسنتر، اینترنت اختصاصی، اجاره IP، سامانه های هوانوردی و سرویس های Home Check-in و CIP Express فعالیت می کند.",
    "facts": [
        ("نام رسمی", "فاوا ایمن الکا"),
        ("نام انگلیسی", "Fava Emen Olka"),
        ("دامنه رسمی", "olkaa.ir"),
        ("حوزه فعالیت", "نرم افزار، شبکه، دیتاسنتر، هوانوردی و خدمات CIP"),
        ("دفاتر", "تهران، کیش، فرودگاه امام خمینی"),
    ],
    "sections": [
        ("راهکارهای نرم افزاری", "طراحی و توسعه سامانه های سازمانی برای مدیریت مشتریان، عملیات، امور مالی، درآمد و فرایندهای داخلی."),
        ("شبکه و دیتاسنتر", "ارائه خدمات زیرساختی شامل اینترنت اختصاصی، پهنای باند، اجاره IPv4، مانیتورینگ و پشتیبانی سرویس."),
        ("هوانوردی و CIP", "توسعه و پشتیبانی سرویس های عملیاتی برای پذیرش مسافر، Home Check-in، تشریفات اختصاصی و تجربه فرودگاهی."),
    ],
}

SERVICE_PAGES = {
    "aviation-software": {
        "title": "نرم افزار هوانوردی | فاوا ایمن الکا",
        "description": "صفحه معرفی راهکارهای نرم افزار هوانوردی فاوا ایمن الکا برای فرایندهای عملیاتی، مسافری، گزارش گیری و هماهنگی سازمان های فرودگاهی و هوانوردی.",
        "eyebrow": "Aviation Software",
        "headline": "نرم افزار هوانوردی برای عملیات دقیق، سریع و قابل پیگیری",
        "lead": "فاوا ایمن الکا راهکارهای نرم افزاری مرتبط با عملیات هوانوردی، خدمات مسافر، گزارش گیری، هماهنگی واحدها و کنترل فرایندهای عملیاتی را بر اساس نیاز سازمان طراحی و توسعه می دهد.",
        "status": "In Development",
        "keywords": ["نرم افزار هوانوردی", "سامانه فرودگاهی", "Airport ERP", "خدمات مسافر", "عملیات فرودگاهی"],
        "audience": ["فرودگاه ها", "شرکت های خدمات فرودگاهی", "مجموعه های تشریفات", "واحدهای عملیات و گزارش گیری"],
        "features": [
            "مدیریت فرایندهای عملیاتی و هماهنگی واحدها",
            "ثبت، پیگیری و گزارش گیری از خدمات مسافر",
            "زیرساخت قابل توسعه برای اتصال به ماژول های مالی، CRM و تیکتینگ",
            "طراحی متناسب با نیاز سازمان و سطح دسترسی کاربران",
        ],
        "related": ["cip-express", "home-check-in"],
    },
    "datacenter": {
        "title": "خدمات دیتاسنتر و شبکه | فاوا ایمن الکا",
        "description": "خدمات دیتاسنتر فاوا ایمن الکا شامل زیرساخت شبکه، اینترنت اختصاصی، مانیتورینگ، پشتیبانی سرویس و مدیریت عملیات برای سازمان ها است.",
        "eyebrow": "Datacenter Services",
        "headline": "خدمات دیتاسنتر و شبکه برای سرویس های پایدار سازمانی",
        "lead": "زیرساخت شبکه و دیتاسنتر باید قابل مشاهده، قابل پیگیری و قابل پشتیبانی باشد. فاوا ایمن الکا خدمات زیرساختی را با تمرکز بر پایداری، مانیتورینگ و پاسخگویی عملیاتی ارائه می کند.",
        "status": "Production",
        "keywords": ["خدمات دیتاسنتر", "اینترنت اختصاصی", "مانیتورینگ سرور", "پشتیبانی شبکه", "دیتاسنتر سازمانی"],
        "audience": ["سازمان ها", "شرکت های فناوری", "مجموعه های دارای سرویس آنلاین", "تیم های شبکه و زیرساخت"],
        "features": [
            "اینترنت اختصاصی و سرویس های ارتباطی سازمانی",
            "مانیتورینگ اولیه سرورها و سرویس های حیاتی",
            "ثبت مسئول پشتیبانی و راهنمای اقدام برای هر سرویس",
            "قابلیت توسعه به گزارش گیری، هشدار و کنترل عملیات شبکه",
        ],
        "related": ["ipv4-leasing", "aviation-software"],
    },
    "ipv4-leasing": {
        "title": "اجاره IPv4 و مدیریت IP | فاوا ایمن الکا",
        "description": "معرفی خدمات اجاره IPv4 و مدیریت IP فاوا ایمن الکا برای سازمان هایی که به آدرس IP، پیگیری، ثبت و پشتیبانی شبکه نیاز دارند.",
        "eyebrow": "IPv4 Leasing",
        "headline": "اجاره IPv4 با مدیریت، ثبت و پشتیبانی عملیاتی",
        "lead": "فاوا ایمن الکا سرویس اجاره و مدیریت IP را به عنوان بخشی از خدمات زیرساختی و دیتاسنتر ارائه می کند تا استفاده از منابع شبکه قابل پیگیری و قابل مدیریت باشد.",
        "status": "Production",
        "keywords": ["اجاره IPv4", "اجاره IP", "IPv4 Leasing", "مدیریت IP", "IP سازمانی"],
        "audience": ["ارائه دهندگان سرویس", "شرکت های زیرساخت", "سازمان های دارای سرویس آنلاین", "تیم های شبکه"],
        "features": [
            "مدیریت بلوک های IP و وضعیت تخصیص",
            "ثبت اطلاعات سرویس، مشتری و دوره استفاده",
            "قابلیت اتصال به مالی و قراردادها در پورتال داخلی",
            "پشتیبانی عملیاتی برای پیگیری سرویس و منابع شبکه",
        ],
        "related": ["datacenter"],
    },
    "home-check-in": {
        "title": "Home Check-in | پذیرش مسافر در محل | فاوا ایمن الکا",
        "description": "Home Check-in فاوا ایمن الکا سرویس پذیرش مسافر در منزل یا هتل، هماهنگی بار، ترانسفر و اتصال به تشریفات فرودگاهی را معرفی می کند.",
        "eyebrow": "Home Check-in",
        "headline": "Home Check-in برای تجربه مسافر بدون صف و اصطکاک عملیاتی",
        "lead": "Home Check-in بخشی از سرویس های مسافری فاوا ایمن الکا است که فرایند پذیرش، هماهنگی بار، ترانسفر و اتصال به خدمات فرودگاهی را از محل مسافر تا فرودگاه منظم می کند.",
        "status": "In Development",
        "keywords": ["Home Check-in", "پذیرش در منزل", "پذیرش مسافر", "خدمات فرودگاهی", "CIP"],
        "audience": ["مسافران ویژه", "آژانس ها", "هتل ها", "شرکت های خدمات فرودگاهی"],
        "features": [
            "ثبت درخواست پذیرش در محل",
            "هماهنگی زمان، بار و اطلاعات مسافر",
            "اتصال به فرایند تشریفات و ترانسفر اختصاصی",
            "قابلیت توسعه به پنل مشتری، پرداخت و گزارش عملیاتی",
        ],
        "related": ["cip-express", "aviation-software"],
    },
    "cip-express": {
        "title": "CIP Express | خدمات تشریفات فرودگاهی | فاوا ایمن الکا",
        "description": "CIP Express فاوا ایمن الکا سرویس تشریفات فرودگاهی، Fast Track، لانژ اختصاصی، هماهنگی مسافر و تجربه سفر سازمان یافته را معرفی می کند.",
        "eyebrow": "CIP Express",
        "headline": "CIP Express برای تشریفات فرودگاهی منظم و قابل پیگیری",
        "lead": "CIP Express با هدف کاهش اصطکاک سفر و هماهنگی بهتر خدمات فرودگاهی طراحی شده است؛ از پذیرش و Fast Track تا لانژ، ترانسفر و بدرقه مسافر.",
        "status": "In Development",
        "keywords": ["CIP Express", "خدمات CIP", "تشریفات فرودگاهی", "Fast Track", "لانژ اختصاصی"],
        "audience": ["مسافران تجاری", "شرکت ها", "آژانس های گردشگری", "مجموعه های فرودگاهی"],
        "features": [
            "هماهنگی فرایند تشریفات و خدمات مسافر",
            "پشتیبانی از Fast Track و لانژ اختصاصی",
            "ثبت و پیگیری درخواست ها در ساختار عملیاتی",
            "قابلیت اتصال به Home Check-in و سامانه های مالی/CRM",
        ],
        "related": ["home-check-in", "aviation-software"],
    },
}

COMMON = {
    "sections": ["solutions", "signature", "datacenter", "clients", "offices", "contact"],
    "meta": [("DOMAIN", "olkaa.ir"), ("OFFICES", None), ("IPV4 POOL", "64,000")],
    "solutions": [
        ("AVIATION", {"fa": "نرم افزار هوانوردی", "en": "Aviation software", "ar": "برمجيات الطيران"}, "aviation-software"),
        ("DATACENTER", {"fa": "خدمات دیتاسنتر", "en": "Datacenter services", "ar": "خدمات مراكز البيانات"}, "datacenter"),
        ("IPV4", {"fa": "اجاره IPv4", "en": "IPv4 leasing", "ar": "تأجير IPv4"}, "ipv4-leasing"),
        ("CIP", {"fa": "CIP Express", "en": "CIP Express", "ar": "CIP Express"}, "cip-express"),
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
            "about_url": _absolute(request, reverse("website:about")),
        },
    )


def about(request):
    canonical = _absolute(request, reverse("website:about"))
    return render(
        request,
        "website/about.html",
        {
            "content": ABOUT_CONTENT,
            "canonical": canonical,
            "home_url": _absolute(request, reverse("website:home")),
        },
    )


def service_detail(request, slug):
    service = SERVICE_PAGES.get(slug)
    if not service:
        raise Http404("Service page not found")
    canonical = _absolute(request, reverse("website:service_detail", kwargs={"slug": slug}))
    related_services = [
        {**SERVICE_PAGES[related_slug], "slug": related_slug}
        for related_slug in service["related"]
        if related_slug in SERVICE_PAGES
    ]
    return render(
        request,
        "website/service_detail.html",
        {
            "canonical": canonical,
            "home_url": _absolute(request, reverse("website:home")),
            "service": service,
            "related_services": related_services,
            "slug": slug,
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
        (code, request.build_absolute_uri("/" + data["path"]), "1.0" if code == "fa" else "0.8")
        for code, data in LANGUAGES.items()
    ]
    urls.append(("fa-about", request.build_absolute_uri(reverse("website:about")), "0.9"))
    for slug in SERVICE_PAGES:
        urls.append(
            (
                f"service-{slug}",
                request.build_absolute_uri(reverse("website:service_detail", kwargs={"slug": slug})),
                "0.9",
            )
        )
    today = timezone.localdate().isoformat()
    items = []
    language_urls = urls[: len(LANGUAGES)]
    for code, url, priority in urls:
        links = "".join(
            f'<xhtml:link rel="alternate" hreflang="{alt_code}" href="{alt_url}" />'
            for alt_code, alt_url, _priority in language_urls
        ) if code in LANGUAGES else ""
        links += f'<xhtml:link rel="alternate" hreflang="x-default" href="{language_urls[0][1]}" />' if code in LANGUAGES else ""
        items.append(
            "<url>"
            f"<loc>{url}</loc>"
            f"<lastmod>{today}</lastmod>"
            "<changefreq>weekly</changefreq>"
            f"<priority>{priority}</priority>"
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
