'''
Example input:
python generate.py "asd" --name tr_@ --arg1 fixed --arg2[a] [2,3] --arg3[b] '[1.2, 1.3]'

Output:
asd --name tr_a2_b1.2 --arg1 fixed --arg2 2 --arg3 1.2
asd --name tr_a2_b 1.3 --arg1 fixed --arg2 2 --arg3  1.3
asd --name tr_a3_b1.2 --arg1 fixed --arg2 3 --arg3 1.2
asd --name tr_a3_b 1.3 --arg1 fixed --arg2 3 --arg3  1.3
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys


def generate_commands(name_k, name_v, pairs, prefix, name):
    if not pairs:
        name = '_'.join([k+v for k, v in name])
        prefix = [prefix[0]] + [name_k, name_v.replace('@', name)] + prefix[1:]
        print(' '.join(prefix))
        return
    key, value = pairs[0]
    if value.startswith('[') and value.endswith(']'):
        index = key.index('[')
        alias = key[index+1:-1]  # TODO alias for values
        key = key[:index]
        opts = value[1:-1].split(',')
        for opt in opts:
            generate_commands(name_k, name_v, pairs[1:], prefix + [key, opt], name + [(alias, opt)])
    else:
        generate_commands(name_k, name_v, pairs[1:], prefix + [key, value], name)


if __name__ == '__main__':
    script_name = sys.argv[1]
    args = sys.argv[2:]
    pairs = []
    name_k, name_v = None, None
    for i in range(0, len(args), 2):
        k = args[i]
        v = args[i+1]
        if '@' in v:  # TODO escape @
            name_k, name_v = k, v
        else:
            pairs.append([k, v])
    generate_commands(name_k, name_v, pairs, [script_name], [])
