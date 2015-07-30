# encoding: shift-jis

class _CALLBACK_ENTITY:
    """
    インスタンスを保持するクラス.
    シングルトン.
    """
    def __init__(self):
        import commander_system as cs
        self.reload = cs.ReloadCommander()
        self.open_snippet_folder = cs.OpenSnippetDirectoryCommander()
        self.open_hotkey_config = cs.OpenHotkeyConfigCommander()
        self.version = cs.VersionCommander()
        self.open_file = cs.OpenFileCommander()

_entity = _CALLBACK_ENTITY()

# ホットキーに割り当てられる処理の一覧.
# key はホットキーの識別子文字列
# value は commander_system のインスタンス
#
# @todo private method を呼び出してしまっているので改善必要?
#
# value は commander_system のインスタンスで統一したい.
#
# @todo これだと複数の open を書けない(最後に書いたopenのみ適用される) \n
#       原因は callback_map が dict だから. 同一keyのvalueは一つ.
callback_map = {
    "reload"              : _entity.reload._interpret,
    "open_snippet_folder" : _entity.open_snippet_folder._interpret,
    "open_hotkey_config"  : _entity.open_hotkey_config._interpret,
    "version"             : _entity.version._interpret,
    "open"                : _entity.open_file._interpret,
}
