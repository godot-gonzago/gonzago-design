@tool
extends HBoxContainer

signal editor_theme_selected
signal default_theme_selected
signal theme_file_selected(resource_path : String)

var _theme_tabs : TabBar
var _theme_files : Array[String] = []
var _open : Button
var _dialog : EditorFileDialog

func _init() -> void:
    _theme_tabs = TabBar.new()
    _theme_tabs.add_tab("Editor")
    _theme_tabs.add_tab("Default")
    _theme_tabs.tab_changed.connect(_tab_changed)
    _theme_tabs.tab_close_pressed.connect(_tab_close_pressed)
    _theme_tabs.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    add_child(_theme_tabs)

    _open = Button.new()
    _open.flat = true
    _open.pressed.connect(_open_file_dialog)
    add_child(_open)

    _dialog = EditorFileDialog.new()
    _dialog.file_mode = EditorFileDialog.FILE_MODE_OPEN_FILE
    var extentions : PackedStringArray = ResourceLoader.get_recognized_extensions_for_type("Theme")
    for i in extentions.size():
        extentions[i] = "*.%s" % extentions[i]
    _dialog.add_filter(", ".join(extentions), "Themes")
    _dialog.file_selected.connect(_file_selected)
    add_child(_dialog)

func _notification(what: int) -> void:
    match what:
        NOTIFICATION_READY:
            _tab_changed(_theme_tabs.current_tab)
        NOTIFICATION_THEME_CHANGED:
            _open.icon = get_theme_icon("Load", "EditorIcons")

#func _get_theme_from_tab(tab : int) -> Theme:
#    match tab:
#        0:
#            var plugin := EditorPlugin.new()
#            var interface := plugin.get_editor_interface()
#            return interface.get_base_control().theme
#        1:
#            return ThemeDB.get_default_theme()
#        _:
#            var idx : int = tab - 2
#            if idx < _theme_files.size():
#                var path : String = _theme_files[idx]
#                return ResourceLoader.load(path, "Theme")
#            return null

func _tab_changed(tab: int) -> void:
    _theme_tabs.tab_close_display_policy = TabBar.CLOSE_BUTTON_SHOW_ACTIVE_ONLY if tab > 1 else TabBar.CLOSE_BUTTON_SHOW_NEVER
    match tab:
        0: emit_signal("editor_theme_selected")
        1: emit_signal("default_theme_selected")
        _:
            var idx : int = tab - 2
            if idx < _theme_files.size():
                var path : String = _theme_files[idx]
                emit_signal("theme_file_selected", path)

func _tab_close_pressed(tab: int) -> void:
    if tab > 1:
        _theme_tabs.remove_tab(tab)

func _open_file_dialog() -> void:
    _dialog.popup_centered_ratio()

func _file_selected(path: String) -> void:
    var theme : Theme = ResourceLoader.load(path, "Theme") as Theme
    if theme:
        _dialog.hide()

        var idx : int = _theme_files.find(path) + 2
        if idx < 2:
            idx = _theme_tabs.tab_count
            _theme_files.append(path)
            _theme_tabs.add_tab(path.get_file())

        _theme_tabs.current_tab = idx
