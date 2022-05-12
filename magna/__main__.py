import typer

from magna.cli.ncbi import app as ncbi_app
from magna.cli.rq import app as rq_app

app = typer.Typer()

app.add_typer(ncbi_app, name='ncbi')
app.add_typer(rq_app, name='rq')

# Purely for documentation
typer_click_object = typer.main.get_command(app)

if __name__ == "__main__":
    app()
