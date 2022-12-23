use crate::language::BinaryOperator;
use crate::nodes::{Node, Value};

#[derive(Debug)]
pub struct BinaryOperation {
    op: BinaryOperator,
    lhs: Box<dyn Value>,
    rhs: Box<dyn Value>,
}

impl BinaryOperation {
    pub fn new(op: BinaryOperator, lhs: Box<dyn Value>, rhs: Box<dyn Value>) -> Self {
        Self { op, lhs, rhs }
    }
}

impl Node for BinaryOperation {}

impl Value for BinaryOperation {}
