use crate::nodes;
use crate::parser::recovery::{Mode, Recover};
use crate::parser::{self, Filter, TokenStream, TokenType};
use crate::report::{ErrorCode, Location};

pub fn parse_unit(program: &mut nodes::Program, stream: &mut TokenStream) -> parser::Result<()> {
    let mut last_invalid = false;

    while let Some(token) = stream.next() {
        last_invalid = match token.type_ {
            TokenType::KeywordParams => {
                let params = nodes::Parameters::parse(stream)
                    .recover(stream, Mode::SkipUntil(TokenType::BlankLineBreak))?;

                if program.has_params() {
                    return Err(stream.report_error(
                        String::from(""),
                        ErrorCode::E250ParametersRedeclaration,
                        Some(token.location),
                    ));
                } else {
                    program.set_params(params);
                }
                false
            }

            TokenType::KeywordFunc => {
                if let Some(func) = nodes::NamedFunction::parse(stream)
                    .recover(stream, Mode::SkipUntil(TokenType::BlankLineBreak))?
                {
                    program.functions.push(func);
                }
                false
            }

            TokenType::LineBreak | TokenType::BlankLineBreak => false,

            _ => {
                if !last_invalid {
                    stream.report_error(
                        format!("unexpected {} in program body", token.type_),
                        ErrorCode::E100InvalidSyntax,
                        Some(token.location),
                    );
                }
                true
            }
        }
    }

    Ok(())
}

pub trait Item {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self>
    where
        Self: Sized;

    fn may_parse(stream: &mut TokenStream) -> bool
    where
        Self: Sized;
}

impl Item for nodes::BoundValue {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        let (name, location) = parser::expect_identifier(stream, "binding", "binding")?;

        Ok(Self {
            name,
            location,
            symbol: None,
        })
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::Identifier(..)) => true,
            _ => false,
        }
    }
}

impl Item for nodes::NamedFunction {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        let (name, location) = parser::expect_identifier(stream, "function name", "function")?;

        parser::expect(stream, TokenType::OpeningParens, "function")?;

        stream.push_filter(Filter::AllLineBreaks);
        let params = parser::parse_static_csl(stream, Some(TokenType::ClosingParens))?;
        stream.pop_filter();

        parser::expect(stream, TokenType::Arrow, "function")?;

        let body = parser::parse_expression(stream)?;

        Ok(Self {
            name,
            location,
            params,
            body,
            context: None,
            symbol: None,
        })
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::Identifier(..)) => true,
            _ => false,
        }
    }
}

impl Item for nodes::FunctionParameter {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        Ok(Self {})
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::Dollar)
            | Some(TokenType::AtSymbol)
            | Some(TokenType::Identifier(..)) => true,
            _ => false,
        }
    }
}

impl Item for nodes::Print {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        let (ln, start) = match stream.next() {
            Some(token) => match token.type_ {
                TokenType::KeywordPrintln => (true, token.location),

                invalid => {
                    return Err(stream.report_error(
                        format!("{} is not a print expression", invalid),
                        ErrorCode::E100InvalidSyntax,
                        Some(token.location),
                    ))
                }
            },

            None => {
                return Err(stream.report_error(
                    String::from("where a print expression was expected"),
                    ErrorCode::E120UnexpectedEof,
                    None,
                ))
            }
        };

        let value = parser::parse_expression(stream)?;

        let location = Location::between_locations(start, value.location());

        Ok(Self {
            ln,
            value,
            location,
        })
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::KeywordPrintln) => true,
            _ => false,
        }
    }
}

impl Item for nodes::TypeName {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        match stream.next() {
            Some(token) => match token.type_ {
                TokenType::Identifier(name) => Ok(Self {
                    name,
                    location: token.location,
                }),

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

impl Item for nodes::Parameters {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        stream.push_filter(Filter::LineBreaks);
        let params = parser::parse_static_csl(stream, None)?;
        stream.pop_filter();

        Ok(params)
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        return nodes::Parameter::may_parse(stream);
    }
}

impl Item for nodes::Parameter {
    fn parse(stream: &mut TokenStream) -> Result<Self, ()> {
        let (name, location) = match stream.next() {
            Some(token) => match token.type_ {
                TokenType::Identifier(name) => (name, token.location),
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

        Ok(Self {
            name,
            location,
            type_,
            symbol: None,
        })
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::Identifier(..)) => true,
            Some(_) => false,
            None => false,
        }
    }
}
