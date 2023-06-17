@tool
extends AcceptDialog

const ThemeItemList = preload("./list.gd")


var editor_theme : Theme
var _list: ThemeItemList


func _init() -> void:
    title = tr("Theme Explorer")

    _list = ThemeItemList.new()
    _list.set_anchors_preset(Control.PRESET_FULL_RECT)
    add_child(_list)


func _notification(what: int) -> void:
    match what:
        NOTIFICATION_READY:
            _list.explore_theme(editor_theme)
        NOTIFICATION_TRANSLATION_CHANGED:
            title = tr("Theme Explorer")
