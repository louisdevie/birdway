use crate::report::Report;
use crate::target::OutputInfo;
use std::path::Path;

#[cfg(feature = "c_backend")]
pub mod c;

pub trait Generator {
    fn new(report: Report, output_dir: &Path, entry_point: &Path) -> Result<Self, Report>
    where
        Self: Sized;

    fn finish(self) -> (Report, OutputInfo);
}
