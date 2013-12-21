# encoding: shift-jis

import os
import unittest

import snippet_loader

class SnippetLoadertTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__load_and_merge(self):
        """
        �}�[�W��ɐ������ꂽ���X�g�̍s�����e�X�g����.
        �e�X�g�f�[�^�t�@�C���͂��炩���ߗp��.
        """
        file_content_list = snippet_loader._load_and_merge()

        actual_len = len(file_content_list)
        # �e�t�@�C���̊��ҍs�����t�@�C���������ő������킹�Ă���.
        # �ڍׂ͊e�e�X�g�f�[�^�t�@�C�����Q��.
        expect_len = 8+2 + 2+2+3+24
        self.assertEqual(expect_len, actual_len)

    def test__convert_to_snippetdict(self):
        """
        �X�j�y�b�g�������\�z�ł��Ă��邱�Ƃ��e�X�g����.
        ���ɉ��s�̌����Ӑ}�������ł��邩���d�_�I�Ƀ`�F�b�N.

        �O��
        - �����Ƃ��č\�z�������e�X�g�p�t�@�C���͖��O�� snippet_ �Ŏn�߂邱��.
        - snippet_ �Ŏn�܂�Ȃ��t�@�C���ɂ̓X�j�y�b�g�̕��@���L�q���Ȃ�����.
        """
        file_content_list = snippet_loader._load_and_merge()
        snippetdict = snippet_loader._convert_to_snippetdict(file_content_list)

        # ��s�̕���}���邽�߂̃G�C���A�X
        d = snippetdict      # Dict
        L = os.linesep       # Linesep
        a = self.assertEqual # Assert

        a(
            d["1line"],
            "this is the phrase consisting of 1-line."
        )
        a(
            d["nline"],
            "n�s����Ȃ��^��." + L + "�Ƃ肠����" + L + "3�s��."
        )
        a(
            d["1 beginmark"],
            "ok"
        )
        a(
            d["1 endmark"],
            "ok"
        )
        a(
            d["no endmark"],
            "ng"
        )
        a(
            d["no beginmark test"],
            "no beginmark=" + L + \
            "if there is not beginmark, it is not a snippet."
        )
        a(
            d["emptysnippet"],
            ""
        )
        a(
            d["nline contains empty linesep"],
            "hoge" + L + L + "�ӂ�" + L + L + L + L + "piyo"
        )
        # �s���̋�s�͖��������
        a(
            d["end_is_empty_linesep"],
            # "foobarbuz" + L
            "foobarbuz"
        )
        a(
            d["end_is_not_empty_linesep"],
            "foobarbuz"
        )
        # �s���̋�s�͖��������
        a(
            d["end_is_two_empty_linesep"],
            #"foobarbuz" + L + L
            "foobarbuz" + L
        )


if __name__ == "__main__":
    unittest.main()
