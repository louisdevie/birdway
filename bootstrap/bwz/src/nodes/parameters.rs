use crate::nodes::TypeNode;

pub type Parameters = Vec<Parameter>;

#[derive(Debug)]
pub struct Parameter {
    pub name: String,
    pub type_: Box<dyn TypeNode>,
}
