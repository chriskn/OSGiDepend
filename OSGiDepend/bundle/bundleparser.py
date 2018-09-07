#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bundle.bundle import Bundle
import os,re

class BundleParser:
    
    def __init__(self, directory, ignoredPathSegments):
        self.directory = directory
        self.ignoredPathSegments = ignoredPathSegments

    def parseBundles(self):
        bundlePaths = self.__scanForBundles()
        bundles = [self.__parseBundle(bundle) for bundle in bundlePaths]
        return bundles

    def __scanForBundles(self):
        bundels = set()
        for dirpath, dirNames, files in os.walk(self.directory):
            ignored = any(ignoredSegment in dirpath for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                for file in files:
                    if file == "MANIFEST.MF": 
                        bundels.add(os.path.dirname(dirpath))
        return bundels

    def __parseBundle(self,bundlePath):
        manifestPath = bundlePath + "/META-INF/MANIFEST.MF"
        symbolicName, version, exportedPackages, importedPackages, requiredBundles = self.__parseManifest(manifestPath)
        numberOfDependencies = len(requiredBundles)+len(importedPackages)
        bundle = Bundle(bundlePath, symbolicName, version, exportedPackages, importedPackages, requiredBundles, numberOfDependencies)
        return bundle

    def __parseManifest(self,manifestPath):
        manifestContent = open(manifestPath, 'rb').read().decode()
        entries = re.split(r'[\r\n]+(?!\s)',manifestContent)
        requiredBundles = []
        importedPackages = []
        exportedPackages = []
        version = ""
        symbolicName = ""
        for entry in entries: 
            if entry.startswith("Require-Bundle:"):
                requiredBundles = [self.__trim(bundle) for bundle in self.__splitEntries(entry,"Require-Bundle:")]
            elif entry.startswith("Import-Package:"):
                importedPackages = [self.__trim(package) for package in self.__splitEntries(entry,"Import-Package:")]
            elif entry.startswith("Export-Package:"):
                # removes 'uses' declaration
                if ';' in entry: entry = entry[:entry.index(';')]
                exportedPackages = [self.__trim(package) for package in self.__splitEntries(entry,"Export-Package:")]
            elif entry.startswith("Bundle-Version:"):
                version = self.__trim(entry.replace("Bundle-Version:", ""))
            elif entry.startswith("Bundle-SymbolicName:"):
                symbolicName = self.__trim(entry.replace("Bundle-SymbolicName:", ""))
                if ";" in symbolicName:
                    symbolicName = symbolicName[:symbolicName.index(";")]
        # remove additional information (ie. bundle-version)
        requiredBundles[:] = [requiredBundle[:requiredBundle.index(";")]  if ";" in requiredBundle else requiredBundle for requiredBundle in requiredBundles]
        return symbolicName, version, exportedPackages, importedPackages, requiredBundles

    def __trim(self, str):
        return str.replace("\n","").replace("\r","").strip(" ")

    def __splitEntries(self, entry, entryName):
        return re.split(r",(?!\d)", entry.replace(entryName, ""))