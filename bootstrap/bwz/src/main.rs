use std::env;

mod checks;
mod language;
mod nodes;
mod parser;
mod report;

use parser::Units;
use report::{Report, ReportResult};

const SUCESS: i32 = 0;
const FAIL: i32 = 1;
const ERR_USAGE: i32 = 64;

fn main() {
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

    println!("{:#?}", ast);

    report.wrap(())
}
