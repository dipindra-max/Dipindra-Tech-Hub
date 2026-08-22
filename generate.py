#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TechPulse Hub — static site generator.
Produces every HTML page (home, blog index, 5 articles, about, contact,
privacy policy, terms, 404) plus sitemap.xml from the data + content
defined below. Pure Python standard library only.

Usage:  python3 generate.py
Output: writes .html files into the project root / posts folder.
"""
import os, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_NAME = "TechPulse Hub"
SITE_URL = "https://www.techpulsehub.com"  # CHANGE before deploying (see README)
SITE_DESC = "Practical, no-fluff guides on gadgets, software, and consumer tech."
AUTHOR = "TechPulse Hub Editorial Team"
YEAR = datetime.datetime.now().year
TODAY = datetime.date.today().isoformat()

def render(tpl, **kw):
    for k, v in kw.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    return tpl

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)

# ---------------------------------------------------------------------
# Shared HEAD / HEADER / FOOTER
# ---------------------------------------------------------------------

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESCRIPTION}}">
<meta name="keywords" content="{{KEYWORDS}}">
<meta name="author" content="{{AUTHOR}}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{{CANONICAL}}">

<!-- Open Graph -->
<meta property="og:type" content="{{OGTYPE}}">
<meta property="og:site_name" content="{{SITE_NAME}}">
<meta property="og:title" content="{{TITLE}}">
<meta property="og:description" content="{{DESCRIPTION}}">
<meta property="og:url" content="{{CANONICAL}}">
<meta property="og:image" content="{{OGIMAGE}}">
<meta property="og:locale" content="en_US">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{TITLE}}">
<meta name="twitter:description" content="{{DESCRIPTION}}">
<meta name="twitter:image" content="{{OGIMAGE}}">

<link rel="icon" href="{{ROOT}}images/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ROOT}}css/style.css">

<!--
  GOOGLE ADSENSE: once your AdSense account is approved, uncomment the
  line below and replace ca-pub-XXXXXXXXXXXXXXXX with your publisher ID.
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
-->

{{JSONLD}}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<progress class="reading-bar" value="0" max="100" aria-hidden="true"></progress>
"""

HEADER = """<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{{ROOT}}index.html">
      <span class="brand-mark">TP</span> Tech<span class="dot">Pulse</span> Hub
    </a>
    <button class="nav-toggle" aria-label="Toggle navigation menu" aria-expanded="false">☰ Menu</button>
    <nav class="main-nav">
      <a href="{{ROOT}}index.html" class="{{A_HOME}}">Home</a>
      <a href="{{ROOT}}blog.html" class="{{A_BLOG}}">Blog</a>
      <a href="{{ROOT}}about.html" class="{{A_ABOUT}}">About</a>
      <a href="{{ROOT}}contact.html" class="{{A_CONTACT}}">Contact</a>
    </nav>
  </div>
</header>
"""

FOOTER = """<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <div class="brand" style="color:#fff;margin-bottom:10px;"><span class="brand-mark">TP</span> TechPulse Hub</div>
      <p class="small" style="color:#9aa2b7;max-width:34ch;">Practical, no-fluff guides on gadgets, software, and consumer tech — written by people who actually use the stuff.</p>
    </div>
    <div>
      <h4>Explore</h4>
      <a href="{{ROOT}}index.html">Home</a>
      <a href="{{ROOT}}blog.html">Blog</a>
      <a href="{{ROOT}}about.html">About</a>
      <a href="{{ROOT}}contact.html">Contact</a>
    </div>
    <div>
      <h4>Categories</h4>
      <a href="{{ROOT}}blog.html#software">Software</a>
      <a href="{{ROOT}}blog.html#hardware">Hardware</a>
      <a href="{{ROOT}}blog.html#smart-home">Smart Home</a>
      <a href="{{ROOT}}blog.html#networking">Networking</a>
    </div>
    <div>
      <h4>Legal</h4>
      <a href="{{ROOT}}privacy-policy.html">Privacy Policy</a>
      <a href="{{ROOT}}terms.html">Terms of Service</a>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>&copy; <span data-year>{{YEAR}}</span> TechPulse Hub. All rights reserved.</span>
    <span>Built with care for readers, not just clicks.</span>
  </div>
</footer>
<script src="{{ROOT}}js/main.js"></script>
</body>
</html>
"""

def page(title, description, keywords, canonical_path, body_html, ogtype="website",
         active="", jsonld="", root_prefix="", ogimage=None):
    canonical = SITE_URL.rstrip("/") + "/" + canonical_path.lstrip("/")
    ogimg = ogimage or (SITE_URL.rstrip("/") + "/images/og-default.svg")
    head = render(HEAD, TITLE=title, DESCRIPTION=description, KEYWORDS=keywords,
                  AUTHOR=AUTHOR, CANONICAL=canonical, OGTYPE=ogtype, SITE_NAME=SITE_NAME,
                  OGIMAGE=ogimg, ROOT=root_prefix, JSONLD=jsonld)
    header = render(HEADER, ROOT=root_prefix,
                     A_HOME="active" if active == "home" else "",
                     A_BLOG="active" if active == "blog" else "",
                     A_ABOUT="active" if active == "about" else "",
                     A_CONTACT="active" if active == "contact" else "")
    footer = render(FOOTER, ROOT=root_prefix, YEAR=str(YEAR))
    return head + header + body_html + footer

# ---------------------------------------------------------------------
# Post data
# ---------------------------------------------------------------------
POSTS = [
    {
        "slug": "best-chrome-extensions-productivity-2026",
        "title": "10 Must-Have Chrome Extensions for Productivity in 2026",
        "description": "A hands-on, curated list of the 10 Chrome extensions actually worth installing in 2026 for focus, writing, tab management, and privacy.",
        "category": "Software",
        "category_id": "software",
        "read_time": "9 min read",
        "date": "2026-01-12",
        "keywords": "chrome extensions 2026, best productivity extensions, browser tools for work, tab management extension, focus extension chrome",
        "excerpt": "We tested dozens of extensions so you don't have to. Here are the ten that actually earn a permanent spot in your toolbar.",
    },
    {
        "slug": "how-to-choose-laptop-for-programming-2026",
        "title": "How to Choose the Right Laptop for Programming in 2026",
        "description": "A practical buyer's guide to picking a programming laptop in 2026: how much RAM you really need, CPU vs. battery trade-offs, and picks by use case.",
        "category": "Hardware",
        "category_id": "hardware",
        "read_time": "11 min read",
        "date": "2026-01-19",
        "keywords": "best laptop for programming 2026, laptop for developers, coding laptop specs, RAM for programming, laptop buying guide",
        "excerpt": "Specs on a spec sheet don't tell you how a laptop feels after six hours of compiling. Here's what actually matters.",
    },
    {
        "slug": "understanding-ai-chips-explained",
        "title": "Understanding AI Chips: What Makes a Processor 'AI-Ready'?",
        "description": "NPUs, TOPS, and AI PCs explained in plain English — what an AI chip actually does differently from a regular CPU, and whether you need one.",
        "category": "Hardware",
        "category_id": "hardware",
        "read_time": "10 min read",
        "date": "2026-01-27",
        "keywords": "what is an NPU, AI chip explained, AI PC meaning, TOPS processor, do I need an AI laptop",
        "excerpt": "Every new laptop ad mentions an 'AI chip.' Here's what that silicon actually does, and when it matters for you.",
    },
    {
        "slug": "smart-home-setup-guide-2026",
        "title": "The Complete Guide to Setting Up a Smart Home in 2026",
        "description": "A step-by-step smart home setup guide covering hubs, Matter compatibility, security cameras, and the most common beginner mistakes to avoid.",
        "category": "Smart Home",
        "category_id": "smart-home",
        "read_time": "13 min read",
        "date": "2026-02-03",
        "keywords": "smart home setup guide, Matter smart home standard, best smart home hub 2026, home automation for beginners, smart home devices",
        "excerpt": "You don't need forty apps and a weekend of frustration. Here's how to build a smart home that actually works together.",
    },
    {
        "slug": "5g-vs-wifi-7-which-do-you-need",
        "title": "5G vs. Wi-Fi 7: Which Wireless Tech Do You Actually Need?",
        "description": "5G and Wi-Fi 7 solve different problems. This guide breaks down real-world speed, latency, and cost differences so you know which one is worth paying for.",
        "category": "Networking",
        "category_id": "networking",
        "read_time": "8 min read",
        "date": "2026-02-10",
        "keywords": "5G vs Wi-Fi 7, wifi 7 explained, do I need wifi 7 router, 5G home internet vs wifi, wireless standards comparison",
        "excerpt": "They get compared constantly, but 5G and Wi-Fi 7 aren't really competing. Here's what each one is actually for.",
    },
]

