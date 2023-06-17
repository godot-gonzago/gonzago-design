@tool
extends EditorPlugin

const TOOL_MENU_NAME : String = "Editor Theme Explorer..."
const ThemeWindow : Script = preload("./ui/window.gd")
#const ThemeWindow : Script = preload("./test/window.gd")

var _window : ThemeWindow
var _button : Button

func _enter_tree() -> void:
    add_tool_menu_item(TOOL_MENU_NAME, _show_theme_window)
    var editor_theme : Theme = get_editor_interface().get_base_control().theme
    _window = ThemeWindow.new()
    _window.editor_theme = editor_theme
    get_editor_interface().get_base_control().add_child(_window)

func _exit_tree() -> void:
    _window.queue_free()
    remove_tool_menu_item(TOOL_MENU_NAME)

func _show_theme_window() -> void:
    _window.popup_centered_ratio()

