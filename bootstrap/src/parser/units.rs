use crate::report::{ErrorCode, Report, ReportResult};
use std::collections::HashMap;
use std::fs;

pub struct Units {
    units: HashMap<String, Unit>,
}

struct Unit {
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

    pub fn load(&mut self, file: &str) -> ReportResult<&str> {
        let report = Report::new();

        let source = match fs::read_to_string(&file) {
            Ok(source) => source,
            Err(error) => return report.fatal(error.to_string(), ErrorCode::None, None),
        };
        let lines = lines(&source);

        let unit = self
            .units
            .entry(String::from(file))
            .or_insert(Unit { source, lines });

        report.wrap(&unit.source)
    }

    pub fn line_position(&self, unit: &str, chr: usize) -> Option<(usize, usize)> {
        let unit = self.units.get(unit)?;

        for (i, line) in unit.lines.iter().enumerate().rev() {
            if line.char_start <= chr {
                return Some((i, chr - line.char_start));
            }
        }

        None
    }

    pub fn line_content<'a>(&'a self, unit: &str, line: usize) -> Option<&'a str> {
        let unit = self.units.get(unit)?;
        let line = unit.lines.get(line)?;

        match line.byte_end {
            Some(end) => unit.source.get(line.byte_start..end),
            None => unit.source.get(line.byte_start..),
        }
    }
}
