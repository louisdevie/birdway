use std::io::Write;

pub struct Writer<W: Write> {
    output: W,
}

impl<W: Write> Writer<W> {
    pub fn new(output: W) -> Self {
        Self { output }
    }

    pub fn close(self) {}
}
