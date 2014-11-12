#######################################################
# This script is for reduce pakage size of ipa file
# copyright reserved xiabin
# trimpackage.py
#######################################################

import sys
import os
import re
import types

xcext = "xcodeproj"
pbxname = "project.pbxproj"

# Help
def help():
	print "Please using this script like this \"python trimpackage.py project path\""

# Check the argument
def argvcheck():
	if len(sys.argv) < 2:
		return False
	else:
		global projpath
    	projpath = sys.argv[1]
    	# Check if file exist
    	exist = os.path.exists(projpath)
    	if exist == False:
      		return False
    	else:
    		return projpath.endswith(xcext)

# Get compiled .png and source file
def getresource(pngdic,sourcedic):
	# 1.Get project file path
	pbxpath = projpath + "/" + pbxname
	# 2.Read project file
	pbxhandle = open(pbxpath,"r")

	isresblock = False
	issourceblock = False
	# 3.Get .png and source file
	for line in pbxhandle:
		if (line.find("Begin PBXResourcesBuildPhase section") == -1) and  (not isresblock) and (line.find("Begin PBXSourcesBuildPhase section") == -1) and  (not issourceblock):
			continue
		elif line.find("Begin PBXResourcesBuildPhase section") != -1:
			isresblock = True
		elif line.find("Begin PBXSourcesBuildPhase section") != -1:
			issourceblock = True
		elif line.find("End PBXResourcesBuildPhase section") != -1:
			isresblock = False
		elif line.find("End PBXSourcesBuildPhase section") != -1:
			issourceblock = False
		else:
			if isresblock: # In resource block
				pattern = re.compile(r"\*\s(.+)(?:@2x)+\.png")
				match = pattern.findall(line)
				if match:
					pngdic[match[0]] = match[0]
			if issourceblock: # In source block
				pattern = re.compile(r"\*\s(.+\.m*)")
				match = pattern.findall(line)
				if match:
					sourcedic[match[0]] = match[0]
	pbxhandle.close()

def checkinfile(filepath, pngdic):
	print "Checking file: " + filepath
	# Read source file
	filehandle = open(filepath)
	iscomment = False
	pattern = re.compile(r'.*imageNamed:@"([^@\.]*)(?:@2x)*(?:\.png)*"') # Find the source
	for line in filehandle:
        # Trim white space
		if iscomment:
			commentendpos = line.find("*/")
			if commentendpos != -1:
				iscomment = False
				# In this version, we ignore this case "...*/ your code"
		else:
			commentbeginpos = line.find("/*")
			if commentbeginpos != -1:
				iscomment = True
				continue
				# In this version, we ignore this case "your code /*..."
			commentpos = line.find("//")
			match = pattern.match(line)
			matchpos = -1
			if match:
				group = match.groups(match.lastindex)
				filename = group[0]
				matchpos = match.start(match.lastindex)
				if matchpos < commentpos or commentpos == -1: # Code not in comment
					print "find " + filename
					# Remove file name from pngdic
					if pngdic.get(filename, 0) == filename:
						pngdic.pop(filename)


def check(root, pngdic, sourcedic):
	# Travel the path
	for onepath in os.listdir(root):
		fullpath = os.path.join(root,onepath)
		if os.path.isdir(fullpath):
			if not fullpath.endswith(xcext):
				check(fullpath, pngdic, sourcedic)
		else:
			if sourcedic.get(onepath, 0) == onepath:
				checkinfile(fullpath,pngdic)
				
#######################################################
if __name__ == "__main__":
    if argvcheck() == True:
        allpngdic = {}
        allsourcedic = {}
        getresource(allpngdic,allsourcedic)
        # Travel project
        projroot = os.path.dirname(projpath)
        check(projroot, allpngdic, allsourcedic)
        print "The png files which are not compiled are list as follows:"
        for filename in allpngdic:
        	print filename
    else:
        help()


