# TechPulse Hub — Static Blog Website

A complete, ready-to-deploy blog website: 5 full articles, an SEO setup
(meta tags, Open Graph, JSON-LD structured data, sitemap.xml, robots.txt),
and the pages Google AdSense requires before it will approve a site
(About, Contact, Privacy Policy, Terms of Service).

It's plain HTML/CSS/JS — no build step, no server, no database required.
You can open `index.html` directly in a browser right now.

## 1. Before you deploy — required changes

Open `generate.py`, edit the top of the file, then re-run `python3 generate.py`
to regenerate every page with your real details (or hand-edit the HTML files
directly if you don't want to touch Python):

| Variable | What to change it to |
|---|---|
| `SITE_URL` | Your real domain, e.g. `https://www.yoursite.com` |
| `SITE_NAME` | Your blog's real name, if different from "TechPulse Hub" |
| `AUTHOR` | Your name or team name |

Also replace:
- **`hello@techpulsehub.com`** in `contact.html` with your real email.
- The bracketed placeholders in `privacy-policy.html` and `terms.html`
  with your real business/contact information.
- `images/og-default.svg` and the cover images in `images/covers/` with
  real photos/graphics if you want richer social-share previews (SVG
  placeholders are included so the site works immediately, but a real
  1200x630 JPG/PNG performs better on social platforms).

## 2. How to deploy (pick one — all are free for a site this size)

### Option A: Netlify (easiest, drag-and-drop)
1. Go to https://app.netlify.com/drop
2. Drag the whole `techpulse-hub` folder onto the page.
3. Netlify gives you a live URL immediately. Add a custom domain under
   Site settings → Domain management if you own one.

### Option B: Vercel
1. Go to https://vercel.com/new
2. Import this folder (or push it to a GitHub repo first and import the repo).
3. Framework preset: "Other" / static site. Deploy.

### Option C: GitHub Pages (free, good for a personal project)
1. Create a new GitHub repository and push this folder's contents to it.
2. Go to Settings → Pages → Source, select the `main` branch and `/root`.
3. Your site will be live at `https://yourusername.github.io/reponame/`.
   If you want a root-level custom domain, add a `CNAME` file with your
   domain name in it and configure your DNS provider accordingly.

### Option D: Any traditional web host
Upload every file and folder here via FTP/cPanel File Manager into your
host's public web folder (often called `public_html` or `www`). No PHP,
database, or special server config is needed.

## 3. Connecting Google AdSense

1. Deploy the site live on your own domain first — AdSense will not
   review a site that isn't publicly accessible.
2. Make sure the site has been live for a little while with real,
   original content (this site ships with 5 full articles — adding
   more before applying will improve your approval odds).
3. Go to https://www.google.com/adsense, sign up, and add your site's URL.
4. Google will give you a snippet like:
   ```html
   <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
   ```
   Paste your real `ca-pub-...` ID into the commented-out line already
   present in the `<head>` of every page (search for "GOOGLE ADSENSE" in
   `generate.py`, or find the commented `<script>` tag near the top of
   any `.html` file) and uncomment it.
5. Create an `ads.txt` file at the site root with the line Google gives
   you (looks like `google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0`)
   — this is required for AdSense to serve ads on your domain.
6. Once approved, replace the `.ad-slot` placeholder `<div>` blocks in
   `index.html` and each article page with your real AdSense ad unit
   code (Google's "Ads" → "By ad unit" dashboard gives you the exact
   HTML snippet to paste in).
7. Submit `sitemap.xml` to Google Search Console
   (https://search.google.com/search-console) so Google indexes your
   pages faster.

### Why this site is built AdSense-policy-friendly
- Original, substantive articles (900+ words each) — not spun or
  AI-boilerplate filler content, and not duplicate/scraped content.
- A clear **About**, **Contact**, **Privacy Policy** (mentioning cookies
  and AdSense specifically), and **Terms of Service** page — all
  required by AdSense's program policies.
- Easy site navigation, no deceptive elements, no prohibited content
  categories.
- Mobile-responsive layout and reasonably fast load (no heavy frameworks).
- Ad placeholder slots are clearly separated from article content, not
  disguised as content — this matters for AdSense's ad-placement policies.

Google's actual approval decision is manual and can still take days to
weeks, and depends on factors outside this template (your traffic,
domain age, and how much content you've published by the time you apply).
Publishing more original articles regularly after launch meaningfully
improves approval odds.

## 4. SEO features already included

- Unique `<title>`, meta description, and keywords per page.
- Canonical URLs on every page (prevents duplicate-content issues).
- Open Graph + Twitter Card tags for rich social link previews.
- JSON-LD structured data: `Organization` + `WebSite` on the homepage,
  `Article` + `BreadcrumbList` on every blog post (helps eligibility for
  rich results in Google Search).
- `sitemap.xml` and `robots.txt` at the site root.
- Semantic HTML (`<article>`, `<nav>`, heading hierarchy, alt text on
  every image, a skip-to-content link).
- Internal linking: related posts, a table of contents per article, and
  prev/next navigation.

### Ongoing SEO checklist after launch
- [ ] Submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.
- [ ] Keep publishing original articles — freshness and depth are
      still the strongest ranking signals for content sites.
- [ ] Add real backlinks (guest posts, directories relevant to your niche).
- [ ] Replace SVG cover images with real optimized JPG/WebP images for
      faster load and better image-search visibility.
- [ ] Set up Google Analytics or a privacy-friendly alternative to track
      what's working.

## 5. Editing or adding new articles

Every article is defined in `generate.py` in two places:
1. The `POSTS` list — title, slug, description, category, date, keywords.
2. The `ARTICLE_CONTENT` dictionary — the actual HTML body of the article
   (use `<h2 id="...">` / `<h3 id="...">` for section headings — the
   table of contents is generated automatically from these).

Add a new entry to both, then run:
```bash
python3 generate.py
```
This regenerates every HTML page, the sitemap, and a matching SVG cover
image automatically — you don't need to touch any HTML by hand.

## 6. Folder structure

```
techpulse-hub/
├── index.html            Homepage
├── blog.html              All-articles archive with search/filter
├── about.html
├── contact.html
├── privacy-policy.html    Includes AdSense/cookie disclosures
├── terms.html
├── 404.html
├── sitemap.xml
├── robots.txt
├── generate.py            Site generator — edit this to add/change content
├── css/style.css
├── js/main.js              Nav toggle, reading progress bar, search/filter
├── images/
│   ├── logo.svg, favicon.svg, og-default.svg
│   └── covers/            Auto-generated cover image per article
└── posts/                  One HTML file per article
```

## 7. Local preview

No install needed — just open `index.html` in a browser. For a closer-to-
production preview (so relative links and the search box behave exactly
like they will live), run a simple local server from this folder:
```bash
python3 -m http.server 8000
```
Then visit `http://localhost:8000` in your browser.
