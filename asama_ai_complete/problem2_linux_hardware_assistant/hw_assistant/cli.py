import json,typer
from rich.console import Console
from rich.panel import Panel
from .assistant import answer
from .tools import available_tools,collect_hardware
app=typer.Typer(help="Local Linux Hardware Q&A Assistant")
console=Console()
@app.command()
def status(): console.print_json(json.dumps(available_tools()))
@app.command()
def inspect(): console.print_json(json.dumps(collect_hardware(),indent=2))
@app.command()
def ask(question:str=typer.Argument(...)):
    result,facts=answer(question)
    console.print(Panel(result,title="Hardware Assistant"))
    console.print("[dim]Tools used: "+", ".join(facts)+"[/dim]")
if __name__=="__main__": app()
