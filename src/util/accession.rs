use pyo3::prelude::*;
use pyo3::py_run;

pub fn canonical_gid(gid: &str) -> String {
    let mut out = gid.to_string();
    if out.starts_with('U') {
        return out;
    }
    out = out.replace("RS_", "");
    out = out.replace("GB_", "");
    out = out.replace("GCA_", "G");
    out = out.replace("GCF_", "G");
    if out.contains('.') {
        out = out.split('.').next().unwrap().to_string();
    }
    out
}

#[test]
fn test_canonical_gid() {
    assert_eq!(canonical_gid("GCF_005435135.1_ASM543513v1_genomic"), "G005435135");
    assert_eq!(canonical_gid("UBA1234"), "UBA1234");
    assert_eq!(canonical_gid("GCF_005435135.1"), "G005435135");
    assert_eq!(canonical_gid("GCA_005435135.1"), "G005435135");
    assert_eq!(canonical_gid("GB_GCA_005435135.1"), "G005435135");
    assert_eq!(canonical_gid("RS_GCF_005435135.1"), "G005435135");
}


#[pyfunction]
#[pyo3(name = "canonical_gid")]
fn py_canonical_gid(gid: &str) -> PyResult<String> {
    Ok(canonical_gid(gid))
}


pub(crate) fn pymodule(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // Register the name of this submodule
    let submodule = PyModule::new(_py, "magna.util.accession")?;

    // Add bindings
    submodule.add_function(wrap_pyfunction!(py_canonical_gid, submodule)?)?;

    // Register this module to allow for "from a.b import c" imports
    py_run!(_py, submodule, "import sys; sys.modules['magna.util.accession'] = submodule");
    m.add_submodule(submodule)?;

    // Done
    Ok(())
}
