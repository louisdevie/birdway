use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

#[derive(Debug)]
pub struct Symbol {}

pub type SymbolCell = Rc<RefCell<Symbol>>;

#[derive(Debug)]
pub struct Context {
    symbol_table: HashMap<String, SymbolCell>,
}

impl Context {
    pub fn new() -> Self {
        Self {
            symbol_table: HashMap::new(),
        }
    }

    pub fn look_up(&self, name: &str) -> Option<&SymbolCell> {
        self.symbol_table.get(name)
    }

    pub fn register(&mut self, name: String) -> &SymbolCell {
        self.symbol_table
            .entry(name)
            .or_insert_with(|| Rc::new(RefCell::new(Symbol {})))
    }
}
