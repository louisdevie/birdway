use super::ErrorCode;
use super::Location;
use crate::parser::Units;
use std::fmt;

#[derive(Copy, Clone, PartialEq)]
pub enum ErrorKind {
    Warning,
    Recoverable,
    Fatal,
}

#[derive(Clone)]
pub struct Error {
    kind: ErrorKind,
    code: ErrorCode,
    message: String,
    location: Option<Location>,
}

impl Error {
    pub fn warning(message: String, code: ErrorCode, location: Option<Location>) -> Self {
        Self {
            kind: ErrorKind::Warning,
            message,
            code,
            location,
        }
    }
    pub fn recoverable(message: String, code: ErrorCode, location: Option<Location>) -> Self {
        Self {
            kind: ErrorKind::Recoverable,
            message,
            code,
            location,
        }
    }
    pub fn fatal(message: String, code: ErrorCode, location: Option<Location>) -> Self {
        Self {
            kind: ErrorKind::Fatal,
            message,
            code,
            location,
        }
    }

    pub fn kind(&self) -> ErrorKind {
        self.kind
    }

    pub fn _set_location(&mut self, location: Location) {
        self.location = Some(location);
    }
}

impl super::Display for Error {
    fn fmt(&self, units: &Units, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self.kind {
            ErrorKind::Warning => write!(formatter, "\x1b[1;33m")?,
            ErrorKind::Recoverable | ErrorKind::Fatal => write!(formatter, "\x1b[1;31m")?,
        }

        if self.code == ErrorCode::None {
            write!(
                formatter,
                "{}",
                match self.kind {
                    ErrorKind::Warning => "Warning",
                    ErrorKind::Recoverable | ErrorKind::Fatal => "Error",
                }
            )?;
        } else {
            write!(formatter, "{}", self.code)?;
        }

        write!(formatter, "\x1b[39m")?;
        write!(formatter, ": {}", self.message)?;
        writeln!(formatter, "\x1b[0m")?;

        match &self.location {
            Some(loc) => {
                loc.display(units, formatter)?;
                writeln!(formatter)?;
            }
            None => {}
        }

        Ok(())
    }
}
