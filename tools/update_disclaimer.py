# Update disclaimer as the same format as LICENSE

import textwrap

disclaimer_path = '../DISCLAIMER.md'
wrapper = textwrap.TextWrapper(width=80)

with open(disclaimer_path, 'r') as f:
    text = f.read()

paragraphs = text.split('\n\n')
output = ""
for para in paragraphs:
    word_list = wrapper.wrap(text=para)
    for element in word_list:
        output += element
        output += "\n"
    output += "\n"
output = output[:-1]

assert(output != "")
with open(disclaimer_path, 'w') as f:
    f.write(output)