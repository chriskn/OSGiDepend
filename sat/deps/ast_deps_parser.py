#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from javalang.tree import (
    ClassDeclaration,
    ConstructorDeclaration,
    EnumDeclaration,
    FieldDeclaration,
    InterfaceDeclaration,
    MethodDeclaration,
)

from sat.deps.domain import Class, Declaration, Enum, Interface, Method, SourceFile

_LOGGER = logging.getLogger("Java Deps Parser")


def parse_java_sourcefile(sourcefile):
    packagename = sourcefile.packagename
    package_imports = {imp.path for imp in getattr(sourcefile.ast, "imports")}
    types = getattr(sourcefile.ast, "types")
    concrete_classes = [
        parse_class(type, packagename)
        for type in types
        if isinstance(type, ClassDeclaration) and "abstract" not in type.modifiers
    ]
    abstract_classes = [
        parse_class(type, packagename, "abstract")
        for type in types
        if isinstance(type, ClassDeclaration) and "abstract" in type.modifiers
    ]
    interfaces = [
        parse_interface(type, packagename)
        for type in types
        if isinstance(type, InterfaceDeclaration)
    ]
    enums = [
        parse_enum(type, packagename)
        for type in types
        if isinstance(type, EnumDeclaration)
    ]
    return SourceFile(
        sourcefile.abs_path,
        sourcefile.rel_path,
        sourcefile.name,
        package_imports,
        concrete_classes,
        abstract_classes,
        interfaces,
        enums,
    )


def parse_enum(enum, packagename=""):
    name = enum.name
    constants = [constant.name for constant in enum.body.constants]
    modifiers = enum.modifiers
    return Enum(name, _fqn(packagename, name), constants, modifiers)


def parse_interface(interface, packagename=""):
    name = interface.name
    extends = (
        [interface.name for interface in interface.extends] if interface.extends else ""
    )
    modifiers = interface.modifiers
    attributes = [
        _parse_attribute(attribute) for attribute in _filter_attributes(interface.body)
    ]
    methods = [_parse_method(methode) for methode in _filter_methods(interface.body)]
    fqn = _fqn(packagename, name)
    return Interface(name, fqn, methods, attributes, extends, modifiers)


def parse_class(clazz, packagename="", stereotype=""):
    modifiers = clazz.modifiers
    implements = [impl.name for impl in clazz.implements] if clazz.implements else []
    extends = clazz.extends.name if clazz.extends else ""
    name = clazz.name
    attributes = [
        _parse_attribute(attribute) for attribute in _filter_attributes(clazz.body)
    ]
    methods = [_parse_method(methode) for methode in _filter_methods(clazz.body)]
    return Class(
        name,
        _fqn(packagename, name),
        methods,
        attributes,
        implements,
        extends,
        modifiers,
        stereotype,
    )


def _fqn(packagename, name):
    if packagename:
        return packagename + "." + name
    return name


def _filter_methods(body):
    return list(
        filter(
            lambda type: isinstance(
                type, ((ConstructorDeclaration, MethodDeclaration))
            ),
            body,
        )
    )


def _filter_attributes(body):
    return list(
        filter(
            lambda type: isinstance(type, ((FieldDeclaration, EnumDeclaration))), body
        )
    )


def _parse_attribute(attribute):
    if isinstance(attribute, EnumDeclaration):
        return parse_enum(attribute)
    type_name = attribute.type.name
    name = attribute.declarators[0].name
    modifiers = attribute.modifiers
    return Declaration(name, type_name, modifiers)


def _parse_method(method):
    modifiers = method.modifiers
    name = method.name
    return_type = ""
    if isinstance(method, MethodDeclaration):
        return_type = method.return_type.name if method.return_type else ""
    parameter = [_parse_parameter(param) for param in method.parameters]
    return Method(name, return_type, modifiers, parameter)


def _parse_parameter(param):
    modifiers = param.modifiers
    name = param.name
    type_name = param.type.name
    return Declaration(name, type_name, modifiers)
