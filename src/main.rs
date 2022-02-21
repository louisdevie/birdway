use std::io::Read;
use std::io::Write;

mod generator;
mod help;
mod lexer;
mod parser;

fn main() {
    let mut files = Vec::new();
    let mut count = 0;

    for (i, arg) in std::env::args().enumerate() {
        if i != 0 {
            if arg == "--help" {
                help::display_help_message();
                return;
            } else {
                files.push((i, arg));
                count += 1;
            }
        }
    }

    for (i, file) in files {
        compile(&file, i, count);
    }
}

fn compile(file_path: &str, position: usize, count: usize) {
    println!("Compiling {} ({}/{}) ...", file_path, position, count);

    match std::fs::OpenOptions::new().read(true).open(file_path) {
        Err(why) => println!("  Unable to open script : {}", why),

        Ok(mut file) => {
            let mut script = String::new();

            match file.read_to_string(&mut script) {
                Err(why) => println!("  Unable to read script : {}", why),

                Ok(_) => {
                    let result = generator::generate(parser::parse(lexer::parse(&script)));

                    match std::fs::OpenOptions::new()
                        .write(true)
                        .create(true)
                        .open(std::path::Path::new(file_path).with_extension("bwtmp.c"))
                    {
                        Err(why) => println!("  Unable to create output file : {}", why),

                        Ok(mut file) => write!(file, "{}", result).unwrap(),
                    }
                }
            }
        }
    };
}
