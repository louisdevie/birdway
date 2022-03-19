from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective


class SyntaxDef(nodes.Admonition, nodes.Element):
    pass


class SyntaxDirective(SphinxDirective):
    has_content = True

    def run(self):
        targetid = "syntaxdef-%d" % self.env.new_serialno("syntaxdef")

        targetnode = nodes.target("", "", ids=[targetid])

        syntax_def_node = SyntaxDef("\n".join(self.content))

        syntax_def_node += nodes.title(_("Syntax"), _("Syntax"))

        self.state.nested_parse(self.content, self.content_offset, syntax_def_node)

        return [targetnode, syntax_def_node]


def html_visit_syntaxdef_node(self, node):
    self.body.append('<div class="syntax-definition">')
    self.visit_admonition(node)


def html_depart_syntaxdef_node(self, node):
    self.depart_admonition(node)
    self.body.append("</div>")


def setup(app):
    app.add_node(
        SyntaxDef,
        html=(html_visit_syntaxdef_node, html_depart_syntaxdef_node),
    )

    app.add_directive("syntax", SyntaxDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
