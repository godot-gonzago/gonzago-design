@tool
extends EditorScript


func _run() -> void:
    var theme_path := "res://theme/default.theme"
    if not ResourceLoader.exists(theme_path):
        printerr("Theme does't exist")
        return
    var theme := ResourceLoader.load(theme_path) as Theme
    if not theme:
        printerr("Couldn't load theme")
        return
    if theme.resource_path.is_empty():
        printerr("Not persistent theme")
        return

    var new_theme_path := theme.resource_path.get_basename() + ".tres"
    var new_theme := theme.duplicate() as Theme
    var types := theme.get_stylebox_type_list()
    for type in types:
        var names := theme.get_stylebox_list(type)
        for name in names:
            var sb := theme.get_stylebox(name, type)
            if not sb or sb.resource_path.is_empty():
                continue
            var new_sb_path := sb.resource_path.get_basename() + ".tres"
            if not ResourceLoader.exists(new_sb_path, "StyleBox"):
                ResourceSaver.save(sb.duplicate(), new_sb_path)
            var new_sb := ResourceLoader.load(new_sb_path, "StyleBox") as StyleBox
            new_theme.set_stylebox(name, type, new_sb)
    ResourceSaver.save(new_theme, new_theme_path)