print("Post metadata ready:", len(POSTS))

# ---------------------------------------------------------------------
# Article bodies (full, original content)
# ---------------------------------------------------------------------
ARTICLE_CONTENT = {}

ARTICLE_CONTENT["best-chrome-extensions-productivity-2026"] = """
<p>Your browser toolbar is prime real estate. Every extension you install competes for memory, permissions, and your attention — so it should earn its spot. We spent several weeks running a rotating set of over 40 extensions across research, writing, and day-to-day browsing to see which ones actually changed how we worked, rather than just looking useful in a screenshot.</p>
<p>Here are the ten that survived the cut, organized by the problem they solve.</p>

<h2 id="focus">Focus and distraction control</h2>

<h3>1. Tab suspender for memory and focus</h3>
<p>If you're the type of person with 40 tabs open "for later," a tab suspender pays for itself within a day. It automatically unloads inactive tabs from memory after a set period, which keeps your browser fast without forcing you to actually close anything. The best ones let you whitelist sites (so your music player or a live dashboard never gets suspended) and restore a tab instantly on click.</p>

<h3>2. A strict site blocker with scheduling</h3>
<p>Blocklists only work if they're hard to turn off mid-craving. Look for an extension that supports scheduled blocking (e.g., news and social sites blocked 9am–5pm on weekdays) and a "lock" mode that prevents you from disabling it for a set number of minutes, even if you try.</p>

<h2 id="writing">Writing and communication</h2>

<h3>3. A grammar and clarity checker</h3>
<p>Real-time grammar checking has gotten good enough that it catches genuine clarity issues, not just typos — passive voice, run-on sentences, and repeated words. Enable it selectively; running it on every code comment box gets old fast, so pick one that lets you toggle it per-site.</p>

<h3>4. A text expander</h3>
<p>This is the most underrated productivity extension category. Typing a short trigger like <code>;addr</code> to expand into your full mailing address, or <code>;sig</code> for an email signature, saves minutes every single day across dozens of small repeated tasks — support replies, standup updates, meeting invites.</p>

<h3>5. A read-later / reader-view tool</h3>
<p>Save articles to read distraction-free, later, on your own schedule, instead of reading them immediately (badly) the moment you find them. The reader-view strip-down also removes autoplay video and pop-up newsletter prompts, which is reason enough to install one.</p>

<h2 id="tabs">Tab and window management</h2>

<h3>6. Tab grouping by project</h3>
<p>Chrome's built-in tab groups are good, but a dedicated extension adds saved sessions — so you can close "Project A: 12 tabs" entirely and reopen the exact same set tomorrow with one click. This alone eliminates the anxiety of closing tabs you're "not done with yet."</p>

<h3>7. A quick screenshot and annotation tool</h3>
<p>For anyone who reports bugs, writes documentation, or shares feedback on designs, a one-click full-page screenshot tool with basic arrow/text annotation removes an entire round trip to a separate app.</p>

<h2 id="privacy">Privacy and security</h2>

<h3>8. A tracker and ad blocker</h3>
<p>Beyond blocking ads, a good tracker blocker meaningfully speeds up page loads, since a large share of a typical news site's load time is third-party tracking scripts, not the article itself.</p>

<h3>9. A password manager extension</h3>
<p>If you're still reusing passwords because remembering unique ones is a hassle, a password manager extension removes the excuse entirely — it generates and autofills strong, unique passwords per site. This is one of the highest-leverage security habits available to anyone.</p>

<h3>10. An HTTPS enforcer</h3>
<p>Some older or smaller sites still default to unencrypted HTTP. An extension that automatically upgrades connections to HTTPS when available adds a layer of protection with essentially zero downside.</p>

<h2 id="setup-tips">Setup tips that actually matter</h2>
<ul>
  <li><strong>Audit your extensions quarterly.</strong> Open <code>chrome://extensions</code> and remove anything you haven't used in 90 days — each one is a permissions surface, not just clutter.</li>
  <li><strong>Check requested permissions before installing.</strong> A simple screenshot tool asking for "read and change all your data on all websites" is a red flag worth investigating in the reviews.</li>
  <li><strong>Prefer extensions with recent update history.</strong> An extension untouched for two years is more likely to be abandoned — or worse, sold to a new owner who monetizes it differently.</li>
</ul>

<blockquote>The best productivity tool is the one you forget you're using. If an extension requires daily conscious effort to benefit from, it's adding friction, not removing it.</blockquote>

<h2 id="faq">Frequently asked questions</h2>
<h3>Do more extensions slow down Chrome?</h3>
<p>Yes, but the effect varies enormously by extension. A well-built tab suspender can make Chrome faster overall, while a poorly optimized ad-heavy extension can slow it down noticeably. Memory usage under <code>chrome://extensions</code> (with "Details" expanded) is the best way to check.</p>
<h3>Are free extensions safe to use?</h3>
<p>Many excellent extensions are free and safe, but "free" sometimes means the business model is selling browsing data. Stick to extensions with transparent developers, clear privacy policies, and a healthy volume of recent, detailed reviews.</p>
"""

