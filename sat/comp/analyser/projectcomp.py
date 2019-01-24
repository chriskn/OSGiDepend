#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import OrderedDict

import pandas as pd

import comp.repo.projectrepo as prepo
import comp.repo.typerepo as repo
import report.plot as plot
import report.xls as xls
import scanner
from app.analyser import Analyser
from comp.domain import Method, Type

_COLUMNS = ["Project", "Complexity", "Path"]

class ProjectComp(Analyser):

    @staticmethod
    def name():
        return "projects"

    def load_data(self, workingdir, ignored_path_segments):
        self._projects = prepo.projects(workingdir, ignored_path_segments) 

    def analyse(self, ignoredPathSegments):
        self._logger.info("Analysing Project Complexity.")
        data = []
        for project in self._projects:
            data.append((project.name, project.complexity, project.path))
        df = pd.DataFrame(data, columns=_COLUMNS)
        self._df = df.sort_values(_COLUMNS[1], ascending=False)
        return self._df

    def write_results(self, outputdir):
        xls.write_data_frame(self._df, "cognitive_complexity_per_project.xls", outputdir, "Project Complexity")
        tm_data = self._create_treemap_data()
        plot.plot_treemap(tm_data, "Cognitive complexity per project", outputdir,
                              "cognitive_complexity_per_project.pdf", "complexity:")
    
   
    def _create_treemap_data(self):
        tm_data = self._df.drop(columns=["Path"])
        return tm_data[tm_data.Complexity > 0]