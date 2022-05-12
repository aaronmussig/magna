import typer

from magna.rq import rq_start_worker, rq_delete_queue, rq_enqueue_conda

app = typer.Typer()


@app.command()
def worker():
    typer.echo('Starting rq worker...')
    rq_start_worker()
    typer.echo(f'Done.')


@app.command()
def delete(queue: str):
    typer.echo(f'Deleting queue: {queue}...')
    rq_delete_queue(queue)
    typer.echo(f'Done.')


@app.command()
def conda(queue: str, env: str, cmd: str):
    typer.echo(f'Enqueueing job in {queue} ({env}): {cmd}')
    rq_enqueue_conda(queue, env, cmd)
    typer.echo(f'Done.')