ARTICLE_CONTENT["how-to-choose-laptop-for-programming-2026"] = """
<p>Buying a laptop for programming is different from buying one for general use, but it's also easier than the spec-sheet marketing makes it seem. You don't need the most expensive machine on the shelf — you need the right balance of memory, sustained performance, keyboard comfort, and battery life for how you actually work.</p>

<h2 id="ram">How much RAM do you actually need?</h2>
<p>RAM is the single most common bottleneck for developers, because it's consumed by your editor, your browser (with its own dozens of tabs), any local containers or virtual machines, and background services — all at once.</p>
<table>
<tr><th>Use case</th><th>Realistic minimum</th><th>Comfortable</th></tr>
<tr><td>Web development, scripting</td><td>16GB</td><td>16–32GB</td></tr>
<tr><td>Mobile app development (with emulators)</td><td>16GB</td><td>32GB</td></tr>
<tr><td>Running Docker containers locally</td><td>16GB</td><td>32GB+</td></tr>
<tr><td>Data science / local ML experimentation</td><td>16GB</td><td>32–64GB</td></tr>
</table>
<p>If you're deciding between spending extra on RAM or on CPU speed, RAM usually wins for day-to-day comfort — running out of memory causes swapping, which is far more disruptive than a slightly slower CPU.</p>

<h2 id="cpu">CPU: cores, sustained performance, and thermals</h2>
<p>Core count matters most for parallel workloads: compiling large codebases, running test suites, or building containers. But raw core count on a spec sheet is misleading if the laptop can't sustain that performance without overheating and throttling. Thin-and-light laptops often hit their thermal ceiling within minutes under sustained compile loads, dropping clock speeds noticeably. If your work includes long compile times or heavy builds, prioritize laptops with reputations for good sustained (not just peak burst) performance.</p>

<h2 id="battery">Battery life vs. raw power</h2>
<p>This is the classic trade-off, and it's worth being honest with yourself about which side you're on:</p>
<ul>
  <li><strong>If you mostly work from a desk with power nearby</strong>, prioritize a more powerful chip and don't worry much about battery life claims.</li>
  <li><strong>If you work from cafés, coworking spaces, or move between meetings</strong>, real-world battery life (not the marketing number) should weigh as heavily as raw performance. Look for independent reviews with actual workload testing, not just video-playback loop numbers.</li>
</ul>

<h2 id="screen-keyboard">Screen and keyboard: the parts you touch all day</h2>
<p>These get less attention than benchmarks, but they affect your body every single day:</p>
<ul>
  <li><strong>Resolution and size:</strong> A 14–16 inch screen at 1920×1200 or higher gives comfortable room for a code editor and a terminal side by side without constant zooming.</li>
  <li><strong>Keyboard travel:</strong> If you type for hours, try the keyboard in person if at all possible. Reviews can tell you specs; only your hands can tell you if it's comfortable for your typing style.</li>
  <li><strong>Matte vs. glossy display:</strong> Matte finishes handle glare far better if you ever work near a window.</li>
</ul>

<h2 id="storage">Storage: type matters more than raw size</h2>
<p>An NVMe SSD is non-negotiable for programming work in 2026 — the difference in project load times, git operations, and container builds compared to a SATA SSD or (worse) a spinning drive is dramatic. 512GB is a reasonable starting point for most developers; go to 1TB if you regularly work with large datasets, media assets, or multiple local VM images.</p>

<h2 id="os">Operating system: pick based on your stack, not habit</h2>
<p>All three major platforms are viable for most programming work today, but each has friction points:</p>
<ul>
  <li><strong>macOS:</strong> Unix-based, excellent for iOS development (required, in fact), strong battery life, but pricier and less repairable.</li>
  <li><strong>Windows with WSL2:</strong> A genuinely solid Linux development experience now, wide hardware selection at every price point, best for gaming crossover or Windows-specific work.</li>
  <li><strong>Linux natively:</strong> The most direct match for server environments and DevOps work, but hardware compatibility (especially for newer laptops) needs a quick compatibility check before buying.</li>
</ul>

<h2 id="checklist">A quick pre-purchase checklist</h2>
<ol>
  <li>Does it have at least 16GB RAM, non-upgradeable or otherwise? (Buy the RAM you'll need now — most modern thin laptops can't be upgraded later.)</li>
  <li>Is storage an NVMe SSD, and can you afford 1TB if you work with large projects?</li>
  <li>Have independent reviews confirmed sustained performance under real workloads, not just burst benchmarks?</li>
  <li>Does the battery life claim hold up in independent real-world testing, not just the manufacturer's number?</li>
  <li>Have you physically typed on the keyboard, or read reviews from people who did?</li>
</ol>

<blockquote>The "best" programming laptop is the one that disappears — the one you stop thinking about because it never runs out of memory mid-task and never dies before you get to an outlet.</blockquote>
"""

print("Loaded 2 of 5 articles")

ARTICLE_CONTENT["understanding-ai-chips-explained"] = """
<p>"AI-ready processor." "Built-in NPU." "45 TOPS of AI performance." If you've shopped for a laptop or phone recently, you've seen these phrases on every box, often without a clear explanation of what they mean. Here's what's actually happening inside that silicon, in plain terms.</p>

<h2 id="what-is-npu">What is an NPU?</h2>
<p>An NPU, or Neural Processing Unit, is a dedicated chip component built specifically to run the math behind machine learning models — mostly matrix multiplication, performed in parallel, at relatively low precision. That's different from a CPU (general-purpose, good at sequential logic and a huge variety of tasks) and a GPU (great at massively parallel work like graphics rendering, which happens to overlap well with AI workloads).</p>
<p>The NPU exists because doing AI inference (running an already-trained model, not training it) on a CPU works, but burns far more power for the same result. An NPU is purpose-built to do that specific kind of math efficiently, which matters most on battery-powered devices.</p>

<h2 id="tops">What does "TOPS" actually measure?</h2>
<p>TOPS stands for Trillion Operations Per Second — a raw throughput number for how many low-precision AI calculations a chip can perform each second. It's a useful rough comparison between chips, similar to how "megapixels" gives you a rough sense of a camera, but it isn't the whole story:</p>
<ul>
  <li>TOPS numbers from different manufacturers aren't always measured the same way, so cross-brand comparisons can be misleading.</li>
  <li>Real-world performance also depends on memory bandwidth, software optimization, and whether an app actually knows how to use the NPU at all.</li>
  <li>A higher TOPS number doesn't guarantee a better experience if the software you use hasn't been optimized to take advantage of it.</li>
</ul>

<h2 id="ai-pc">What is an "AI PC," really?</h2>
<p>Industry groups have loosely defined an AI PC as a computer with a CPU, GPU, and NPU that together can run AI workloads locally, without needing to send data to the cloud. In practice, today that mostly enables things like:</p>
<ul>
  <li>Real-time background blur, eye contact correction, and noise removal in video calls, processed locally.</li>
  <li>On-device photo editing tools (object removal, smart selection) that don't require an internet connection.</li>
  <li>Local voice transcription and translation without sending audio to a server.</li>
  <li>Faster, more private autocomplete and writing assistance in supported apps.</li>
</ul>
<p>Notably, most large, general-purpose AI chatbot models still run in the cloud, because they're too large to fit comfortably in a laptop's memory and power budget. An NPU mostly accelerates smaller, specific, local tasks rather than replacing cloud AI entirely — at least with current-generation hardware.</p>

<h2 id="do-you-need-one">Do you actually need an AI chip?</h2>
<p>Here's an honest way to think about it, based on how you actually use your device:</p>
<table>
<tr><th>You...</th><th>Verdict</th></tr>
<tr><td>Take frequent video calls and want better background/audio effects</td><td>Worth having, meaningful benefit</td></tr>
<tr><td>Do local photo/video editing with AI-assisted tools</td><td>Worth having, can speed up specific tasks</td></tr>
<tr><td>Mostly use cloud-based AI chatbots and browser-based tools</td><td>Low priority — an NPU won't change that experience much yet</td></tr>
<tr><td>Are buying primarily for gaming or heavy creative rendering</td><td>Low priority — prioritize GPU instead</td></tr>
</table>

<h2 id="how-to-check">How to check what a specific chip can do</h2>
<p>Marketing TOPS numbers are a starting point, not the full answer. Before buying based on "AI performance," check:</p>
<ol>
  <li>Whether the specific software you plan to use (video call app, editing suite, OS features) actually lists that chip family as supported for local acceleration.</li>
  <li>Independent reviews that test real local AI features, not just synthetic TOPS benchmarks.</li>
  <li>Whether the feature you care about even requires local NPU acceleration, or works fine (if slower) without it.</li>
</ol>

<blockquote>An NPU is a specialized tool for a specific job, not a general upgrade to "how smart" your computer is. The chip that matters most for your day-to-day experience still depends heavily on what software you actually run.</blockquote>

<h2 id="faq">Frequently asked questions</h2>
<h3>Will an AI chip make my computer feel faster overall?</h3>
<p>Not directly. It accelerates specific AI-related tasks; it won't speed up general browsing, spreadsheet work, or non-AI software.</p>
<h3>Is a higher TOPS number always better?</h3>
<p>Generally yes for AI-specific workloads, but only when comparing chips measured the same way, and only for software that's actually optimized to use that hardware.</p>
"""

