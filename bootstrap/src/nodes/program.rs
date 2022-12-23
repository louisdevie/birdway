use crate::nodes::Item;
use crate::nodes::NamedFunction;
use crate::nodes::Parameters;
use crate::parser::recovery::Mode;
use crate::parser::{self, Recover, TokenStream, TokenType};
use crate::report::{ErrorCode, Report};

#[derive(Debug)]
pub struct Program {
    params: Option<Parameters>,
    functions: Vec<NamedFunction>,
}

impl Program {
    pub fn new() -> Self {
        Self {
            params: None,
            functions: Vec::new(),
        }
    }

    pub fn parse(&mut self, stream: &mut TokenStream) -> parser::Result<()> {
        let mut last_invalid = false;

        while let Some(token) = stream.next() {
            last_invalid = match token.type_ {
                TokenType::KeywordParams => {
                    let params = Parameters::parse(stream)
                        .recover(stream, Mode::SkipUntil(TokenType::BlankLineBreak))?;

                    match self.params {
                        None => {
                            self.params = params;
                        }
                        Some(_) => {
                            return Err(stream.report_error(
                                String::from(""),
                                ErrorCode::E250ParametersRedeclaration,
                                Some(token.location),
                            ))
                        }
                    }
                    false
                }

                TokenType::KeywordFunc => {
                    if let Some(func) = NamedFunction::parse(stream)
                        .recover(stream, Mode::SkipUntil(TokenType::BlankLineBreak))?
                    {
                        self.functions.push(func);
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
}
