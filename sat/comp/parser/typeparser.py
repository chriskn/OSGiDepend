#!/usr/bin/env python
# -*- coding: utf-8 -*-
from javalang.tree import (
    ClassDeclaration,
    ConstructorDeclaration,
    EnumDeclaration,
    InterfaceDeclaration,
    MethodDeclaration,
)

from sat.comp.domain import Method, Type
import sat.comp.compcalculator as comp


def parse(sourcefile):
    parsed_types = []
    ast = sourcefile.ast
    if ast:
        types = _collect_types(ast, list())
        for ast_type in types:
            parsed_type = _parse_type(ast_type, sourcefile.abs_path)
            parsed_types.append(parsed_type)
    return parsed_types


def is_method(body_element):
    return isinstance(body_element, (MethodDeclaration, ConstructorDeclaration))


def is_type(type_):
    return isinstance(type_, (ClassDeclaration, InterfaceDeclaration, EnumDeclaration))


def _collect_types(node, types):
    children = node.children
    for child in children:
        if isinstance(child, list):
            for ele in child:
                if is_type(ele):
                    types.append(ele)
                    _collect_types(ele, types)
    return types


def _parse_type(ast_type, path):
    analysed_methods = _parse_methods(ast_type)
    parsed_type = Type(path, ast_type.name, analysed_methods)
    return parsed_type


def _parse_methods(ast_type):
    methods = list(filter(is_method, ast_type.body))
    analysed_methods = [_analyse_method(method) for method in methods]
    return analysed_methods


def _analyse_method(method):
    name = method.name
    body = method.body
    complexity = comp.complexity(body) if body else 0
    comp_method = Method(name, complexity)
    return comp_method
