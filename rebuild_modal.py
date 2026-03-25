#!/usr/bin/env python3
"""Rebuild clean modal in all analysis pages by replacing the broken script block."""
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

MODAL_HTML = """<!-- Diagram Modal -->
<div id="diag-modal" role="dialog" aria-modal="true" aria-label="Diagram viewer">
  <div id="diag-modal-inner">
    <button id="diag-close" aria-label="Close diagram">&times;</button>
  </div>
</div>

"""

BASE = "/home/waheed/WebCrawl"

for rel in FILES:
    path = os.path.join(BASE, rel)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # ── 1. Extract the themeVariables block from the broken script ──
    tv_match = re.search(
        r'(    themeVariables: \{.*?    \})',
        html,
        flags=re.DOTALL
    )
    if not tv_match:
        print(f"  SKIP (no themeVariables): {rel}")
        continue
    theme_vars = tv_match.group(1)

    # ── 2. Build the clean script block ──
    clean_script = f"""<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'dark',
{theme_vars}
  }});

  document.addEventListener('DOMContentLoaded', function () {{
    // Wrap each mermaid diagram to make it clickable
    var tryWrap = function(attempts) {{
      var divs = document.querySelectorAll('.mermaid');
      var allRendered = [].every.call(divs, function(d) {{ return d.querySelector('svg'); }});
      if (!allRendered && attempts > 0) {{
        return setTimeout(function() {{ tryWrap(attempts - 1); }}, 300);
      }}
      [].forEach.call(divs, function(div) {{
        if (div.parentNode && div.parentNode.classList && div.parentNode.classList.contains('diagram-click')) return;
        var wrap = document.createElement('div');
        wrap.className = 'diagram-click';
        wrap.style.cssText = 'cursor:zoom-in;position:relative;';
        div.parentNode.insertBefore(wrap, div);
        wrap.appendChild(div);
        wrap.addEventListener('click', function() {{ openModal(div); }});
      }});
    }};
    tryWrap(20);

    var modal    = document.getElementById('diag-modal');
    var inner    = document.getElementById('diag-modal-inner');
    var closeBtn = document.getElementById('diag-close');

    function openModal(sourceDiv) {{
      var svg = sourceDiv.querySelector('svg');
      if (!svg) return;
      inner.querySelectorAll('svg').forEach(function(s) {{ s.remove(); }});
      var clone = svg.cloneNode(true);
      clone.removeAttribute('width');
      clone.removeAttribute('height');
      clone.style.cssText = 'width:auto;height:auto;max-width:88vw;max-height:80vh;display:block;margin:0 auto;';
      inner.appendChild(clone);
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    }}

    function closeModal() {{
      modal.classList.remove('open');
      document.body.style.overflow = '';
    }}

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function(e) {{ if (e.target === modal) closeModal(); }});
    document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') closeModal(); }});
  }});
</script>
</body>
</html>"""

    # ── 3. Remove the broken script block (from <script> to </html>) ──
    html = re.sub(
        r'\n<script>\n  mermaid\.initialize\(\{.*',
        '\n' + MODAL_HTML + clean_script,
        html,
        flags=re.DOTALL
    )

    # ── 4. Ensure duplicate .diagram-wrap CSS doesn't exist (clean up) ──
    # The existing CSS in <style> already has diagram-wrap from original + our injected
    # Remove our injected duplicate if pattern appears twice
    count = html.count('.diagram-wrap {')
    if count > 1:
        # Remove the last occurrence block (the one we injected at the bottom of <style>)
        html = re.sub(
            r'\n    /\* ── Diagram Modal ── \*/\n    \.diagram-wrap \{.*?#diag-close:hover \{ color: #fff; \}\n',
            '\n',
            html,
            count=1,
            flags=re.DOTALL
        )

    # ── 5. Ensure modal CSS is present ──
    if '#diag-modal {' not in html:
        modal_css = """
    /* ── Diagram Modal ── */
    .diagram-click { cursor: zoom-in; }
    #diag-modal {
      display: none; position: fixed; inset: 0; z-index: 9999;
      background: rgba(0,0,0,.88); backdrop-filter: blur(6px);
      align-items: center; justify-content: center; padding: 24px;
    }
    #diag-modal.open { display: flex; }
    #diag-modal-inner {
      position: relative; max-width: 95vw; max-height: 92vh; overflow: auto;
      background: #1a1d27; border: 1px solid #2d3250; border-radius: 16px;
      padding: 48px 32px 32px; box-shadow: 0 24px 80px rgba(0,0,0,.8);
    }
    #diag-close {
      position: absolute; top: 12px; right: 16px; background: none; border: none;
      color: #8892b0; font-size: 1.6rem; cursor: pointer; line-height: 1; transition: color .2s;
    }
    #diag-close:hover { color: #fff; }
"""
        html = html.replace('  </style>', modal_css + '  </style>', 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK: {rel}")

print("\nAll done.")
