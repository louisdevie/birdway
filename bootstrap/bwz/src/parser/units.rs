use crate::report::{ErrorCode, Report, ReportResult};
use std::collections::hash_map::DefaultHasher;
use std::collections::HashMap;
use std::fs;
use std::hash::{Hash, Hasher};

pub struct Units {
    units: HashMap<u64, Unit>,
}

struct Unit {
    name: String,
    source: String,
    lines: Vec<Line>,
}

#[derive(Debug)]
struct Line {
    char_start: usize,
    byte_start: usize,
    byte_end: Option<usize>,
}

fn lines(text: &str) -> Vec<Line> {
    let mut lines = vec![Line {
        char_start: 0,
        byte_start: 0,
        byte_end: None,
    }];

    for (pos, (byte, chr)) in text.char_indices().enumerate() {
        if chr == '\n' {
            lines.last_mut().unwrap().byte_end = Some(byte);
            lines.push(Line {
                char_start: pos + 1,
                byte_start: byte + 1,
                byte_end: None,
            });
        }
    }

    lines
}

impl Units {
    pub fn new() -> Self {
        Self {
            units: HashMap::new(),
        }
    }

    pub fn load(&mut self, file: &str) -> ReportResult<u64> {
        let report = Report::new();

        let mut hasher = DefaultHasher::new();
        file.hash(&mut hasher);
        let id = hasher.finish();

        if !self.units.contains_key(&id) {
            let source = match fs::read_to_string(&file) {
                Ok(content) => content,
                Err(error) => return report.fatal_error(error.to_string(), ErrorCode::None, None),
            };

            let lines = lines(&source);

            self.units.insert(
                id,
                Unit {
                    name: file.to_owned(),
                    source,
                    lines,
                },
            );
        }

        report.wrap(id)
    }

    pub fn file_content(&self, unit: u64) -> Option<&str> {
        self.units.get(&unit).map(|unit| &unit.source as &str)
    }

    pub fn file_name(&self, unit: u64) -> Option<&str> {
        self.units.get(&unit).map(|unit| &unit.name as &str)
    }

    pub fn line_position(&self, unit: u64, chr: usize) -> Option<(usize, usize)> {
        let unit = self.units.get(&unit)?;

        for (i, line) in unit.lines.iter().enumerate().rev() {
            if line.char_start <= chr {
                return Some((i, chr - line.char_start));
            }
        }

        None
    }

    pub fn line_content<'a>(&'a self, unit: u64, line: usize) -> Option<&'a str> {
        let unit = self.units.get(&unit)?;
        let line = unit.lines.get(line)?;

        match line.byte_end {
            Some(end) => unit.source.get(line.byte_start..end),
            None => unit.source.get(line.byte_start..),
        }
    }
}
