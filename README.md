# Tex 2 HTML

This tools converts LaTeX source files to HTML using LaTeXML. The process if forked from arvix.

## Install

```
git clone
cd tex2html
uv sync

```

## Usage

## Test

```bash
copy-item "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\doc2tex\test\skript\chapters" -destination "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\tex2html\test" -recurse -force
copy-item "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\doc2tex\test\skript\new media" -destination "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\tex2html\test" -recurse -force
copy-item "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\doc2tex\test\skript\combined.tex" -destination "C:\Users\Jax\Coding\Strohrmann-Lecture-Platform\tex2html\test" -recurse -force

cd test
uv run tex2html "test.tex" --output-file "html/test.html"
```

```bash
latexmk -C --outdir="_build" && latexmk -pdf -interaction=nonstopmode -synctex=1 -file-line-error --shell-escape --outdir="_build" combined.tex
latexmk -C --outdir="_build" && latexmk -lualatex -pdf -interaction=nonstopmode -synctex=1 -file-line-error --shell-escape --outdir="_build" combined.tex
```

## To Do

- Replace scrbook with book. KOMA is not supported by LaTeXML.
- create binding for awesomefont5
- --whatsout=fragment for embedding in other pages?
- create binding to supress tcolorbox errors
- --javascript=LaTeXML-maybeMathJax.js: The LaTeXML-maybeMathJax.js script loads MathJax for browsers without native MathML support, as a fallback rendering solution.