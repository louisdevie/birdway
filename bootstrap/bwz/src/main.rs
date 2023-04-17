use std::env;
use std::process;

mod checks;
mod language;
mod nodes;
mod parser;
mod report;
mod target;

use parser::Units;
use report::{ErrorCode, Report, ReportResult};

const SUCESS: i32 = 0;
const FAIL: i32 = 1;
const ERR_USAGE: i32 = 64;

fn main() {
    println!(
        "BWZ v0.1.1 ({}, {})",
        target::language::INFO,
        target::platform::INFO
    );

    let args: Vec<String> = env::args().collect();

    let code = if args.len() == 1 {
        println!("No input file given");
        ERR_USAGE
    } else if args.len() == 2 {
        println!("Compiling {}...", args[1]);

        let mut units = Units::new();
        let report = Report::from_result(compile(&args[1], &mut units));
        let error_count = report.error_count();

        println!("{}", report.bind(&units));

        match error_count {
            0 => {
                println!("Done !");
                SUCESS
            }
            one_or_more => {
                println!("Could not compile due to {} error(s)", one_or_more);
                FAIL
            }
        }
    } else {
        println!("Too many arguments");
        ERR_USAGE
    };

    std::process::exit(code);
}

fn compile(source: &str, units: &mut Units) -> ReportResult<()> {
    let mut report = Report::new();

    let p = parser::Parser::new(source, units);

    let mut ast = report.unwrap_strict(p.parse())?;

    report.unwrap_strict(checks::run_all(&mut ast))?;

    // println!("{:#?}", ast);

    report.unwrap_strict(target::output(&ast, source))?;

    report.wrap(())
}

pub fn execute(mut cmd: process::Command) -> ReportResult<()> {
    let report = Report::new();

    match cmd.status() {
        Ok(status) => {
            if status.success() {
                report.fatal_error(
                    format!(
                        "{} exited with status {}",
                        cmd.get_program().to_string_lossy(),
                        status
                    ),
                    ErrorCode::None,
                    None,
                )
            } else {
                report.wrap(())
            }
        }
        Err(io_error) => report.fatal_error(io_error.to_string(), ErrorCode::None, None),
    }
}
