import re

PhaseDesc = '       cccc \n   ccaaaaa  '

PhaseDesc = re.sub(r'^\s*','',PhaseDesc)
PhaseDesc = re.sub(r'(\n)(?:\s+)','\n',PhaseDesc)


print (PhaseDesc)