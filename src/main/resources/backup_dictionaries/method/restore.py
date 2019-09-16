#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same

#print "THIS %s" % thisCi
deployedApplication = repositoryService.read(thisCi.id)
print deployedApplication

task_info = taskService.getSteps(params.taskId)
print task_info.metadata
metadata = task_info.metadata

environment = repositoryService.read(deployedApplication.environment.id)
print "Environment %s" % environment
if not environment.id == metadata['environment_id']:
    raise Exception("The environment doesn't match '{0}' vs '{1}'".format(str(environment.id), metadata['environment_id']))

version = repositoryService.read(deployedApplication.version.id)
print "Version %s" % version
if not version.name == metadata['version']:
    raise Exception("The versionapplication doesn't match '{0}' vs '{1}'".format(version.name, metadata['version']))


application = repositoryService.read(str(version.application))
print "Application %s" % application

if not application.name == metadata['application']:
    raise Exception("The application doesn't match '{0}' vs '{1}'".format(application.name, metadata['application']))


print "Dictionaries %s "% environment.dictionaries
current_dictionaries = {}
for ci in environment.dictionaries:
    current_dictionaries[ci.name]=ci

print current_dictionaries



p="{0}/{1}".format(environment.backupDictionariesDirectory,params.taskId)
if not repositoryService.exists(p):
    raise Exception("The dictionaries associated with the deployment tasks {0} doesn't exist in {1}".format(params.taskId, environment.backupDictionariesDirectory))

result = repositoryService.query(None, p, None,'',None, None,0, -1)
for r in result:
    print r
    ci = repositoryService.read(r.id)
    print ci.name
    if ci.name in current_dictionaries:
        current_dict = repositoryService.read(current_dictionaries[ci.name].id)
        print "* Update {0} with its backup {1}".format(current_dict.id,ci)
        #print "current values {0}".format(current_dict.entries)
        #print "backup  values {0}".format(ci.entries)
        added, removed, modified, same = dict_compare(current_dict.entries, ci.entries)
        if len(added)>0 or len(removed) > 0 or len(modified) > 0:
            print "The dictionary entries have been modified,overide the current entries with the entries of the backup"
            print "added:    {0}".format(added)
            print "removed:  {0}".format(removed)
            print "modified: {0}".format(modified)
            current_dict.entries = ci.entries
            repositoryService.update(current_dict.id, current_dict)
        else:
            print "No modification in the entries, skip the update"

