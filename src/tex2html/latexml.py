from dataclasses import dataclass
from pathlib import Path
import subprocess
import typer

from .log_handling import list_missing_packages, list_undefined_macros
from . import ui


# Configuration
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
    is_fatal: bool  # True if conversion completely failed or timed out


def convert_latex_to_html(input_file: Path, output_file: Path, output_dir: Path) -> LaTeXMLOutput:
    """Convert LaTeX file to HTML using LaTeXML."""
    log_path = output_dir / "_stdout.txt"

    ui.console.print(f"Logfile is at '{log_path}'.")

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

    ui.console.print(f"Command: {' '.join(latexml_config)}")

    returncode = -1
    is_fatal = False

    # 1. Provide visual feedback during the long conversion process
    with ui.console.status("[bold blue]Running LaTeXML conversion (this may take a while)...[/bold blue]"):
        try:
            result = subprocess.run(
                latexml_config,
                check=False,
                text=True,
                timeout=LATEXML_TIMEOUT_SEC + 5,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE, # Capture stdout so it doesn't bleed into the CLI
            )
            returncode = result.returncode
            if result.stderr:
                ui.console.print("[dim]Output: [/dim]")
                ui.console.print(f"[dim]{result.stderr.strip()}[/dim]")

            # LaTeXML semantics: 0=Success, 1=Warnings, 2=Errors (partial output), 3+=Fatal
            if returncode == 0:
                ui.console.print(f"[bold green]Successfully written LaTeXML conversion to {output_file.name}[/bold green]")
            elif returncode == 1:
                ui.console.print(f"[bold yellow]Converted with warnings. Exit code: {returncode}[/bold yellow]")
            else:
                ui.console.print(f"[bold red]LaTeXML encountered a fatal error (Exit code {returncode})[/bold red]")
                is_fatal = True

            if "LaTeXML died!" in result.stderr:
                ui.console.print(f"[bold red]LaTeXML process died unexpectedly.[/bold red]")
                is_fatal = True
            

        except subprocess.TimeoutExpired:
            ui.console.print(f"[bold red]LaTeXML conversion timed out after {LATEXML_TIMEOUT_SEC}s[/bold red]")
            is_fatal = True
        except FileNotFoundError:
            ui.console.print("[bold red]Could not find 'latexmlc.bat'. Is LaTeXML installed and in your PATH?[/bold red]")
            is_fatal = True
        except Exception as e:
            ui.console.print(f"[bold red]Unexpected execution error:[/bold red] {e}")
            is_fatal = True

    # 2. Safely parse logs (only if the process actually ran and created the file)
    missing_packages = []
    undefined_macros = []
    
    if log_path.exists():
        missing_packages = list_missing_packages(log_path)
        if missing_packages:
            ui.console.print(f"[yellow]  Missing packages:[/yellow] {', '.join(missing_packages)}")
            
        undefined_macros = list_undefined_macros(log_path)
        if undefined_macros:
            ui.console.print(f"[yellow]  Undefined macros:[/yellow] {', '.join(undefined_macros)}")

    return LaTeXMLOutput(
        returncode=returncode,
        missing_packages=missing_packages,
        undefined_macros=undefined_macros,
        is_fatal=is_fatal,
    )