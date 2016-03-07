# ######################################################
# The MIT License (MIT)
#
# Copyright (c) 2014-2016 BinXia wuwen.xb@alibaba-inc.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#######################################################

import sys
import os
import re

############################# UnusedImageFinder ##############################


class UnusedImageFinder:

    """Use me to find the unused images in an Xcode project."""

    def __init__(self, projectPath, sourceFilePath=""):
        self.xcProjectExt = "xcodeproj"
        self.projectPath = projectPath
        if len(sourceFilePath) == 0:
            # Default source file path is current path
            self.sourceFilePath = os.path.dirname(self.projectPath)
        else:
            self.sourceFilePath = sourceFilePath
        self.pbxFilePath = os.path.join(self.projectPath, "project.pbxproj")
        self.imageFiles = {}
        self.codeFiles = {}
        self.imageRefPatterns = []

    def validateProject(self):
        fileExist = os.path.exists(self.projectPath)
        if not fileExist:
            return False
        return self.projectPath.endswith(self.xcProjectExt)

    def findCodeSources(self):
        pattern = re.compile(r".*\s(.+\.m+).*")
        pbxFileHandle = open(self.pbxFilePath, "r")
        isCodeSourceBlock = False
        isCodeSourceDone = False

        # Traverse the "project.pbxproj" file
        # "Begin PBXResourcesBuildPhase section" is first line of resources block
        # "Begin PBXSourcesBuildPhase section" is first line of sources block
        for line in pbxFileHandle.readlines():
            isCodeSourceBegin = (line.find("Begin PBXSourcesBuildPhase section") != -1)
            isCodeSourceEnd = (line.find("End PBXSourcesBuildPhase section") != -1)

            if (isCodeSourceDone):
                break
            elif isCodeSourceBegin:
                isCodeSourceBlock = True
            elif isCodeSourceEnd:
                isCodeSourceBlock = False
                isCodeSourceDone = True
            else:
                # Code source block
                if isCodeSourceBlock:
                    match = re.match(pattern, line)
                    if match:
                        self.codeFiles[match.groups()[0]] = match.groups()[0]

    def findImageResourceInPath(self, path):
        pattern = re.compile(r"(.+?)(@\dx)*(\.png|\.jpg)")
        for subPathName in os.listdir(path):
            subPath = os.path.join(path, subPathName)
            if os.path.isdir(subPath):
                    if not subPath.endswith(self.xcProjectExt):
                        self.findImageResourceInPath(subPath)
            else:
                match = re.match(pattern, subPathName)
                if match:
                    self.imageFiles[match.groups()[0]] = subPath

    def findImageRefInPath(self, path):
        for subPathName in os.listdir(path):
            subPath = os.path.join(path, subPathName)
            if os.path.isdir(subPath):
                if not subPath.endswith(self.xcProjectExt):
                    self.findImageRefInPath(subPath)
            else:
                if self.codeFiles.get(subPathName, 0) == subPathName:
                    self.findImageRefInFile(subPath)

    def findImageRefInFile(self, filePath):
        if not os.path.exists(filePath):
            return
        print "Checking [%s] ..." % filePath

        fileHandle = open(filePath, "r")
        isComment = False

        for line in fileHandle.readlines():
            # Trim the white space
            if isComment:
                if line.find("*/") != -1:
                    isComment = False
                    # For now, we cann't deal with case like this " ...*/ YOUR CODE"
            else:
                isCommentBegin = (line.find("/*") != -1)
                if isCommentBegin:
                    isComment = True
                    # For now, we cann't deal with case like this " YOUR CODE /*... "
                    continue
                commentIndex = line.find("//")
                # Comment at begin of line
                if commentIndex == 0:
                    continue

                fileName = ""
                for pattern in self.imageRefPatterns:
                    match = re.match(pattern, line)
                    if match:
                        fileName = match.groups()[0]
                        break
                if len(fileName) == 0:
                    continue

                matchIndex = line.find(fileName)

                # Code not in comment
                if matchIndex < commentIndex or commentIndex == -1:
                    if self.imageFiles.get(fileName, 0) == fileName:
                        self.imageFiles.pop(fileName)

    def run(self):
        if not self.validateProject():
            showHelp()
            return
        if len(self.imageRefPatterns) == 0:
            print "Please set valid match patterns!"
            return

        print "Checking project:[%s], source path:[%s]" % (self.projectPath, self.sourceFilePath)
        # Find build code source files
        self.findCodeSources()
        # Find all image resource files
        self.findImageResourceInPath(self.sourceFilePath)
        # Traverse from source path
        self.findImageRefInPath(self.sourceFilePath)
        # Output results
        outputFilePath = os.path.join("result.txt")
        if os.path.exists(outputFilePath):
            os.remove(outputFilePath)
        with open(outputFilePath, "a") as f:
            for key in self.imageFiles:
                f.write(key + "\t" + self.imageFiles[key] + "\n")
        print "Done! Result has been written to %s" % outputFilePath


############################# Static ##############################


def showHelp():
    print "Please using this script like this \"python unused_images_finder.py PROJECT_PATH {SOURCE_PATH}\""


imageReferencePatterns = [re.compile(r".*imageNamed:@\"(.+?)(@\dx)*(\.png|\.jpg)*\".*")]

############################# main ##############################
if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        showHelp()
    else:
        if len(args) >= 3:
            finder = UnusedImageFinder(args[1], args[2])
        else:
            finder = UnusedImageFinder(args[1])
        finder.imageRefPatterns = imageReferencePatterns
        finder.run()