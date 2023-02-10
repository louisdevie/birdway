use crate::nodes::{Node, TypeNode};
use crate::report::Location;

#[derive(Debug, Node, TypeNode)]
pub struct TypeName {
    pub location: Location,
    pub name: String,
}
