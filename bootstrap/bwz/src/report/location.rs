use crate::parser::Units;
use std::fmt;
use std::ops::{Add, AddAssign, BitAnd, BitAndAssign};

#[derive(Clone, Copy)]
pub struct Location {
    file_id: u64,
    position: usize,
    span: usize,
}

impl Location {
    pub fn at(file_id: u64, position: usize) -> Self {
        Self {
            file_id,
            position,
            span: 1,
        }
    }

    pub fn from(file_id: u64, start: usize, span: usize) -> Self {
        Self {
            file_id,
            position: start,
            span,
        }
    }

    pub fn from_location(location: Location, span: usize) -> Self {
        Self {
            file_id: location.file_id,
            position: location.position,
            span,
        }
    }

    pub fn between(file_id: u64, start: usize, end: usize) -> Self {
        Self {
            file_id,
            position: start,
            span: end.checked_sub(start).unwrap_or(0),
        }
    }

    pub fn between_locations(start: Location, end: Location) -> Self {
        Self {
            file_id: start.file_id,
            position: start.position,
            span: (end.position + end.span)
                .checked_sub(start.position)
                .unwrap_or(0),
        }
    }

    pub fn extend_to(mut self, end: usize) -> Self {
        self.span = end.checked_sub(self.position).unwrap_or(0);
        self
    }

    pub fn extend_to_location(mut self, end: Location) -> Self {
        self.span = (end.position + end.span)
            .checked_sub(self.position)
            .unwrap_or(0);
        self
    }

    pub fn extend_by(mut self, span: usize) -> Self {
        self.span += span;
        self
    }

    pub fn display(&self, units: &Units, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let (line, col) = units
            .line_position(self.file_id, self.position)
            .expect("couldn't retrieve line position");

        let content = units
            .line_content(self.file_id, line)
            .expect("couldn't retrieve line contents");

        let file = units
            .file_name(self.file_id)
            .expect("couldn't retrieve file_name");

        writeln!(formatter, "-> {}", file)?;
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

    pub fn file_id(&self) -> u64 {
        self.file_id
    }
}

impl fmt::Debug for Location {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "...")
    }
}

impl BitAnd for Location {
    type Output = Location;

    fn bitand(mut self, rhs: Location) -> Location {
        self.span = (rhs.position + rhs.span)
            .checked_sub(self.position)
            .unwrap_or(0);
        self
    }
}

impl BitAndAssign for Location {
    fn bitand_assign(&mut self, rhs: Location) {
        self.span = (rhs.position + rhs.span)
            .checked_sub(self.position)
            .unwrap_or(0);
    }
}

impl BitAnd<usize> for Location {
    type Output = Location;
    fn bitand(mut self, rhs: usize) -> Location {
        self.span = rhs.checked_sub(self.position).unwrap_or(0);
        self
    }
}

impl BitAndAssign<usize> for Location {
    fn bitand_assign(&mut self, rhs: usize) {
        self.span = rhs.checked_sub(self.position).unwrap_or(0);
    }
}

impl Add<usize> for Location {
    type Output = Location;
    fn add(mut self, rhs: usize) -> Location {
        self.span += rhs;
        self
    }
}

impl AddAssign<usize> for Location {
    fn add_assign(&mut self, rhs: usize) {
        self.span += rhs;
    }
}
