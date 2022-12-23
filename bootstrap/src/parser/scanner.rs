use crate::report::{ErrorCode, Location, Report};
use std::borrow::Borrow;
use std::collections::VecDeque;
use std::fmt;
use std::str::Chars;

#[derive(Debug, Clone)]
pub struct Token {
    pub location: Location,
    pub type_: TokenType,
}

impl Token {
    pub fn new(location: Location, type_: TokenType) -> Self {
        Self { location, type_ }
    }
}

#[derive(Debug, PartialEq, Clone)]
pub enum TokenType {
    // PUNCTUATION
    OpeningBrace,
    ClosingBrace,
    OpeningParens,
    ClosingParens,
    OpeningBracket,
    ClosingBracket,
    Dot,
    Comma,
    Colon,
    AtSymbol,
    Dollar,
    Underscore,
    EqualSign,
    Arrow,

    // OPERATORS
    Plus,

    // KEYWORDS
    KeywordFunc,
    KeywordParams,
    KeywordPrintln,

    // OTHER
    LineBreak,
    BlankLineBreak,
    Identifier(String),
}

impl TokenType {
    pub fn from_identifier(ident: &str) -> Self {
        match ident {
            "_" => Self::Underscore,
            "func" => Self::KeywordFunc,
            "params" => Self::KeywordParams,
            "println" => Self::KeywordPrintln,
            other => Self::Identifier(String::from(other)),
        }
    }
}

impl fmt::Display for TokenType {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "{}",
            match self {
                Self::OpeningBrace => "'{{'",
                Self::ClosingBrace => "'}}'",
                Self::OpeningParens => "'('",
                Self::ClosingParens => "')'",
                Self::OpeningBracket => "'['",
                Self::ClosingBracket => "']'",
                Self::Dot => "'.'",
                Self::Comma => "','",
                Self::Colon => "':'",
                Self::AtSymbol => "'@'",
                Self::Dollar => "'$'",
                Self::Underscore => "'_'",
                Self::EqualSign => "'='",
                Self::Arrow => "'->'",
                Self::Plus => "'+'",

                Self::KeywordFunc => "keyword 'func'",
                Self::KeywordParams => "keyword 'params'",
                Self::KeywordPrintln => "keyword 'println'",

                Self::LineBreak | Self::BlankLineBreak => "line break",
                Self::Identifier(ident) => return write!(formatter, "identifier '{}'", ident),
            }
        )
    }
}

#[derive(Debug, PartialEq)]
enum Scanner {
    // MAIN CONTEXT
    Ready,
    NewLine,
    OneHyphen,
    TwoHyphens,
    Identifier(String),

    // COMMENTS
    BlockComment,
    BlockCommentOneHyphen,
    BlockCommentTwoHyphens,
}

#[derive(Copy, Clone)]
pub enum Filter {
    None,
    LineBreaks,
    AllLineBreaks,
}

impl Filter {
    pub fn filter(&self, token: &Token) -> bool {
        match self {
            Self::None => true,

            Self::LineBreaks => match token.type_ {
                TokenType::LineBreak => false,
                _ => true,
            },

            Self::AllLineBreaks => match token.type_ {
                TokenType::LineBreak | TokenType::BlankLineBreak => false,
                _ => true,
            },
        }
    }

    pub fn apply<B: Borrow<Token>>(&self, token: Option<B>) -> Option<B> {
        match token {
            Some(t) => {
                if self.filter(t.borrow()) {
                    Some(t)
                } else {
                    None
                }
            }
            None => None,
        }
    }
}

pub struct TokenStream<'a> {
    file: &'a str,
    source: Chars<'a>,
    scanner: Scanner,
    chars_count: usize,
    last_token: usize,
    buffer: VecDeque<Token>,
    report: Report,
    filters: Vec<Filter>,
}

impl<'a> TokenStream<'a> {
    pub fn from(file: &'a str, source: &'a str) -> Self {
        Self {
            file,
            source: source.chars(),
            scanner: Scanner::Ready,
            chars_count: 0,
            last_token: 0,
            buffer: VecDeque::with_capacity(3),
            report: Report::new(),
            filters: Vec::new(),
        }
    }

