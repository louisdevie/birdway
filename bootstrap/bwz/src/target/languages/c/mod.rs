pub const INFO: &str = "C backend";

mod features;
mod generator;
mod syntax;
mod writer;

pub use generator::Generator;
