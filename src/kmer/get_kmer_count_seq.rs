use std::collections::HashMap;

use pyo3::{pyfunction, PyResult};

use crate::fasta::dna_sequence::DnaSequence;
use crate::kmer::get_kmer_to_idx::get_kmer_to_idx;
use crate::kmer::kmer_count_result::KmerCountResult;

fn get_kmer_count_seq_single(seq: &str, k: u8, k_to_idx: &HashMap<String, usize>) -> KmerCountResult {
    let mut counts = vec![0_u64; k_to_idx.len()];
    let mut n_kmers = 0_u64;

    let seq_len = seq.len();
    for i in 0..seq_len {
        let k_from = i;
        let k_to = i + (k as usize);
        if k_to > seq_len {
            break;
        } else {
            let kmer = &seq[k_from..k_to];
            let kmer_idx = k_to_idx.get(kmer).unwrap();
            counts[*kmer_idx] += 1;
            n_kmers += 1;
        }
    }
    KmerCountResult::new(k, n_kmers, counts)
}

pub fn get_kmer_count_seq(seq: &str, k: u8, use_rev_complement: bool) -> KmerCountResult {
    let k_to_idx = get_kmer_to_idx(k);
    let fwd_counts = get_kmer_count_seq_single(seq, k, &k_to_idx);

    // Single direction
    if !use_rev_complement {
        return fwd_counts;
    }

    // Include reverse complement
    let seq = DnaSequence::new(seq);
    let rev_counts = get_kmer_count_seq_single(&seq.rev_complement().seq, k, &k_to_idx);

    // Add the values together
    &fwd_counts + &rev_counts
}


#[pyfunction]
#[pyo3(name = "get_kmer_count_seq")]
pub fn py_get_kmer_count_seq(seq: &str, k: u8, use_rev_complement: bool) -> PyResult<KmerCountResult> {
    Ok(get_kmer_count_seq(seq, k, use_rev_complement))
}

#[test]
fn test_kmer_count_seq() {
    let seq = "ATCGA";
    let k = 2;
    let kmer_count_result = get_kmer_count_seq(seq, k, false);
    assert_eq!(kmer_count_result.k, k);
    assert_eq!(kmer_count_result.total, 4);
    assert_eq!(kmer_count_result.counts, vec![0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]);
    println!("{:?}", kmer_count_result.counts);
}

#[test]
fn test_kmer_count_seq_rev() {
    let seq = "ATCGA";
    let k = 2;
    let kmer_count_result = get_kmer_count_seq(seq, k, true);
    assert_eq!(kmer_count_result.k, k);
    assert_eq!(kmer_count_result.total, 8);
    assert_eq!(kmer_count_result.counts, vec![0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 0]);
    println!("{:?}", kmer_count_result.counts);
}
