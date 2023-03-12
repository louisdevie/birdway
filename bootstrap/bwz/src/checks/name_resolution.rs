use crate::checks::Check;
use crate::nodes::context::{Context, SymbolCell};
use crate::nodes::visit::{VisitMut, VisitorMut};
use crate::nodes::{self, Node};
use crate::report::{ErrorCode, Location, Report};
use std::rc::Rc;

pub struct NameResolution {
    report: Report,
    stack: Vec<Context>,
}

impl NameResolution {
    fn push_new_context(&mut self) {
        self.stack.push(Context::new());
    }

    fn pop_context(&mut self) -> Option<Context> {
        self.stack.pop()
    }

    fn look_up_symbol(&self, name: &str) -> Option<&SymbolCell> {
        self.stack
            .iter()
            .rev()
            .find_map(|frame| frame.look_up(name))
    }

    fn register_symbol(
        &mut self,
        name: String,
        location: Location,
    ) -> Result<&SymbolCell, &SymbolCell> {
        self.stack.last_mut().unwrap().register(name, location)
    }
}

impl Check for NameResolution {
    fn run(ast: &mut nodes::Program) -> Report {
        let mut visitor = Self {
            report: Report::new(),
            stack: Vec::new(),
        };
        visitor.visit_mut(ast);
        visitor.report
    }
}

impl VisitorMut for NameResolution {}

impl VisitMut<nodes::Program> for NameResolution {
    fn visit_mut(&mut self, node: &mut nodes::Program) {
        self.push_new_context();

        for param in node.params_mut() {
            match self.register_symbol(param.name.clone(), param.location) {
                Ok(added) => param.symbol = Some(Rc::clone(added)),
                Err(_previous) => self.report.recovered_error(
                    format!("'{}' is defined multiple times", param.name),
                    ErrorCode::E212ValueAlreadyExists,
                    Some(param.location),
                ),
            }
        }

        for func in &mut node.functions {
            match self.register_symbol(func.name.clone(), func.location) {
                Ok(added) => func.symbol = Some(Rc::clone(added)),
                Err(_previous) => self.report.recovered_error(
                    format!("'{}' is defined multiple times", func.name),
                    ErrorCode::E212ValueAlreadyExists,
                    Some(func.location),
                ),
            }
            self.visit_mut(func);
        }

        // check for main function
        match self.look_up_symbol("main") {
            Some(symbol) => node.entry_point = Some(Rc::clone(symbol)),
            None => self.report.recovered_error(
                format!("'main' function not found"),
                ErrorCode::E211ValueNotFound,
                Some(node.location()),
            ),
        }

        node.context = self.pop_context();
    }
}

impl VisitMut<nodes::BoundValue> for NameResolution {
    fn visit_mut(&mut self, node: &mut nodes::BoundValue) {
        match self.look_up_symbol(&node.name) {
            Some(symbol) => node.symbol = Some(symbol.clone()),
            None => self.report.recovered_error(
                format!("cannot find '{}' in this scope", node.name),
                ErrorCode::E211ValueNotFound,
                Some(node.location()),
            ),
        }
    }
}

impl VisitMut<nodes::NamedFunction> for NameResolution {
    fn visit_mut(&mut self, node: &mut nodes::NamedFunction) {
        self.push_new_context();

        self.visit_node_mut(node.body.as_mut_node());

        node.context = self.pop_context();
    }
}

impl VisitMut<nodes::Print> for NameResolution {
    fn visit_mut(&mut self, node: &mut nodes::Print) {
        self.visit_node_mut(node.value.as_mut_node());
    }
}

impl VisitMut<nodes::BinaryOperation> for NameResolution {
    fn visit_mut(&mut self, node: &mut nodes::BinaryOperation) {
        self.visit_node_mut(node.lhs.as_mut_node());
        self.visit_node_mut(node.rhs.as_mut_node());
    }
}

impl VisitMut<nodes::TypeName> for NameResolution {
    fn visit_mut(&mut self, _: &mut nodes::TypeName) {}
}
