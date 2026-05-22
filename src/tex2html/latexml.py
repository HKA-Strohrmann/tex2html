
# LaTeX to HTML conversion using LaTeXML
from dataclasses import dataclass
from pathlib import Path
import subprocess

import typer

from .log_handling import list_missing_packages, list_undefined_macros
from . import ui

# Configuration constants
CUSTOM_BINDINGS = ["trfsigns.sty.ltxml"]
LATEXML_PATHS = ["/test/chapters", "/test/media", "/assets/bindings"]
LATEXML_TIMEOUT_SEC = 540
LATEXML_URL_BASE = "https://arxiv.org/static/browse/0.3.4"
JAVASCRIPT_URL = f"{LATEXML_URL_BASE}/js/arxiv-html-papers-20260131.js"
CSS_URL = f"{LATEXML_URL_BASE}/css/arxiv-html-papers-20260131.css"


@dataclass
class LaTeXMLOutput:
    returncode: int
    missing_packages: list[str]
    undefined_macros: list[str]


def convert_latex_to_html(input_file: Path, output_file: Path, output_dir: Path) -> LaTeXMLOutput:
    """Convert LaTeX file to HTML using LaTeXML."""

    log_path = (output_dir / "_stdout.txt")

    # Build LaTeXML command
    latexml_config = [
        "latexmlc.bat",
        "--whatsin=directory",
        "--pmml",
        "--mathtex",
        "--noinvisibletimes",
        "--format=html5",
        "--navigationtoc=context",
        "--splitat=section",
        f"--log={log_path}",
        f"--timeout={LATEXML_TIMEOUT_SEC}",
        f"--css={CSS_URL}",
        f"--javascript={JAVASCRIPT_URL}",
        f"--dest={output_file}",
    ]
    for binding in CUSTOM_BINDINGS:
        latexml_config.append(f"--preload={binding}")
    for path in LATEXML_PATHS:
        latexml_config.append(f"--path={path}")
    latexml_config.append(str(input_file))

    ui.console.print(f"[blue] Converting LaTeX to HTML with '{ ' '.join(latexml_config) }'... [/blue]")

    returncode = 0
    try:
        result = subprocess.run(
            latexml_config,
            check=False,    # dont raise exception on non-zero exit, we will handle it based on returncode and log content
            text=True,
            timeout=LATEXML_TIMEOUT_SEC + 5,
            # stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            if result.stderr:
                ui.console.print(f"[bold red]LaTeXML conversion failed: {result.stderr}[/bold red]")
        
        returncode = result.returncode
    except subprocess.TimeoutExpired:
        ui.console.print(f"[bold red]LaTeXML conversion timed out after {LATEXML_TIMEOUT_SEC}s [/bold red]")
        returncode = 1
    except Exception as e:
        ui.console.print(f"[bold red]LaTeXML conversion failed:[/bold red] {e}")
        returncode = 1

    if returncode == 0:
        ui.console.print(f"[bold green]Successfully written LaTeXML conversion to {output_file}[/bold green]")
    
    missing_packages = list_missing_packages(log_path)
    if missing_packages:
        ui.console.print(f"[yellow]Missing packages: {', '.join(missing_packages)}[/yellow]")
    undefined_macros = list_undefined_macros(log_path)
    if undefined_macros:
        ui.console.print(f"[yellow]Undefined macros: {', '.join(undefined_macros)}[/yellow]")

    return LaTeXMLOutput(
        returncode=returncode,
        missing_packages=missing_packages,
        undefined_macros=undefined_macros,
    )
