#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=E0401

from sat.changes.analyser.filechanges import FileChanges
from sat.changes.analyser.packagechanges import PackageChanges
from sat.changes.analyser.projectchanges import ProjectChanges
from sat.comp.analyser.classcomp import ClassComp
from sat.comp.analyser.methodcomp import MethodComp
from sat.comp.analyser.packagecomp import PackageComp
from sat.comp.analyser.projectcomp import ProjectComp
from sat.deps.analyser.bundleanalyser import BundleAnalyser
from sat.deps.analyser.plainjavaanalyser import PlainJavaAnalyser

_DEPS_ANALYSER_CLASSES = [PlainJavaAnalyser, BundleAnalyser]
_CHANGE_ANALYSER_CLASSES = [FileChanges, PackageChanges, ProjectChanges]
_COMP_ANALYSER_CLASSES = [MethodComp, ClassComp, PackageComp, ProjectComp]

_DEPS_ANALYSER_CLS_BY_NAME = {
    analyser.name(): analyser for analyser in _DEPS_ANALYSER_CLASSES
}
_CHANGE_ANALYSER_CLS_BY_NAME = {
    analyser.name(): analyser for analyser in _CHANGE_ANALYSER_CLASSES
}
_COMP_ANALYSER_CLS_BY_NAME = {
    analyser.name(): analyser for analyser in _COMP_ANALYSER_CLASSES
}


class AnalyserRepo:
    @staticmethod
    def deps_analyser_classes_by_name():
        return _DEPS_ANALYSER_CLS_BY_NAME

    @staticmethod
    def change_analyser_classes_by_name():
        return _CHANGE_ANALYSER_CLS_BY_NAME

    @staticmethod
    def comp_analyser_classes_by_name():
        return _COMP_ANALYSER_CLS_BY_NAME
