use pyo3::prelude::*;

use crate::fasta::dna_sequence::DNA;

pub fn get_possible_kmers(k: u8) -> Vec<String> {
    // return k^4 possible kmers for this length
    // must return sorted
    let mut buffer: Vec<String> = vec!["".to_string()];
    for _ in 0..k {
        let mut new_buffer: Vec<String> = Vec::new();
        for nt in DNA {
            for res in &buffer {
                new_buffer.push(format!("{}{}", res, nt));
            }
        }
        buffer = new_buffer;
    }
    buffer.sort();
    buffer
}

#[pyfunction]
#[pyo3(name = "get_possible_kmers")]
pub fn py_get_possible_kmers(k: u8) -> PyResult<Vec<String>> {
    Ok(get_possible_kmers(k))
}

#[test]
fn test_get_possible_kmers() {
    let k = 2;
    let possible_kmers = get_possible_kmers(k);
    assert_eq!(possible_kmers, vec!["AA", "AC", "AG", "AT", "CA", "CC", "CG", "CT", "GA", "GC", "GG", "GT", "TA", "TC", "TG", "TT"]);
}
