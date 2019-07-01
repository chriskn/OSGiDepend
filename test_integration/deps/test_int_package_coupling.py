#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sat.__main__ as main
import unittest
import sat.deps.parser.projectparser as parser

import sat.deps.coupling as sut

_ROOT_LOCATION = os.path.dirname(os.path.dirname(os.path.abspath(main.__file__)))
EXAMPLE_PROJECTS_LOCATION = os.path.join(_ROOT_LOCATION, "exampleprojects")


class TestPackageCoupling(unittest.TestCase):
    def setUp(self):
        projects = parser.parse(EXAMPLE_PROJECTS_LOCATION, [])
        self.packages = []
        for proj in projects:
            self.packages.extend(proj.source_packages)
        self.expected_index = [
            "my.dummy.project5.domain",
            "my.dummy.project5.domain",
            "my.dummy.project4.impl",
            "my.dummy.project4.api",
            "my.dummy.project3.impl",
            "my.dummy.project2.impl",
            "my.dummy.project2.api",
            "my.dummy.project1.impl",
            "my.dummy.project1.api",
        ]

    def test_package_coupling_dataframe_has_expected_index(self):
        dataframe = sut.package_coupling_dataframe(self.packages)

        self.assertListEqual(list(dataframe.index.values), self.expected_index)

    def test_package_coupling_dataframe_has_expected_columns(self):
        dataframe = sut.package_coupling_dataframe(self.packages)

        self.assertListEqual(list(dataframe.columns.values), self.expected_index[::-1])

    def test_package_coupling_dataframe_has_expected_values(self):
        dataframe = sut.package_coupling_dataframe(self.packages)

        self.assertListEqual(
            dataframe.values.tolist(),
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0],
                [2, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 0, 0, 0],
            ],
        )
