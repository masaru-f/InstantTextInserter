# encoding: shift-jis

import os
import sys

import util_win.multiplelaunch as multiplelaunch

import dialog_wrapper
import selfinfo

def check_and_dispose():
    """
    ��d�N���������烁�b�Z�[�W���o���đ����ɏI������.
    """
    if multiplelaunch.is_already_running(selfinfo.WINDOWCLASSNAME):
        dialog_wrapper.ok(
            "��d�N���ł�." + os.linesep +
            "�V�����N���������͏I�����܂�."
        )
        sys.exit(0)
