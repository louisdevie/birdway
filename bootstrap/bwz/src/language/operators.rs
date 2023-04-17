use crate::language::Type;
use crate::parser::TokenType;
use std::fmt;

#[derive(Debug)]
pub enum BinaryOperator {
    Addition,
}

impl BinaryOperator {
    pub fn result(&self, lhs: &Type, rhs: &Type) -> Option<Type> {
        match self {
            Self::Addition => Self::addition_result(lhs, rhs),
        }
    }

    fn addition_result(lhs: &Type, rhs: &Type) -> Option<Type> {
        match (lhs, rhs) {
            (Type::Int, Type::Int) => Some(Type::Int),
            _ => None,
        }
    }
}

impl From<TokenType> for BinaryOperator {
    fn from(token: TokenType) -> BinaryOperator {
        match token {
            TokenType::Plus => Self::Addition,
            _ => unreachable!(),
        }
    }
}

impl fmt::Display for BinaryOperator {
    fn fmt(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        write!(
            formatter,
            "{}",
            match self {
                Self::Addition => "+",
            }
        )
    }
}
