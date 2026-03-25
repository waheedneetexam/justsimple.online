#!/usr/bin/env python3
"""Add clickable diagram modal lightbox to all analysis pages."""
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

    /* Modal overlay */
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

MODAL_HTML = """
<!-- Diagram Modal -->
<div id="diag-modal" role="dialog" aria-modal="true" aria-label="Diagram viewer">
  <div id="diag-modal-inner">
    <button id="diag-close" aria-label="Close diagram">&times;</button>
  </div>
</div>
"""

MODAL_JS = """
  // ── Diagram click-to-expand modal ──
  mermaid.initialize && mermaid.initialize({ startOnLoad: true });
  document.addEventListener('DOMContentLoaded', function () {
    // Wait for mermaid to render SVGs
    const tryWrap = (attempts) => {
      const divs = document.querySelectorAll('.mermaid');
      const allRendered = [...divs].every(d => d.querySelector('svg'));
      if (!allRendered && attempts > 0) {
        return setTimeout(() => tryWrap(attempts - 1), 300);
      }
      divs.forEach(div => {
        if (div.closest('.diagram-wrap')) return; // already wrapped
        const wrap = document.createElement('div');
        wrap.className = 'diagram-wrap';
        div.parentNode.insertBefore(wrap, div);
        wrap.appendChild(div);
        wrap.addEventListener('click', () => openModal(div));
      });
    };
    tryWrap(20);

    const modal  = document.getElementById('diag-modal');
    const inner  = document.getElementById('diag-modal-inner');
    const closeBtn = document.getElementById('diag-close');

    function openModal(sourceDiv) {
      const svg = sourceDiv.querySelector('svg');
      if (!svg) return;
      // Remove any previous clone
      inner.querySelectorAll('svg').forEach(s => s.remove());
      const clone = svg.cloneNode(true);
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
    modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
  });
"""

BASE = "/home/waheed/WebCrawl"
ok = 0
skip = 0

for rel in FILES:
    path = os.path.join(BASE, rel)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Skip if already done
    if "diag-modal" in html:
        print(f"  SKIP (already done): {rel}")
        skip += 1
        continue

    # 1. Inject CSS before </style>
    if MODAL_CSS.strip() not in html:
        html = html.replace("  </style>", MODAL_CSS + "  </style>", 1)

    # 2. Inject modal HTML before <script> at the end (the mermaid init script)
    # Find the last <script> block (mermaid.initialize)
    html = re.sub(
        r'(<script>\s*\n\s*mermaid\.initialize\()',
        MODAL_HTML + r'\n<script>\n  \1',
        html,
        count=1
    )

    # 3. Replace the closing </script> of the mermaid block with modal JS + </script>
    # The mermaid init script ends with  });  then </script>
    html = re.sub(
        r'(\s*}\s*\);\s*\n</script>\s*\n</body>)',
        r'\1',  # keep as-is, we'll inject differently
        html
    )

    # Actually inject modal JS right before the closing </script></body>
    # Find mermaid.initialize block end
    html = re.sub(
        r'(  \}\);\n</script>\n</body>)',
        MODAL_JS + r'\n</script>\n</body>',
        html,
        count=1
    )

    # Remove duplicate mermaid.initialize — the MODAL_JS has a guard call but the original is still there
    # The original mermaid.initialize is fine, just remove the guard line from MODAL_JS
    # Actually we added "mermaid.initialize && mermaid.initialize({ startOnLoad: true });" in MODAL_JS
    # which is harmless (calling initialize twice is safe with mermaid v10)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK: {rel}")
    ok += 1

print(f"\nDone: {ok} updated, {skip} skipped.")
