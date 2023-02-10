use proc_macro::TokenStream;
use quote::quote;
use syn::parse_macro_input;
use syn::DeriveInput;

#[proc_macro_derive(Node)]
pub fn derive_node(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = input.ident;

    let (impl_generics, ty_generics, where_clause) = input.generics.split_for_impl();

    let expanded = quote! {
        impl #impl_generics crate::nodes::Node for #name #ty_generics #where_clause {
            fn accept(&self, visitor: &mut dyn crate::nodes::visit::Visitor) {
                visitor.visit(self)
            }

            fn accept_mut(&mut self, visitor: &mut dyn crate::nodes::visit::VisitorMut) {
                visitor.visit_mut(self)
            }

            fn location(&self) -> Location {
                self.location
            }
        }
    };

    proc_macro::TokenStream::from(expanded)
}

#[proc_macro_derive(ValueNode)]
pub fn derive_value_node(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = input.ident;

    let (impl_generics, ty_generics, where_clause) = input.generics.split_for_impl();

    let expanded = quote! {
        impl #impl_generics crate::nodes::ValueNode for #name #ty_generics #where_clause {
            fn accept(&self, visitor: &mut dyn crate::nodes::visit::ValueVisitor) {
                visitor.visit(self)
            }

            fn accept_mut(&mut self, visitor: &mut dyn crate::nodes::visit::ValueVisitorMut) {
                visitor.visit_mut(self)
            }

            fn as_node(&self) -> &dyn Node {
                self
            }

            fn as_mut_node(&mut self) -> &mut dyn Node {
                self
            }
        }
    };

    proc_macro::TokenStream::from(expanded)
}

#[proc_macro_derive(TypeNode)]
pub fn derive_type_node(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = input.ident;

    let (impl_generics, ty_generics, where_clause) = input.generics.split_for_impl();

    let expanded = quote! {
        impl #impl_generics crate::nodes::TypeNode for #name #ty_generics #where_clause {
            fn accept(&self, visitor: &mut dyn crate::nodes::visit::TypeVisitor) {
                visitor.visit(self)
            }

            fn accept_mut(&mut self, visitor: &mut dyn crate::nodes::visit::TypeVisitorMut) {
                visitor.visit_mut(self)
            }

            fn as_node(&self) -> &dyn Node {
                self
            }

            fn as_mut_node(&mut self) -> &mut dyn Node {
                self
            }
        }
    };

    proc_macro::TokenStream::from(expanded)
}
