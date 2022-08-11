import re
# RE to remove urls
reUrl = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)

# RE to remove tags & css
reTags = re.compile(r'{\|(.*?)\|}',re.DOTALL)

# Regular Expression to remove {{cite **}} or {{vcite **}}
reCite = re.compile(r'{{v?cite(.*?)}}',re.DOTALL)

# Regular Expression to remove [[file:]]
reFile = re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL)

# pattern to get only alphnumeric text
reText = re.compile("[^a-zA-Z0-9]")