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
    """
    Class to generate source files for AST objects
    """
    def __init__(self, output_dir, verbose=False):
        self.output_dir = output_dir
        self.ast_types = {
            'Binary'   : ['left', 'op', 'right'],
            'Grouping' : ['expression'],
            'Literal'  : ['value'],
            'Unary'    : ['op', 'right']
        }

        #self._define_ast(self.output_dir, "Expr", self.ast_types.keys())
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
        if 'op' in field_list:
            s.append('\t\tif type(op) is not Token.Token:\n')
            s.append('\t\t\traise ValueError("op must be a token")\n')
        for f in field_list:
            s.append('\t\tself.%s = %s\n' % (str(f), str(f)))
        s.append('\n')

        # Add __str__
        s.append('\tdef __str__(self):\n')
        s.append('\t\ts = []\n')
        s.append('\t\ts.append("')
        for n in range(len(field_list)):
            if n == len(field_list) - 1:
                s.append('%s\\n')
            else:
                s.append('%s, ')
        s.append('" % (')
        for n, f in enumerate(field_list):
            if n == len(field_list) - 1:
                s.append('str(self.%s)' % str(f))
            else:
                s.append('str(self.%s), ' % str(f))
        s.append('))\n\n')
        s.append('\t\treturn "".join(s)\n\n')
        # Add __repr__
        s.append('\tdef __repr__(self):\n')
        s.append('\t\treturn self.__str__()\n')
        s.append('\n')
        # Add __eq__
        s.append('\tdef __eq__(self, other):\n')
        s.append('\t\treturn self.__dict__ == other.__dict__\n')
        s.append('\n')

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
        s.append('\n')
        # Modules
        s.append('import os\n')
        s.append('import sys\n')
        s.append('sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))\n')
        s.append('\n')
        s.append('from loxpy import Token\n')
        s.append('\n\n')

        # Base class
        s.append('class %s(object):\n' % str(basename))
        s.append('\tpass\n')
        s.append('\n\n')

        # The AST classes
        for t in types_list:
            classname = t
            s.append(self._define_type(basename, t, self.ast_types[t]))
            s.append('\n')

        text = ''.join(s)
        # Write out the string to dist
        with open(path, 'w') as fp:
            fp.write(text)

    def main(self):
        self._define_ast(self.output_dir, "Expression", self.ast_types.keys())

