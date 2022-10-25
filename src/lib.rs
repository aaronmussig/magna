use pyo3::prelude::*;

mod util;
mod hmmer;
mod kmer;
mod fasta;

#[pymodule]
fn magna(_py: Python<'_>, m: &PyModule) -> PyResult<()> {

    // Add submodules
    util::accession::pymodule(_py, m)?;
    hmmer::tophit::pymodule(_py, m)?;
    kmer::pymodule(_py, m)?;
    fasta::pymodule(_py, m)?;

    Ok(())
}
