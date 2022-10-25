use std::cmp::Ordering;
use std::collections::HashMap;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, Write};
use std::path::Path;

use itertools::Itertools;
use pyo3::class::basic::CompareOp;
use pyo3::prelude::*;
use pyo3::py_run;

#[derive(Clone)]
#[pyclass]
struct Hit {
    gene_id: String,
    hmm_id: String,
    e_val: f64,
    bit_score: f64,
}

#[pymethods]
impl Hit {
    #[new]
    fn new(gene_id: &str, hmm_id: &str, e_val: f64, bit_score: f64) -> Self {
        Self {
            gene_id: gene_id.to_string(),
            hmm_id: hmm_id.to_string(),
            e_val,
            bit_score,
        }
    }

    #[getter]
    fn gene_id(&self) -> PyResult<&str> {
        Ok(&self.gene_id)
    }

    #[getter]
    fn hmm_id(&self) -> PyResult<&str> {
        Ok(&self.hmm_id)
    }

    #[getter]
    fn e_val(&self) -> PyResult<f64> {
        Ok(self.e_val)
    }

    #[getter]
    fn bit_score(&self) -> PyResult<f64> {
        Ok(self.bit_score)
    }

    fn __repr__(&self) -> String {
        format!("{} {} ({}/{})", self.gene_id, self.hmm_id, self.e_val, self.bit_score)
    }

    fn __richcmp__(&self, other: &Self, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Lt => Ok(self < other),
            CompareOp::Le => Ok(self <= other),
            CompareOp::Eq => Ok(self == other),
            CompareOp::Ne => Ok(self != other),
            CompareOp::Gt => Ok(self > other),
            CompareOp::Ge => Ok(self >= other),
        }
    }

    fn hmm_str(&self) -> String {
        format!("{},{},{}", self.hmm_id, self.e_val, self.bit_score)
    }
}

impl Hash for Hit {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.gene_id.hash(state);
        self.hmm_id.hash(state);
    }
}

impl PartialEq<Self> for Hit {
    fn eq(&self, other: &Self) -> bool {
        self.gene_id == other.gene_id
            && self.hmm_id == other.hmm_id
            && self.e_val == other.e_val
            && self.bit_score == other.bit_score
    }
}

impl Eq for Hit {}

impl PartialOrd for Hit {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Hit {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.bit_score < other.bit_score {
            Ordering::Less
        } else if self.bit_score == other.bit_score {
            if self.e_val > other.e_val {
                Ordering::Less
            } else if self.e_val == other.e_val {
                Ordering::Equal
            } else {
                Ordering::Greater
            }
        } else {
            Ordering::Greater
        }
    }
}

#[pyclass]
struct TopHitFile {
    path: String,
    hits: HashMap<String, HashMap<String, Hit>>,
}

#[pymethods]
impl TopHitFile {
    #[new]
    fn new(path: String) -> Self {
        Self {
            path,
            hits: HashMap::new(),
        }
    }

    #[getter]
    fn path(&self) -> PyResult<&str> {
        Ok(&self.path)
    }

    // #[getter]
    // fn hits(&self) -> PyResult<PyDict> {
    //     let gil = Python::acquire_gil();
    //     let py = gil.python();
    //     let hits = self
    //         .hits
    //         .iter()
    //         .map(|(gene_id, hits)| {
    //             (
    //                 gene_id,
    //                 hits.values()
    //                     .map(|hit| hit.hmm_str())
    //                     .collect::<Vec<String>>()
    //                     .join(";"),
    //             )
    //         })
    //         .collect::<HashMap<&String, String>>();
    //     Ok(hits.into_py_dict(py))
    // }

    fn add_hit(&mut self, gene_id: &str, hmm_id: &str, e_val: f64, bit_score: f64) {
        let new_hit = Hit::new(gene_id, hmm_id, e_val, bit_score);
        match self.hits.get(gene_id) {
            Some(hits) => {
                match hits.get(hmm_id) {
                    Some(hit) => {
                        if hit < &new_hit {
                            self.hits.get_mut(gene_id).unwrap().insert(hmm_id.to_string(), new_hit);
                        }
                    }
                    None => {
                        self.hits.get_mut(gene_id).unwrap().insert(hmm_id.to_string(), new_hit);
                    }
                }
            }
            None => {
                let mut hits = HashMap::new();
                hits.insert(hmm_id.to_string(), new_hit);
                self.hits.insert(gene_id.to_string(), hits);
            }
        }
    }

