use super::context::{Context, SymbolCell};
use super::NamedFunction;
use super::Node;
use super::Parameter;
use super::Parameters;
use crate::report::Location;

#[derive(Debug)]
pub struct Program {
    params: Option<Parameters>,
    pub functions: Vec<NamedFunction>,
    pub context: Option<Context>,
    pub entry_point: Option<SymbolCell>,
}

impl Program {
    pub fn new() -> Self {
        Self {
            params: None,
            functions: Vec::new(),
            context: None,
            entry_point: None,
        }
    }

    pub fn has_params(&self) -> bool {
        self.params.is_some()
    }

    pub fn params(&self) -> &[Parameter] {
        match &self.params {
            Some(params) => params,
            None => &[],
        }
    }

    pub fn params_mut(&mut self) -> &mut [Parameter] {
        match &mut self.params {
            Some(params) => params,
            None => &mut [],
        }
    }

    pub fn set_params(&mut self, value: Option<Vec<Parameter>>) {
        self.params = value
    }
}

impl Node for Program {
    fn accept(&self, visitor: &mut dyn super::visit::Visitor) {
        visitor.visit(self)
    }

    fn accept_mut(&mut self, visitor: &mut dyn super::visit::VisitorMut) {
        visitor.visit_mut(self)
    }

    fn location(&self) -> Location {
        panic!("The whole program has no location");
    }
}
