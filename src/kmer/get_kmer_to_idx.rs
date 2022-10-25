use std::collections::HashMap;
use pyo3::{pyfunction, PyResult};
use crate::kmer::get_possible_kmers::get_possible_kmers;

/// Return the index of a specific k-mer (sorted)
pub fn get_kmer_to_idx(k: u8) -> HashMap<String, usize> {
    let mut out = HashMap::new();
    for (i, kmer) in get_possible_kmers(k).iter().enumerate() {
        out.insert(kmer.to_string(), i);
    }
    out
}

#[pyfunction]
#[pyo3(name = "get_kmer_to_idx")]
pub fn py_get_kmer_to_idx(k: u8) -> PyResult<HashMap<String, usize>> {
    Ok(get_kmer_to_idx(k))
}

#[test]
fn test_get_kmer_to_idx() {
    let k = 2;
    let kmer_to_idx = get_kmer_to_idx(k);
    assert_eq!(kmer_to_idx.len(), 16);
    assert_eq!(kmer_to_idx.get("AA").unwrap(), &0);
    assert_eq!(kmer_to_idx.get("AC").unwrap(), &1);
    assert_eq!(kmer_to_idx.get("AG").unwrap(), &2);
    assert_eq!(kmer_to_idx.get("AT").unwrap(), &3);
    assert_eq!(kmer_to_idx.get("CA").unwrap(), &4);
    assert_eq!(kmer_to_idx.get("CC").unwrap(), &5);
    assert_eq!(kmer_to_idx.get("CG").unwrap(), &6);
    assert_eq!(kmer_to_idx.get("CT").unwrap(), &7);
    assert_eq!(kmer_to_idx.get("GA").unwrap(), &8);
    assert_eq!(kmer_to_idx.get("GC").unwrap(), &9);
    assert_eq!(kmer_to_idx.get("GG").unwrap(), &10);
    assert_eq!(kmer_to_idx.get("GT").unwrap(), &11);
    assert_eq!(kmer_to_idx.get("TA").unwrap(), &12);
    assert_eq!(kmer_to_idx.get("TC").unwrap(), &13);
    assert_eq!(kmer_to_idx.get("TG").unwrap(), &14);
    assert_eq!(kmer_to_idx.get("TT").unwrap(), &15);
}