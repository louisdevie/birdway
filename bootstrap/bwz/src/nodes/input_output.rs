use crate::nodes::{Node, ValueNode};
use crate::report::Location;

#[derive(Debug, Node, ValueNode)]
pub struct Print {
    pub location: Location,
    pub ln: bool,
    pub value: Box<dyn ValueNode>,
}
