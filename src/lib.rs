use pyo3::prelude::*;

mod util;
mod hmmer;

#[pymodule]
fn magna(_py: Python<'_>, m: &PyModule) -> PyResult<()> {

    // Add submodules
    util::accession::pymodule(_py, m)?;
    hmmer::tophit::pymodule(_py, m)?;

    Ok(())
}
