# encoding: shift-jis

class _CALLBACK_ENTITY:
    """
    �C���X�^���X��ێ�����N���X.
    �V���O���g��.
    """
    def __init__(self):
        import commander_system as cs
        self.reload = cs.ReloadCommander()
        self.open_snippet_folder = cs.OpenSnippetDirectoryCommander()
        self.open_hotkey_config = cs.OpenHotkeyConfigCommander()
        self.version = cs.VersionCommander()

_entity = _CALLBACK_ENTITY()

# �z�b�g�L�[�Ɋ��蓖�Ă��鏈���̈ꗗ.
# key �̓z�b�g�L�[�̎��ʎq������
# value �� commander_system �̃C���X�^���X
# @todo private method ���Ăяo���Ă��܂��Ă���̂ŉ��P�K�v?
#
# value �� commander_system �̃C���X�^���X�œ��ꂵ����.
callback_map = {
    "reload"              : _entity.reload._interpret,
    "open_snippet_folder" : _entity.open_snippet_folder._interpret,
    "open_hotkey_config"  : _entity.open_hotkey_config._interpret,
    "version"             : _entity.version._interpret,
}
