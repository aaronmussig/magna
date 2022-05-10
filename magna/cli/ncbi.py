import typer

from magna.ncbi.web import download_ncbi_assembly_file_to_disk, NcbiAssemblyFileType

app = typer.Typer()


@app.command()
def download(gid: str, target: str, file: NcbiAssemblyFileType = NcbiAssemblyFileType.fna):
    download_ncbi_assembly_file_to_disk(gid, target, file)
