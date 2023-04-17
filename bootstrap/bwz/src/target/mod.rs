use crate::nodes::visit::Visit;
use crate::nodes::Program;
use crate::report::{ErrorCode, Report, ReportResult};
use crate::target::languages::Generator;
use std::fs;
use std::path::Path;
use std::process::Command;

mod languages;
mod platforms;

#[cfg(feature = "c_backend")]
pub use languages::c as language;

#[cfg(target_os = "linux")]
pub use platforms::linux as platform;

pub struct OutputInfo {}

pub fn output(ast: &Program, entry_point: &str) -> ReportResult<Vec<Command>> {
    let report = Report::new();

    let output_dir = match Path::new(entry_point).parent() {
        Some(path) => path.join(".bw"),
        None => {
            return report.fatal_error(
                format!("{} doesn't have a parent directory", entry_point),
                ErrorCode::None,
                None,
            )
        }
    };

    if let Err(error) = fs::create_dir_all(&output_dir) {
        return report.fatal_error(
            format!("Cannot create output directory: {}", error),
            ErrorCode::None,
            None,
        );
    }

    let mut visitor = match language::Generator::new(report, &output_dir, &Path::new(entry_point)) {
        Ok(generator) => generator,
        Err(report) => return Err(report),
    };
    visitor.visit(ast);

    let (report, output_info) = visitor.finish();

    report.wrap(platform::build_process(output_info))
}
