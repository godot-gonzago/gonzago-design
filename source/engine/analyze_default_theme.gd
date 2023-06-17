@tool
extends EditorScript


func _run() -> void:
    var theme_data: Dictionary = {}
    var theme := ThemeDB.get_default_theme()
    for data_type in Theme.DATA_TYPE_MAX:
        var types := theme.get_theme_item_type_list(data_type)
        for type in types:
            var names := theme.get_theme_item_list(data_type, type)
            for name in names:
                var theme_key: Variant = theme.get_theme_item(data_type, name, type)
                var theme_entries: Dictionary
                if not theme_data.has(theme_key):
                    theme_entries = {}
                    theme_data[theme_key] = theme_entries
                else:
                    theme_entries = theme_data[theme_key] as Dictionary
                var entries: Array[String]
                if not theme_entries.has(name):
                    entries = []
                    theme_entries[name] = entries
                else:
                    entries = theme_entries[name] as Array[String]
                entries.append(type)
    for theme_key in theme_data.keys():
        print("-+ %s" % theme_key)
        var theme_entries := theme_data[theme_key] as Dictionary
        for key in theme_entries.keys():
            print(" |-+ %s" % key)
            var entries := theme_entries[key] as Array[String]
            for entry in entries:
                print(" | |-+ %s" % entry)
