use crate::nodes::context::SymbolCell;
use crate::nodes::TypeNode;
use crate::report::Location;

pub type Parameters = Vec<Parameter>;

#[derive(Debug)]
pub struct Parameter {
    pub location: Location,
    pub name: String,
    pub type_: Box<dyn TypeNode>,
    pub symbol: Option<SymbolCell>,
}
