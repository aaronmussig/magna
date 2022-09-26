use pyo3::prelude::*;

pub mod util;

#[pymodule]
fn magna(_py: Python<'_>, m: &PyModule) -> PyResult<()> {

    // Add submodules
    util::accession::pymodule(_py, m)?;

    Ok(())
}
