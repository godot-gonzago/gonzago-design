@tool
extends AcceptDialog

const ThemeSelection : Script = preload("./theme_selection.gd")
const Filter : Script = preload("./filter.gd")
const List : Script = preload("./list.gd")

var editor_theme : Theme
var _list : List

func _init() -> void:
    var panel : VBoxContainer = VBoxContainer.new()
    panel.set_anchors_preset(Control.PRESET_FULL_RECT)
    add_child(panel)

    var theme_selection : ThemeSelection = ThemeSelection.new()
    panel.add_child(theme_selection)

    var filter : Filter = Filter.new()
    panel.add_child(filter)

    var split : HSplitContainer = HSplitContainer.new()
    split.size_flags_vertical = Control.SIZE_EXPAND_FILL
    panel.add_child(split)

    #var scroll : ScrollContainer = ScrollContainer.new()
    #scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    #scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
    #split.add_child(scroll)

    _list = List.new()
    _list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    _list.size_flags_stretch_ratio = 2
    split.add_child(_list)
    #scroll.add_child(_list)

    var detail : VBoxContainer = VBoxContainer.new()
    detail.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    split.add_child(detail)

    theme_selection.editor_theme_selected.connect(_editor_theme_selected)
    theme_selection.default_theme_selected.connect(_default_theme_selected)
    #theme_selection.theme_file_selected.connect(_theme_file_selected)

    filter.text_changed.connect(_list.filter)

func _editor_theme_selected() -> void:
    if editor_theme:
        print("EditorTheme available")
    else:
        print("EditorTheme is null")
    _list.explore_theme(editor_theme)

func _default_theme_selected() -> void:
    _list.explore_theme(ThemeDB.get_default_theme())

#func _enter_tree() -> void:
#    var editor_theme : Theme = _find_root_theme()
#    _list.explore_theme(editor_theme)

func _find_root_theme() -> Theme:
    var theme : Theme = null
    var node : Node = self
    while node:
        if node is Control and node.theme:
            theme = node.theme
        node = node.get_parent()
    return theme
