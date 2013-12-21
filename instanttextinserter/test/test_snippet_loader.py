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
        マージ後に生成されたリストの行数をテストする.
        テストデータファイルはあらかじめ用意.
        """
        file_content_list = snippet_loader._load_and_merge()

        actual_len = len(file_content_list)
        # 各ファイルの期待行数をファイル名昇順で足しあわせている.
        # 詳細は各テストデータファイルを参照.
        expect_len = 8+2 + 2+2+3+24
        self.assertEqual(expect_len, actual_len)

    def test__convert_to_snippetdict(self):
        """
        スニペット辞書が構築できていることをテストする.
        特に改行の個数が意図した数であるかを重点的にチェック.

        前提
        - 辞書として構築したいテスト用ファイルは名前を snippet_ で始めること.
        - snippet_ で始まらないファイルにはスニペットの文法を記述しないこと.
        """
        file_content_list = snippet_loader._load_and_merge()
        snippetdict = snippet_loader._convert_to_snippetdict(file_content_list)

        # 一行の幅を抑えるためのエイリアス
        d = snippetdict      # Dict
        L = os.linesep       # Linesep
        a = self.assertEqual # Assert

        a(
            d["1line"],
            "this is the phrase consisting of 1-line."
        )
        a(
            d["nline"],
            "n行からなる定型文." + L + "とりあえず" + L + "3行で."
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
            "hoge" + L + L + "ふが" + L + L + L + L + "piyo"
        )
        # 行末の空行は無視される
        a(
            d["end_is_empty_linesep"],
            # "foobarbuz" + L
            "foobarbuz"
        )
        a(
            d["end_is_not_empty_linesep"],
            "foobarbuz"
        )
        # 行末の空行は無視される
        a(
            d["end_is_two_empty_linesep"],
            #"foobarbuz" + L + L
            "foobarbuz" + L
        )


if __name__ == "__main__":
    unittest.main()
