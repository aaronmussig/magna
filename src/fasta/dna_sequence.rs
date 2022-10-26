use std::hash::{Hash, Hasher};

use pyo3::prelude::*;

pub static DNA: [char; 4] = ['A', 'C', 'G', 'T'];


#[pyclass]
pub struct DnaSequence {
    pub seq: String,
}

#[pymethods]
impl DnaSequence {
    #[new]
    pub fn new(seq: &str) -> Self {
        Self {
            seq: seq.to_string()
        }
    }

    #[getter]
    fn seq(&self) -> PyResult<&str> {
        Ok(&self.seq)
    }

     #[pyo3(name = "rev_complement")]
    fn py_rev_complement(&self) -> PyResult<DnaSequence> {
        Ok(self.rev_complement())
    }

}

impl DnaSequence {
      pub fn rev_complement(&self) -> DnaSequence {
        let mut out = String::new();
        for c in self.seq.chars().rev() {
            match c {
                'A' => out.push('T'),
                'T' => out.push('A'),
                'G' => out.push('C'),
                'C' => out.push('G'),
                _ => out.push('N'),
            }
        }
        DnaSequence::new(&out)
    }
}

impl Hash for DnaSequence {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.seq.hash(state);
    }
}

impl PartialEq<Self> for DnaSequence {
    fn eq(&self, other: &Self) -> bool {
        self.seq == other.seq
    }
}

impl Eq for DnaSequence {}


#[test]
fn test_dna_sequence() {
    let seq = DnaSequence::new("ATCGA");
    assert_eq!(seq.seq, "ATCGA");
    assert_eq!(seq.rev_complement().seq, "TCGAT");
}

