import re
import glob

# regex patterns to remove
patterns = [
    # facebook domain verification
    r'<meta name="facebook-domain-verification" content="[^"]*">\s*',
    # dns prefetch for googletagmanager
    r'<link rel="dns-prefetch" href="//www\.googletagmanager\.com">\s*',
    # R4aKrnBMyhUp.com scripts (which is GTM renamed)
    r'<script async=""\s*src="R4aKrnBMyhUp\.com/[^"]*"></script>\s*',
    # GTM snippet that calls R4aKrnBMyhUp.com
    r'<script>\(function \(w, d, s, l, i\).*?</script>\s*',
    # GTM noscript iframe
    r'<noscript><iframe src="https://R4aKrnBMyhUp\.com/ns\.html\?id=GTM-[^"]*" height="0" width="0"\s*style="display:none;visibility:hidden"></iframe></noscript>\s*',
    # Start and End Google Tag Manager comments
    r'<!-- Start Google Tag Manager -->\s*',
    r'<!-- End Google Tag Manager -->\s*',
    r'<!-- End Google Tag Manager \(noscript\) -->\s*',
    # GTM kit plugin scripts
    r'<script id="gtmkit-js-before"[^>]*>.*?</script>\s*',
    r'<script id="gtmkit-datalayer-js-before"[^>]*>.*?</script>\s*',
    r'<script src="[^"]*gtm-kit[^"]*"[^>]*></script>\s*'
]

for filepath in glob.glob("index-*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    for pattern in patterns:
        content = re.sub(pattern, "", content, flags=re.DOTALL)
        
    with open(filepath, "w", encoding="utf-8") as out:
        out.write(content)

print("Cleaned up tracking from localized files.")
