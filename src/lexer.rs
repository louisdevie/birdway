use lazy_static::lazy_static;
use regex::Regex;

#[derive(Debug)]
pub enum Token {
    BlockBegin {},
    BlockEnd {},
    DoubleQuotes {},
    Identifier { name: String },
    Keyword { keyword: Keyword },
    UnaryLeftOperator { operator: UnaryLeftOperator },
    LineEnd {},
    StringContent { value: String },
    Variable { name: String },
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
pub enum UnaryLeftOperator {
    NOTNULL,
}

pub fn parse(script: &str) -> Vec<Token> {
    let mut result = Vec::new();

    parse_generic(script, &mut result, 0);

    println!("{:#?}", result);
    return result;
}

fn parse_generic(input: &str, output: &mut Vec<Token>, mut cursor: usize) -> usize {
    lazy_static! {
        static ref KEYWORD: Regex = Regex::new(r"\b(args|(as|(authors|(break|(case|(close|(default|(description|(do|(else|(fail|(flag|(for(each)?|(from|(func|(homepage|(if|(in|(let|(long|(meta|(mode|(name|(open|(option(al)?|(param|(print(ln)?|(read(ln)?|(repeat|(return|(run|(short|(skip|(success|(switch|(then|(to|(type|(until|(version|(while)))))))))))))))))))))))))))))))))))))))))\b").unwrap();
        static ref SPACING: Regex = Regex::new(r"\s+").unwrap();
        static ref OBRACE: Regex = Regex::new(r"\{").unwrap();
        static ref CBRACE: Regex = Regex::new(r"\}").unwrap();
        static ref SEMICOLON: Regex = Regex::new(r";").unwrap();
        static ref DQUOTES: Regex = Regex::new("\"").unwrap();
        static ref IDENTIFIER: Regex = Regex::new(r"\b\w+\b").unwrap();
        static ref VARIABLE: Regex = Regex::new(r"\$\b\w+\b").unwrap();
        static ref LOPERATOR: Regex = Regex::new(r"\?").unwrap();
    }

    let end = input.len();

    while cursor < end {
        if let Some(m) = KEYWORD.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::Keyword {
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

        if let Some(m) = DQUOTES.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::DoubleQuotes {});
                cursor = parse_double_quoted(input, output, cursor);
                continue;
            }
        }

        if let Some(m) = IDENTIFIER.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::Identifier {
                    name: String::from(m.as_str()),
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = VARIABLE.find_at(input, cursor) {
            if m.start() == cursor {
                let mut without_dollar = String::from(m.as_str());
                without_dollar.remove(0);
                output.push(Token::Variable {
                    name: without_dollar,
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = OBRACE.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::BlockBegin {});
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = CBRACE.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::BlockEnd {});
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = SEMICOLON.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::LineEnd {});
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = LOPERATOR.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::UnaryLeftOperator {
                    operator: UnaryLeftOperator::NOTNULL,
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = SPACING.find_at(input, cursor) {
            if m.start() == cursor {
                cursor = m.end();
                continue;
            }
        }

        panic!("Invalid character at position {}", cursor);
    }

    return cursor;
}

fn parse_double_quoted(input: &str, output: &mut Vec<Token>, mut cursor: usize) -> usize {
    lazy_static! {
        static ref LOPERATOR: Regex = Regex::new(r"\?").unwrap();
    }

    let end = input.len();

    while cursor < end {
        if let Some(m) = DQUOTES.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::DoubleQuotes {});

                continue;
            }
        }

        if let Some(m) = IDENTIFIER.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::Identifier {
                    name: String::from(m.as_str()),
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = VARIABLE.find_at(input, cursor) {
            if m.start() == cursor {
                let mut without_dollar = String::from(m.as_str());
                without_dollar.remove(0);
                output.push(Token::Variable {
                    name: without_dollar,
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = OBRACE.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::BlockBegin {});
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = CBRACE.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::BlockEnd {});
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = SEMICOLON.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::LineEnd {});
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = LOPERATOR.find_at(input, cursor) {
            if m.start() == cursor {
                output.push(Token::UnaryLeftOperator {
                    operator: UnaryLeftOperator::NOTNULL,
                });
                cursor = m.end();
                continue;
            }
        }

        if let Some(m) = SPACING.find_at(input, cursor) {
            if m.start() == cursor {
                cursor = m.end();
                continue;
            }
        }

        panic!("Invalid character at position {}", cursor);
    }

    return cursor;
}
