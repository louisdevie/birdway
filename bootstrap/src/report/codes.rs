use std::fmt;

#[derive(PartialEq, Clone)]
pub enum ErrorCode {
    None,
    E100InvalidSyntax,
    E110InvalidCharacter,
    E120UnexpectedEof,
    E250ParametersRedeclaration,
}

impl fmt::Display for ErrorCode {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "{}",
            match self {
                Self::None => "",
                Self::E100InvalidSyntax => "Invalid syntax [E100]",
                Self::E110InvalidCharacter => "Invalid character [E110]",
                Self::E120UnexpectedEof => "Unexpected EOF [E120]",
                Self::E250ParametersRedeclaration => "Parameters are already declared [E250]",
            }
        )?;

        Ok(())
    }
}
