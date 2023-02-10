use crate::parser::{self, TokenStream, TokenType};

pub enum Mode {
    SkipUntil(TokenType),
}

pub trait Recover<T, E> {
    fn recover(self, stream: &mut TokenStream, mode: Mode) -> Result<Option<T>, E>;
}

impl<T> Recover<T, ()> for parser::Result<T> {
    fn recover(self, stream: &mut TokenStream, mode: Mode) -> parser::Result<Option<T>> {
        match self {
            Ok(value) => Ok(Some(value)),
            Err(()) => match mode {
                Mode::SkipUntil(limit) => {
                    while let Some(token) = stream.next() {
                        if token.type_ == limit {
                            break;
                        }
                    }
                    Ok(None)
                }
            },
        }
    }
}