print("Loaded 3 of 5 articles")

ARTICLE_CONTENT["smart-home-setup-guide-2026"] = """
<p>The biggest reason smart home setups fail isn't bad hardware — it's starting with too many brands, too many apps, and no plan for how everything will actually talk to each other. Here's a setup order that avoids the most common regrets.</p>

<h2 id="step1">Step 1: Pick your ecosystem foundation first</h2>
<p>Before buying a single bulb, decide which voice assistant and app ecosystem you'll center your home around (Google Home, Amazon Alexa, or Apple Home are the three major options). This single decision determines which devices will feel native and which will feel bolted-on. You can still mix brands of physical devices — the point is choosing one control hub, not one device manufacturer.</p>

<h2 id="matter">Understanding Matter (and why it actually matters)</h2>
<p>Matter is a cross-brand smart home standard designed to let devices from different manufacturers work together and be controlled from any compatible app, instead of being locked into one brand's ecosystem. In practice, checking for a "Matter compatible" logo before buying a device meaningfully reduces the odds you'll end up with a gadget stuck in its own isolated app that never talks to anything else.</p>
<p>It isn't a perfect solve-everything standard yet — some advanced features still only work fully within a single brand's own app — but it's the strongest signal available today that a device won't become an orphaned isolated gadget.</p>

<h2 id="step2">Step 2: Start with one room, not the whole house</h2>
<p>Buying everything at once is the fastest path to a frustrating weekend and a pile of returns. Instead:</p>
<ol>
  <li>Pick one room — usually the living room or bedroom works well as a first test.</li>
  <li>Add 2–3 devices (a smart plug, a smart bulb set, and either a speaker or a display hub).</li>
  <li>Live with that setup for a week before expanding, so you learn your actual usage patterns rather than guessing.</li>
</ol>

<h2 id="step3">Step 3: Automations that are actually worth setting up</h2>
<p>Most people set up far too many "cool but useless" automations early on, then abandon the whole system when it feels more complicated than useful. Start with automations that solve a real recurring annoyance:</p>
<ul>
  <li><strong>Sunset-triggered lighting</strong>, so you never come home to a dark house.</li>
  <li><strong>A single "leaving home" routine</strong> that locks doors, turns off lights, and adjusts the thermostat with one tap or voice command.</li>
  <li><strong>Motion-triggered lighting</strong> in hallways or bathrooms, especially useful at night.</li>
</ul>
<p>Resist the urge to automate everything on day one. Add one automation, use it for a few days, then decide if it earns a permanent place.</p>

<h2 id="cameras">Security cameras: what actually matters</h2>
<table>
<tr><th>Feature</th><th>Why it matters</th></tr>
<tr><td>Local storage option</td><td>Avoids ongoing cloud subscription costs and reduces reliance on a company's servers for your footage</td></tr>
<tr><td>End-to-end encryption</td><td>Prevents footage from being intercepted or accessed without your permission</td></tr>
<tr><td>Person/vehicle detection (not just "motion")</td><td>Drastically cuts down false alerts from trees, shadows, and passing cars</td></tr>
<tr><td>Matter/ecosystem compatibility</td><td>Lets you view footage alongside your other smart home devices instead of in a separate isolated app</td></tr>
</table>

<h2 id="mistakes">Common beginner mistakes to avoid</h2>
<ul>
  <li><strong>Buying non-Matter devices from five different brands before checking compatibility.</strong> This is the #1 cause of the dreaded "five separate apps" problem.</li>
  <li><strong>Skipping firmware updates.</strong> Smart home devices receive real security patches; an outdated device is a real vulnerability, not just a missed feature update.</li>
  <li><strong>Using the default Wi-Fi password on your router.</strong> Every smart device is a new device on your network — network-level security matters more, not less, as you add devices.</li>
  <li><strong>Over-automating before understanding your own habits.</strong> A few reliable automations beat a dozen you'll eventually ignore or disable out of frustration.</li>
</ul>

<h2 id="budget">A realistic starter budget</h2>
<p>You do not need to spend a fortune to get a genuinely useful smart home. A hub or smart speaker, two to three smart plugs, a smart bulb multi-pack, and one entry-level camera is enough to feel the benefit without overcommitting before you know what you'll actually use day to day.</p>

<blockquote>A smart home succeeds when it removes small daily friction — lights that just come on, doors you don't worry about — not when it has the most devices connected.</blockquote>

<h2 id="faq">Frequently asked questions</h2>
<h3>Do I need a separate hub, or can I just use apps?</h3>
<p>Many devices work fine through their own app alone, but a hub (or a smart speaker acting as one) is what enables cross-brand automations and voice control across your whole setup, rather than device-by-device.</p>
<h3>Is Matter compatibility worth paying extra for?</h3>
<p>In most cases, yes — it protects your investment against ecosystem lock-in and future-proofs your setup as you add more devices from different brands over time.</p>
"""

print("Loaded 4 of 5 articles")

