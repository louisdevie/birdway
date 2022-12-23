use crate::parser::Units;
use std::fmt;

#[derive(Debug, Clone)]
pub struct Location {
    file: String,
    position: usize,
    span: usize,
}

impl Location {
    pub fn at(file: String, position: usize) -> Self {
        Self {
            file: file.into(),
            position,
            span: 1,
        }
    }

    pub fn from(file: String, start: usize, span: usize) -> Self {
        Self {
            file: file.into(),
            position: start,
            span,
        }
    }

    pub fn from_location(location: Location, span: usize) -> Self {
        Self {
            file: location.file,
            position: location.position,
            span,
        }
    }

    pub fn between(file: String, start: usize, end: usize) -> Self {
        Self {
            file: file.into(),
            position: start,
            span: end.checked_sub(start).unwrap_or(0),
        }
    }

    pub fn between_locations(start: Location, end: Location) -> Self {
        Self {
            file: start.file,
            position: start.position,
            span: end.position + end.span,
        }
    }

    pub fn display(&self, units: &Units, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let (line, col) = units
            .line_position(&self.file, self.position)
            .expect("couldn't retrieve line position");

        let content = units
            .line_content(&self.file, line)
            .expect("couldn't retrieve line contents");

        writeln!(formatter, "-> {}", self.file)?;
        writeln!(formatter)?;
        writeln!(formatter, " {:<4}| {}", line + 1, content)?;
        write!(
            formatter,
            "       {}\x1b[1;36m{}\x1b[0m",
            " ".repeat(col),
            "^".repeat(self.span)
        )?;

        Ok(())
    }

    pub fn position(&self) -> usize {
        self.position
    }

    pub fn span(&self) -> usize {
        self.span
    }

    pub fn file(&self) -> &str {
        &self.file
    }
}
