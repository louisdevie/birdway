use crate::nodes::context::{Context, SymbolCell};
use crate::nodes::{Node, ValueNode};
use crate::report::Location;

#[derive(Debug, Node, ValueNode)]
pub struct NamedFunction {
    pub location: Location,
    pub name: String,
    pub symbol: Option<SymbolCell>,
    pub params: Vec<FunctionParameter>,
    pub body: Box<dyn ValueNode>,
    pub context: Option<Context>,
}

#[derive(Debug)]
pub struct FunctionParameter {}
