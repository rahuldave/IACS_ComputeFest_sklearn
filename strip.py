from collections import OrderedDict

import json
import os

def strip_answers(infile):
    with open(infile) as fd:
        data = json.load(fd)
    n_strip = 0
    strip_ct = 0
    print data.keys()
    for k,cell in enumerate(data['cells']):
        print cell['cell_type']
        cell=data['cells'][k]
        if cell['cell_type']=='code':
            for i in range(len(cell['source'])):
                if 'your code here' in cell['source'][i].lower():
                    n_strip += len(cell['source']) - i
                    strip_ct += 1
                    cell['source'] = cell['source'][:i+1]
                    break
                if 'your alternate code here' in cell['source'][i].lower():
                    data['cells'][k]="BLA"
                    break
            if 'no_strip' not in cell['metadata']:
                cell['outputs'] = []
        elif cell['cell_type']=='markdown':
            for i in range(len(cell['source'])):
                if '*your answer here*' in cell['source'][i].lower():
                    n_strip += len(cell['source']) - i
                    strip_ct += 1
                    cell['source'] = cell['source'][:i+1]
                    break
                if '*your alternate answer here*' in cell['source'][i].lower():
                    data['cells'][k]="BLA"
                    break
        else:
            continue

    data['cells']=[e for e in data['cells'] if e != 'BLA']
    print "%s: Strip %i cells, %i lines" % (infile, strip_ct, n_strip)

    result = OrderedDict()
    for k in ['metadata', 'nbformat', 'nbformat_minor', 'cells']:
        result[k] = data[k]
    with open("distribute_"+infile, 'w') as outfile:
        json.dump(result, outfile, indent=2)


if __name__ == '__main__':
    import sys
    doc=sys.argv[1]
    strip_answers(doc)
