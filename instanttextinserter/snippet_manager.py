# encoding: shift-jis

import os
from time import sleep

import snippet_paster

class SnippetManager:
    # �L�[�R�[�h�ɑΉ����镶�����n�[�h�R�[�h.
    # �������ȗ��n�ɑΉ����Ă��Ȃ��L�[�R�[�h�͖��ߍ���łȂ�
    keycode2chara = ['?','?','?','?','?','?','?','?','?','\t','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?',' ','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','0','1','2','3','4','5','6','7','8','9','?','?','?','?','?','?','?','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','?','?','?','?','?','0','1','2','3','4','5','6','7','8','9','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?',':',';',',','-','.','/','@','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','[','\\',']','^','?','?','?','\\','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?']
    # �ȗ��n�ɑΉ������L�[�̃L�[�R�[�h�̈ꗗ���n�[�h�R�[�h
    supported_keycode_list = [9,32,48,49,50,51,52,53,54,55,56,57,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,96,97,98,99,100,101,102,103,104,105,186,187,188,189,190,191,192,219,220,221,222,226]

    def __init__(self):
        # �����o�ϐ��̏�����
        self.clear()

        self._paster = snippet_paster.SnippetPaster()

    def add(self, abbr, phrase):
        """
        �d�������ȗ��`��n����Ă����Ɍ����͂��Ȃ�.
        �����Ƃ��Ă�, �ŏ��ɓn���ꂽ�ȗ��`���̗p�����(see input() method)��,
        �ŏ��ɉ���n�����͌Ăяo��������.
        """
        self._abbrlist.append(abbr.upper())
        self._phraselist.append(phrase)
        self._inputlist.append(0)

        self._list_len = len(self._abbrlist)

    def clear(self):
        """
        �o�^����Ă���X�j�y�b�g�����N���A����.
        """
        # i�Ԗڂ� �Z�k�`i ����ꂽ���X�g
        self._abbrlist = []
        # i�Ԗڂ� �Z�k�`i���������ڂ܂œ��͂ƈ�v���Ă��邩 ����ꂽ���X�g
        self._inputlist = []
        # i�Ԗڂ� ��^��i ����ꂽ���X�g
        self._phraselist = []
        # ���X�g�̒���.
        # �������� len �Ōv�Z����ƒx���̂Ń����o�Ƃ��ĕێ�����.
        # �ǂ̃��X�g�����������ɂȂ�͂��Ȃ̂�, ���������΂���.
        self._list_len = 0

    def printlists(self):
        """
        �f�o�b�O�p.
        """
        print self._abbrlist
        print self._phraselist
        print self._inputlist

    def input(self, keycode):
        """
        �ǂ̒Z�k�`�ƈ�v���邩�𒲂�,
        ��v������y�[�X�g�����������Ď��s����.
        """
        for i in range(self._list_len):
            abbr_len = len(self._abbrlist[i])

            # IndexError��h��
            if self._inputlist[i] == abbr_len:
                self._inputlist[i] = 0
                continue

            # ���͕�����������v���Ă��邩���ׂ�
            # ��v���Ȃ�������ŏ������蒼��
            character = SnippetManager.keycode2chara[keycode]
            if self._abbrlist[i][self._inputlist[i]] != character:
                self._inputlist[i] = 0
                continue

            # �N�G���̍Ō�܂ň�v���Ă����犮�S�Ɉ�v.
            # ���S��v���̏������s������,
            # ����܂ł̕�����v����S�ăN���A����.
            if abbr_len-1 == self._inputlist[i]:
                # �f�o�b�O�p
                #print "hit:" + self._abbrlist[i]
                #print "phrase:" + self._phraselist[i]
                self._paster.paste(self._abbrlist[i], self._phraselist[i])
                self._clear_all_input()
                break

            # ��r����ꏊ������炷
            self._inputlist[i] += 1

        # �f�o�b�O�p.
        #print self._inputlist

    def _clear_all_input(self):
        for j in range(self._list_len):
            self._inputlist[j] = 0

if __name__ == '__main__':
    pass
