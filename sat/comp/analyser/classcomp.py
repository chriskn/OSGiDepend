#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

import report.plot as plot
import report.xls as xls

from app.analyser import Analyser

import comp.repo.typerepo as repo


class ClassComp(Analyser):
    @staticmethod
    def name():
        return "classes"

    def __init__(self):
        self._analysis_result = None
        self._types = None

    def load_data(self, working_dir, ignored_path_segments):
        self._types = repo.types(working_dir, ignored_path_segments)

    def analyse(self, ignored_path_segments):
        self._logger.info("Analysing Class Complexity.")
        data = []
        complexity_col = "Complexity"
        columns = ["Class", complexity_col, "Methods with complexity > 0", "Path"]
        for type_ in self._types:
            sorted_methods = sorted(
                type_.methods, key=lambda x: x.complexity, reverse=True
            )
            comp_for_methods = [
                "%s:%d" % (method.name, method.complexity)
                for method in sorted_methods
                if method.complexity > 0
            ]
            data.append(
                [type_.name, type_.complexity, ", ".join(comp_for_methods), type_.path]
            )
        class_data_frame = pd.DataFrame(data, columns=columns)
        self._analysis_result = class_data_frame.sort_values(
            complexity_col, ascending=False
        )
        return self._analysis_result

    def write_results(self, output_dir):
        xls.write_data_frame(
            self._analysis_result,
            "cognitive_complexity_per_class.xls",
            output_dir,
            "Class Complexity",
        )
        batchart_data = self._create_barchart_data()
        plot.plot_barchart(
            batchart_data,
            "Cognitive complexity",
            "Classes with highest cognitive complexity",
            output_dir,
            "most_complex_classes.pdf",
        )

    def _create_barchart_data(self):
        classes_with_comp = self._analysis_result.drop(
            columns=["Methods with complexity > 0", "Path"]
        )
        return classes_with_comp[classes_with_comp.Complexity > 0]
