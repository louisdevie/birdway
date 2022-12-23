use crate::nodes::{Item, Type};
use crate::parser::{self, Filter, TokenStream, TokenType};
use crate::report::ErrorCode;

#[derive(Debug)]
pub struct Parameters {
    params: Vec<Parameter>,
}

impl Item for Parameters {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        stream.push_filter(Filter::LineBreaks);
        let params = parser::parse_static_csl(stream, None)?;
        stream.pop_filter();

        Ok(Self { params })
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        return Parameter::may_parse(stream);
    }
}

#[derive(Debug)]
pub struct Parameter {
    name: String,
    type_: Box<dyn Type>,
}

impl Item for Parameter {
    fn parse(stream: &mut TokenStream) -> Result<Self, ()> {
        let name = match stream.next() {
            Some(token) => match token.type_ {
                TokenType::Identifier(name) => name,
                invalid => {
                    return Err(stream.report_error(
                        format!("Expected command-line parameter name, found {}", invalid),
                        ErrorCode::E100InvalidSyntax,
                        Some(token.location),
                    ))
                }
            },
            None => {
                return Err(stream.report_error(
                    format!("while parsing command-line parameter"),
                    ErrorCode::E120UnexpectedEof,
                    None,
                ))
            }
        };

        match stream.next() {
            Some(token) => match token.type_ {
                TokenType::Colon => {}
                invalid => {
                    return Err(stream.report_error(
                        format!("Expected ':', found {}", invalid),
                        ErrorCode::E100InvalidSyntax,
                        Some(token.location),
                    ))
                }
            },
            None => {
                return Err(stream.report_error(
                    format!("while parsing command-line parameter"),
                    ErrorCode::E120UnexpectedEof,
                    None,
                ))
            }
        }

        let type_ = parser::parse_type(stream)?;

        Ok(Self { name, type_ })
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::Identifier(..)) => true,
            Some(_) => false,
            None => false,
        }
    }
}
