"""
ASTGENERATE
Generate a Lox AST

Stefan Wong 2018
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time

# Format here is 'type' : [args]

class ASTGenerate(object):
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
        s.append('    def __init__(self')
        for f in field_list:
            s.append(', %s' % str(f))
        s.append('):\n')
        # assign args to internal data members
        if 'op' in field_list:
            s.append('        if type(op) is not Token.Token:\n')
            s.append('            raise ValueError("op must be a token")\n')
        for f in field_list:
            s.append('        self.%s = %s\n' % (str(f), str(f)))
        s.append('\n')

        # Add __str__
        s.append('    def __str__(self):\n')
        s.append('        s = []\n')
        s.append('        s.append("')
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
        s.append('        return "".join(s)\n\n')
        # Add __repr__
        s.append('    def __repr__(self):\n')
        s.append('        return self.__str__()\n')
        s.append('\n')
        # Add __eq__
        s.append('    def __eq__(self, other):\n')
        s.append('        return self.__dict__ == other.__dict__\n')
        s.append('\n')
        # Add accept method
        s.append('    def accept(self, visitor):\n')
        s.append('        visitor.visit(self)\n')
        s.append('\n')

        return ''.join(s)

    def _define_ast(self, output_dir, basename, types_list):    # TODO : rename?
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
        s.append('    def accept(self, visitor):\n')
        s.append('        raise NotImplementedError("This method should be called on dervied classes")\n')
        s.append('\n\n')
        # The AST classes
        for t in types_list:
            s.append(self._define_type(basename, t, self.ast_types[t]))
            s.append('\n')
        text = ''.join(s)
        # Write out the string to dist
        with open(path, 'w') as fp:
            fp.write(text)

    def _define_visitor(self, basename, arg_list):
        s = []
        s.append('    def visit(self,')
        for n, a in enumerate(arg_list):
            if n == len(arg_list) - 1:
                s.append('%s' % str(a))
            else:
                s.append('%s,' % str(a))
        s.append('):\n')

        return ''.join(s)

    def main(self):
        self._define_ast(self.output_dir, "Expression", self.ast_types.keys())

if __name__ == '__main__':
    # Generate Expressions for use in the project
    output_dir = 'loxpy'
    gen = ASTGenerate(output_dir, verbose=True)
    gen.main()
