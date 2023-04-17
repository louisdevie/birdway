use crate::target::OutputInfo;
use std::process::Command;

pub const INFO: &str = "linux";

#[cfg(feature = "c_backend")]
pub fn build_process(_info: OutputInfo) -> Vec<Command> {
    vec![]
}
