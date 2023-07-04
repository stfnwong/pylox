# modules under test
from tools import ASTGenerate

TEST_OUTPUT_DIR = 'tests/ast'
TEST_VERBOSE = True

def test_generate_ast_binary():
    gen = ASTGenerate.ASTGenerate(TEST_OUTPUT_DIR, verbose=TEST_VERBOSE)
    gen.main()

    print(gen)
