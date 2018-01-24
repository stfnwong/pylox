"""
GENERATEAST
Generate a Lox AST

Stefan Wong 2018
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time

# Format here is 'type' : [args]


class GenerateAST(object):

    def __init__(self, output_dir, verbose=False):
        self.output_dir = output_dir
        self.ast_types = {
            'Binary'   : ['left', 'op', 'right'],
            'Grouping' : ['expression'],
            'Literal'  : ['value'],
            'Unary'    : ['op', 'right']
        }

        self._define_ast(self.output_dir, "Expr", self.ast_types.keys())
        # Debug
        self.verbose = verbose

    def __str__(self):
        s = []
        s.append('Output dir : %s' % self.output_dir)

        return ''.join(s)

    def _define_type(self, basename, classname, field_list):
        if type(field_list) is not list:
            raise ValueError('field_list must be a list')

        s = []
        s.append('class %s(%s):\n' % (classname, basename))
        s.append('\tdef ___init__(self')
        for f in field_list:
            s.append(', %s' % str(f))
        s.append('):\n')
        # assign args to internal data members
        for f in field_list:
            s.append('\t\tself.%s = %s\n' % (str(f), str(f)))
        s.append('\n\n')

        # Add __str__, __repr__

        return ''.join(s)

    def _define_ast(self, output_dir, basename, types_list):
        time.ctime()
        cur_time = time.strftime('%l:%M%p %Z on %b %d %Y')
        path = '%s/%s.py' % (output_dir, basename)

        # Print the content of the python file
        s = []
        s.append('"""\n')
        s.append('Abstract class %s\n' % str(basename))
        s.append('Generated automatically at %s\n' % str(cur_time))
        s.append('"""\n')

        # The AST classes
        for t in types_list:
            classname = t
            s.append(self._define_type(basename, t, self.ast_types[t]))

        text = ''.join(s)
        # Write out the string to dist
        with open(path, 'w') as fp:
            fp.write(text)
            #for line in s:
            #    fp.write(line)

    def main(self):
        self._define_ast(self.output_dir, "Expr", self.ast_types.keys())

