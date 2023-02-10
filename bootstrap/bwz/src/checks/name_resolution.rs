use crate::checks::Check;
use crate::nodes::context::{Context, SymbolCell};
use crate::nodes::visit::{VisitMut, VisitorMut};
use crate::nodes::{self, Node};
use crate::report::{ErrorCode, Report};

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

    fn register_symbol(&mut self, name: String) -> Option<&SymbolCell> {
        self.stack
            .last_mut()
            .and_then(|frame| Some(frame.register(name)))
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

        for param in node.params() {
            self.register_symbol(param.name.clone());
        }

        for func in &mut node.functions {
            self.visit_mut(func);
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
