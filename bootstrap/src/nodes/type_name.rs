use crate::nodes::{Item, Node, Type};
use crate::parser::{self, TokenStream, TokenType};
use crate::report::ErrorCode;

#[derive(Debug)]
pub struct TypeName {
    name: String,
}

impl Item for TypeName {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        match stream.next() {
            Some(token) => match token.type_ {
                TokenType::Identifier(name) => Ok(Self { name }),

                invalid => Err(stream.report_error(
                    format!("{} is not a valid type name", invalid),
                    ErrorCode::E100InvalidSyntax,
                    Some(token.location),
                )),
            },

            None => Err(stream.report_error(
                String::from("while parsing type name"),
                ErrorCode::E120UnexpectedEof,
                None,
            )),
        }
    }
    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::Identifier(..)) => true,
            Some(_) => false,
            None => false,
        }
    }
}

impl Node for TypeName {}

impl Type for TypeName {}
