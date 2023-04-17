use crate::checks::Check;
use crate::language::Type;
use crate::nodes;
use crate::nodes::visit::{TypeVisitor, Visit, VisitMut, VisitorMut};
use crate::report::{ErrorCode, Report};

macro_rules! maybe {
    ($e:expr) => {
        match ($e) {
            Some(value) => value,
            None => return,
        }
    };
}

pub struct TypeChecking {
    report: Report,
    result: Option<Type>,
}

impl TypeChecking {}

impl Check for TypeChecking {
    fn run(ast: &mut nodes::Program) -> Report {
        let mut visitor = Self {
            report: Report::new(),
            result: None,
        };
        visitor.visit_mut(ast);
        visitor.report
    }
}

impl VisitorMut for TypeChecking {}

impl VisitMut<nodes::Program> for TypeChecking {
    fn visit_mut(&mut self, node: &mut nodes::Program) {
        for param in node.params() {
            if let Some(symbol) = &param.symbol {
                let mut type_resolver = TypeResolution::new();
                type_resolver.visit_type(param.type_.as_ref());
                self.report.collect(type_resolver.report).unwrap();

                if let Some(type_) = type_resolver.result {
                    *symbol.borrow_mut().type_mut() = Some(type_);
                }
            }
        }

        for func in &mut node.functions {
            self.visit_mut(func);
        }
    }
}

impl VisitMut<nodes::BoundValue> for TypeChecking {
    fn visit_mut(&mut self, node: &mut nodes::BoundValue) {
        self.result = node
            .symbol
            .as_ref()
            .and_then(|symbol| symbol.borrow().type_().clone())
    }
}

impl VisitMut<nodes::NamedFunction> for TypeChecking {
    fn visit_mut(&mut self, node: &mut nodes::NamedFunction) {
        self.visit_node_mut(node.body.as_mut_node());
        let return_type = maybe!(self.result.take());

        if return_type == Type::Void {
            let function_type = Some(Type::Function);
            *node.symbol.as_ref().unwrap().borrow_mut().type_mut() = function_type.clone();
            self.result = function_type;
        } else {
            self.report.recovered_error(
                format!("a function can't return {}", return_type),
                ErrorCode::E300TypeError,
                Some(node.body.location()),
            )
        }
    }
}

impl VisitMut<nodes::Print> for TypeChecking {
    fn visit_mut(&mut self, node: &mut nodes::Print) {
        self.visit_node_mut(node.value.as_mut_node());

        self.result = Some(Type::Void);
    }
}

impl VisitMut<nodes::BinaryOperation> for TypeChecking {
    fn visit_mut(&mut self, node: &mut nodes::BinaryOperation) {
        self.visit_node_mut(node.lhs.as_mut_node());
        let lhs_type = maybe!(self.result.take());

        self.visit_node_mut(node.rhs.as_mut_node());
        let rhs_type = maybe!(self.result.take());

        self.result = node.op.result(&lhs_type, &rhs_type);
        if self.result.is_none() {
            self.report.recovered_error(
                format!(
                    "Invalid operand types for {} ({} and {})",
                    node.op, lhs_type, rhs_type
                ),
                ErrorCode::E300TypeError,
                Some(node.location),
            )
        }
    }
}

impl VisitMut<nodes::TypeName> for TypeChecking {
    fn visit_mut(&mut self, _: &mut nodes::TypeName) {}
}

pub struct TypeResolution {
    report: Report,
    result: Option<Type>,
}

impl TypeResolution {
    pub fn new() -> Self {
        Self {
            report: Report::new(),
            result: None,
        }
    }
}

impl TypeVisitor for TypeResolution {}

impl Visit<nodes::TypeName> for TypeResolution {
    fn visit(&mut self, node: &nodes::TypeName) {
        self.result = match node.name.as_ref() {
            "Int" => Some(Type::Int),
            other => {
                self.report.recovered_error(
                    format!("unknown type '{}'", other),
                    ErrorCode::E221TypeNotFound,
                    Some(node.location),
                );
                None
            }
        };
    }
}
