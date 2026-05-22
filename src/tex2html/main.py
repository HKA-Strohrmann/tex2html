from pathlib import Path
import shutil
import typer
from typing import Annotated

from . import ui

from .latexml import convert_latex_to_html, LaTeXMLOutput


app = typer.Typer(help="CLI for LaTeX to HTML conversion")

@app.command()
def main(
    input_file: Annotated[str, typer.Argument(help="Input LaTeX file")],
    output_file: Annotated[str, typer.Option("--output-file", help="Output file")] = "html/output.html",
) -> typer.Exit:
    """Convert a LaTeX file to HTML."""    

    input_path = Path(input_file)
    if not input_path.exists():
        raise typer.BadParameter(f"Input file '{input_path}' does not exist.")
    if not input_path.is_file() or input_path.suffix != ".tex":
        raise typer.BadParameter(f"Input must be a .tex file: {input_path}")
    
    output_path = Path(output_file)
    if not output_path.suffix == ".html":
        raise typer.BadParameter(f"Output file '{output_path}' is not a .html file.")
    
    output_dir = output_path.parent
    if output_dir.exists():
        shutil.rmtree(output_dir, ignore_errors=True)
        ui.console.print(f"Cleared output directory '{output_dir}'.")    
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        result: LaTeXMLOutput = convert_latex_to_html(input_path, output_path, output_dir)
        return typer.Exit(code=result.returncode or 0)

    except Exception as e:
        ui.console.print(f"[bold red]Unexpected Error:[/bold red] {e}")
        return typer.Exit(code=2)
