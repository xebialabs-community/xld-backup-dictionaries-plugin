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
import com.xebialabs.deployit.plugin.api.reflect.Type as Type

working_directory=deployedApplication.environment.backupDictionariesDirectory
if not repositoryService.exists(working_directory):
    raise Exception("{0} doesn't exist, please create it and re-run the step again".format(working_directory))
target_directory = repositoryService.read(working_directory)
task_id = context.getTask().getId()
print ("task_id {0}".format(task_id))
new_folder = "{0}/{1}".format(target_directory,task_id)
if repositoryService.exists(new_folder):
    repositoryService.delete(new_folder)


type = Type.valueOf('core.Directory')
configuration_item = type.descriptor.newInstance(new_folder)
print ("create new folder {0}".format(configuration_item))
repositoryService.create([configuration_item])

for d in dictionaries:
    dict_name = d.name
    new_id = "{0}/{1}".format(new_folder,d.name)
    print ("Backup {0} -> {1}".format(d.id,new_id))
    new_dictionary = repositoryService.copy(d.id,new_id)




