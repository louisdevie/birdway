use crate::language::BinaryOperator;
use crate::nodes::{Node, ValueNode};
use crate::report::Location;

#[derive(Debug, Node, ValueNode)]
pub struct BinaryOperation {
    pub location: Location,
    pub op: BinaryOperator,
    pub lhs: Box<dyn ValueNode>,
    pub rhs: Box<dyn ValueNode>,
}