ARTICLE_CONTENT["5g-vs-wifi-7-which-do-you-need"] = """
<p>5G and Wi-Fi 7 show up in the same marketing conversations so often that it's easy to assume you're choosing between them. In reality, they're built to solve different problems, and most people benefit from understanding both rather than picking a "winner."</p>

<h2 id="what-each-is">What each technology is actually for</h2>
<ul>
  <li><strong>5G</strong> is a cellular network standard — it connects your device directly to a mobile carrier's towers, giving you internet access anywhere there's coverage, with no router or home network required.</li>
  <li><strong>Wi-Fi 7</strong> is a local wireless networking standard — it connects your devices to a router that's already connected to the internet (via cable, fiber, or even a 5G home internet connection), working only within your home or office's range.</li>
</ul>
<p>In other words: 5G gets an internet connection <em>to</em> a location; Wi-Fi 7 distributes that connection <em>within</em> a location. They're often complementary rather than competing.</p>

<h2 id="speed">Real-world speed comparison</h2>
<p>Marketing numbers for both technologies list theoretical maximums that are rarely hit in practice. What actually matters:</p>
<table>
<tr><th></th><th>Typical real-world speed</th><th>Main limiting factor</th></tr>
<tr><td>5G (mid-band, most common)</td><td>Roughly 100–400 Mbps</td><td>Distance from tower, network congestion, physical obstructions</td></tr>
<tr><td>5G (mmWave, less common)</td><td>Can exceed 1 Gbps</td><td>Very short range, easily blocked by walls</td></tr>
<tr><td>Wi-Fi 7</td><td>Multiple Gbps on supported devices</td><td>Distance from router, interference, whether your internet plan itself is fast enough to fill that pipe</td></tr>
</table>
<p>Notice that last point: Wi-Fi 7's blazing local speeds are capped by your actual internet plan. If you pay for a 300 Mbps connection, a Wi-Fi 7 router won't make your internet faster than 300 Mbps — it will make your local network more efficient at handling many devices at once and reduce interference-related slowdowns.</p>

<h2 id="latency">Latency: the difference that's easy to miss</h2>
<p>For video calls, competitive gaming, and cloud-based work tools, latency (the delay before data starts moving) often matters more than raw speed. Wi-Fi, with a wired backbone behind it, generally offers lower and more consistent latency than any cellular connection, because it doesn't have to travel through a cell tower and carrier network first. If you're setting up a serious home office or a gaming space, prioritize a solid wired or Wi-Fi 7 connection over relying on 5G, even where 5G speeds look competitive on paper.</p>

<h2 id="use-cases">Which one should you actually pay for?</h2>
<h3>Choose 5G home internet if:</h3>
<ul>
  <li>You don't have access to fiber or cable internet at your address.</li>
  <li>You move frequently or need internet access quickly without a wired installation.</li>
  <li>Your household's usage is moderate (browsing, streaming, video calls) rather than heavy simultaneous multi-device use.</li>
</ul>
<h3>Choose to upgrade to Wi-Fi 7 if:</h3>
<ul>
  <li>You already have a fast wired internet connection (fiber or high-speed cable) and want your home network to fully use it.</li>
  <li>Your household has many devices active simultaneously — streaming, gaming, video calls, smart home devices — and experiences congestion-related slowdowns.</li>
  <li>You do latency-sensitive work or gaming and want the most consistent connection possible.</li>
</ul>

<h2 id="do-you-need-both">Do you need both?</h2>
<p>Many households benefit from both, used for their actual strengths: a fast wired or fiber connection distributed through a Wi-Fi 7 router at home, plus 5G on your phone for connectivity outside the house. Where they do compete directly is in the specific case of 5G home internet as a replacement for a wired connection — that's a genuine either/or decision, and it comes down to what's available and reliable at your specific address.</p>

<blockquote>Don't buy Wi-Fi 7 hardware expecting it to fix a slow internet plan, and don't expect 5G home internet to match the consistency of a wired connection during peak network congestion hours.</blockquote>

<h2 id="faq">Frequently asked questions</h2>
<h3>Does Wi-Fi 7 require a new router and new devices?</h3>
<p>Yes to the router; your existing devices will still connect at their own maximum supported speed, and you'll only see full Wi-Fi 7 benefits on devices that also support the standard.</p>
<h3>Is 5G home internet reliable enough to fully replace cable or fiber?</h3>
<p>It can be, especially in areas with strong coverage, but it's more susceptible to network congestion during peak hours and to physical obstructions than a wired connection. Check independent local reviews and speed tests for your specific area before switching.</p>
"""

print("Loaded 5 of 5 articles")

# ---------------------------------------------------------------------
# SVG placeholder cover image generator (no external image deps needed)
# ---------------------------------------------------------------------
COVER_COLORS = {
    "Software":   ("#3D5AFE", "#00B39B"),
    "Hardware":   ("#F5A623", "#3D5AFE"),
    "Smart Home": ("#00B39B", "#F5A623"),
    "Networking": ("#3D5AFE", "#F5A623"),
}

def make_cover_svg(title, category, filename):
    c1, c2 = COVER_COLORS.get(category, ("#3D5AFE", "#00B39B"))
    words = title.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 26:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    lines = lines[:4]
    tspans = "".join(
        '<tspan x="60" dy="{}">{}</tspan>'.format(0 if i == 0 else 44, l.replace("&", "&amp;"))
        for i, l in enumerate(lines)
    )
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{C1}"/>
      <stop offset="100%" stop-color="{C2}"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="675" fill="#12161f"/>
  <rect width="1200" height="675" fill="url(#g)" opacity="0.14"/>
  <g stroke="{C1}" stroke-opacity="0.25" stroke-width="1">
    <line x1="0" y1="560" x2="1200" y2="560"/>
    <line x1="0" y1="580" x2="1200" y2="580"/>
    <line x1="0" y1="600" x2="1200" y2="600"/>
  </g>
  <rect x="60" y="60" width="150" height="34" rx="17" fill="{C1}"/>
  <text x="80" y="83" font-family="JetBrains Mono, monospace" font-size="15" fill="#0b0e14">{CAT}</text>
  <text x="60" y="270" font-family="Space Grotesk, sans-serif" font-size="44" font-weight="700" fill="#ffffff">{TS}</text>
  <text x="60" y="620" font-family="JetBrains Mono, monospace" font-size="18" fill="#c8cddb">techpulsehub.com</text>
</svg>""".format(C1=c1, C2=c2, CAT=category.upper(), TS=tspans)
    write(filename, svg)

def article_jsonld(p):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p["title"],
        "description": p["description"],
        "image": [SITE_URL + "/images/covers/" + p["slug"] + ".svg"],
        "datePublished": p["date"],
        "dateModified": p["date"],
        "author": {"@type": "Organization", "name": AUTHOR, "url": SITE_URL},
        "publisher": {
            "@type": "Organization", "name": SITE_NAME,
            "logo": {"@type": "ImageObject", "url": SITE_URL + "/images/logo.svg"}
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": SITE_URL + "/posts/" + p["slug"] + ".html"}
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/index.html"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE_URL + "/blog.html"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": SITE_URL + "/posts/" + p["slug"] + ".html"},
        ]
    }
    return ('<script type="application/ld+json">' + json.dumps(data) + '</script>\n'
            '<script type="application/ld+json">' + json.dumps(breadcrumb) + '</script>')

def org_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "url": SITE_URL,
        "logo": SITE_URL + "/images/logo.svg",
        "description": SITE_DESC,
        "sameAs": []
    }
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_URL,
        "potentialAction": {
            "@type": "SearchAction",
            "target": SITE_URL + "/blog.html?q={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }
    return ('<script type="application/ld+json">' + json.dumps(data) + '</script>\n'
            '<script type="application/ld+json">' + json.dumps(website) + '</script>')

print("Helper functions ready.")

# ---------------------------------------------------------------------
# Reusable post-card renderer
# ---------------------------------------------------------------------
def post_card(p, root=""):
    return """
    <a class="post-card" data-post-card data-category="{CATID}" data-search="{SEARCH}" href="{ROOT}posts/{SLUG}.html">
      <img src="{ROOT}images/covers/{SLUG}.svg" alt="Cover illustration for the article: {TITLE}" loading="lazy" width="1200" height="675">
      <div class="body">
        <span class="tag">{CAT}</span>
        <h3>{TITLE}</h3>
        <p>{EXCERPT}</p>
        <span class="meta">{READ} &middot; {DATE}</span>
      </div>
    </a>""".format(
        CATID=p["category_id"], SEARCH=(p["title"] + " " + p["category"]).lower(),
        ROOT=root, SLUG=p["slug"], TITLE=p["title"], CAT=p["category"],
        EXCERPT=p["excerpt"], READ=p["read_time"], DATE=p["date"]
    )

# ---------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------
def build_home():
    featured = POSTS[-1]
    rest = POSTS[:-1]
    mini_cards = "".join("""
      <a class="mini-card" href="posts/{SLUG}.html">
        <img src="images/covers/{SLUG}.svg" alt="Cover for {TITLE}" loading="lazy" width="92" height="68">
        <div>
          <span class="tag">{CAT}</span>
          <h3>{TITLE}</h3>
          <span class="meta">{READ}</span>
        </div>
      </a>""".format(SLUG=p["slug"], TITLE=p["title"], CAT=p["category"], READ=p["read_time"])
        for p in rest[:3])

    grid = "".join(post_card(p) for p in POSTS)

    body = """
