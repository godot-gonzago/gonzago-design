@tool
extends EditorScript

func _run() -> void:
    var base_control := get_editor_interface().get_base_control()
    var window := AcceptDialog.new()
    var items := ItemList.new()
    items.max_columns = 0
    items.fixed_column_width = 16 * int(base_control.theme.default_base_scale)
    items.icon_mode = ItemList.ICON_MODE_TOP
    items.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
    window.add_child(items)

    var fs := get_editor_interface().get_resource_filesystem()
    var dir := fs.get_filesystem_path("res://editor_icons")
    _build_dir(items, dir)

    window.close_requested.connect(window.queue_free)
    window.ready.connect(window.popup_centered_ratio)
    base_control.add_child(window)

func _build_dir(items: ItemList, dir: EditorFileSystemDirectory) -> void:
    for subdir_idx in dir.get_subdir_count():
        var subdir := dir.get_subdir(subdir_idx)
        _build_dir(items, subdir)
    for file_idx in dir.get_file_count():
        var file_path := dir.get_file_path(file_idx)
        if file_path.get_extension() != "svg":
            continue
        var icon := ResourceLoader.load(file_path) as Texture2D
        var item_idx := items.item_count
        items.add_icon_item(icon)
        items.set_item_tooltip(item_idx, file_path)
        items.set_item_tooltip_enabled(item_idx, true)
