use std::collections::HashMap;

use bio::io::fasta;
use pyo3::{pyfunction, PyResult};

use crate::kmer::get_kmer_count_seq::get_kmer_count_seq;
use crate::kmer::kmer_count_result::KmerCountResult;

pub fn get_kmer_count_fasta(path: &str, k: u8, use_rev_complement: bool) -> HashMap<String, KmerCountResult> {
    let mut out: HashMap<String, KmerCountResult> = HashMap::new();

    let mut records = fasta::Reader::from_file(path).unwrap().records();
    while let Some(Ok(record)) = records.next() {
        let cur_seq = String::from_utf8(record.seq().to_vec()).unwrap();
        out.insert(record.id().to_string(), get_kmer_count_seq(&cur_seq, k, use_rev_complement));
    }
    out
}


#[pyfunction]
#[pyo3(name = "get_kmer_count_fasta")]
pub fn py_get_kmer_count_fasta(path: &str, k: u8, use_rev_complement: bool) -> PyResult<HashMap<String, KmerCountResult>> {
    Ok(get_kmer_count_fasta(path, k, use_rev_complement))
}

