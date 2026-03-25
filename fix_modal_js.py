#!/usr/bin/env python3
"""Replace the broken tryWrap approach with immediate event delegation + loading state."""
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

# Replace the DOMContentLoaded block with a simpler, race-condition-free version
OLD_PATTERN = re.compile(
    r'  document\.addEventListener\(\'DOMContentLoaded\'.*?  \}\);\n',
    re.DOTALL
)

NEW_JS = """\
  document.addEventListener('DOMContentLoaded', function () {
    var modal    = document.getElementById('diag-modal');
    var inner    = document.getElementById('diag-modal-inner');
    var closeBtn = document.getElementById('diag-close');

    // Make every .diagram-wrap clickable immediately — no waiting for Mermaid
    document.querySelectorAll('.diagram-wrap').forEach(function(wrap) {
      wrap.style.cursor = 'zoom-in';
      wrap.addEventListener('click', function () {
        var mDiv = wrap.querySelector('.mermaid');
        if (mDiv) openModal(mDiv);
      });
    });

    function openModal(mDiv) {
      // Clear previous content (keep close button)
      inner.querySelectorAll('svg, .diag-loading').forEach(function(el) { el.remove(); });
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';

      var svg = mDiv.querySelector('svg');
      if (svg) {
        showSvg(svg);
      } else {
        // Mermaid hasn't rendered yet — show loader and wait
        var loader = document.createElement('p');
        loader.className = 'diag-loading';
        loader.textContent = 'Rendering diagram…';
        loader.style.cssText = 'color:#8892b0;text-align:center;padding:60px 20px;font-size:1rem;';
        inner.appendChild(loader);

        var timer = setInterval(function () {
          var s = mDiv.querySelector('svg');
          if (s) {
            clearInterval(timer);
            loader.remove();
            showSvg(s);
          }
        }, 80);
      }
    }

    function showSvg(svg) {
      inner.querySelectorAll('svg').forEach(function(s) { s.remove(); });
      var clone = svg.cloneNode(true);
      clone.removeAttribute('width');
      clone.removeAttribute('height');
      // Let CSS control sizing
      clone.style.cssText = '';
      inner.appendChild(clone);
    }

    function closeModal() {
      modal.classList.remove('open');
      document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });
  });
"""

BASE = "/home/waheed/WebCrawl"
for rel in FILES:
    path = os.path.join(BASE, rel)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    new_html, n = OLD_PATTERN.subn(NEW_JS, html, count=1)
    if n == 0:
        print(f"  SKIP (pattern not found): {rel}")
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"  OK: {rel}")

print("\nDone.")
