@tool
extends Control


var _theme: Theme = null

var _scroll: ScrollContainer
var _content: ThemeContainer
var _items: Array[ThemeItem] = []

#var _loader: ThemeLoader


func _init() -> void:
    #_loader = ThemeLoader.new()

    _scroll = ScrollContainer.new()
    _scroll.set_anchors_preset(Control.PRESET_FULL_RECT)
    _scroll.clip_contents = true
    add_child(_scroll)

    _content = ThemeContainer.new()
    _scroll.add_child(_content)


func _notification(what: int) -> void:
    match what:
        NOTIFICATION_THEME_CHANGED:
            _scroll.add_theme_stylebox_override("panel", get_theme_stylebox("panel", "Tree"))
#        NOTIFICATION_DRAW:
#            draw_style_box(
#                get_theme_stylebox("panel", "Tree"),
#                Rect2(Vector2.ZERO, size)
#            )


# TODO: Use threads?
func explore_theme(theme : Theme) -> void:
    if _theme == theme: return

    # TODO: Show spinner
    # TODO: Use https://docs.godotengine.org/en/stable/classes/class_workerthreadpool.html
    # https://gist.github.com/mashumafi/fced71eaf2ac3f90c158fd05d21379a3
    # TODO: Or use this https://docs.godotengine.org/en/stable/classes/class_thread.html

    _items.clear()
    _content.clear()
    _theme = theme
    if not theme: return

    var theme_types := theme.get_type_list()
    theme_types.sort()
    for theme_type in theme_types:
        var type_container := TypeContainer.new(theme_type, theme.get_type_variation_base(theme_type))
        _content.add_child(type_container)

        for data_type in Theme.DATA_TYPE_MAX:
            var item_names := theme.get_theme_item_list(data_type, theme_type)
            if item_names.is_empty():
                continue

            var data_type_container := DataTypeContainer.new(data_type)
            type_container.add_child(data_type_container)

            var items_container := ThemeItemsContainer.new()
            data_type_container.add_child(items_container)

            item_names.sort()
            for item_name in item_names:
                var item : ThemeItem = ThemeItemsContainer.get_theme_item(theme, theme_type, data_type, item_name)
                items_container.add_child(item)

                var searchables := PackedStringArray()
                searchables.append(theme_type)
                searchables.append(DataTypeContainer.get_data_type_name(data_type))
                searchables.append(item_name)
                item.set_meta("searchables", searchables)

                _items.append(item)

    # Threaded is dreadfully slow!!!
    #if _loader.finished.is_connected(_loader_finished):
    #    _loader.finished.disconnect(_loader_finished)
    #_loader.finished.connect(_loader_finished, CONNECT_ONE_SHOT)
    #print("loading...")
    #_loader.load_theme(theme)


#func _loader_finished(result: ThemeLoaderResult):
#    if result.error == OK:
#        print("loaded")
#        print("items: %d" % result.items.size())
#        print("content: %d" % result.content.size())
#        _items.append_array(result.items)
#        for child in result.content:
#            _content.add_child(child)


func filter(filter : String) -> void:
    var terms: PackedStringArray = filter.split(" ", false)
    var any_visible: bool = not terms.size()

    for item in _items:
        var is_item_visible := any_visible
        if terms.size():
            var searchables : PackedStringArray = item.get_meta("searchables")
            for term in terms:
                for searchable in searchables:
                    if term.is_subsequence_ofn(searchable):
                        is_item_visible = true
                        break
                if is_item_visible:
                    break
        if item.visible != is_item_visible:
            item.visible = is_item_visible


