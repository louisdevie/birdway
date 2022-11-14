from komoe.plugin import *

import pygments


@setup
def setup(ctx, cfg):
    ctx.markdown.disable_default_extension("fenced_code")
    ctx.markdown.configure_extension(
        "toc",
        permalink="§",
        permalink_title="Permalink",
        toc_depth="2-5",
        title="Table of contents",
    )

    ctx.markdown.add_extension("pymdownx.superfences")
    ctx.markdown.add_extension("pymdownx.highlight", auto_title=True)
    ctx.markdown.add_extension("pymdownx.inlinehilite")
