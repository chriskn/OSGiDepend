# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import os
# import unittest

# import mock

# import sat.comp.repo.projectrepo as sut
# from sat.comp.domain import Package


# class TestProjectRepo(unittest.TestCase):
#     def tearDown(self):
#         # pylint: disable = W0212
#         sut._projects = dict()

#     @mock.patch("sat.comp.parser.projectparser.parse_projects")
#     def test_projects_not_calls_parse_projects_twice_for_same_input(
#         self, parse_projects
#     ):
#         workingdir = "dir"
#         ignored = ["bar", "", "foo"]
#         sut.projects(workingdir, ignored)
#         sut.projects(workingdir, ignored)
#         self.assertEqual(parse_projects.call_count, 1)

#     @mock.patch("sat.comp.parser.projectparser.parse_projects")
#     def test_projects_calls_parse_projects_depending_on_dir_and_ignored(
#         self, parse_projects
#     ):
#         workingdir = "foo"
#         ignored = ["bar", "", "foo"]
#         sut.projects(workingdir, ignored)
#         # duplicate
#         sut.projects(workingdir, ignored)
#         sut.projects(workingdir, ignored + ["another"])
#         sut.projects(workingdir + "another", ignored)
#         self.assertEqual(parse_projects.call_count, 3)

#     @mock.patch("sat.comp.parser.projectparser.parse_projects")
#     def test_projects_calls_parse_projects(self, parse_projects):
#         sut.projects("someworkingdir", "")
#         self.assertEqual(parse_projects.call_count, 1)

#     @mock.patch("sat.app.workspace.scanner.find_projects", return_value=dict())
#     def test_scanner_is_called_with_expected_params(self, scanner):
#         # disabled not self use. test must be checked anyway
#         # pylint: disable = R0201
#         workingdir = "test"
#         ignored = ["bar"]
#         sut.projects(workingdir, ignored)
#         # self.assertEqual(scanner.call_count, 1)
#         scanner.assert_called_with(workingdir, ignored)

#     @mock.patch("sat.comp.parser.typeparser.parse")
#     def test_parser_is_not_called_if_no_file_found(self, parser):
#         sut.projects("", "")
#         self.assertEqual(parser.call_count, 0)

#     @mock.patch("sat.app.workspace.scanner.find_projects")
#     @mock.patch("sat.comp.repo.packagerepo.packages")
#     def test_parser_creates_expected_projects(self, packagerepo, scanner):
#         scanner_result = {
#             "foo//bar//proj1//a1/b1//": "a1" + os.sep + "b1",
#             # single slash after proj2 is by intention
#             "bar//proj2/a2//": "a2",
#             "proj3//a2//": "a2",
#         }
#         packages = [
#             Package("foo//bar//proj1//a1/b1//package1", "package1", []),
#             Package("bar//proj2/a2//package2", "package2", []),
#             Package("proj3//a2//package3", "package3", []),
#         ]

#         scanner.return_value = scanner_result
#         packagerepo.return_value = packages

#         projects = sut.projects("", "")

#         self.assertEqual(len(projects), 3)
#         project1 = projects[0]
#         project2 = projects[1]
#         project3 = projects[2]
#         self._assert_project(project1, "foo//bar//proj1//a1/b1//", "a1.b1", packages[0])
#         self._assert_project(project2, "bar//proj2/a2//", "a2", packages[1])
#         self._assert_project(project3, "proj3//a2//", "a2", packages[2])
#         print(projects)

#     def _assert_project(self, project, exp_path, exp_name, exp_package):
#         self.assertEqual(project.path, exp_path)
#         self.assertEqual(project.name, exp_name)
#         self.assertEqual(project.packages[0], exp_package)