#class ThemeLoader extends RefCounted:
#    signal finished(result: ThemeLoaderResult)
#
#
#    var _thread: Thread
#    var _mutex: Mutex = Mutex.new()
#    var _exit_thread := false
#
#
#    func _notification(what: int) -> void:
#        match what:
#            NOTIFICATION_PREDELETE:
#                if is_instance_valid(_thread) and _thread.is_started():
#                    _mutex.lock()
#                    _exit_thread = true
#                    _mutex.unlock()
#                    _thread.wait_to_finish()
#
#
#    func load_theme(theme: Theme) -> void:
#        if is_instance_valid(_thread) and _thread.is_started():
#            _mutex.lock()
#            _exit_thread = true
#            _mutex.unlock()
#            var result: ThemeLoaderResult = _thread.wait_to_finish()
#            finished.emit(result)
#
#        _mutex.lock()
#        _exit_thread = false
#        _mutex.unlock()
#        _thread = Thread.new()
#        _thread.start(_build_nodes.bind(theme))
#
#
#    func _build_nodes(theme: Theme) -> ThemeLoaderResult:
#        var result := ThemeLoaderResult.new()
#
#        var theme_types := theme.get_type_list()
#        theme_types.sort()
#        for theme_type in theme_types:
#            _mutex.lock()
#            var should_exit := _exit_thread
#            _mutex.unlock()
#            if should_exit:
#                result.error = ERR_SKIP
#                result.content.clear()
#                result.items.clear()
#                _build_nodes_done.call_deferred()
#                return result
#
#            var type_container := TypeContainer.new(theme, theme_type)
#            result.content.append(type_container)
#
#            for data_type in Theme.DATA_TYPE_MAX:
#                var item_names := theme.get_theme_item_list(data_type, theme_type)
#                if item_names.is_empty():
#                    continue
#
#                var data_type_container := DataTypeContainer.new(data_type)
#                type_container.add_child(data_type_container)
#
#                var items_container := ThemeItemsContainer.new()
#                data_type_container.add_child(items_container)
#
#                item_names.sort()
#                for item_name in item_names:
#                    var item : ThemeItem = ThemeItemsContainer.get_theme_item(theme, theme_type, data_type, item_name)
#                    items_container.add_child(item)
#
#                    var searchables := PackedStringArray()
#                    searchables.append(theme_type)
#                    searchables.append(DataTypeContainer.get_data_type_name(data_type))
#                    searchables.append(item_name)
#                    item.set_meta("searchables", searchables)
#
#                    result.items.append(item)
#
#        _build_nodes_done.call_deferred()
#        return result
#
#
#    func _build_nodes_done() -> void:
#        var result: ThemeLoaderResult = _thread.wait_to_finish()
#        finished.emit(result)
#
#
#class ThemeLoaderResult extends RefCounted:
#    var error: int = OK
#    var content: Array[Control] = []
#    var items: Array[ThemeItem] = []


class ControlUtil extends RefCounted:
    static func has_visible_children(control: Control, include_internal: bool = false) -> bool:
        for idx in control.get_child_count(include_internal):
            var child := control.get_child(idx, include_internal) as Control
            if (
                is_instance_valid(child)
                and not child.top_level
                and child.visible
            ):
                return true
        return false


class ThemeContainer extends Container:
    var _no_entries_label: Label

    func _init() -> void:
        size_flags_horizontal = Control.SIZE_EXPAND_FILL
        size_flags_vertical = Control.SIZE_SHRINK_BEGIN

        _no_entries_label = Label.new()
        _no_entries_label.text = tr("No entries found...")
        _no_entries_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        add_child(_no_entries_label, false, Node.INTERNAL_MODE_FRONT)

    func _notification(what: int) -> void:
        match what:
            NOTIFICATION_PRE_SORT_CHILDREN:
                var has_visible_children := false
                for idx in get_child_count():
                    var child := get_child(idx) as Control
                    if is_instance_valid(child) and child.visible:
                        has_visible_children = true
                        break
                _no_entries_label.visible = not has_visible_children
            NOTIFICATION_SORT_CHILDREN:
                var ofs := 0
                for idx in get_child_count(true):
                    var child := get_child(idx, true) as Control
                    if not is_instance_valid(child) or child.top_level or not child.visible:
                        continue
                    var child_size := child.get_minimum_size()
                    var child_rect := Rect2(0, ofs, size.x, child_size.y)
                    fit_child_in_rect(child, child_rect)
                    ofs += child_size.y + get_theme_constant("separation", "BoxContainer")
            NOTIFICATION_THEME_CHANGED:
                update_minimum_size()
            NOTIFICATION_TRANSLATION_CHANGED, NOTIFICATION_LAYOUT_DIRECTION_CHANGED:
                queue_sort()

    func _get_minimum_size() -> Vector2:
        var minimum := Vector2.ZERO
        var separator_count := -1
        for idx in get_child_count(true):
            var child := get_child(idx, true) as Control
            if not is_instance_valid(child) or child.top_level or not child.visible:
                continue
            var child_size := child.get_combined_minimum_size()
            minimum.x = maxf(minimum.x, child_size.x)
            minimum.y += child_size.y
            separator_count += 1
        if separator_count > 0:
            minimum.y += get_theme_constant("separation", "BoxContainer") * separator_count
        return minimum

    func clear() -> void:
        for child in get_children():
            remove_child(child)
            child.queue_free()


