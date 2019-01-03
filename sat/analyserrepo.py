#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.bundleanalysis import BundleAnalyser
from analysis.projectanalysis import ProjectAnalyser
from analysis.plainjavaanalysis import PlainJavaAnalyser
from git.filechanges import FileChanges
from git.packagechanges import PackageChanges
from git.projectchanges import ProjectChanges
from comp.methodcomp import MethodComp
from comp.classcomp import ClassComp


_DEPS_ANALYSER_CLASSES = [PlainJavaAnalyser, ProjectAnalyser, BundleAnalyser]
_CHANGE_ANALYSER_CLASSES = [FileChanges, PackageChanges, ProjectChanges]
_COMP_ANALYSER_CLASSES = [MethodComp, ClassComp]

_DEPS_ANALYSER_CLS_BY_NAME = {
    analyser.name(): analyser for analyser in _DEPS_ANALYSER_CLASSES}
_CHANGE_ANALYSER_CLS_BY_NAME = {
    analyser.name(): analyser for analyser in _CHANGE_ANALYSER_CLASSES}
_COMP_ANALYSER_CLS_BY_NAME = {
    analyser.name(): analyser for analyser in _COMP_ANALYSER_CLASSES}


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
