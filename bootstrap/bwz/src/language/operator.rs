use crate::parser::TokenType;

#[derive(Debug)]
pub enum BinaryOperator {
    Addition,
}

impl From<TokenType> for BinaryOperator {
    fn from(token: TokenType) -> BinaryOperator {
        match token {
            TokenType::Plus => Self::Addition,
            _ => unreachable!(),
        }
    }
}
