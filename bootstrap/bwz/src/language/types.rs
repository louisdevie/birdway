use std::fmt;

#[derive(Clone, PartialEq)]
pub enum Type {
    Void,
    Int,
    Function,
}

impl Type {}

impl fmt::Debug for Type {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(self, formatter)
    }
}

impl fmt::Display for Type {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Void => write!(formatter, "Void"),
            Self::Int => write!(formatter, "Int"),
            Self::Function => write!(formatter, "() -> Void"),
        }
    }
}
