use crate::nodes::{Item, Node, Value};
use crate::parser::{self, TokenStream, TokenType};
use crate::report::ErrorCode;

#[derive(Debug)]
pub struct Print {
    ln: bool,
    value: Box<dyn Value>,
}

impl Item for Print {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        let ln = match stream.next() {
            Some(token) => match token.type_ {
                TokenType::KeywordPrintln => true,

                invalid => {
                    return Err(stream.report_error(
                        format!(
                            "Unexpected {} at the beginning of a print expression",
                            invalid
                        ),
                        ErrorCode::E100InvalidSyntax,
                        Some(token.location),
                    ))
                }
            },

            None => {
                return Err(stream.report_error(
                    String::from("while parsing print expression"),
                    ErrorCode::E120UnexpectedEof,
                    None,
                ))
            }
        };

        let value = parser::parse_expression(stream)?;

        Ok(Self { ln, value })
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::KeywordPrintln) => true,
            _ => false,
        }
    }
}

impl Node for Print {}

impl Value for Print {}
