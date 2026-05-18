# Tex 2 HTML

This tools converts LaTeX source files to HTML using LaTeXML. The process if forked from arvix.

## Install

## Usage

## Test

```bash
copy-item "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\doc2tex\test\chapters" -destination "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\tex2html\test" -recurse
copy-item "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\doc2tex\test\media" -destination "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\tex2html\test" -recurse
copy-item "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\doc2tex\test\svg-inkscape" -destination "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\tex2html\test" -recurse
copy-item "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\doc2tex\test\combined.tex" -destination "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\tex2html\test" -recurse


uv run tex2html --input test/combined.tex --output test/html/
```
