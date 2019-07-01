#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Too few public methods, too many args, too many attributes
# pylint: disable=R0903,R0913,R0902


class Project:
    def __init__(self, name, location, source_packages):
        self.name = name
        self.location = location
        self.source_packages = source_packages

    def imports(self):
        imports = []
        for package in self.source_packages:
            imports.extend(package.imports())
        return imports

    def __lt__(self, other):
        return self.name < other.name


class Bundle:
    def __init__(
        self,
        path,
        name,
        version,
        exported_packages,
        imported_packages,
        required_bundles,
        num_dependencies,
    ):
        self.path = path.strip(" ")
        self.name = name.strip(" ")
        self.version = version.strip(" ")
        self.exported_packages = exported_packages
        self.imported_packages = imported_packages
        self.required_bundles = required_bundles
        self.num_dependencies = num_dependencies

    def __lt__(self, other):
        return self.name < other.name


class Package:
    def __init__(self, name, path, sourcefiles):
        self.name = name
        self.path = path
        self.sourcefiles = sourcefiles

    def imports(self):
        imports = []
        for source_file in self.sourcefiles:
            for imp in source_file.imports:
                imports.append(imp)
        return imports


class SourceFile:
    def __init__(
        self,
        name,
        language,
        imports,
        concrete_classes,
        abstract_classes,
        interfaces,
        enums,
    ):
        self.name = name
        self.language = language
        self.imports = imports
        self.concrete_classes = concrete_classes
        self.abstract_classes = abstract_classes
        self.interfaces = interfaces
        self.enums = enums

    def toplevelelements(self):
        tles = []
        tles.extend(self.concrete_classes)
        tles.extend(self.abstract_classes)
        tles.extend(self.interfaces)
        tles.extend(self.enums)
        return tles


class Interface:
    def __init__(self, name, fqn, methods, attributes, extends, modifiers):
        self.name = name
        self.fqn = fqn
        self.methods = methods
        self.attributes = attributes
        self.extends = extends
        self.modifiers = modifiers
        self.stereotype = "interface"


class Enum:
    def __init__(self, name, fqn, constants, modifiers):
        self.name = name
        self.fqn = fqn
        self.constants = constants
        self.modifiers = modifiers
        self.typename = "enum"
        self.stereotype = "enum"


class Class:
    def __init__(
        self,
        name,
        fqn,
        methods,
        attributes,
        implements,
        extends,
        modifiers,
        stereotype="",
    ):
        self.name = name
        self.fqn = fqn
        self.methods = methods
        self.attributes = attributes
        self.implements = implements
        self.extends = extends
        self.modifiers = modifiers
        self.stereotype = stereotype


class Method:
    def __init__(self, name, return_type_name, modifiers, parameters):
        self.name = name
        self.return_type_name = return_type_name
        self.modifiers = modifiers
        self.parameters = parameters


class Declaration:
    def __init__(self, name, type_name, modifiers):
        self.name = name
        self.typename = type_name
        self.modifiers = modifiers