    pub fn peek(&mut self, depth: usize) -> Option<&TokenType> {
        let filter = *self.filters.last().unwrap_or(&Filter::None);

        let mut i = 0; // real position
        let mut f = 0; // number of items that passed the filter
        while f <= depth {
            match self.peek_unfiltered(i) {
                Some(token) => {
                    if filter.filter(token) {
                        f += 1;
                    }
                }
                // no more items, abort
                None => return None,
            }
            i += 1;
        }

        self.buffer.get(i - 1).and_then(|tok| Some(&tok.type_))
    }

    fn peek_unfiltered(&mut self, depth: usize) -> Option<&Token> {
        while self.buffer.len() <= depth {
            match self.source.next() {
                Some(c) => {
                    self.scanner_next(c);
                    self.chars_count += 1;
                }
                None => {
                    self.scanner_stop();
                    break;
                }
            }
        }

        self.buffer.get(depth)
    }

    pub fn report_warning(&mut self, message: String, code: ErrorCode, location: Option<Location>) {
        self.report.warning(message, code, location);
    }

    pub fn report_error(&mut self, message: String, code: ErrorCode, location: Option<Location>) {
        self.report.error(message, code, location);
    }

    pub fn into_report(self) -> Report {
        self.report
    }

    pub fn push_filter(&mut self, filter: Filter) {
        self.filters.push(filter);
    }

    pub fn pop_filter(&mut self) {
        self.filters.pop();
    }

    fn yield_token(&mut self, token: TokenType) {
        self.buffer.push_back(Token::new(
            Location::between(
                String::from(self.file),
                self.last_token,
                self.chars_count + 1,
            ),
            token,
        ));
        self.last_token = self.chars_count + 1;
    }

    fn yield_token_at(&mut self, start: usize, span: usize, token: TokenType) {
        self.buffer.push_back(Token::new(
            Location::from(String::from(self.file), start, span),
            token,
        ));
        self.last_token = start + span;
    }

    fn skip(&mut self) {
        self.last_token = self.chars_count + 1;
    }

    fn skip_to(&mut self, position: usize) {
        self.last_token = position;
    }

    fn error(&mut self, message: String, code: ErrorCode) {
        self.report
            .error(message, code, Some(self.current_location()));
        self.last_token = self.chars_count + 1;
    }

    fn current_location(&self) -> Location {
        Location::at(String::from(self.file), self.chars_count)
    }

    fn last_token_location(&self) -> Location {
        Location::at(String::from(self.file), self.last_token)
    }

