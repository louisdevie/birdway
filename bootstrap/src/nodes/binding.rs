use crate::nodes::{Item, Node, Value};
use crate::parser::{self, TokenStream, TokenType};

#[derive(Debug)]
pub struct BoundValue {
    name: String,
}

impl Item for BoundValue {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        let name = parser::expect_identifier(stream, "binding", "binding")?;

        Ok(Self { name })
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::Identifier(..)) => true,
            _ => false,
        }
    }
}

impl Node for BoundValue {}

impl Value for BoundValue {}
