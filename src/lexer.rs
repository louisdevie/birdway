use lazy_static::lazy_static;
use regex::Regex;

#[derive(Debug)]
pub enum Token {
    BlockBegin {},
    BlockEnd {},
    Identifier { name: String },
    Keyword { keyword: Keyword },
    LeftOperator { operator: LeftOperator },
    LineEnd {},
    StringLiteral { value: String },
    Variable { name: String },
}

pub fn parse(script: &str) -> Vec<Token> {
    lazy_static! {
        static ref KEYWORD: Regex = Regex::new(r"\b(args|(as|(authors|(break|(case|(close|(default|(description|(do|(else|(fail|(flag|(for(each)?|(from|(func|(homepage|(if|(in|(let|(long|(meta|(mode|(name|(open|(option(al)?|(param|(print(ln)?|(read(ln)?|(repeat|(return|(run|(short|(skip|(success|(switch|(then|(to|(type|(until|(version|(while)))))))))))))))))))))))))))))))))))))))))\b").unwrap();
        static ref SPACING: Regex = Regex::new(r"\s+").unwrap();
        static ref OBRACE: Regex = Regex::new(r"\{").unwrap();
        static ref CBRACE: Regex = Regex::new(r"\}").unwrap();
        static ref SEMICOLON: Regex = Regex::new(r";").unwrap();
        static ref STRING: Regex = Regex::new("\".*?[^\\\\]?\"").unwrap();
        static ref IDENTIFIER: Regex = Regex::new(r"\b\w+\b").unwrap();
        static ref VARIABLE: Regex = Regex::new(r"\$\b\w+\b").unwrap();
        static ref LOPERATOR: Regex = Regex::new(r"\?").unwrap();
    }

    let mut tokens = Vec::new();

    let end = script.len();
    let mut cursor = 0;
    while cursor < end {
        if let Some(m) = KEYWORD.find_at(script, cursor) {
            if m.start() == cursor {
                tokens.push(Token::Keyword {
                    keyword: match m.as_str() {
                        "meta" => Keyword::META,
                        "name" => Keyword::NAME,
                        "args" => Keyword::ARGS,
                        "param" => Keyword::PARAM,
                        "optional" => Keyword::OPTIONAL,
                        "description" => Keyword::DESCRIPTION,
                        "run" => Keyword::RUN,
                        "if" => Keyword::IF,
                        "then" => Keyword::THEN,
                        "println" => Keyword::PRINTLN,
                        "else" => Keyword::ELSE,
                        "success" => Keyword::SUCCESS,
                        &_ => panic!("Invalid keyword"),
                    },
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = STRING.find_at(script, cursor) {
            if m.start() == cursor {
                let mut without_quotes = String::from(m.as_str());
                without_quotes.remove(0);
                without_quotes.pop().unwrap();
                tokens.push(Token::StringLiteral {
                    value: without_quotes,
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = IDENTIFIER.find_at(script, cursor) {
            if m.start() == cursor {
                tokens.push(Token::Identifier {
                    name: String::from(m.as_str()),
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = VARIABLE.find_at(script, cursor) {
            if m.start() == cursor {
                let mut without_dollar = String::from(m.as_str());
                without_dollar.remove(0);
                tokens.push(Token::Variable {
                    name: without_dollar,
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = OBRACE.find_at(script, cursor) {
            if m.start() == cursor {
                tokens.push(Token::BlockBegin {});
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = CBRACE.find_at(script, cursor) {
            if m.start() == cursor {
                tokens.push(Token::BlockEnd {});
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = SEMICOLON.find_at(script, cursor) {
            if m.start() == cursor {
                tokens.push(Token::LineEnd {});
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = LOPERATOR.find_at(script, cursor) {
            if m.start() == cursor {
                tokens.push(Token::LeftOperator {
                    operator: LeftOperator::NOTNULL,
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = SPACING.find_at(script, cursor) {
            if m.start() == cursor {
                cursor = m.end();
                continue;
            }
        }

        panic!("Invalid character at position {}", cursor);
    }

    println!("{:#?}", tokens);
    return tokens;
}

#[derive(Debug)]
pub enum Keyword {
    META,
    NAME,
    ARGS,
    PARAM,
    OPTIONAL,
    DESCRIPTION,
    RUN,
    IF,
    THEN,
    PRINTLN,
    ELSE,
    SUCCESS,
}

#[derive(Debug)]
pub enum LeftOperator {
    NOTNULL,
}
