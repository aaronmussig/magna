use pyo3::{py_run, PyResult, Python, wrap_pyfunction};
use pyo3::prelude::PyModule;

use crate::kmer::get_kmer_count_fasta::py_get_kmer_count_fasta;
use crate::kmer::get_kmer_count_seq::py_get_kmer_count_seq;
use crate::kmer::get_kmer_to_idx::py_get_kmer_to_idx;
use crate::kmer::get_possible_kmers::py_get_possible_kmers;
use crate::kmer::kmer_count_result::KmerCountResult;

pub mod get_possible_kmers;
pub mod kmer_count_result;
pub mod get_kmer_to_idx;
pub mod get_kmer_count_seq;
pub mod get_kmer_count_fasta;

pub(crate) fn pymodule(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // Register the name of this submodule
    let submodule = PyModule::new(_py, "magna.kmer")?;

    // Add bindings
    submodule.add_function(wrap_pyfunction!(py_get_kmer_count_fasta, submodule)?)?;
    submodule.add_function(wrap_pyfunction!(py_get_kmer_count_seq, submodule)?)?;
    submodule.add_function(wrap_pyfunction!(py_get_kmer_to_idx, submodule)?)?;
    submodule.add_function(wrap_pyfunction!(py_get_possible_kmers, submodule)?)?;
    submodule.add_class::<KmerCountResult>()?;

    // Register this module to allow for "from a.b import c" imports
    py_run!(_py, submodule, "import sys; sys.modules['magna.kmer'] = submodule");
    m.add_submodule(submodule)?;

    // Done
    Ok(())
}


