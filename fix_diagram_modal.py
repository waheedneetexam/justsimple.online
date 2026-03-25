#!/usr/bin/env python3
"""Fix/apply clickable diagram modal to all analysis pages (clean pass)."""
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

MODAL_CSS = """
    /* ── Diagram Modal ── */
    .diagram-wrap {
      position: relative;
      cursor: zoom-in;
    }
    .diagram-wrap::after {
      content: '⤢ Click to expand';
      position: absolute;
      bottom: 10px;
      right: 14px;
      background: rgba(0,0,0,.65);
      color: #a78bfa;
      font-size: .75rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 20px;
      pointer-events: none;
      opacity: 0;
      transition: opacity .2s;
    }
    .diagram-wrap:hover::after { opacity: 1; }
    .diagram-wrap:hover { box-shadow: 0 0 0 2px #7c3aed66; border-radius: 12px; }
    #diag-modal {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 9999;
      background: rgba(0,0,0,.88);
      backdrop-filter: blur(6px);
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    #diag-modal.open { display: flex; }
    #diag-modal-inner {
      position: relative;
      max-width: 95vw;
      max-height: 92vh;
      overflow: auto;
      background: #1a1d27;
      border: 1px solid #2d3250;
      border-radius: 16px;
      padding: 48px 32px 32px;
      box-shadow: 0 24px 80px rgba(0,0,0,.8);
    }
    #diag-modal-inner svg {
      width: auto !important;
      height: auto !important;
      max-width: 88vw;
      max-height: 80vh;
      display: block;
      margin: 0 auto;
    }
    #diag-close {
      position: absolute;
      top: 12px;
      right: 16px;
      background: none;
      border: none;
      color: #8892b0;
      font-size: 1.6rem;
      cursor: pointer;
      line-height: 1;
      transition: color .2s;
    }
    #diag-close:hover { color: #fff; }
"""

MODAL_HTML = """<!-- Diagram Modal -->
<div id="diag-modal" role="dialog" aria-modal="true" aria-label="Diagram viewer">
  <div id="diag-modal-inner">
    <button id="diag-close" aria-label="Close diagram">&times;</button>
  </div>
</div>
"""

MODAL_JS = """
  // ── Diagram click-to-expand modal ──
  document.addEventListener('DOMContentLoaded', function () {
    var tryWrap = function(attempts) {
      var divs = document.querySelectorAll('.mermaid');
      var allRendered = Array.prototype.every.call(divs, function(d) { return d.querySelector('svg'); });
      if (!allRendered && attempts > 0) {
        return setTimeout(function() { tryWrap(attempts - 1); }, 300);
      }
      divs.forEach(function(div) {
        if (div.closest && div.closest('.diagram-wrap')) return;
        var wrap = document.createElement('div');
        wrap.className = 'diagram-wrap';
        div.parentNode.insertBefore(wrap, div);
        wrap.appendChild(div);
        wrap.addEventListener('click', function() { openModal(div); });
      });
    };
    tryWrap(20);

    var modal   = document.getElementById('diag-modal');
    var inner   = document.getElementById('diag-modal-inner');
    var closeBtn = document.getElementById('diag-close');

    function openModal(sourceDiv) {
      var svg = sourceDiv.querySelector('svg');
      if (!svg) return;
      inner.querySelectorAll('svg').forEach(function(s) { s.remove(); });
      var clone = svg.cloneNode(true);
      clone.removeAttribute('width');
      clone.removeAttribute('height');
      clone.style.width = '';
      clone.style.height = '';
      inner.appendChild(clone);
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function closeModal() {
      modal.classList.remove('open');
      document.body.style.overflow = '';
    }
    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function(e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeModal(); });
  });
"""

BASE = "/home/waheed/WebCrawl"

for rel in FILES:
    path = os.path.join(BASE, rel)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # ── Step 1: Clean up any previous (broken) injection ──
    # Remove duplicate <script> tag that appears right after <script>
    html = re.sub(r'(<script>)\n\s*<script>', r'\1', html)

    # Remove the stale guard call we injected last time
    html = html.replace(
        '  mermaid.initialize && mermaid.initialize({ startOnLoad: true });\n', ''
    )

    # Remove broken modal HTML+JS if already present (so we can reinject cleanly)
    html = re.sub(
        r'\n<!-- Diagram Modal -->.*?</div>\n\n',
        '\n',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'\n  // ── Diagram click-to-expand modal ──.*?  }\);\n',
        '\n',
        html,
        flags=re.DOTALL
    )

    # ── Step 2: Add CSS if missing ──
    if 'diagram-wrap' not in html:
        html = html.replace('  </style>', MODAL_CSS + '  </style>', 1)

    # ── Step 3: Insert modal HTML before the closing mermaid <script> block ──
    if 'diag-modal' not in html:
        html = re.sub(
            r'\n<script>\n  mermaid\.initialize\(',
            '\n' + MODAL_HTML + '\n<script>\n  mermaid.initialize(',
            html,
            count=1
        )

    # ── Step 4: Append modal JS inside the script block before </script> ──
    if 'diag-modal' in html and 'addEventListener' not in html:
        # Find the closing of mermaid.initialize and append after it
        html = re.sub(
            r'(  \}\);\n)(</script>\n</body>)',
            r'\1' + MODAL_JS + r'\2',
            html,
            count=1
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK: {rel}")

print("\nAll done.")
