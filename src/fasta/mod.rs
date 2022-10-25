pub mod dna_sequence;

use pyo3::prelude::PyModule;
use pyo3::{py_run, PyResult, Python};
use crate::fasta::dna_sequence::DnaSequence;

pub(crate) fn pymodule(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // Register the name of this submodule
    let submodule = PyModule::new(_py, "magna.fasta")?;

    // Add bindings
    submodule.add_class::<DnaSequence>()?;

    // Register this module to allow for "from a.b import c" imports
    py_run!(_py, submodule, "import sys; sys.modules['magna.fasta'] = submodule");
    m.add_submodule(submodule)?;

    // Done
    Ok(())
}

