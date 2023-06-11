@tool
extends EditorScript


func _run() -> void:
    var styleboxes := {}
    var theme := ThemeDB.get_default_theme()
    var types := theme.get_stylebox_type_list()
    for type in types:
        var names := theme.get_stylebox_list(type)
        for name in names:
            var sb := theme.get_stylebox(name, type)
            var entries: Array[String]
            if not styleboxes.has(sb):
                entries = []
                styleboxes[sb] = entries
            else:
                entries = styleboxes[sb] as Array[String]
            entries.append("%s, %s" % [name, type])
    for key in styleboxes.keys():
        var sb := key as StyleBox
        if not sb:
            continue
        var sb_name: String
        if not sb.resource_name.is_empty():
            sb_name = sb.resource_name
        elif not sb.resource_path.is_empty():
            sb_name = sb.resource_path
        else:
            sb_name = str(sb)
        print("%s:" % sb_name)
        var entries := styleboxes[sb] as Array[String]
        print(";\n".join(entries))
