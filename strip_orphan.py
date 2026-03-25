#!/usr/bin/env python3
"""Remove the orphan broken-injection code that follows the good DOMContentLoaded block."""
import re, os

FILES = [
    "amazon.com/index.html",
    "bing.com/index.html",
    "btcpayserver.org/index.html",
    "duckduckgo.com/index.html",
    "netflix.com/index.html",
    "phoenix.acinq.co/index.html",
    "temu.com/index.html",
    "tiktok.com/index.html",
    "weather.com/index.html",
    "yahoo.co.jp/index.html",
    "yahoo.com/index.html",
]

# The orphan block starts with "    };" after the good closing "  });"
# and ends with "  });" just before "</script>"
# Pattern: after our good DOMContentLoaded ends (  });), remove everything up to </script>,
# then put </script> back.
ORPHAN = re.compile(
    r'(  \}\);\n)    \};\n    tryWrap.*?  \}\);\n(</script>)',
    re.DOTALL
)

BASE = "/home/waheed/WebCrawl"
for rel in FILES:
    path = os.path.join(BASE, rel)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    new_html, n = ORPHAN.subn(r'\1\2', html, count=1)
    if n == 0:
        print(f"  SKIP (orphan not found): {rel}")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  OK: {rel}")

print("\nDone.")
