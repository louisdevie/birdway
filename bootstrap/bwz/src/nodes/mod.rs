use crate::report::Location;
use bwz_derive::{Node, TypeNode, ValueNode};
use std::fmt::Debug;

pub mod context;
pub mod visit;

mod binding;
mod function;
mod input_output;
mod operation;
mod parameters;
mod program;
mod typing;

pub use binding::BoundValue;
pub use function::{FunctionParameter, NamedFunction};
pub use input_output::Print;
pub use operation::BinaryOperation;
pub use parameters::{Parameter, Parameters};
pub use program::Program;
pub use typing::TypeName;

pub trait Node: Debug {
    fn accept(&self, visitor: &mut dyn visit::Visitor);
    fn accept_mut(&mut self, visitor: &mut dyn visit::VisitorMut);

    fn location(&self) -> Location;
}

pub trait ValueNode: Node {
    fn accept(&self, visitor: &mut dyn visit::ValueVisitor);
    fn accept_mut(&mut self, visitor: &mut dyn visit::ValueVisitorMut);

    fn as_node(&self) -> &dyn Node;
    fn as_mut_node(&mut self) -> &mut dyn Node;
}

pub trait TypeNode: Node {
    fn accept(&self, visitor: &mut dyn visit::TypeVisitor);
    fn accept_mut(&mut self, visitor: &mut dyn visit::TypeVisitorMut);

    fn as_node(&self) -> &dyn Node;
    fn as_mut_node(&mut self) -> &mut dyn Node;
}