# https://github.com/godotengine/godot/blob/master/scene/gui/box_container.cpp
class TypeContainer extends Container:
    var _theme_type: StringName
    var _base_type: StringName

    func _init(theme_type: StringName, base_type: StringName) -> void:
        _theme_type = theme_type
        _base_type = base_type

    func _notification(what: int) -> void:
        match what:
            NOTIFICATION_PRE_SORT_CHILDREN:
                visible = ControlUtil.has_visible_children(self)
            NOTIFICATION_SORT_CHILDREN:
                var ofs := _get_header_min().y + get_theme_constant("separation", "BoxContainer")
                for idx in get_child_count(true):
                    var child := get_child(idx, true) as Control
                    if not is_instance_valid(child) or child.top_level or not child.visible:
                        continue
                    var child_size := child.get_minimum_size()
                    var child_rect := Rect2(0, ofs, size.x, child_size.y)
                    fit_child_in_rect(child, child_rect)
                    ofs += child_size.y + get_theme_constant("separation", "BoxContainer")
            NOTIFICATION_THEME_CHANGED:
                update_minimum_size()
            NOTIFICATION_TRANSLATION_CHANGED, NOTIFICATION_LAYOUT_DIRECTION_CHANGED:
                queue_sort()
            NOTIFICATION_DRAW:
                var icon_size := Vector2(16, 16) * get_theme_default_base_scale()
                var font := get_theme_font("main", "EditorFonts")
                var font_size := get_theme_font_size("main_size", "EditorFonts")
                var font_height := font.get_height(font_size)

                var background := get_theme_stylebox("title_button_normal", "Tree")
                var background_rect = Rect2(
                    0, 0, size.x, maxf(icon_size.y, font_size) + background.get_minimum_size().y
                )
                draw_style_box(background, background_rect)

                var separation := get_theme_constant("separation", "BoxContainer")
                var icon := (
                    get_theme_icon(_theme_type, "EditorIcons")
                    if has_theme_icon(_theme_type, "EditorIcons")
                    else get_theme_icon("NodeDisabled", "EditorIcons")
                )
                var icon_rect = Rect2(background.get_offset(), icon_size)
                draw_texture_rect(icon, icon_rect, false)

                var font_rect := Rect2(
                    icon_rect.end.x + separation, icon_rect.position.y + font.get_ascent(font_size),
                    size.x + background.get_margin(SIDE_RIGHT) - icon_rect.end.x + separation,
                    font_height
                )
                var font_color := get_theme_color("font_color", "Tree")

                var txt := TextLine.new()
                txt.add_string(_theme_type, font, font_size)
                txt.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
                txt.width = font_rect.size.x
                txt.draw(get_canvas_item(), Vector2(icon_rect.end.x + separation, icon_rect.position.y), font_color)

                var base_type_separator := get_theme_icon("GuiTreeArrowRight", "EditorIcons")
                var base_type_label_color := get_theme_color("disabled_font_color", "Editor")

    func _get_header_min() -> Vector2:
        var minimum := Vector2(16, 16) * get_theme_default_base_scale()

        var font := get_theme_font("main", "EditorFonts")
        var font_size := get_theme_font_size("main_size", "EditorFonts")
        minimum.x += font.get_string_size("...", HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x * 2
        minimum.x += get_theme_constant("separation", "BoxContainer") * 2
        minimum.x += 16 * get_theme_default_base_scale()
        minimum.y = maxf(minimum.y, font.get_height(font_size))

        var background := get_theme_stylebox("title_button_normal", "Tree")
        minimum += background.get_minimum_size()

        return minimum


    func _get_minimum_size() -> Vector2:
        var minimum := _get_header_min()

        var font := get_theme_font("main", "EditorFonts")
        var font_size := get_theme_font_size("main_size", "EditorFonts")
        minimum.x += font.get_string_size("...", HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x * 2
        minimum.x += get_theme_constant("separation", "BoxContainer") * 2
        minimum.x += 16 * get_theme_default_base_scale()
        minimum.y = maxf(minimum.y, font.get_height(font_size))

        var background := get_theme_stylebox("title_button_normal", "Tree")
        minimum += background.get_minimum_size()

        var separator_count := -1
        for idx in get_child_count():
            var child := get_child(idx) as Control
            if not is_instance_valid(child) or child.top_level or not child.visible:
                continue
            var child_size := child.get_combined_minimum_size()
            minimum.x = maxf(minimum.x, child_size.x)
            minimum.y += child_size.y
            separator_count += 1
        if separator_count > 0:
            minimum.y += get_theme_constant("separation", "BoxContainer") * separator_count
        return minimum


class DataTypeContainer extends HBoxContainer:
    var _data_type: int
    var _panel: PanelContainer
    var _icon: TextureRect

    func _init(data_type: int) -> void:
        _data_type = data_type

        _panel = PanelContainer.new()
        add_child(_panel, false, Node.INTERNAL_MODE_FRONT)
        _icon = TextureRect.new()
        _icon.stretch_mode = TextureRect.STRETCH_KEEP
        _panel.add_child(_icon)


    func _notification(what: int) -> void:
        match what:
            NOTIFICATION_READY, NOTIFICATION_TRANSLATION_CHANGED:
                _icon.tooltip_text = tr(get_data_type_name(_data_type))
            NOTIFICATION_THEME_CHANGED:
                var editor_icon_name := get_editor_icon(_data_type)
                _icon.texture = get_theme_icon(editor_icon_name, "EditorIcons")
                var panel_stylebox := get_theme_stylebox("disabled", "Button")
                _panel.add_theme_stylebox_override("panel", panel_stylebox)
            NOTIFICATION_PRE_SORT_CHILDREN:
                visible = ControlUtil.has_visible_children(self)


    static func get_data_type_name(data_type: int) -> String:
        match data_type:
            Theme.DATA_TYPE_COLOR:      return "Colors"
            Theme.DATA_TYPE_CONSTANT:   return "Constants"
            Theme.DATA_TYPE_FONT:       return "Fonts"
            Theme.DATA_TYPE_FONT_SIZE:  return "Font sizes"
            Theme.DATA_TYPE_ICON:       return "Icons"
            Theme.DATA_TYPE_STYLEBOX:   return "Styleboxes"
            _:                          return ""


    static func get_editor_icon(data_type: int) -> StringName:
        match data_type:
            Theme.DATA_TYPE_COLOR:      return "Color"
            Theme.DATA_TYPE_CONSTANT:   return "MemberConstant"
            Theme.DATA_TYPE_FONT:       return "Font"
            Theme.DATA_TYPE_FONT_SIZE:  return "FontSize"
            Theme.DATA_TYPE_ICON:       return "ImageTexture"
            Theme.DATA_TYPE_STYLEBOX:   return "StyleBoxFlat"
            _:                          return "Theme"


class ThemeItemsContainer extends HFlowContainer:
    func _init() -> void:
        size_flags_horizontal = Control.SIZE_EXPAND_FILL


    func _notification(what: int) -> void:
        match what:
            NOTIFICATION_PRE_SORT_CHILDREN:
                visible = ControlUtil.has_visible_children(self)


    static func get_theme_item(theme: Theme, theme_type: StringName, data_type: int, item_name: StringName) -> ThemeItem:
        match data_type:
            Theme.DATA_TYPE_COLOR:
                return ColorItem.new(theme, theme_type, data_type, item_name)
            Theme.DATA_TYPE_CONSTANT:
                return ConstantItem.new(theme, theme_type, data_type, item_name)
            Theme.DATA_TYPE_FONT:
                return FontItem.new(theme, theme_type, data_type, item_name)
            Theme.DATA_TYPE_FONT_SIZE:
                return FontSizeItem.new(theme, theme_type, data_type, item_name)
            Theme.DATA_TYPE_ICON:
                return IconItem.new(theme, theme_type, data_type, item_name)
            Theme.DATA_TYPE_STYLEBOX:
                return StyleboxItem.new(theme, theme_type, data_type, item_name)
            _:
                return ThemeItem.new(theme, theme_type, data_type, item_name)



class ThemeItem extends MarginContainer:
    var _theme : Theme = null
    var _theme_type : StringName = StringName()
    var _data_type : int = -1
    var _item_name : StringName = StringName()

    var _vbox : VBoxContainer
    var _label : Label
    var _control : Control

    var _context: PopupMenu

    var _data: Dictionary = Dictionary()

    func _init(theme : Theme, theme_type : StringName, data_type : int, item_name : StringName) -> void:
        _context = PopupMenu.new()
        _context.about_to_popup.connect(_build_context_menu)
        _context.id_pressed.connect(_handle_context_menu)
        add_child(_context, false, Node.INTERNAL_MODE_FRONT)

        _theme = theme
        _data_type = data_type
        _theme_type = theme_type
        _item_name = item_name
        theme_type_variation = "MarginContainer4px"

        tooltip_text = item_name
        focus_mode = Control.FOCUS_ALL

        _vbox = VBoxContainer.new()
        add_child(_vbox)

        _control.size_flags_vertical = Control.SIZE_EXPAND_FILL
        _vbox.add_child(_control)

        _label = Label.new()
        _label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
        _label.size_flags_vertical = Control.SIZE_SHRINK_END
        _label.text = item_name
        _vbox.add_child(_label)


    func _notification(what: int) -> void:
        match what:
            NOTIFICATION_THEME_CHANGED:
                _control.custom_minimum_size = _get_minimum_size()
            NOTIFICATION_DRAW:
                var rect := Rect2(Vector2.ZERO, size)
                draw_style_box(get_theme_stylebox("normal", "Button"), rect)
                if has_focus():
                    draw_style_box(get_theme_stylebox("focus", "Button"), rect)


    func _gui_input(event: InputEvent) -> void:
        var mb := event as InputEventMouseButton
        if is_instance_valid(mb) and mb.button_index == MOUSE_BUTTON_RIGHT and mb.is_pressed():
            var rect: Rect2 = Rect2(mb.global_position, _context.min_size)
            _context.popup_on_parent(rect)


    func _make_custom_tooltip(for_text: String) -> Object:
        var panel := PanelContainer.new()
        panel.theme_type_variation = "TooltipPanel"
        var vbox := VBoxContainer.new()
        panel.add_child(vbox)

        # TODO: item preview
        var preview := _get_custom_tooltip_preview()
        if is_instance_valid(preview):
            vbox.add_child(preview)

        # TODO: item name, fields etc.
        var text := _get_custom_tooltip_text()
        if text.is_empty():
            text = "%s, %s" % [_item_name, _theme_type]
        var label = Label.new()
        label.text = text
        label.theme_type_variation = "TooltipLabel"
        vbox.add_child(label)

        var data_table := RichTextLabel.new()
        data_table.autowrap_mode = TextServer.AUTOWRAP_OFF
        data_table.scroll_active = false
        data_table.bbcode_enabled = true
        data_table.fit_content = true
        data_table.push_table(2)
        for key in _data:
            data_table.push_cell()
            data_table.add_text("%s:" % key)
            data_table.pop()
            data_table.push_cell()
            data_table.add_text(str(_data[key]))
            data_table.pop()
        data_table.pop()
        vbox.add_child(data_table)

        return panel


    func _get_custom_tooltip_preview() -> Control:
        return null


    func _get_custom_tooltip_text() -> String:
        return ""


    func _build_context_menu() -> void:
        _context.clear()


    func _add_copy_context_item(snippet: String, prefix: String = "Copy snippet: ") -> void:
        var id: int = _context.get_item_count()
        _context.add_item(prefix + snippet, id)
        _context.set_item_icon(id, get_theme_icon("ActionCopy", "EditorIcons"))
        _context.set_item_metadata(id, snippet)


    func _handle_context_menu(id : int) -> void:
        var copy_buffer: String = _context.get_item_metadata(id)
        DisplayServer.clipboard_set(copy_buffer)
        print('Copied to clipboard: %s' % copy_buffer)


class ColorItem extends ThemeItem:
    func _init(theme : Theme, theme_type : StringName, data_type : int, item_name : StringName) -> void:
        var color_rect : ColorRect = ColorRect.new()
        color_rect.mouse_filter = Control.MOUSE_FILTER_PASS
        color_rect.color = theme.get_color(item_name, theme_type)
        _control = color_rect
        super._init(theme, theme_type, data_type, item_name)

        var color := theme.get_color(item_name, theme_type)
        _data["RGBA"] = "Color(%d, %d, %d, %d)" % [
            color.r, color.g, color.b, color.a
        ]
        if color.a == 1.0:
            _data["RGB"] = "Color(%d, %d, %d)" % [
            color.r, color.g, color.b
        ]
        _data["RGBA8"] = "Color(%d, %d, %d, %d)" % [
            color.r8, color.g8, color.b8, color.a8
        ]
        if color.a == 1.0:
            _data["RGB8"] = "Color(%d, %d, %d)" % [
            color.r8, color.g8, color.b8
        ]
        _data["HTML"] = "#%s" % color.to_html(color.a < 1.0)
        _data["HEX"] = "0x%x" % color.to_rgba32()

    func _get_minimum_size() -> Vector2:
        return Vector2(96, 48) * get_theme_default_base_scale()


    func _get_custom_tooltip_preview() -> Control:
        var color_rect : ColorRect = ColorRect.new()
        color_rect.mouse_filter = Control.MOUSE_FILTER_PASS
        color_rect.color = _theme.get_color(_item_name, _theme_type)
        return color_rect


    func _build_context_menu() -> void:
        _context.clear()

        var color := _theme.get_color(_item_name, _theme_type)
        _add_copy_context_item('get_theme_color(\"%s\", \"%s\")' % [_item_name, _theme_type])
        _add_copy_context_item('Color(%s, %s, %s, %s)' % [color.r, color.g, color.b, color.a])
        _add_copy_context_item('Color(\"%s\")' % color.to_html(true))
        _add_copy_context_item(color.to_html(true), "Copy HTML: ")


class ConstantItem extends ThemeItem:
    func _init(theme : Theme, theme_type : StringName, data_type : int, item_name : StringName) -> void:
        var label : Label = Label.new()
        label.text = "%d" % theme.get_constant(item_name, theme_type)
        _control = label
        super._init(theme, theme_type, data_type, item_name)

        var constant := theme.get_constant(item_name, theme_type)
        var units: PackedStringArray = ["border", "margin", "separation", "offset", "spacing", "width", "height", "size"]
        var suffix: String = ""
        for unit in units:
            if unit in item_name:
                suffix = "px"
                break
        if suffix.is_empty():
            if constant == 0:
                suffix = " (false)"
            if constant == 1:
                suffix = " (true)"
        _data["Value"] = "%d%s" % [constant, suffix]


    func _get_minimum_size() -> Vector2:
        return Vector2(96, 0) * get_theme_default_base_scale()


    func _build_context_menu() -> void:
        _context.clear()

        var constant := _theme.get_constant(_item_name, _theme_type)
        _add_copy_context_item('get_theme_constant(\"%s\", \"%s\")' % [_item_name, _theme_type])
        _add_copy_context_item(str(constant), "Copy value: ")


class FontItem extends ThemeItem:
    func _init(theme : Theme, theme_type : StringName, data_type : int, item_name : StringName) -> void:
        var label : Label = Label.new()
        label.autowrap_mode = TextServer.AUTOWRAP_WORD
        label.text = "The quick brown fox jumps over the lazy dog"
        label.add_theme_font_override("font", theme.get_font(item_name, theme_type))
        var font_size_name : String = "%s_size" % item_name
        if theme.has_font_size(font_size_name, theme_type):
            label.add_theme_font_size_override("font_size", theme.get_font_size(font_size_name, theme_type))
        _control = label
        super._init(theme, theme_type, data_type, item_name)

        var font := theme.get_font(item_name, theme_type)
        var font_size := ThemeDB.fallback_font_size
        if theme.has_font_size(font_size_name, theme_type):
            _data["Matching Font Size"] = "%s, %s" % [font_size_name, theme_type]
            font_size = theme.get_font_size(font_size_name, theme_type)
        _data["Font Size"] = font_size
        _data["Height"] = font.get_height(font_size)
        _data["Ascent"] = font.get_ascent(font_size)
        _data["Descent"] = font.get_descent(font_size)
        #_data["Face Count"] = font.get_face_count()
        _data["Font Family"] = font.get_font_name()
        _data["Font Style"] = font.get_font_style_name()
        _data["Font Weight"] = font.get_font_weight()

    func _get_minimum_size() -> Vector2:
        return Vector2(204, 48) * get_theme_default_base_scale()


    func _get_custom_tooltip_preview() -> Control:
        var label : Label = Label.new()
        label.autowrap_mode = TextServer.AUTOWRAP_WORD
        label.text = "The quick brown fox jumps over the lazy dog"
        label.add_theme_font_override("font", _theme.get_font(_item_name, _theme_type))
        var font_size_name : String = "%s_size" % _item_name
        if _theme.has_font_size(font_size_name, _theme_type):
            label.add_theme_font_size_override("font_size", _theme.get_font_size(font_size_name, _theme_type))

        label.theme_changed.connect(
            func() -> void:
                label.custom_minimum_size = Vector2(204, 48) * label.get_theme_default_base_scale()
        )

        return label


    func _build_context_menu() -> void:
        _context.clear()

        _add_copy_context_item('get_theme_font(\"%s\", \"%s\")' % [_item_name, _theme_type])
        var font_size_name : String = "%s_size" % _item_name
        if _theme.has_font_size(font_size_name, _theme_type):
            _add_copy_context_item('get_theme_font_size(\"%s\", \"%s\")' % [font_size_name, _theme_type])


class FontSizeItem extends ThemeItem:
    func _init(theme : Theme, theme_type : StringName, data_type : int, item_name : StringName) -> void:
        var label : Label = Label.new()
        label.autowrap_mode = TextServer.AUTOWRAP_WORD
        label.text = "The quick brown fox jumps over the lazy dog"
        label.add_theme_font_size_override("font_size", theme.get_font_size(item_name, theme_type))
        if item_name.ends_with("_size"):
            var font_name : String = item_name.substr(0, item_name.length() - 5)
            if theme.has_font(font_name, theme_type):
                label.add_theme_font_override("font", theme.get_font(font_name, theme_type))
        _control = label
        super._init(theme, theme_type, data_type, item_name)

        var font_size := theme.get_font_size(item_name, theme_type)
        _data["Font Size"] = font_size
        if item_name.ends_with("_size"):
            var font_name : String = item_name.substr(0, item_name.length() - 5)
            if theme.has_font(font_name, theme_type):
                _data["Matching Font"] = "%s, %s" % [font_name, theme_type]


    func _get_minimum_size() -> Vector2:
        return Vector2(204, 48) * get_theme_default_base_scale()


    func _get_custom_tooltip_preview() -> Control:
        var label : Label = Label.new()
        label.autowrap_mode = TextServer.AUTOWRAP_WORD
        label.text = "The quick brown fox jumps over the lazy dog"
        label.add_theme_font_size_override("font_size", _theme.get_font_size(_item_name, _theme_type))
        if _item_name.ends_with("_size"):
            var font_name : String = _item_name.substr(0, _item_name.length() - 5)
            if _theme.has_font(font_name, _theme_type):
                label.add_theme_font_override("font", _theme.get_font(font_name, _theme_type))

        label.theme_changed.connect(
            func() -> void:
                label.custom_minimum_size = Vector2(204, 48) * label.get_theme_default_base_scale()
        )

        return label


    func _build_context_menu() -> void:
        _context.clear()

        _add_copy_context_item('get_theme_font_size(\"%s\", \"%s\")' % [_item_name, _theme_type])
        if _item_name.ends_with("_size"):
            var font_name : String = _item_name.substr(0, _item_name.length() - 5)
            if _theme.has_font(font_name, _theme_type):
                _add_copy_context_item('get_theme_font(\"%s\", \"%s\")' % [font_name, _theme_type])


class IconItem extends ThemeItem:
    func _init(theme: Theme, theme_type: StringName, data_type: int, item_name: StringName) -> void:
        var texture_rect: TextureRect = TextureRect.new()
        var icon: Texture2D = theme.get_icon(item_name, theme_type)
        texture_rect.texture = icon
        _control = texture_rect
        super._init(theme, theme_type, data_type, item_name)

        _data["Size"] = "%dx%dpx" % [icon.get_width(), icon.get_height()]
        _data["Has Alpha"] = icon.has_alpha()

    func _notification(what: int) -> void:
        match what:
            NOTIFICATION_THEME_CHANGED:
                _control.custom_minimum_size = _get_minimum_size()

                var texture_rect := _control as TextureRect
                if texture_rect.texture.get_height() > texture_rect.custom_minimum_size.y:
                    texture_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
                    texture_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
                else:
                    texture_rect.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED


    func _get_minimum_size() -> Vector2:
        return Vector2(96, 48) * get_theme_default_base_scale()


    func _get_custom_tooltip_preview() -> Control:
        var texture_rect: TextureRect = TextureRect.new()
        var icon: Texture2D = _theme.get_icon(_item_name, _theme_type)
        texture_rect.texture = icon
        texture_rect.expand_mode = TextureRect.EXPAND_KEEP_SIZE
        texture_rect.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
        return texture_rect


    func _build_context_menu() -> void:
        _context.clear()
        _add_copy_context_item('get_theme_icon(\"%s\", \"%s\")' % [_item_name, _theme_type])


class StyleboxItem extends ThemeItem:
    func _init(theme : Theme, theme_type : StringName, data_type : int, item_name : StringName) -> void:
        var panel_container : PanelContainer = PanelContainer.new()
        panel_container.mouse_filter = Control.MOUSE_FILTER_IGNORE
        panel_container.add_theme_stylebox_override("panel", theme.get_stylebox(item_name, theme_type))
        _control = panel_container
        super._init(theme, theme_type, data_type, item_name)

        var stylebox := theme.get_stylebox(item_name, theme_type)
        _data["Type"] = stylebox.get_class()
        _data["Min Size"] = "%dx%dpx" % [stylebox.get_minimum_size().x, stylebox.get_minimum_size().y]
        _data["Margins"] = "L=%d, T=%d, R=%d, B=%d" % [
            stylebox.get_margin(SIDE_LEFT),
            stylebox.get_margin(SIDE_TOP),
            stylebox.get_margin(SIDE_RIGHT),
            stylebox.get_margin(SIDE_BOTTOM)
        ]
        _data["Content Margins"] = "L=%d, T=%d, R=%d, B=%d" % [
            stylebox.content_margin_left,
            stylebox.content_margin_top,
            stylebox.content_margin_right,
            stylebox.content_margin_bottom
        ]

        var sb_flat := stylebox as StyleBoxFlat
        if is_instance_valid(sb_flat):
            # https://docs.godotengine.org/en/stable/classes/class_styleboxflat.html#class-styleboxflat
            _data["BG Color"] = "#%s" % sb_flat.bg_color.to_html(true)
            _data["Draw Center"] = sb_flat.draw_center
            _data["Skew"] = "%d, %d" % [sb_flat.skew.x, sb_flat.skew.y]
            _data["Corner Detail"] = sb_flat.corner_detail
            _data["Border Width"] = "L=%d, T=%d, R=%d, B=%d" % [
                sb_flat.border_width_left,
                sb_flat.border_width_top,
                sb_flat.border_width_right,
                sb_flat.border_width_bottom
            ]
            _data["Border Color"] = "#%s" % sb_flat.border_color.to_html(true)
            _data["Border Blend"] = sb_flat.border_blend
            _data["Corner Radius"] = "BL=%d, BR=%d, TL=%d, TR=%d" % [
                sb_flat.corner_radius_bottom_left,
                sb_flat.corner_radius_bottom_right,
                sb_flat.corner_radius_top_left,
                sb_flat.corner_radius_top_right
            ]
            _data["Expand Margins"] = "L=%d, T=%d, R=%d, B=%d" % [
                sb_flat.expand_margin_left,
                sb_flat.expand_margin_top,
                sb_flat.expand_margin_right,
                sb_flat.expand_margin_bottom
            ]
            _data["Shadow Color"] = "#%s" % sb_flat.shadow_color.to_html(true)
            _data["Shadow Size"] = "%dpx" %sb_flat.shadow_size
            _data["Shadow Offset"] = "%dx%dpx" % [sb_flat.shadow_offset.x, sb_flat.shadow_offset.y]
            _data["Anti Aliasing"] = sb_flat.anti_aliasing
            _data["Anti Aliasing Size"] = "%dpx" % sb_flat.anti_aliasing_size
        var sb_line := stylebox as StyleBoxLine
        if is_instance_valid(sb_line):
            # https://docs.godotengine.org/en/stable/classes/class_styleboxline.html#class-styleboxline
            _data["Color"] = "#%s" % sb_line.color.to_html(true)
            _data["Grow Begin"] = "%dpx" % sb_line.grow_begin
            _data["Grow End"] = "%dpx" % sb_line.grow_begin
            _data["Thickness"] = "%dpx" % sb_line.thickness
            _data["Vertical"] = sb_line.vertical
        var sb_texture := stylebox as StyleBoxTexture
        if is_instance_valid(sb_texture):
            # https://docs.godotengine.org/en/stable/classes/class_styleboxtexture.html#class-styleboxtexture
            #_data["Texture"] = sb_texture.texture ??
            _data["Draw Center"] = sb_texture.draw_center
            _data["Texture Margins"] = "L=%d, T=%d, R=%d, B=%d" % [
                sb_texture.texture_margin_left,
                sb_texture.texture_margin_top,
                sb_texture.texture_margin_right,
                sb_texture.texture_margin_bottom
            ]
            _data["Expand Margins"] = "L=%d, T=%d, R=%d, B=%d" % [
                sb_texture.expand_margin_left,
                sb_texture.expand_margin_top,
                sb_texture.expand_margin_right,
                sb_texture.expand_margin_bottom
            ]
            _data["Axis H Stretch"] = sb_texture.axis_stretch_horizontal
            _data["Axis V Stretch"] = sb_texture.axis_stretch_vertical
            _data["Region"] = "x=%d, y=%d, w=%d, h=%d" % [
                sb_texture.region_rect.position.x,
                sb_texture.region_rect.position.y,
                sb_texture.region_rect.size.x,
                sb_texture.region_rect.size.y
            ]
            _data["Mod Color"] = "#%s" % sb_texture.modulate_color.to_html(true)

    func _get_minimum_size() -> Vector2:
        return Vector2(96, 48) * get_theme_default_base_scale()


    func _get_custom_tooltip_preview() -> Control:
        var panel_container : PanelContainer = PanelContainer.new()
        panel_container.mouse_filter = Control.MOUSE_FILTER_IGNORE
        panel_container.add_theme_stylebox_override("panel", _theme.get_stylebox(_item_name, _theme_type))
        return panel_container


    func _build_context_menu() -> void:
        _context.clear()
        _add_copy_context_item('get_theme_stylebox(\"%s\", \"%s\")' % [_item_name, _theme_type])
