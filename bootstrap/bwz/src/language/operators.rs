use crate::language::Type;
use crate::parser::TokenType;

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
