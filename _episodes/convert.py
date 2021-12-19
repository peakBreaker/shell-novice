#!/usr/bin/env python

import re

BASE='''
---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---


'''



def convert(filename='00-test.md', output_filename='out/test.md'):
    with open(output_filename, 'w') as writefile:
        writefile.write(BASE)
        record_code = False
        recorded_code = []
        recorded_text = []
        toskip = 0
        reset_code = False
        cell_type=''

        with open(filename) as f:
            for line in f:
                # clean the line and skip empty lines
                line = line.strip()
                if line == '':
                    continue
                #print(line)
                # Find the begin and end flag
                if re.match('.*~~~', line):
                    if record_code:
                        toskip = 2
                    else: # reached a new flag
                        record_code = True
                        toskip = 0 # reset_code skipping if it reaches a new anchor flag 
                        reset_code = True
                
                # handle trailing lines
                if toskip != 0:
                    toskip -= 1
                    record_code = False if toskip == 0 else record_code

                # if we get a reset_code we reset_code before we record_code
                if reset_code:
                    writefile.write('\n'.join(['```'+cell_type, *recorded_code, '```']))
                    writefile.write('\n\n')
                    recorded_code = []
                    cell_type = ''
                    reset_code = False

                # Finally record_code the data
                if record_code:
                    if not re.match('.*~~~', line):
                        recorded_code.append(line)

                    # dump the text if we have any text in memory
                    if len(recorded_text) > 0:
                        writefile.write('\n'.join(recorded_text))
                        writefile.write('\n\n')
                        recorded_text = []    
                else:
                    if not re.match('.*~~~', line):
                        recorded_text.append(line)
                
                if "{: .language-bash}" in line:
                    cell_type = 'bash'
                    reset_code = True


def main():
    import os
    for filename in os.listdir('.'):
        if '.md' in filename:
            out_filename = f'out/{filename}'
            convert(filename, out_filename)
            import jupytext
            notebook = jupytext.read(out_filename)
            jupytext.write(notebook, f'notebooks/{filename[:-2]}ipynb', fmt='notebook')

if __name__ == '__main__':
    main()