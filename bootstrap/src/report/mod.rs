use crate::parser::Units;
use std::fmt;

mod codes;
mod error;
mod location;

pub use codes::ErrorCode;
use error::{Error, ErrorKind};
pub use location::Location;

pub struct Report {
    errors: Vec<Error>,
}

pub type ReportResult<T> = Result<(T, Report), Report>;

impl Report {
    pub fn new() -> Self {
        Self { errors: Vec::new() }
    }

    pub fn from_result<T>(result: ReportResult<T>) -> Self {
        match result {
            Ok((_, report)) => report,
            Err(report) => report,
        }
    }

    pub fn warning(&mut self, message: String, code: ErrorCode, location: Option<Location>) {
        self.errors.push(Error::warning(message, code, location));
    }

    pub fn error(&mut self, message: String, code: ErrorCode, location: Option<Location>) {
        self.errors.push(Error::error(message, code, location));
    }

    pub fn fatal<T>(
        mut self,
        message: String,
        code: ErrorCode,
        location: Option<Location>,
    ) -> ReportResult<T> {
        self.errors.push(Error::fatal(message, code, location));
        Err(self)
    }

    pub fn wrap<T>(self, value: T) -> ReportResult<T> {
        Ok((value, self))
    }

    pub fn collect(&mut self, report: Report) -> Result<(), Report> {
        let mut found_fatal = false;
        for err in report.errors {
            match err.kind() {
                ErrorKind::Fatal => found_fatal = true,
                ErrorKind::Recoverable | ErrorKind::Warning => {}
            };
            self.errors.push(err);
        }
        if found_fatal {
            Err(Self {
                errors: self.errors.clone(),
            })
        } else {
            Ok(())
        }
    }

    pub fn collect_strict(&mut self, report: Report) -> Result<(), Report> {
        let mut found_error = false;
        for err in report.errors {
            match err.kind() {
                ErrorKind::Recoverable | ErrorKind::Fatal => found_error = true,
                ErrorKind::Warning => {}
            };
            self.errors.push(err);
        }
        if found_error {
            Err(Self {
                errors: self.errors.clone(),
            })
        } else {
            Ok(())
        }
    }

    pub fn unwrap<T>(&mut self, result: ReportResult<T>) -> Result<T, Report> {
        match result {
            Ok((value, mut report)) => {
                self.errors.append(&mut report.errors);
                Ok(value)
            }
            Err(mut report) => {
                let mut errs = self.errors.clone();
                errs.append(&mut report.errors);
                Err(Self { errors: errs })
            }
        }
    }

    pub fn unwrap_strict<T>(&mut self, result: ReportResult<T>) -> Result<T, Report> {
        match result {
            Ok((value, report)) => self.collect_strict(report).map(|_| value),
            Err(mut report) => {
                let mut errs = self.errors.clone();
                errs.append(&mut report.errors);
                Err(Self { errors: errs })
            }
        }
    }

    pub fn error_count(&self) -> u32 {
        let mut count = 0;
        for err in &self.errors {
            match err.kind() {
                ErrorKind::Recoverable | ErrorKind::Fatal => count += 1,
                ErrorKind::Warning => {}
            }
        }
        count
    }

    fn display(&self, units: &Units, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        for err in &self.errors {
            writeln!(formatter)?;
            err.display(units, formatter)?;
        }
        Ok(())
    }

    pub fn bind(self, units: &Units) -> BoundReport {
        BoundReport {
            report: self,
            units,
        }
    }
}

pub struct BoundReport<'a> {
    report: Report,
    units: &'a Units,
}

impl fmt::Display for BoundReport<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.report.display(self.units, formatter)
    }
}
