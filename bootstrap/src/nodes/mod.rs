use crate::parser::{self, TokenStream};
use std::fmt::Debug;

mod binding;
mod function;
mod input_output;
mod operation;
mod parameters;
mod program;
mod type_name;

pub use binding::BoundValue;
pub use function::NamedFunction;
pub use input_output::Print;
pub use operation::BinaryOperation;
pub use parameters::Parameters;
pub use program::Program;
pub use type_name::TypeName;

pub trait Item {
    fn parse(stream: &mut TokenStream) -> parser::Result<Self>
    where
        Self: Sized;

    fn may_parse(stream: &mut TokenStream) -> bool
    where
        Self: Sized;
}

pub trait Node
where
    Self: Debug,
{
}

pub trait Value
where
    Self: Node,
{
}

pub trait Type
where
    Self: Node,
{
}
