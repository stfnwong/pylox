# TODO: deprecate all this
from tools.ast_generate import ASTGenerate

TEST_OUTPUT_DIR = 'tests/ast'
TEST_VERBOSE = True

def test_generate_ast_binary():
    gen = ASTGenerate(TEST_OUTPUT_DIR, verbose=TEST_VERBOSE)
    gen.main()

    print(gen)
