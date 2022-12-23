use crate::nodes::{Item, Node, Value};
use crate::parser::{self, Filter, TokenStream, TokenType};

#[derive(Debug)]
pub struct NamedFunction {
    name: String,
    params: Vec<Parameter>,
    body: Box<dyn Value>,
}

#[derive(Debug)]
pub struct Parameter {}

impl Item for NamedFunction {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self> {
        let name = parser::expect_identifier(stream, "function name", "function")?;

        parser::expect(stream, TokenType::OpeningParens, "function")?;

        stream.push_filter(Filter::AllLineBreaks);
        let params = parser::parse_static_csl(stream, Some(TokenType::ClosingParens))?;
        stream.pop_filter();

        parser::expect(stream, TokenType::Arrow, "function")?;

        let body = parser::parse_expression(stream)?;

        Ok(Self { name, params, body })
    }

    fn may_parse(stream: &mut TokenStream) -> bool {
        match stream.peek(0) {
            Some(TokenType::Identifier(..)) => true,
            _ => false,
        }
    }
}

impl Item for Parameter {
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

impl Node for NamedFunction {}

impl Value for NamedFunction {}
