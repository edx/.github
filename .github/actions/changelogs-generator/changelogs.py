"""
Script to generate a changelogs, convert to rst format and append in CHANGELOG.rst
"""

import re
import subprocess
import sys
from datetime import date
import fileinput
import pypandoc

# Save new changelogs in temp.md
changelogs_cmd = "semantic-release changelog"
output = subprocess.check_output(changelogs_cmd.split())
output = "## [" + sys.argv[1] + "] - " + str(date.today()) + "\n"+output.decode("utf-8")

with open('temp.md', 'w') as file:
    file.write(output)

# Convert the changelogs to rst
#pandoc_cmd = "pandoc temp.md -f markdown_strict -t rst -o temp.rst"
#output = subprocess.check_output(pandoc_cmd.split())
output = pypandoc.convert_file('temp.md', 'rst', outputfile='temp.rst')

with open('temp.rst') as f:
    changelogs = f.readlines()

for line_num, line in enumerate(changelogs):
    obj = re.search(r'``[a-zA-Z0-9]{7}``',  line)
    if obj:
        changelogs[line_num] = re.sub(r'``[a-zA-Z0-9]{7}``', obj.group().split('`')[2], line)
changelogs = "".join(changelogs)


# append the changelogs in CHANGELOG.rst
for line in fileinput.FileInput("CHANGELOG.rst", inplace=True):
    if line.startswith(".. <New logs>"):
        line = line.replace(line, line+"\n"+changelogs)
        print(line)
    else:
        print(line.rstrip('\n'))
