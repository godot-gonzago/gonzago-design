@tool
extends EditorScript


func _run() -> void:
    var base_control := get_editor_interface().get_base_control()
    var window := AcceptDialog.new()
    var tree := Tree.new()
    tree.columns = 2
    tree.hide_root = true
    var root := tree.create_item()
    window.add_child(tree)

    var theme_data: Dictionary = {}
    var theme := ThemeDB.get_default_theme()
    for data_type in Theme.DATA_TYPE_MAX:
        var types := theme.get_theme_item_type_list(data_type)
        var data_type_icon := base_control.get_theme_icon("Theme", "EditorIcons")
        match data_type:
            Theme.DATA_TYPE_COLOR:
                data_type_icon = base_control.get_theme_icon("Color", "EditorIcons")
            Theme.DATA_TYPE_CONSTANT:
                data_type_icon = base_control.get_theme_icon("MemberConstant", "EditorIcons")
            Theme.DATA_TYPE_FONT:
                data_type_icon = base_control.get_theme_icon("Font", "EditorIcons")
            Theme.DATA_TYPE_FONT_SIZE:
                data_type_icon = base_control.get_theme_icon("FontSize", "EditorIcons")
            Theme.DATA_TYPE_ICON:
                data_type_icon = base_control.get_theme_icon("ImageTexture", "EditorIcons")
            Theme.DATA_TYPE_STYLEBOX:
                data_type_icon = base_control.get_theme_icon("StyleBoxFlat", "EditorIcons")

        for type in types:
            var type_icon := (
                base_control.get_theme_icon(type, "EditorIcons")
                if base_control.has_theme_icon(type, "EditorIcons")
                else base_control.get_theme_icon("NodeDisabled", "EditorIcons")
            )

            var names := theme.get_theme_item_list(data_type, type)
            for name in names:
                var theme_key: Variant = theme.get_theme_item(data_type, name, type)
                var theme_entry_item: TreeItem
                if not theme_data.has(theme_key):
                    theme_entry_item = root.create_child()
                    theme_entry_item.set_icon(0, data_type_icon)
                    theme_entry_item.set_text(0, str(theme_key))
                    theme_data[theme_key] = theme_entry_item
                else:
                    theme_entry_item = theme_data[theme_key] as TreeItem
                var theme_type_item := theme_entry_item.create_child()
                theme_type_item.set_icon(0, type_icon)
                theme_type_item.set_text(0, type)
                theme_type_item.set_text(1, name)

    window.close_requested.connect(window.queue_free)
    window.ready.connect(window.popup_centered_ratio)
    base_control.add_child(window)