<main id="main">
  <section class="hero">
    <div class="wrap">
      <span class="eyebrow">Consumer tech, explained plainly</span>
      <h1>Gadgets and software, without the hype.</h1>
      <p class="lead">{DESC} New guides on laptops, AI hardware, smart homes, and wireless standards — written to actually help you decide, not just to rank on a keyword.</p>

      <div class="hero-grid">
        <a class="card-featured" href="posts/{FSLUG}.html" style="text-decoration:none;color:inherit;">
          <img src="images/covers/{FSLUG}.svg" alt="Cover for {FTITLE}" width="1200" height="675">
          <div class="body">
            <span class="tag">{FCAT}</span>
            <h2 style="font-size:1.5rem;">{FTITLE}</h2>
            <p style="color:var(--ink-soft);">{FEXCERPT}</p>
            <span class="meta">{FREAD} &middot; {FDATE}</span>
          </div>
        </a>
        <div class="card-featured-list">
          {MINI}
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head">
        <h2>Latest articles</h2>
        <a href="blog.html">View all posts &rarr;</a>
      </div>
      <div class="post-grid">{GRID}</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="ad-slot">Ad placement — 728x90 (leaderboard). Replace this block with your AdSense unit once approved. See README.md.</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="callout">
        <div>
          <h2>Get one useful tech tip a week</h2>
          <p>No spam, no daily noise — just genuinely useful guides when we publish them.</p>
        </div>
        <form id="newsletter-form" style="display:flex;gap:10px;flex-wrap:wrap;">
          <input type="email" required placeholder="you@example.com" aria-label="Email address"
                 style="padding:12px 14px;border-radius:8px;border:none;min-width:220px;">
          <button class="btn" type="submit">Subscribe</button>
        </form>
      </div>
      <p id="newsletter-msg" class="small center" style="margin-top:12px;"></p>
    </div>
  </section>
</main>
""".format(
        DESC=SITE_DESC, FSLUG=featured["slug"], FTITLE=featured["title"], FCAT=featured["category"],
        FEXCERPT=featured["excerpt"], FREAD=featured["read_time"], FDATE=featured["date"],
        MINI=mini_cards, GRID=grid
    )

    html = page(
        title="TechPulse Hub — Practical Gadget & Software Guides",
        description=SITE_DESC,
        keywords="tech blog, gadget reviews, laptop buying guide, smart home guide, AI chips explained, wifi 7, tech tips 2026",
        canonical_path="index.html",
        body_html=body, ogtype="website", active="home", jsonld=org_jsonld(), root_prefix=""
    )
    write("index.html", html)

# ---------------------------------------------------------------------
# BLOG INDEX PAGE
# ---------------------------------------------------------------------
def build_blog():
    cats = sorted(set(p["category"] for p in POSTS))
    chips = '<button class="tag" data-filter="all" style="cursor:pointer;border:none;">All</button>' + "".join(
        '<button class="tag" data-filter="{ID}" style="cursor:pointer;border:none;">{C}</button>'.format(
            ID=c.lower().replace(" ", "-"), C=c) for c in cats
    )
    grid = "".join(post_card(p) for p in POSTS)
    body = """
<main id="main">
  <section class="hero" style="padding:48px 0 28px;">
    <div class="wrap">
      <span class="eyebrow">The archive</span>
      <h1>All articles</h1>
      <p class="lead">Search or filter by topic to find exactly what you need.</p>
      <div style="margin-top:24px;display:flex;gap:14px;flex-wrap:wrap;align-items:center;">
        <input id="blog-search" type="search" placeholder="Search articles..." aria-label="Search articles"
               style="padding:12px 14px;border:1px solid var(--line);border-radius:8px;min-width:240px;font-family:inherit;">
        <div>{CHIPS}</div>
      </div>
    </div>
  </section>
  <section>
    <div class="wrap">
      <div class="post-grid">{GRID}</div>
    </div>
  </section>
</main>
""".format(CHIPS=chips, GRID=grid)

    html = page(
        title="Blog Archive — TechPulse Hub",
        description="Browse every TechPulse Hub article on laptops, AI hardware, smart home setup, software tools, and wireless networking.",
        keywords="tech blog archive, gadget guides, software reviews, smart home articles",
        canonical_path="blog.html",
        body_html=body, ogtype="website", active="blog"
    )
    write("blog.html", html)

print("Home + blog builders ready.")

# ---------------------------------------------------------------------
# ARTICLE PAGES
# ---------------------------------------------------------------------
import re as _re
def build_toc(html_body):
    heads = _re.findall(r'<h([23]) id="([^"]+)">(.*?)</h\1>', html_body)
    items = []
    for level, hid, text in heads:
        indent = "margin-left:14px;" if level == "3" else ""
        items.append('<a style="{IND}" href="#{ID}">{T}</a>'.format(IND=indent, ID=hid, T=text))
    return "\n".join(items)

def build_articles():
    for i, p in enumerate(POSTS):
        make_cover_svg(p["title"], p["category"], "images/covers/" + p["slug"] + ".svg")
        content = ARTICLE_CONTENT[p["slug"]]
        toc = build_toc(content)
        prev_p = POSTS[i - 1] if i > 0 else None
        next_p = POSTS[i + 1] if i < len(POSTS) - 1 else None

        related = [q for q in POSTS if q["slug"] != p["slug"] and q["category"] == p["category"]]
        if len(related) < 2:
            related += [q for q in POSTS if q["slug"] != p["slug"] and q not in related]
        related = related[:2]
        related_html = "".join(post_card(r) for r in related)

        share_url = SITE_URL + "/posts/" + p["slug"] + ".html"
        body = """
<main id="main">
  <div class="wrap breadcrumbs">
    <a href="../index.html">Home</a> / <a href="../blog.html">Blog</a> / <span>{TITLE}</span>
  </div>
  <div class="article-header wrap">
    <span class="tag">{CAT}</span>
    <h1>{TITLE}</h1>
    <p class="lead" style="color:var(--ink-soft);max-width:60ch;">{DESC}</p>
    <div class="meta"><span>{AUTHOR}</span><span>{DATE}</span><span>{READ}</span></div>
  </div>

  <div class="wrap">
    <img class="article-cover" src="../images/covers/{SLUG}.svg" alt="Cover illustration for {TITLE}" width="1200" height="514">

    <div class="article-layout">
      <article class="post-content">
        {CONTENT}

        <div class="author-box">
          <div class="author-avatar" aria-hidden="true"></div>
          <div>
            <strong>{AUTHOR}</strong>
            <p class="small" style="margin:2px 0 0;">We test and research every recommendation before publishing. Have a correction or a question? <a href="../contact.html">Contact us</a>.</p>
          </div>
        </div>

        <div class="share-bar" aria-label="Share this article">
          <a target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?url={SHAREURL}&amp;text={TITLE}">Share on X</a>
          <a target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url={SHAREURL}">Share on LinkedIn</a>
          <a target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u={SHAREURL}">Share on Facebook</a>
        </div>

        <div class="ad-slot" style="margin:32px 0;">In-article ad placement (responsive unit). Replace with your AdSense code once approved.</div>
      </article>

      <aside class="sidebar">
        <div class="box">
          <h4>On this page</h4>
          <nav class="toc">{TOC}</nav>
        </div>
        <div class="box">
          <h4>Keep reading</h4>
          {NAV}
        </div>
        <div class="ad-slot">Sidebar ad placement (300x250)</div>
      </aside>
    </div>

    <section>
      <div class="section-head"><h2>Related articles</h2></div>
      <div class="post-grid">{RELATED}</div>
    </section>
  </div>
