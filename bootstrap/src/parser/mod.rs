use crate::nodes::{BinaryOperation, BoundValue, Print, Program, TypeName};
use crate::nodes::{Item, Type, Value};
use crate::report::{ErrorCode, Report, ReportResult};

pub mod recovery;
mod scanner;
mod units;

pub use recovery::Recover;
pub use scanner::{Filter, TokenStream, TokenType};
pub use units::Units;

pub type Result<T> = std::result::Result<T, ()>;

pub struct Parser<'a> {
    entry_point: String,
    units: &'a mut Units,
    ast: Program,
}

impl<'a> Parser<'a> {
    pub fn new(entry_point: &str, units: &'a mut Units) -> Self {
        Self {
            entry_point: String::from(entry_point),
            units: units,
            ast: Program::new(),
        }
    }

    pub fn parse(&mut self) -> ReportResult<()> {
        let mut report = Report::new();

        report.unwrap(self.parse_entry_point())?;

        println!("{:#?}", self.ast);

        report.wrap(())
    }

    fn parse_entry_point(&mut self) -> ReportResult<()> {
        let mut report = Report::new();

        let source = report.unwrap(self.units.load(&self.entry_point))?;
        let mut tokens = TokenStream::from(&self.entry_point, source);

        self.ast.parse(&mut tokens);

        report.collect(tokens.into_report())?;

        report.wrap(())
    }
}

pub fn expect(stream: &mut TokenStream, token: TokenType, context: &str) -> Result<()> {
    match stream.next() {
        Some(t) => {
            if t.type_ == token {
                Ok(())
            } else {
                Err(stream.report_error(
                    format!("Expected ':', found {}", t.type_),
                    ErrorCode::E100InvalidSyntax,
                    Some(t.location),
                ))
            }
        }

        None => Err(stream.report_error(
            format!("while parsing {}", context),
            ErrorCode::E120UnexpectedEof,
            None,
        )),
    }
}

pub fn expect_identifier(stream: &mut TokenStream, purpose: &str, context: &str) -> Result<String> {
    match stream.next() {
        Some(t) => match t.type_ {
            TokenType::Identifier(name) => Ok(name),
            invalid => Err(stream.report_error(
                format!("Expected {}, found {}", purpose, invalid),
                ErrorCode::E100InvalidSyntax,
                Some(t.location),
            )),
        },

        None => Err(stream.report_error(
            format!("while parsing {}", context),
            ErrorCode::E120UnexpectedEof,
            None,
        )),
    }
}

pub fn follows(stream: &mut TokenStream, token: TokenType) -> bool {
    match stream.next() {
        Some(t) => t.type_ == token,
        None => false,
    }
}

pub fn parse_static_csl<I: Item>(
    stream: &mut TokenStream,
    delimiter: Option<TokenType>,
) -> Result<Vec<I>> {
    let mut nodes = Vec::new();

    loop {
        match &delimiter {
            None => {
                if !I::may_parse(stream) {
                    break;
                }
            }
            Some(d) => {
                if stream.peek(0) == Some(d) {
                    stream.next();
                    break;
                }
            }
        }

        nodes.push(I::parse(stream)?);

        match &delimiter {
            None => match stream.peek(0) {
                Some(TokenType::Comma) => {
                    stream.next();
                }
                _ => break,
            },
            Some(d) => match stream.peek(0) {
                Some(TokenType::Comma) => {
                    stream.next();
                }
                Some(t) if t == d => {
                    stream.next();
                    break;
                }
                _ => {}
            },
        }
    }

    Ok(nodes)
}

pub fn parse_type(stream: &mut TokenStream) -> Result<Box<dyn Type>> {
    if TypeName::may_parse(stream) {
        Ok(Box::new(TypeName::parse(stream)?))
    } else {
        match stream.next() {
            Some(invalid) => Err(stream.report_error(
                format!("Unexpected {} while parsing type", invalid.type_),
                ErrorCode::E100InvalidSyntax,
                Some(invalid.location),
            )),
            None => Err(stream.report_error(
                String::from("while parsing type"),
                ErrorCode::E120UnexpectedEof,
                None,
            )),
        }
    }
}

pub fn parse_expression(stream: &mut TokenStream) -> Result<Box<dyn Value>> {
    if Print::may_parse(stream) {
        Ok(Box::new(Print::parse(stream)?))
    } else {
        let lhs = parse_secondary_expression(stream)?;

        match stream.peek(0) {
            Some(TokenType::Plus) => {
                let op = stream.next().unwrap().type_.into();
                let rhs = parse_expression(stream)?;

                Ok(Box::new(BinaryOperation::new(op, lhs, rhs)))
            }

            _ => Ok(lhs),
        }
    }
}

fn parse_secondary_expression(stream: &mut TokenStream) -> Result<Box<dyn Value>> {
    parse_primary_expression(stream)
}

fn parse_primary_expression(stream: &mut TokenStream) -> Result<Box<dyn Value>> {
    if BoundValue::may_parse(stream) {
        Ok(Box::new(BoundValue::parse(stream)?))
    } else {
        match stream.next() {
            Some(invalid) => Err(stream.report_error(
                format!("Unexpected {} while parsing expression", invalid.type_),
                ErrorCode::E100InvalidSyntax,
                Some(invalid.location),
            )),
            None => Err(stream.report_error(
                String::from("while parsing expression"),
                ErrorCode::E120UnexpectedEof,
                None,
            )),
        }
    }
}
