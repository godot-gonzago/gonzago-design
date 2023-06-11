@tool
extends EditorScript


func _run() -> void:
    var theme_data := {}
    var theme := ThemeDB.get_default_theme()
    for data_type in Theme.DATA_TYPE_MAX:
        var types := theme.get_theme_item_type_list(data_type)
        for type in types:
            var names := theme.get_theme_item_list(data_type, type)
            for name in names:
                var key: Variant = theme.get_theme_item(data_type, name, type)
                var entries: Array[String]
                if not theme_data.has(key):
                    entries = []
                    theme_data[key] = entries
                else:
                    entries = theme_data[key] as Array[String]
                entries.append("%d, %s, %s" % [data_type, name, type])
    for key in theme_data.keys():
        print("%s:" % str(key))
        var entries := theme_data[key] as Array[String]
        print(";\n".join(entries))
