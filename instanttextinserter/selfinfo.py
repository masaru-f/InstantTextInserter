# encoding: shift-jis

import os
import sys

# Program Information
PROGRAM_NAME = "InstantTextInserter"
VERSION = "0.0.1"
AUTHOR = "shouh"
PROGRAM_INFO = PROGRAM_NAME + " " + "v" + VERSION + " (c) " + AUTHOR

# Program window information
WINDOWCLASSNAME = "itiwnd"

# Program pathes
PROGRAM_FULLPATH = sys.argv[0]
PROGRAM_DIRECTORY = os.path.dirname(PROGRAM_FULLPATH)

# Files path
# �����ɒu���ׂ����ǂ�������������
# �ꌳ�Ǘ��ł���̂łƂ肠����������...
SNIPPETFOLDER_FULLPATH = os.path.join(PROGRAM_DIRECTORY, "snippet")