</main>
""".format(
            TITLE=p["title"], CAT=p["category"], DESC=p["description"], AUTHOR=AUTHOR,
            DATE=p["date"], READ=p["read_time"], SLUG=p["slug"], CONTENT=content,
            SHAREURL=share_url, TOC=toc,
            NAV="".join(filter(None, [
                '<a href="{}.html">&larr; {}</a>'.format(prev_p["slug"], prev_p["title"]) if prev_p else "",
                '<a href="{}.html">{} &rarr;</a>'.format(next_p["slug"], next_p["title"]) if next_p else "",
            ])),
            RELATED=related_html
        )

        html = page(
            title=p["title"] + " | " + SITE_NAME,
            description=p["description"],
            keywords=p["keywords"],
            canonical_path="posts/" + p["slug"] + ".html",
            body_html=body, ogtype="article", active="blog",
            jsonld=article_jsonld(p), root_prefix="../",
            ogimage=SITE_URL + "/images/covers/" + p["slug"] + ".svg"
        )
        write("posts/" + p["slug"] + ".html", html)

print("Article builder ready.")

# ---------------------------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------------------------
def build_about():
    body = """
<main id="main">
  <section class="hero" style="padding:48px 0 28px;">
    <div class="wrap">
      <span class="eyebrow">About us</span>
      <h1>We write the tech guide we'd want to read.</h1>
      <p class="lead">TechPulse Hub exists because most gadget content online is either a thinly reworded press release or a listicle written to hit a word count. We do neither.</p>
    </div>
  </section>
  <section style="padding-top:0;">
    <div class="wrap" style="max-width:820px;">
      <article class="post-content">
        <h2>What we cover</h2>
        <p>We focus on consumer technology that people actually use day to day: laptops and the tradeoffs behind buying one, the software and browser tools that quietly save (or waste) your time, smart home setups that are supposed to make life easier, and the wireless and hardware standards that show up in marketing without much explanation.</p>

        <h2>How we write</h2>
        <p>Every article on this site is written and edited by our small editorial team. We prioritize being genuinely useful over being first — we'd rather publish a clear, accurate guide a week later than a rushed one today. Where we mention specifications, comparisons, or standards, we aim to explain the reasoning behind a recommendation, not just hand you a verdict.</p>

        <h2>How we make money</h2>
        <p>TechPulse Hub is supported by display advertising (including Google AdSense) and, where disclosed, affiliate links. Ads and affiliate relationships never influence which topics we choose to cover or what we conclude in an article. If a post contains a sponsored element or an affiliate link, it will be clearly labeled within that article.</p>

        <h2>Corrections</h2>
        <p>We make mistakes occasionally, like any publication. If you spot something inaccurate or outdated, please <a href="contact.html">let us know</a> — we review and correct reported errors promptly and note significant corrections at the bottom of the affected article.</p>

        <h2>Get in touch</h2>
        <p>Questions, feedback, or a topic you'd like us to cover? Visit our <a href="contact.html">contact page</a> — we read every message.</p>
      </article>
    </div>
  </section>
</main>
"""
    html = page(
        title="About Us — TechPulse Hub",
        description="Learn who writes TechPulse Hub, what we cover, how we choose topics, and how the site is funded.",
        keywords="about techpulse hub, tech blog editorial team, who writes this blog",
        canonical_path="about.html", body_html=body, active="about"
    )
    write("about.html", html)

# ---------------------------------------------------------------------
# CONTACT PAGE
# ---------------------------------------------------------------------
def build_contact():
    body = """
<main id="main">
  <section class="hero" style="padding:48px 0 28px;">
    <div class="wrap">
      <span class="eyebrow">Contact</span>
      <h1>Get in touch</h1>
      <p class="lead">Have feedback, a correction, a topic suggestion, or a partnership inquiry? Send us a message below.</p>
    </div>
  </section>
  <section style="padding-top:0;">
    <div class="wrap" style="max-width:640px;">
      <form id="contact-form">
        <div class="form-field">
          <label for="name">Name</label>
          <input id="name" name="name" type="text" required>
        </div>
        <div class="form-field">
          <label for="email">Email</label>
          <input id="email" name="email" type="email" required>
        </div>
        <div class="form-field">
          <label for="subject">Subject</label>
          <input id="subject" name="subject" type="text" required>
        </div>
        <div class="form-field">
          <label for="message">Message</label>
          <textarea id="message" name="message" rows="6" required></textarea>
        </div>
        <button class="btn" type="submit">Send message</button>
        <p id="contact-msg" class="small" style="margin-top:14px;"></p>
      </form>
      <p class="small" style="margin-top:28px;">
        This form is a static front-end demo — see <code>README.md</code> for how to connect it to a real
        form backend (such as Formspree, Getform, or your own endpoint) so messages actually reach your inbox.
        Alternatively, you can email us directly at <strong>hello@techpulsehub.com</strong> (replace with your real address).
      </p>
    </div>
  </section>
</main>
"""
    html = page(
        title="Contact Us — TechPulse Hub",
        description="Get in touch with the TechPulse Hub team for feedback, corrections, topic suggestions, or partnership inquiries.",
        keywords="contact techpulse hub, tech blog contact",
        canonical_path="contact.html", body_html=body, active="contact"
    )
    write("contact.html", html)

# ---------------------------------------------------------------------
# PRIVACY POLICY (AdSense-relevant)
# ---------------------------------------------------------------------
def build_privacy():
    body = """
<main id="main">
  <section class="hero" style="padding:48px 0 28px;">
    <div class="wrap">
      <span class="eyebrow">Legal</span>
      <h1>Privacy Policy</h1>
      <p class="lead">Last updated: {DATE}</p>
    </div>
  </section>
  <section style="padding-top:0;">
    <div class="wrap" style="max-width:820px;">
      <article class="post-content">
        <p>This Privacy Policy explains how {SITE} ("we," "us," or "our") collects, uses, and protects information when you visit {URL}. Replace the bracketed placeholders below with your real business/contact details before publishing this page live.</p>

        <h2>Information we collect</h2>
        <ul>
          <li><strong>Information you provide directly</strong>, such as your name and email address when you use our contact form or subscribe to our newsletter.</li>
          <li><strong>Automatically collected information</strong>, such as browser type, device type, pages visited, and approximate location, gathered through cookies and similar technologies.</li>
          <li><strong>Analytics data</strong>, if we use a service such as Google Analytics, to understand how visitors use the site in aggregate.</li>
        </ul>

        <h2>Cookies and similar technologies</h2>
        <p>We use cookies to operate the site, remember your preferences, and — where applicable — to serve relevant advertising. You can control or disable cookies through your browser settings; note that some site features may not function correctly with cookies disabled.</p>

        <h2>Google AdSense and advertising</h2>
        <p>We use, or intend to use, Google AdSense to display advertisements on this site. Google, as a third-party vendor, uses cookies (including the DoubleClick cookie) to serve ads based on a visitor's prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visit to this site and/or other sites on the Internet.</p>
        <p>You may opt out of personalized advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>. You can also visit <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">www.aboutads.info</a> to opt out of third-party vendors' use of cookies for personalized advertising.</p>

        <h2>Third-party links</h2>
        <p>Our site may contain links to third-party websites. We are not responsible for the privacy practices or content of those external sites. We encourage you to review the privacy policy of any site you visit.</p>

        <h2>Children's privacy</h2>
        <p>This site is not directed at children under 13, and we do not knowingly collect personal information from children under 13. If you believe a child has provided us with personal information, please contact us so we can remove it.</p>

        <h2>Your rights</h2>
        <p>Depending on your location, you may have rights to access, correct, or delete personal information we hold about you, and to object to or restrict certain processing. To exercise these rights, contact us using the details on our <a href="contact.html">Contact page</a>.</p>

        <h2>Data retention</h2>
        <p>We retain personal information only as long as necessary for the purposes described in this policy, or as required by law.</p>

        <h2>Changes to this policy</h2>
        <p>We may update this Privacy Policy from time to time. Changes will be posted on this page with an updated "last updated" date.</p>

        <h2>Contact us</h2>
        <p>If you have questions about this Privacy Policy, please reach out via our <a href="contact.html">Contact page</a>.</p>
      </article>
    </div>
  </section>
