use std::fmt;

#[derive(Debug, PartialEq, Clone)]
pub enum ErrorCode {
    None,
    E100InvalidSyntax,
    E110InvalidCharacter,
    E120UnexpectedEof,
    E211ValueNotFound,
    E212ValueAlreadyExists,
    E221TypeNotFound,
    E250ParametersRedeclaration,
    E300TypeError,
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
                Self::E211ValueNotFound => "Value not found [E211]",
                Self::E212ValueAlreadyExists => "Value already exists [E212]",
                Self::E221TypeNotFound => "Type not found [E221]",
                Self::E250ParametersRedeclaration => "Parameters are already declared [E250]",
                Self::E300TypeError => "Type error [E300]",
            }
        )?;

        Ok(())
    }
}