    fn contains_gene_id(&self, gene_id: &str) -> bool {
        self.hits.contains_key(gene_id)
    }

    fn contains_gene_hmm(&self, gene_id: &str, hmm_id: &str) -> bool {
        match self.hits.get(gene_id) {
            Some(hits) => hits.contains_key(hmm_id),
            None => false,
        }
    }

    #[pyo3(name = "get_top_hit")]
    fn py_get_top_hit(&self, gene_id: &str) -> PyResult<Option<Hit>> {
        let top_hit = self.get_top_hit(gene_id);
        match top_hit {
            Some(hit) => Ok(Some(hit.clone())),
            None => Ok(None),
        }
    }

    #[pyo3(name = "get_hmm_hit")]
    fn py_get_hmm_hit(&self, gene_id: &str, hmm_id: &str) -> PyResult<Option<Hit>> {
        let hit = self.get_hmm_hit(gene_id, hmm_id);
        match hit {
            Some(hit) => Ok(Some(hit.clone())),
            None => Ok(None),
        }
    }

    fn write(&self) {
        let path = Path::new(&self.path);
        let parent_dir = path.parent().unwrap();
        std::fs::create_dir_all(parent_dir).expect("Cannot create directory!");

        let mut file = File::create(path).expect("Cannot create file!");

        writeln!(file, "Gene Id\tTop hits (Family id,e-value,bitscore)").expect("Cannot write to file!");

        // Iterate over all hits
        for (gene_id, hits) in &self.hits {
            // concatenate all hits
            let mut hits_vec: Vec<String> = vec![];
            for hit in hits.values().sorted().rev() {
                hits_vec.push(hit.hmm_str());
            }
            // write the hits
            writeln!(file, "{}\t{}", gene_id, hits_vec.join(";"))
                .expect("TODO: panic message");
        }
    }

    fn read(&mut self) {
        let path = Path::new(&self.path);

        let file = File::open(path).expect("Cannot read file!");

        let mut first_line_skipped = false;
        for res_line in BufReader::new(file).lines() {
            if let Ok(line) = res_line {
                if !first_line_skipped {
                    first_line_skipped = true;
                    continue;
                }
                let mut line_iter = line.split('\t');
                let gene_id = line_iter.next().unwrap();
                let hits_str = line_iter.next().unwrap();
                for hit_str in hits_str.split(';') {
                    let mut hit_iter = hit_str.split(',');
                    let hmm_id = hit_iter.next().unwrap();
                    let e_val = hit_iter.next().unwrap().parse::<f64>().unwrap();
                    let bit_score = hit_iter.next().unwrap().parse::<f64>().unwrap();
                    self.add_hit(gene_id, hmm_id, e_val, bit_score);
                }
            }
        }
    }
}

impl TopHitFile {
    fn get_top_hit(&self, gene_id: &str) -> Option<&Hit> {
        match self.hits.get(gene_id) {
            Some(hits) => {
                hits.values().max_by(|a, b| a.cmp(b))
            }
            None => None,
        }
    }

    fn get_hmm_hit(&self, gene_id: &str, hmm_id: &str) -> Option<&Hit> {
        match self.hits.get(gene_id) {
            Some(hits) => {
                hits.get(hmm_id)
            }
            None => None,
        }
    }
}

pub(crate) fn pymodule(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // Register the name of this submodule
    let submodule = PyModule::new(_py, "magna.hmmer.tophit")?;

    // Add bindings
    submodule.add_class::<Hit>()?;
    submodule.add_class::<TopHitFile>()?;

    // Register this module to allow for "from a.b import c" imports
    py_run!(_py, submodule, "import sys; sys.modules['magna.hmmer.tophit'] = submodule");
    m.add_submodule(submodule)?;

    // Done
    Ok(())
}
