use crate::language::Type;
use crate::report::Location;
use std::cell::RefCell;
use std::collections::hash_map::{Entry, HashMap};
use std::rc::Rc;

#[derive(Debug)]
pub struct Symbol {
    declaration: Location,
    type_: Option<Type>,
}

impl Symbol {
    pub fn new(declaration: Location) -> Self {
        Self {
            declaration,
            type_: None,
        }
    }

    pub fn declaration(&self) -> Location {
        self.declaration
    }

    pub fn type_(&self) -> &Option<Type> {
        &self.type_
    }

    pub fn type_mut(&mut self) -> &mut Option<Type> {
        &mut self.type_
    }
}

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

    pub fn register(
        &mut self,
        name: String,
        location: Location,
    ) -> Result<&SymbolCell, &SymbolCell> {
        match self.symbol_table.entry(name) {
            Entry::Vacant(entry) => Ok(entry.insert(Rc::new(RefCell::new(Symbol::new(location))))),
            Entry::Occupied(entry) => Err(entry.into_mut()),
        }
    }
}
