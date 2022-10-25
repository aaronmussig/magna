use pyo3::prelude::*;
use std::ops::Add;

#[pyclass]
pub struct KmerCountResult {
    pub k: u8,
    pub total: u64,
    pub counts: Vec<u64>,
}

#[pymethods]
impl KmerCountResult {
    #[new]
    pub fn new(k: u8, total: u64, counts: Vec<u64>) -> Self {
        Self {
            k,
            total,
            counts,
        }
    }

    #[getter]
    fn k(&self) -> PyResult<u8> {
        Ok(self.k)
    }

    #[getter]
    fn total(&self) -> PyResult<u64> {
        Ok(self.total)
    }

    #[getter]
    fn counts(&self) -> PyResult<Vec<u64>> {
        Ok(self.counts.clone())
    }
}

impl<'a, 'b> Add<&'b KmerCountResult> for &'a KmerCountResult {
    type Output = KmerCountResult;

    fn add(self, other: &'b KmerCountResult) -> KmerCountResult {
        assert_eq!(self.k, other.k);
        assert_eq!(self.counts.len(), other.counts.len());
        let new_counts = self.counts
            .iter()
            .zip(other.counts.iter())
            .map(|(a, b)| a + b)
            .collect();

        KmerCountResult {
            k: self.k,
            total: self.total + other.total,
            counts: new_counts,
        }
    }
}
