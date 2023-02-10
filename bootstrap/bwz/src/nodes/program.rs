use crate::nodes::context::Context;
use crate::nodes::NamedFunction;
use crate::nodes::Node;
use crate::nodes::Parameter;
use crate::nodes::Parameters;
use crate::report::Location;

#[derive(Debug)]
pub struct Program {
    params: Option<Parameters>,
    pub functions: Vec<NamedFunction>,
    pub context: Option<Context>,
}

impl Program {
    pub fn new() -> Self {
        Self {
            params: None,
            functions: Vec::new(),
            context: None,
        }
    }

    pub fn has_params(&self) -> bool {
        self.params.is_some()
    }

    pub fn params(&self) -> &[Parameter] {
        match &self.params {
            Some(params) => &params,
            None => &[],
        }
    }

    pub fn set_params(&mut self, value: Option<Vec<Parameter>>) {
        self.params = value
    }
}

impl Node for Program {
    fn accept(&self, visitor: &mut dyn crate::nodes::visit::Visitor) {
        visitor.visit(self)
    }

    fn accept_mut(&mut self, visitor: &mut dyn crate::nodes::visit::VisitorMut) {
        visitor.visit_mut(self)
    }

    fn location(&self) -> Location {
        panic!("The whole program has no location");
    }
}
