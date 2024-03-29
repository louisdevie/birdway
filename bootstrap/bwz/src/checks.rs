use crate::nodes;
use crate::report::{Report, ReportResult};

pub mod name_resolution;
pub mod types;

trait Check {
    fn run(ast: &mut nodes::Program) -> Report;
}

pub fn run_all(ast: &mut nodes::Program) -> ReportResult<()> {
    let mut report = Report::new();

    report.collect(name_resolution::NameResolution::run(ast))?;
    report.collect(types::TypeChecking::run(ast))?;

    report.wrap(())
}
