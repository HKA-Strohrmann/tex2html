from bs4 import BeautifulSoup
import json

# 1. Load your LaTeXML output
with open('output.html', 'r', encoding='utf-8') as f:
    raw_html = f.read()

# 2. Extract ONLY the core article content
soup = BeautifulSoup(raw_html, 'html.parser')
article_node = soup.find('article', class_='ltx_document')

# 3. Convert the node back to a string and safely escape it for JavaScript
article_html = str(article_node)
safe_html_string = json.dumps(article_html)

# 4. Generate the MDX file content
mdx_content = f"""---
title: My LaTeX Document
sidebar_position: 1
---

import Head from '@docusaurus/Head';

{/* Inject LaTeXML styles and scripts only for this page */}
<Head>
  <link rel="stylesheet" href="/latex-assets/LaTeXML.css" />
  <link rel="stylesheet" href="/latex-assets/ltx-book.css" />
  <link rel="stylesheet" href="/latex-assets/arxiv-html-papers-20260131.css" />
  <script src="/latex-assets/arxiv-html-papers-20260131.js"></script>
</Head>

{/* Safely inject the raw HTML bypassing JSX strictness */}
<div dangerouslySetInnerHTML={{{{ __html: {safe_html_string} }}}} />
"""

# 5. Save directly into your Docusaurus docs directory
with open('my-docusaurus-project/docs/my-latex-doc.mdx', 'w', encoding='utf-8') as f:
    f.write(mdx_content)