</main>
""".format(DATE=TODAY, SITE=SITE_NAME, URL=SITE_URL)
    html = page(
        title="Privacy Policy — TechPulse Hub",
        description="Read the TechPulse Hub privacy policy, including how we use cookies and Google AdSense advertising.",
        keywords="privacy policy, cookies policy, adsense privacy",
        canonical_path="privacy-policy.html", body_html=body
    )
    write("privacy-policy.html", html)

# ---------------------------------------------------------------------
# TERMS OF SERVICE
# ---------------------------------------------------------------------
def build_terms():
    body = """
<main id="main">
  <section class="hero" style="padding:48px 0 28px;">
    <div class="wrap">
      <span class="eyebrow">Legal</span>
      <h1>Terms of Service</h1>
      <p class="lead">Last updated: {DATE}</p>
    </div>
  </section>
  <section style="padding-top:0;">
    <div class="wrap" style="max-width:820px;">
      <article class="post-content">
        <p>These Terms of Service ("Terms") govern your use of {SITE} (the "Site"). By using this Site, you agree to these Terms. Replace bracketed placeholders with your real business details before publishing.</p>

        <h2>Use of content</h2>
        <p>All articles, images, and other content on this Site are owned by {SITE} or licensed to us, unless otherwise noted. You may share links to our content and quote brief excerpts with attribution and a link back to the original article. Reproducing full articles without permission is not permitted.</p>

        <h2>No professional advice</h2>
        <p>Content on this Site is provided for general informational purposes only and does not constitute professional, technical, financial, or purchasing advice specific to your situation. Product recommendations reflect our editorial judgment at the time of publication and may become outdated as products and prices change.</p>

        <h2>Advertising and affiliate disclosure</h2>
        <p>This Site displays third-party advertising, including through Google AdSense, and may include affiliate links that earn us a commission on qualifying purchases at no extra cost to you. Sponsored content or affiliate links will be clearly disclosed within the relevant article.</p>

        <h2>User conduct</h2>
        <p>When using features such as our contact form or comments (if enabled), you agree not to submit unlawful, abusive, or misleading content, or attempt to interfere with the Site's normal operation.</p>

        <h2>Limitation of liability</h2>
        <p>{SITE} is provided "as is" without warranties of any kind. We are not liable for any damages arising from your use of, or inability to use, this Site or reliance on its content.</p>

        <h2>Changes to these Terms</h2>
        <p>We may revise these Terms from time to time. Continued use of the Site after changes are posted constitutes acceptance of the revised Terms.</p>

        <h2>Contact</h2>
        <p>Questions about these Terms can be sent through our <a href="contact.html">Contact page</a>.</p>
      </article>
    </div>
  </section>
</main>
""".format(DATE=TODAY, SITE=SITE_NAME)
    html = page(
        title="Terms of Service — TechPulse Hub",
        description="Read the TechPulse Hub terms of service, including content use, advertising disclosure, and liability terms.",
        keywords="terms of service, terms and conditions, tech blog terms",
        canonical_path="terms.html", body_html=body
    )
    write("terms.html", html)

# ---------------------------------------------------------------------
# 404 PAGE
# ---------------------------------------------------------------------
def build_404():
    body = """
<main id="main">
  <section class="hero center" style="padding:100px 0;">
    <div class="wrap">
      <span class="eyebrow" style="justify-content:center;">Error 404</span>
      <h1>This page took a wrong turn.</h1>
      <p class="lead" style="margin:0 auto 24px;">The page you're looking for doesn't exist or may have moved.</p>
      <a class="btn" href="index.html">Back to homepage</a>
    </div>
  </section>
</main>
"""
    html = page(
        title="Page Not Found — TechPulse Hub",
        description="The page you're looking for doesn't exist or may have moved.",
        keywords="", canonical_path="404.html", body_html=body
    )
    write("404.html", html)

print("Static page builders ready.")

# ---------------------------------------------------------------------
# SITEMAP + ROBOTS
# ---------------------------------------------------------------------
def build_sitemap():
    urls = [("index.html", "1.0", "weekly"), ("blog.html", "0.9", "weekly"),
            ("about.html", "0.5", "monthly"), ("contact.html", "0.4", "monthly"),
            ("privacy-policy.html", "0.3", "yearly"), ("terms.html", "0.3", "yearly")]
    entries = "".join(
        "  <url><loc>{URL}/{PATH}</loc><lastmod>{TODAY}</lastmod><changefreq>{FREQ}</changefreq><priority>{PRI}</priority></url>\n".format(
            URL=SITE_URL, PATH=path, TODAY=TODAY, FREQ=freq, PRI=pri
        ) for path, pri, freq in urls
    )
    for p in POSTS:
        entries += "  <url><loc>{URL}/posts/{SLUG}.html</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n".format(
            URL=SITE_URL, SLUG=p["slug"], DATE=p["date"]
        )
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + "</urlset>\n"
    write("sitemap.xml", xml)

def build_robots():
    txt = """User-agent: *
Allow: /

Sitemap: {URL}/sitemap.xml
""".format(URL=SITE_URL)
    write("robots.txt", txt)

def build_logo_favicon():
    logo = """<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120">
  <rect width="120" height="120" rx="24" fill="#12161f"/>
  <path d="M30 80 L30 40 L50 40 L50 48 L38 48 L38 56 L48 56 L48 64 L38 64 L38 80 Z" fill="#3D5AFE"/>
  <circle cx="82" cy="60" r="22" fill="none" stroke="#00B39B" stroke-width="6"/>
  <circle cx="82" cy="60" r="6" fill="#00B39B"/>
</svg>"""
    write("images/logo.svg", logo)
    favicon = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#12161f"/>
  <circle cx="34" cy="30" r="12" fill="none" stroke="#3D5AFE" stroke-width="4"/>
  <circle cx="34" cy="30" r="3" fill="#00B39B"/>
  <path d="M18 46 L46 46" stroke="#00B39B" stroke-width="4" stroke-linecap="round"/>
</svg>"""
    write("images/favicon.svg", favicon)
    # generic OG fallback image (svg — replace with a real 1200x630 JPG/PNG before launch)
    og = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#12161f"/>
  <circle cx="1000" cy="120" r="180" fill="#3D5AFE" opacity="0.15"/>
  <text x="80" y="320" font-family="Space Grotesk, sans-serif" font-size="64" font-weight="700" fill="#ffffff">TechPulse Hub</text>
  <text x="80" y="370" font-family="JetBrains Mono, monospace" font-size="22" fill="#c8cddb">Gadgets and software, without the hype.</text>
</svg>"""
    write("images/og-default.svg", og)

print("Sitemap/robots/branding builders ready.")

# ---------------------------------------------------------------------
# BUILD EVERYTHING
# ---------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "images", "covers"), exist_ok=True)
    build_logo_favicon()
    build_home()
    build_blog()
    build_articles()
    build_about()
    build_contact()
    build_privacy()
    build_terms()
    build_404()
    build_sitemap()
    build_robots()
    print("\\nBUILD COMPLETE —", len(POSTS), "articles + all core pages generated.")
