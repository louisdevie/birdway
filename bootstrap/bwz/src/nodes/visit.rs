use crate::nodes::{self, Node, TypeNode, ValueNode};

pub trait Visit<N: Node> {
    fn visit(&mut self, node: &N);
}

pub trait VisitMut<N: Node> {
    fn visit_mut(&mut self, node: &mut N);
}

pub trait Visitor:
    Visit<nodes::BoundValue>
    + Visit<nodes::NamedFunction>
    + Visit<nodes::Print>
    + Visit<nodes::BinaryOperation>
    + Visit<nodes::TypeName>
    + Visit<nodes::Program>
{
    fn visit_node(&mut self, node: &dyn Node)
    where
        Self: Sized,
    {
        node.accept(self)
    }
}

pub trait VisitorMut:
    VisitMut<nodes::BoundValue>
    + VisitMut<nodes::NamedFunction>
    + VisitMut<nodes::Print>
    + VisitMut<nodes::BinaryOperation>
    + VisitMut<nodes::TypeName>
    + VisitMut<nodes::Program>
{
    fn visit_node_mut(&mut self, node: &mut dyn Node)
    where
        Self: Sized,
    {
        node.accept_mut(self)
    }
}

pub trait ValueVisitor:
    Visit<nodes::BoundValue>
    + Visit<nodes::NamedFunction>
    + Visit<nodes::Print>
    + Visit<nodes::BinaryOperation>
{
    fn visit_value(&mut self, node: &dyn ValueNode)
    where
        Self: Sized,
    {
        ValueNode::accept(node, self)
    }
}

pub trait ValueVisitorMut:
    VisitMut<nodes::BoundValue>
    + VisitMut<nodes::NamedFunction>
    + VisitMut<nodes::Print>
    + VisitMut<nodes::BinaryOperation>
{
    fn visit_value_mut(&mut self, node: &mut dyn ValueNode)
    where
        Self: Sized,
    {
        ValueNode::accept_mut(node, self)
    }
}

pub trait TypeVisitor: Visit<nodes::TypeName> {
    fn visit_type(&mut self, node: &dyn TypeNode)
    where
        Self: Sized,
    {
        TypeNode::accept(node, self)
    }
}

pub trait TypeVisitorMut: VisitMut<nodes::TypeName> {
    fn visit_type_mut(&mut self, node: &mut dyn TypeNode)
    where
        Self: Sized,
    {
        TypeNode::accept_mut(node, self)
    }
}
