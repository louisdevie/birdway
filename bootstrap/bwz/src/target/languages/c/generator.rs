use super::writer::Writer;
use crate::nodes;
use crate::nodes::visit::{Visit, Visitor};
use crate::report::{ErrorCode, Report};
use crate::target::languages;
use crate::target::OutputInfo;
use std::fs::File;
use std::path::Path;

pub struct Generator {
    report: Report,
    info: OutputInfo,
    output: Writer<File>,
}

impl languages::Generator for Generator {
    fn new(report: Report, output_dir: &Path, entry_point: &Path) -> Result<Generator, Report> {
        let mut output_name = output_dir.join(
            entry_point
                .file_name()
                .expect("the input file turned out to be a directory"),
        );
        output_name.set_extension("bw.c");

        let output_file = match File::create(output_name) {
            Ok(file) => file,
            Err(error) => {
                return Err(report
                    .fatal_error::<()>(
                        format!("Cannot open output file: {}", error),
                        ErrorCode::None,
                        None,
                    )
                    .unwrap_err())
            }
        };

        Ok(Self {
            report,
            info: OutputInfo {},
            output: Writer::new(output_file),
        })
    }

    fn finish(self) -> (Report, OutputInfo) {
        self.output.close();
        (self.report, self.info)
    }
}

impl Visitor for Generator {}

impl Visit<nodes::Program> for Generator {
    fn visit(&mut self, _node: &nodes::Program) {
        todo!()
    }
}

impl Visit<nodes::TypeName> for Generator {
    fn visit(&mut self, _node: &nodes::TypeName) {
        todo!()
    }
}

impl Visit<nodes::BoundValue> for Generator {
    fn visit(&mut self, _node: &nodes::BoundValue) {
        todo!()
    }
}

impl Visit<nodes::NamedFunction> for Generator {
    fn visit(&mut self, _node: &nodes::NamedFunction) {
        todo!()
    }
}

impl Visit<nodes::Print> for Generator {
    fn visit(&mut self, _node: &nodes::Print) {
        todo!()
    }
}

impl Visit<nodes::BinaryOperation> for Generator {
    fn visit(&mut self, _node: &nodes::BinaryOperation) {
        todo!()
    }
}
