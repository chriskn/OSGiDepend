#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
import sat.__main__ as main

_CUR_DIR = os.path.dirname(os.path.abspath(__file__))
_TEST_RESULTS_FOLDER = os.path.join(_CUR_DIR, "test_results")
_ROOT_LOCATION = os.path.dirname(os.path.dirname(os.path.abspath(main.__file__)))

REF_DATA_FOLDER = os.path.join(_CUR_DIR, "test_data")
EXAMPLE_PROJECTS_LOCATION = os.path.join(_ROOT_LOCATION, "exampleprojects")


def write_test_graph(sut, filename):
    graph_file = os.path.join(_TEST_RESULTS_FOLDER, filename)
    os.makedirs(_TEST_RESULTS_FOLDER, exist_ok=True)
    test_graph_file = open(graph_file, "w", encoding="utf-8")
    test_graph_file.write(sut.serialize())
    test_graph_file.close()


def encrypt(to_encrypt):
    "Files are too big to compare them. Compare md5 hashs instead"
    md5 = hashlib.md5()
    enc = to_encrypt.encode("utf-8")
    md5.update(enc)
    return md5.hexdigest()
