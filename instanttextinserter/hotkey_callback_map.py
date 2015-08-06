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
# * key はホットキーの識別子文字列, value は commander_system のインスタンス.
# * value は commander_system のインスタンスで統一したい.
_callback_map = {
    "reload"              : _entity.reload._interpret,
    "open_snippet_folder" : _entity.open_snippet_folder._interpret,
    "open_hotkey_config"  : _entity.open_hotkey_config._interpret,
    "version"             : _entity.version._interpret,
}
def get(keyname):
    """
    @exception KeyError 指定した設定名に対応するコールバック関数が無い
    """
    # 'open<id>' というパターンを許容する. <id>=0,1,2,...
    openlen = len('open')
    if len(keyname)>=openlen+1 and \
       keyname[:openlen]=='open' and \
       keyname[openlen:].isdigit():
        return _entity.open_file._interpret

    return _callback_map[keyname]
