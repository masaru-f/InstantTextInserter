# encoding: shift-jis

import unittest

import util.terminator_stack as terminator_stack

# �����Ŏg�p����l.
# �{���̓e�X�g�P�[�X���ɒ�`������������,
# ��������� plus1 �֐�������A�N�Z�X�ł��Ȃ������̂�
# �d���Ȃ��O���[�o���ɒu����.
g_testdata = 0

class TerminatorStackTest(unittest.TestCase):
    """
    �I�������Ƃ��ăe�X�g�f�[�^������������֐����g�p���ăe�X�g.
    @todo ���s�����������e�X�g�������̂Œǉ�����.
    """
    def setUp(self):
        global g_testdata
        g_testdata = 0

    def tearDown(self):
        pass

    def test_terminator_case_default(self):
        """
        �I�����ɃG���[���N���Ȃ��ꍇ.
        """
        def plus1():
            global g_testdata
            g_testdata += 1

        def multiple2():
            global g_testdata
            g_testdata *= 2

        with terminator_stack.TerminatorStack() as termstack:
            termstack.push(plus1)
            termstack.push(multiple2)
            termstack.push(plus1)
            termstack.push(plus1)

        global g_testdata
        self.assertEqual(5, g_testdata)

    def test_terminator_case_not_ignoring(self):
        """
        �I�����ɃG���[���N����ꍇ��, �G���[�𖳎����Ȃ��ꍇ.
        """
        def plus1():
            global g_testdata
            g_testdata += 1

        def raiser():
            raise RuntimeError("raised by raiser.")

        try:
            with terminator_stack.TerminatorStack(False) as termstack:
                termstack.push(plus1)
                termstack.push(plus1)
                termstack.push(raiser)
                termstack.push(plus1)
                termstack.push(plus1)
        except RuntimeError:
            pass

        global g_testdata
        # �G���[���N�����Ƃ���܂ł����s����Ă���.
        self.assertEqual(2, g_testdata)

    def test_terminator_case_ignoring(self):
        """
        �I�����ɃG���[���N����ꍇ��, �G���[�𖳎�����ꍇ.
        """
        def plus1():
            global g_testdata
            g_testdata += 1

        def raiser():
            raise RuntimeError("raised by raiser.")

        with terminator_stack.TerminatorStack(True) as termstack:
            termstack.push(plus1)
            termstack.push(raiser)
            termstack.push(plus1)
            termstack.push(raiser)
            termstack.push(raiser)
            termstack.push(plus1)
            termstack.push(plus1)

        global g_testdata
        # �S�Ă̏I�����������s����Ă���.
        self.assertEqual(4, g_testdata)

    def test_terminator_no_element(self):
        """
        �G���[���N���Ȃ����Ƃ��m���߂Ă��邾��.
        """
        with terminator_stack.TerminatorStack() as termstack:
            pass

        with terminator_stack.TerminatorStack(True) as termstack:
            pass

        with terminator_stack.TerminatorStack(False) as termstack:
            pass

if __name__ == "__main__":
    unittest.main()
