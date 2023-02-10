use crate::nodes::context::SymbolCell;
use crate::nodes::{Node, ValueNode};
use crate::report::Location;

#[derive(Debug, Node, ValueNode)]
pub struct BoundValue {
    pub location: Location,
    pub name: String,
    pub symbol: Option<SymbolCell>,
}
