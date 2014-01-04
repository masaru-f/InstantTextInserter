# encoding: shift-jis

"""
���p�҂̓V���O���g���C���X�^���X���g������.
����ȊO�͕⏕�N���X�Ȃ̂Ō����g�����Ƃ͂Ȃ�.
"""

import os

import util.filereader as filereader

import dialog_wrapper
import selfinfo
import snippet_observer

def _load_and_merge():
    """
    snippet files �B��ǂݍ���Ń��X�g������.

    @exception IOError �t�@�C����ǂݍ��߂Ȃ�����
    @return ��v�f�Ɉ�s���̓��e�����������X�g

    """
    # �t�@�C���ꗗ���擾.
    try:
        target_filelist = os.listdir(selfinfo.SNIPPETFOLDER_FULLPATH)
    except WindowsError as e:
        # �����ɗ����ꍇ, �v���O���}���̃~�X��������������Ȃ�.
        # ->�t�H���_��p�ӂ��Ă��Ȃ���.
        # @todo ���ɂ����ɗ��錴�������邩����(�A�N�Z�X�����������ꍇ�Ƃ�?).
        raise IOError(str(e))

    # �e�t�@�C�����e����̃��X�g�Ƀ}�[�W.
    reader = filereader.FileReader()
    ret = []
    for f in target_filelist:
        ret += reader.read(
            os.path.join(selfinfo.SNIPPETFOLDER_FULLPATH, f)
        )

    # �e�v�f�̖����ɂ�����s����菜��.
    for i in range(len(ret)):
        ret[i] = ret[i].rstrip(os.linesep)

    return ret

def _convert_to_snippetdict(file_content_list):
    """
    �}�[�W���ꂽ�X�j�y�b�g�t�@�C�����e���p�[�X����
    �X�j�y�b�g����("�Z�k�`�ƒ�^���̑g" �̎���)������ĕԂ�.
    �������̗p���Ă���̂͏d���l����������.

    �A���S���Y��.
    1. �S�ẴX�j�y�b�g�̊J�n(�s)�ʒu���擾���Ă���.
       ���̈ʒu�ɒZ�k�`�������Ă���̂�, �����Ď��o���Ă���.
    2. �X�j�y�b�g i �̒�^����
       "�X�j�y�b�g i �̊J�n�ʒu" ���� "�X�j�y�b�g i+1 �̊J�n�ʒu"
       �̊Ԃɂ���̂�, ��������o���Ē�^���Ƃ���.

    @param [in] file_content_list �t�@�C�����e��s����v�f�ɓ��������X�g

    """
    ABBRNAME_SURROUNDING_MARK = "="

    # �X�j�y�b�g�ʒu���X�g���\�z
    # �������s���� Zero Origin.
    # snippet_position_list = [
    #   ["sig@", 0]  �Z�k�` sgnt �̃X�j�y�b�g�� 0 �s�ڂ���n�܂�
    #   ["for@", 3]  �Z�k�` for@ �̃X�j�y�b�g�� 3 �s�ڂ���n�܂�
    #   �c
    # ]
    snippet_position_list =[]
    for i in range(len(file_content_list)):
        _line = file_content_list[i]
        _len_line = len(_line)

        # ��s�ł��� or �J�n�s�łȂ��Ȃ��΂�
        if _len_line == 0:
            continue
        if _line[0] != ABBRNAME_SURROUNDING_MARK:
            continue

        _abbrname = _line.strip(ABBRNAME_SURROUNDING_MARK)

        snippet_position_list.append([_abbrname, i])

    # �����Ƀ_�~�[�A�C�e����ǉ�
    # ��������Ȃ��ƍŌ�̃X�j�y�b�g�����o���Ȃ�.
    snippet_position_list.append(["dummy", len(file_content_list)])

    # �X�j�y�b�g�ʒu���X�g����X�j�y�b�g�������\�z
    dict_for_return = {}
    for i in range(len(snippet_position_list)):
        # �_�~�[�͏������Ȃ�(out of range�ɂȂ�)
        if i==len(snippet_position_list)-1:
            break

        _snippet = snippet_position_list[i]
        _abbrname = _snippet[0]
        _snippetpos = _snippet[1]
        _next_snippetpos = snippet_position_list[i+1][1]

        _phrase = ""
        for j in range(_snippetpos+1, _next_snippetpos):
            _phrase = _phrase + \
                      file_content_list[j].rstrip(os.linesep) + \
                      os.linesep

        # ���O�̘A�������ɂ��Ōゾ���]���ȉ��s������̂�
        # �������菜��.
        #
        # strip �͎g��Ȃ�����.
        # strip �͕����̉��s��S�Ď�菜���Ă��܂�����
        # ���[�U���Ӑ}���ċL�q������^�������̉��s�������Ȃ��Ă��܂�.
        _phrase = _phrase[0:-1*len(os.linesep)]

        dict_for_return[_abbrname] = _phrase

    return dict_for_return


class SnippetLoader:
    """
    �V���O���g��.

    �ǂݍ��񂾃f�[�^��ʒm���邽�߂� Observer �p�^�[�����g�p.
    ������ Subject �͕�܂��Ă���.
    """
    def __init__(self):
        self._snippet_subject = snippet_observer.Subject()

    def attach(self, observer):
        self._snippet_subject.attach(observer)

    def reload(self):
        """
        �X�j�y�b�g���ēǍ�������, observer �B�ɍēǍ������f�[�^��ʒm����.

        @note �K�v�Ȃ�r�����䂷�邱��.
        """
        file_content_list = []
        try:
            file_content_list = _load_and_merge()
        except IOError as e:
            dialog_wrapper.ok(
                "�X�j�y�b�g��ǂݍ��ނ��Ƃ��ł��܂���." + os.linesep +
                selfinfo.SNIPPETFOLDER_FULLPATH +
                " ���m�F���Ă�������."
            )
            return

        snippetdict = _convert_to_snippetdict(file_content_list)

        self._notify_all(snippetdict)

    def _notify_all(self, data_for_notify):
        self._snippet_subject.notify_all(
            data_for_notify
        )

#�V���O���g���C���X�^���X
inst = SnippetLoader()

if __name__ == '__main__':
    pass