    fn scanner_next(&mut self, c: char) {
        match &mut self.scanner {
            Scanner::Ready => match c {
                ' ' | '\t' => self.skip(),
                '\n' => self.scanner = Scanner::NewLine,

                '{' => self.yield_token(TokenType::OpeningBrace),
                '}' => self.yield_token(TokenType::ClosingBrace),
                '(' => self.yield_token(TokenType::OpeningParens),
                ')' => self.yield_token(TokenType::ClosingParens),
                '[' => self.yield_token(TokenType::OpeningBracket),
                ']' => self.yield_token(TokenType::ClosingBracket),
                '.' => self.yield_token(TokenType::Dot),
                ',' => self.yield_token(TokenType::Comma),
                ':' => self.yield_token(TokenType::Colon),
                '@' => self.yield_token(TokenType::AtSymbol),
                '$' => self.yield_token(TokenType::Dollar),
                '=' => self.yield_token(TokenType::EqualSign),
                '+' => self.yield_token(TokenType::Plus),

                'a'..='z' | 'A'..='Z' | '0'..='9' | '_' => {
                    self.scanner = Scanner::Identifier(String::from(c))
                }

                '-' => self.scanner = Scanner::OneHyphen,

                _ => self.error(
                    format!("unexpected \"{}\"", c),
                    ErrorCode::E110InvalidCharacter,
                ),
            },

            Scanner::NewLine => match c {
                ' ' | '\t' => {}

                '\n' => {
                    self.yield_token_at(self.last_token, 1, TokenType::BlankLineBreak);
                    self.skip_to(self.chars_count);
                }

                other => {
                    self.yield_token_at(self.last_token, 1, TokenType::LineBreak);
                    self.skip_to(self.chars_count);
                    self.scanner = Scanner::Ready;
                    self.scanner_next(other);
                }
            },

            Scanner::OneHyphen => match c {
                '>' => {
                    self.scanner = Scanner::Ready;
                    self.yield_token(TokenType::Arrow)
                }

                '-' => self.scanner = Scanner::TwoHyphens,

                other => {
                    self.report.error(
                        String::from("unexpected \"-\""),
                        ErrorCode::E110InvalidCharacter,
                        Some(self.last_token_location()),
                    );
                    self.scanner = Scanner::Ready;
                    self.scanner_next(other);
                }
            },

            Scanner::TwoHyphens => match c {
                '>' => {
                    let location = self.last_token_location();
                    let position = location.position();
                    self.report.error(
                        String::from("unexpected \"-\""),
                        ErrorCode::E110InvalidCharacter,
                        Some(location),
                    );
                    self.yield_token_at(position + 1, 2, TokenType::Arrow);
                    self.scanner = Scanner::Ready;
                }

                '-' => self.scanner = Scanner::BlockComment,

                other => {
                    self.scanner = Scanner::Ready;
                    self.report.error(
                        String::from("unexpected \"-\""),
                        ErrorCode::E110InvalidCharacter,
                        Some(self.last_token_location()),
                    );
                    self.scanner_next(other);
                }
            },

            Scanner::Identifier(ident) => match c {
                'a'..='z' | 'A'..='Z' | '0'..='9' | '_' => {
                    ident.push(c);
                }

                other => {
                    let len = ident.len();
                    let token = TokenType::from_identifier(&ident);
                    self.yield_token_at(self.last_token, len, token);
                    self.scanner = Scanner::Ready;
                    self.scanner_next(other);
                }
            },

            Scanner::BlockComment => match c {
                '-' => self.scanner = Scanner::BlockCommentOneHyphen,
                _ => {}
            },
            Scanner::BlockCommentOneHyphen => match c {
                '-' => self.scanner = Scanner::BlockCommentTwoHyphens,
                _ => {}
            },
            Scanner::BlockCommentTwoHyphens => match c {
                '-' => {
                    self.scanner = Scanner::Ready;
                    self.skip()
                }
                _ => {}
            },
        };
    }

    fn scanner_stop(&mut self) {
        match &self.scanner {
            Scanner::Ready => {}

            Scanner::NewLine => self.yield_token_at(self.last_token, 1, TokenType::BlankLineBreak),

            Scanner::OneHyphen => self.report.error(
                String::from("unexpected \"-\""),
                ErrorCode::E110InvalidCharacter,
                Some(self.current_location()),
            ),

            Scanner::Identifier(ident) => {
                let token = TokenType::from_identifier(ident);
                self.yield_token(token);
                self.scanner = Scanner::Ready;
            }

            Scanner::TwoHyphens => {
                self.report.error(
                    String::from("unexpected \"-\""),
                    ErrorCode::E110InvalidCharacter,
                    Some(self.last_token_location()),
                );
                self.report.error(
                    String::from("unexpected \"-\""),
                    ErrorCode::E110InvalidCharacter,
                    Some(self.current_location()),
                );
            }
            Scanner::BlockComment
            | Scanner::BlockCommentOneHyphen
            | Scanner::BlockCommentTwoHyphens => {
                self.report.error(
                    String::from("unterminated block comment"),
                    ErrorCode::E120UnexpectedEof,
                    Some(self.current_location()),
                );
            }
        };
    }
}

impl<'a> Iterator for TokenStream<'a> {
    type Item = Token;

    fn next(&mut self) -> Option<Self::Item> {
        let filter = *self.filters.last().unwrap_or(&Filter::None);

        match filter.apply(self.buffer.pop_front()) {
            Some(token) => return Some(token),
            None => {}
        }

        loop {
            match self.source.next() {
                Some(c) => {
                    self.scanner_next(c);
                    self.chars_count += 1;

                    match filter.apply(self.buffer.pop_front()) {
                        Some(token) => break Some(token),
                        None => {}
                    }
                }
                None => {
                    self.scanner_stop();

                    match filter.apply(self.buffer.pop_front()) {
                        Some(token) => break Some(token),

                        None => break None,
                    }
                }
            }
        }
    }
}
