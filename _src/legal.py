"""Legal pages for the Cabaña 28 site. Plain-language templates, not legal advice."""

UPDATED = "November 11, 2026"


def pages(tel, phone):
    call = f'<a href="{tel}">{phone}</a>'
    addr = "6351 N Andrews Ave, Fort Lauderdale, FL 33309"
    return {
        "privacy": ("Privacy Policy", f"""
<p>This policy explains what information the Cabaña 28 website collects and how it is used. It applies to this website only.</p>
<h2>What we collect</h2>
<p>This website has no forms, accounts or newsletter, and we do not collect your name, email, phone number or payment details through it. We do not sell or share personal information.</p>
<p>If you call us, including to order catering, we only use what you tell us to answer your question, take your order and deliver it.</p>
<h2>Online ordering and delivery</h2>
<p>When you click to order, you leave this website. Delivery and pickup orders on our ordering page are handled by orders.co, and we are also on DoorDash, Uber Eats and ezCater. Those companies collect the information needed to place your order, including payment details, under their own privacy policies. Please read their policies before you order.</p>
<h2>Third-party services on this site</h2>
<p>This website loads an embedded Google Map and fonts from Google Fonts. When your browser loads them, Google may receive technical information such as your IP address and browser type. Google's use of that information is covered by the <a href="https://policies.google.com/privacy">Google Privacy Policy</a>. Our website host, GitHub Pages, may keep standard server logs for security.</p>
<h2>Cookies</h2>
<p>This website does not set its own cookies or use advertising or tracking tools. The embedded Google Map may set cookies. You can block or delete cookies in your browser settings, and the rest of the site will still work.</p>
<h2>Children</h2>
<p>This website is not directed to children under 13, and we do not knowingly collect information from them.</p>
<h2>Changes</h2>
<p>We may update this policy. The date at the top shows when it last changed.</p>
<h2>Contact</h2>
<p>Questions about this policy? Call us at {call} or visit us at {addr}.</p>
"""),
        "terms": ("Terms of Use", f"""
<p>By using the Cabaña 28 website you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>Menu, prices and hours</h2>
<p>We work to keep the menu, prices, photos and hours on this site accurate, but they can change without notice and may differ from what is in the restaurant or on our ordering partners. Photos show how dishes are typically served; portions and plating may vary. The price you pay is the price shown at checkout or in the restaurant.</p>
<h2>Allergies and food safety</h2>
<p>Our kitchen handles fish, shellfish, milk, eggs, wheat, soy, peanuts and tree nuts, and we cannot guarantee that any dish is free of allergens. Tell us about any allergy before you order. Some dishes, including our ceviches and leche de tigre, are served raw or undercooked. Consuming raw or undercooked meats, poultry, seafood, shellfish, or eggs may increase your risk of foodborne illness, especially if you have certain medical conditions.</p>
<h2>Ordering through other companies</h2>
<p>Links to orders.co, DoorDash, Uber Eats and ezCater take you to independent services. Orders, payments, delivery times, refunds and fees on those services are governed by their own terms. We are not responsible for the content or practices of other websites.</p>
<h2>Our content</h2>
<p>The Cabaña 28 name, photos, text and design of this site belong to Cabaña 28. You may share links to the site, but you may not copy or reuse its content for commercial purposes without our written permission.</p>
<h2>No warranties</h2>
<p>This website is provided as is. We do not promise that it will always be available or free of errors.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent allowed by law, Cabaña 28 is not liable for any indirect or consequential damages arising from your use of this website.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the State of Florida. Any dispute will be handled in the courts of Broward County, Florida.</p>
<h2>Changes</h2>
<p>We may update these terms. The date at the top shows when they last changed.</p>
<h2>Contact</h2>
<p>Call us at {call} or visit us at {addr}.</p>
"""),
        "accessibility": ("Accessibility", f"""
<p>We want everyone to be able to use our website, read our menu and order from us.</p>
<h2>Our goal</h2>
<p>We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1, Level AA. This site is built with readable text contrast, headings in a logical order, text descriptions on photos, keyboard navigation with visible focus, a skip link to the main content, and support for reduced-motion settings. The full menu is written as text, not as an image, so screen readers can read it.</p>
<h2>Known limits</h2>
<p>The embedded Google Map and the ordering pages at orders.co, DoorDash, Uber Eats and ezCater are run by other companies, and we cannot control how accessible they are.</p>
<h2>Need help or found a problem?</h2>
<p>If something on this site is hard to use, call us at {call}. We will read you the menu, answer questions and take your order by phone. Please also tell us about the problem so we can fix it.</p>
<p>Our restaurant is at {addr}.</p>
"""),
    }


CSS = """  <style>
    .legal { max-width: 760px; padding: 64px 24px 96px; }
    .legal h1 { font-size: clamp(34px, 4.5vw, 52px); margin-bottom: 10px; color: var(--red); }
    .legal .updated { color: var(--muted); font-size: 15px; margin: 0 0 36px; }
    .legal h2 { font-size: 22px; margin: 40px 0 12px; color: var(--red); }
    .legal p { color: var(--ink-soft); margin: 0 0 14px; }
    .legal a { color: var(--red); }
    @media (max-width: 760px) { .legal { padding: 48px 16px 72px; } }
  </style>"""


def main_html(title, body):
    return f"""    <div class="wrap legal">
      <p class="kicker">Cabaña 28</p>
      <h1>{title}</h1>
      <p class="updated">Last updated {UPDATED}</p>
{body}
    </div>
"""
