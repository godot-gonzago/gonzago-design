@tool
extends Control

# https://docs.godotengine.org/en/4.0/tutorials/ui/custom_gui_controls.html
# https://github.com/godotengine/godot/blob/master/scene/gui/item_list.cpp


var _theme: Theme
var _theme_cache: _ThemeCache
var _size_cache: _SizeCache
var _root: ThemeGroup


var _loader: ThemeLoader


func _init() -> void:
    _loader = ThemeLoader.new()

    _theme_cache = _ThemeCache.new()
    _size_cache = _SizeCache.new()
    _root = ThemeGroup.new()


func _notification(what: int) -> void:
    match what:
        NOTIFICATION_MOUSE_ENTER:
            pass # Mouse entered the area of this control.
        NOTIFICATION_MOUSE_EXIT:
            pass # Mouse exited the area of this control.
        NOTIFICATION_FOCUS_ENTER:
            pass # Control gained focus.
        NOTIFICATION_FOCUS_EXIT:
            pass # Control lost focus.
        NOTIFICATION_THEME_CHANGED:
            _theme_cache.update_theme_cache(self)
            _update_size_cache()
        NOTIFICATION_RESIZED:
            _update_size_cache()
        #NOTIFICATION_DRAW:
        #    pass
        NOTIFICATION_PREDELETE:
            _theme_cache.free()
            _size_cache.free()
            _root.free()


func _gui_input(event: InputEvent) -> void:
    pass


func _draw() -> void:
    var rect: Rect2i = Rect2i(Vector2i.ZERO, size)
    draw_style_box(_theme_cache.background, rect)
    if has_focus():
        draw_style_box(_theme_cache.focused, rect)


func _update_size_cache() -> void:
    pass


func explore_theme(theme : Theme) -> void:
    _root.clear()

#    var theme_types := theme.get_type_list()
#    theme_types.sort()
#    for theme_type in theme_types:
#        var type_container := ThemeTypeContainer.new()
#        _root.theme_types.append(type_container)
#        for data_type in Theme.DATA_TYPE_MAX:
#            var item_names := theme.get_theme_item_list(data_type, theme_type)
#            if item_names.is_empty():
#                continue
#            var data_type_container := DataTypeContainer.new()
#            type_container.data_types.append(data_type_container)
#            item_names.sort()
#            for item_name in item_names:
#                var item: ThemeItem = ThemeItem.new()
#                data_type_container.items.append(item)

    # Threaded is dreadfully slow!!!
    if _loader.finished.is_connected(_loader_finished):
        _loader.finished.disconnect(_loader_finished)
    _loader.finished.connect(_loader_finished, CONNECT_ONE_SHOT)
    print("loading...")
    _loader.load_theme(theme)


func _loader_finished(result: ThemeLoaderResult):
    if result.error == OK:
        print("loaded")
        print("items: %d" % result.items.size())
        print("content: %d" % result.content.size())
        _root.theme_types.append_array(result.content)


class ThemeLoader extends RefCounted:
    signal finished(result: ThemeLoaderResult)


    var _thread: Thread
    var _mutex: Mutex = Mutex.new()
    var _exit_thread := false


    func _notification(what: int) -> void:
        match what:
            NOTIFICATION_PREDELETE:
                if is_instance_valid(_thread) and _thread.is_started():
                    _mutex.lock()
                    _exit_thread = true
                    _mutex.unlock()
                    _thread.wait_to_finish()


    func load_theme(theme: Theme) -> void:
        if is_instance_valid(_thread) and _thread.is_started():
            _mutex.lock()
            _exit_thread = true
            _mutex.unlock()
            var result: ThemeLoaderResult = _thread.wait_to_finish()
            finished.emit(result)

        _mutex.lock()
        _exit_thread = false
        _mutex.unlock()
        _thread = Thread.new()
        _thread.start(_build_nodes.bind(theme))


    func _build_nodes(theme: Theme) -> ThemeLoaderResult:
        var result := ThemeLoaderResult.new()

        var theme_types := theme.get_type_list()
        theme_types.sort()
        for theme_type in theme_types:
            _mutex.lock()
            var should_exit := _exit_thread
            _mutex.unlock()
            if should_exit:
                result.error = ERR_SKIP
                result.content.clear()
                result.items.clear()
                _build_nodes_done.call_deferred()
                return result

            var type_container := ThemeTypeContainer.new()
            result.content.append(type_container)
            for data_type in Theme.DATA_TYPE_MAX:
                var item_names := theme.get_theme_item_list(data_type, theme_type)
                if item_names.is_empty():
                    continue
                var data_type_container := DataTypeContainer.new()
                type_container.data_types.append(data_type_container)
                item_names.sort()
                for item_name in item_names:
                    var item: ThemeItem = ThemeItem.new()
                    data_type_container.items.append(item)
                    result.items.append(item)

        _build_nodes_done.call_deferred()
        return result


    func _build_nodes_done() -> void:
        var result: ThemeLoaderResult = _thread.wait_to_finish()
        finished.emit(result)


class ThemeLoaderResult extends RefCounted:
    var error: int = OK
    var content: Array[ThemeTypeContainer] = []
    var items: Array[ThemeItem] = []


class _ThemeCache extends Object:
    var background: StyleBox
    var focused: StyleBox
    var scroll_border: int
    var icon_size: Vector2i
    var separation: Vector2i

    var theme_type_background: StyleBox
    var theme_type_margin_start: Vector2i
    var theme_type_margin_end: Vector2i
    var theme_type_icon_rect: Rect2i
    var theme_type_font: Font
    var theme_type_font_size: int
    var theme_type_font_rect: Rect2i
    var theme_type_font_color: Color
    var theme_type_base_type_separator: Texture2D
    var theme_type_base_type_separator_rect: Rect2i
    var theme_type_base_type_font_color: Color
    var theme_type_min_size: Vector2i

    var data_type_background: StyleBox
    var data_type_margin_start: Vector2i
    var data_type_margin_end: Vector2i
    var data_type_icon_rect: Rect2i
    var data_type_min_size: Vector2i

    var theme_item_preview_dark_background: StyleBox
    var theme_item_preview_light_background: StyleBox
    var theme_item_preview_transparent_background: StyleBox
    var theme_item_preview_margin_start: Vector2i
    var theme_item_preview_margin_end: Vector2i
    var theme_item_preview_small_min_size: Vector2i
    var theme_item_preview_large_min_size: Vector2i

    var theme_item_background: StyleBox
    var theme_item_focus: StyleBox
    var theme_item_hover: StyleBox
    var theme_item_selected: StyleBox
    var theme_item_selected_focus: StyleBox
    var theme_item_cursor: StyleBox
    var theme_item_cursor_unfocused: StyleBox
    var theme_item_margin_start: Vector2i
    var theme_item_margin_end: Vector2i
    var theme_item_font: Font
    var theme_item_font_size: int
    var theme_item_font_color: Color
    var theme_item_font_color_selected: Color
    var theme_item_large_font_rect: Rect2i
    var theme_item_small_font_rect: Rect2i
    var theme_item_small_min_size: Vector2i
    var theme_item_large_min_size: Vector2i

    var type_icons: Dictionary = Dictionary()
    var data_type_names: Dictionary = Dictionary()
    var data_type_icons: Dictionary = Dictionary()


    func update_theme_cache(c: Control) -> void:
        background = c.get_theme_stylebox("panel", "Tree")
        focused = c.get_theme_stylebox("focus", "Tree")
        scroll_border = c.get_theme_constant("scroll_border", "Tree")
        icon_size = Vector2i(
            16 * c.get_theme_default_base_scale(),
            16 * c.get_theme_default_base_scale()
        )
        separation = Vector2i(
            c.get_theme_constant("h_separation", "FlowContainer"),
            c.get_theme_constant("v_separation", "FlowContainer")
        )

        theme_type_background = c.get_theme_stylebox("title_button_normal", "Tree")
        theme_type_min_size = theme_type_background.get_minimum_size()
        theme_type_min_size += icon_size
        theme_type_margin_start = Vector2i(
            theme_type_background.get_margin(SIDE_LEFT),
            theme_type_background.get_margin(SIDE_TOP)
        )
        theme_type_margin_end = Vector2i(
            theme_type_background.get_margin(SIDE_RIGHT),
            theme_type_background.get_margin(SIDE_BOTTOM)
        )
        theme_type_icon_rect = Rect2i(
            theme_type_margin_start,
            icon_size
        )
        theme_type_font = c.get_theme_font("main", "EditorFonts")
        theme_type_font_size = c.get_theme_font_size("main_size", "EditorFonts")
        theme_type_font_color = c.get_theme_color("font_color", "Tree")
        theme_type_font_rect = Rect2i(
            Vector2i(
                theme_type_icon_rect.end.x + separation.x,
                theme_type_margin_start.y + theme_type_font.get_ascent()
            ),
            Vector2i(0, theme_type_font.get_height(theme_type_font_size))
        )
        theme_type_base_type_separator = c.get_theme_icon("arrow_collapsed", "Tree")
        theme_type_base_type_font_color = c.get_theme_color("disabled_font_color", "Editor")
        theme_type_base_type_separator_rect = Rect2i(
            Vector2i(0, theme_type_margin_start.y),
            theme_type_base_type_separator.get_size()
        )

        data_type_background = c.get_theme_stylebox("disabled", "Button")
        data_type_margin_start = Vector2i(
            data_type_background.get_margin(SIDE_LEFT),
            data_type_background.get_margin(SIDE_TOP)
        )
        data_type_margin_end = Vector2i(
            data_type_background.get_margin(SIDE_RIGHT),
            data_type_background.get_margin(SIDE_BOTTOM)
        )
        data_type_icon_rect = Rect2i(
            data_type_margin_start,
            icon_size
        )
        data_type_min_size = data_type_background.get_minimum_size()
        data_type_min_size += icon_size

        theme_item_preview_dark_background = c.get_theme_stylebox("Background", "EditorStyles")
        theme_item_preview_light_background = c.get_theme_stylebox("Content", "EditorStyles")
        theme_item_preview_transparent_background = StyleBoxTexture.new()
        theme_item_preview_transparent_background.texture = c.get_theme_icon("Checkerboard", "EditorIcons")
        theme_item_preview_transparent_background.axis_stretch_horizontal = StyleBoxTexture.AXIS_STRETCH_MODE_TILE
        theme_item_preview_transparent_background.axis_stretch_vertical = StyleBoxTexture.AXIS_STRETCH_MODE_TILE
        theme_item_preview_small_min_size = Vector2i(96, 48) * c.get_theme_default_base_scale()
        theme_item_preview_large_min_size = Vector2i(204, 96) * c.get_theme_default_base_scale()
        theme_item_preview_margin_start = Vector2i(
            theme_item_preview_dark_background.get_margin(SIDE_LEFT),
            theme_item_preview_dark_background.get_margin(SIDE_TOP)
        )
        theme_item_preview_margin_end = Vector2i(
            theme_item_preview_dark_background.get_margin(SIDE_RIGHT),
            theme_item_preview_dark_background.get_margin(SIDE_BOTTOM)
        )

        theme_item_background = c.get_theme_stylebox("normal", "Button")
        theme_item_focus = c.get_theme_stylebox("focus", "Button")
        theme_item_hover = c.get_theme_stylebox("hover", "Button")
        theme_item_selected = c.get_theme_stylebox("pressed", "Button")
        theme_item_selected_focus = c.get_theme_stylebox("pressed", "Button")
        theme_item_cursor = c.get_theme_stylebox("cursor", "Tree")
        theme_item_cursor_unfocused = c.get_theme_stylebox("cursor_unfocused", "Tree")
        theme_item_margin_start = Vector2i(
            theme_item_background.get_margin(SIDE_LEFT),
            theme_item_background.get_margin(SIDE_TOP)
        )
        theme_item_margin_end = Vector2i(
            theme_item_background.get_margin(SIDE_RIGHT),
            theme_item_background.get_margin(SIDE_BOTTOM)
        )
        theme_item_font = c.get_theme_font("main", "EditorFonts")
        theme_item_font_size = c.get_theme_font_size("main_size", "EditorFonts")
        theme_item_font_color = c.get_theme_color("font_color", "Tree")
        theme_item_font_color_selected = c.get_theme_color("font_selected_color", "Tree")
        theme_item_large_font_rect = Rect2i(
            Vector2i(
                theme_item_margin_start.x,
                theme_item_margin_start.y + theme_item_preview_large_min_size.y + separation.y + theme_item_font.get_ascent(theme_item_font_size)
            ),
            Vector2i(
                theme_item_preview_large_min_size.x,
                theme_item_font.get_height(theme_item_font_size)
            )
        )
        theme_item_small_font_rect = Rect2i(
            Vector2i(
                theme_item_margin_start.x,
                theme_item_margin_start.y + theme_item_preview_small_min_size.y + separation.y + theme_item_font.get_ascent(theme_item_font_size)
            ),
            Vector2i(
                theme_item_preview_small_min_size.x,
                theme_item_font.get_height(theme_item_font_size)
            )
        )
        #theme_item_small_min_size: Vector2i
        #theme_item_large_min_size: Vector2i

        # Calculate cell size?
        # columns = floor((Total width - margins - cell_width) / (cell_width + separation)) + 1


    func update_icons_cache() -> void:
        pass


    func update_translation_cache() -> void:
        pass


class _SizeCache extends Object:
    var viewport: Vector2i

    var theme_item_small_size: Vector2i
    var theme_item_small_preview_rect: Rect2i
    var theme_item_small_label_rect: Rect2i
    var theme_item_large_size: Vector2i
    var theme_item_large_preview_rect: Rect2i
    var theme_item_large_label_rect: Rect2i


class ThemeEntity extends Object:
    var rect: Rect2i

    func is_valid() -> bool:
        return false

    func filter(filter : String) -> bool:
        return false


class ThemeGroup extends ThemeEntity:
    var _children: Array[ThemeEntity] = []
    var _valid_children: int = 0

    func _notification(what: int) -> void:
        match what:
            NOTIFICATION_PREDELETE:
                clear()

    func clear() -> void:
        while not _children.is_empty():
            var child: ThemeEntity = _children.pop_back()
            child.free()

    func is_valid() -> bool:
        return _valid_children > 0

    func filter(filter : String) -> bool:
        _valid_children = 0
        for child in _children:
            if child.filter(filter):
                _valid_children += 1
        return _valid_children > 0

class ThemeTypeCache extends Object:
    var background: StyleBox
    var hseparation: int
    var label_font: Font
    var label_font_size: int
    var label_font_color: Color
    var base_type_separator: Texture2D
    var base_type_font_color: Color

    var label_min_size: Vector2i
    var content_start: Vector2i
    var content_end: Vector2i
    var content_min_size: Vector2i
    var icon_y: int
    var label_y: int
    var header_min_size: Vector2i

    func update(c: Control, icon_size: Vector2i) -> void:
        background = c.get_theme_stylebox("title_button_normal", "Tree")
        hseparation = c.get_theme_constant("h_separation", "FlowContainer")
        label_font = c.get_theme_font("main", "EditorFonts")
        label_font_size = c.get_theme_font_size("main_size", "EditorFonts")
        label_font_color = c.get_theme_color("font_color", "Tree")
        base_type_separator = c.get_theme_icon("arrow_collapsed", "Tree")
        base_type_font_color = c.get_theme_color("disabled_font_color", "Editor")

        label_min_size = label_font.get_string_size("...", 0, -1, label_font_size)
        content_start = Vector2i(
            background.get_margin(SIDE_LEFT),
            background.get_margin(SIDE_TOP)
        )
        content_end = Vector2i(
            background.get_margin(SIDE_RIGHT),
            background.get_margin(SIDE_BOTTOM)
        )
        content_min_size = Vector2i(
            icon_size.x * 2 + label_min_size.x * 2 + hseparation * 3,
            max(icon_size.y, label_min_size.y)
        )
        icon_y = content_start.y + (content_min_size.y - icon_size.y) * 0.5
        label_y = content_start.y + (content_min_size.y - label_min_size.y) * 0.5
        header_min_size = Vector2i(
            content_start.x + content_min_size.x + content_end.x,
            content_start.y + content_min_size.y + content_end.y
        )

class ThemeTypeContainer extends ThemeGroup:
    var icon: Texture2D = null
    var theme_type: StringName = StringName()
    var base_type: StringName = StringName()

    var header_rect: Rect2i
    var icon_rect: Rect2i
    var label_rect: Rect2i
    var base_type_separator_rect: Rect2i
    var base_type_rect: Rect2i

    func push(child: DataTypeContainer) -> void:
        _children.push_back(child)

class DataTypeCache extends Object:
    var background: StyleBox
    var icons: Array[Texture2D] = Array()
    var tooltips: Array[String] = Array()

    var header_icon_start: Vector2i
    var header_icon_end: Vector2i
    var header_min_size: Vector2i
    var items_start: Vector2i
    var items_end: Vector2i
    var items_separation: Vector2i

    var small_item_size: Vector2i
    var large_item_size: Vector2i
    var small_columns: int
    var large_columns: int

    func update(c: Control, icon_size: Vector2i) -> void:
        background = c.get_theme_stylebox("disabled", "Button")
        icons.clear()
        icons.append(c.get_theme_icon("Color", "EditorIcons"))
        icons.append(c.get_theme_icon("MemberConstant", "EditorIcons"))
        icons.append(c.get_theme_icon("Font", "EditorIcons"))
        icons.append(c.get_theme_icon("FontSize", "EditorIcons"))
        icons.append(c.get_theme_icon("ImageTexture", "EditorIcons"))
        icons.append(c.get_theme_icon("StyleBoxFlat", "EditorIcons"))
        icons.append(c.get_theme_icon("Theme", "EditorIcons"))

        header_icon_start = Vector2i(
            background.get_margin(SIDE_LEFT),
            background.get_margin(SIDE_TOP)
        )
        header_icon_end = Vector2i(
            background.get_margin(SIDE_RIGHT),
            background.get_margin(SIDE_BOTTOM)
        )
        header_min_size = Vector2i(
            header_icon_start.x + icon_size.x + header_icon_end.x,
            header_icon_end.y + icon_size.y + header_icon_end.y
        )
        items_start = Vector2i(
            c.get_theme_constant("h_separation", "FlowContainer"),
            0
        )
        items_end = Vector2i(
            0,
            0
        )
        items_separation = Vector2i(
            c.get_theme_constant("h_separation", "FlowContainer"),
            c.get_theme_constant("v_separation", "FlowContainer")
        )

    func update_items() -> void:
        pass

    func update_tooltips() -> void:
        tooltips.clear()
        tooltips.append(tr("Colors"))
        tooltips.append(tr("Constants"))
        tooltips.append(tr("Fonts"))
        tooltips.append(tr("Font sizes"))
        tooltips.append(tr("Icons"))
        tooltips.append(tr("Styleboxes"))

class DataTypeContainer extends ThemeGroup:
    var data_type: int = -1
    #var columns: int = -1
    #var rows: int = -1

    var header_rect: Rect2i
    var icon_rect: Rect2i

    func push(child: ThemeItem) -> void:
        _children.push_back(child)


class ThemeItemPreviewCache extends Object:
    var dark_background: StyleBox
    var light_background: StyleBox
    var transparent_background: StyleBox
    var content_start: Vector2i
    var content_end: Vector2i

    var small_min_size: Vector2i
    var large_min_size: Vector2i

class ThemeItemCache extends Object:
    var background: StyleBox
    var focus: StyleBox
    var hover: StyleBox
    var selected: StyleBox
    var selected_focus: StyleBox
    var cursor: StyleBox
    var cursor_unfocused: StyleBox
    var vseparation: int
    var font: Font
    var font_size: int
    var font_color: Color
    var font_color_selected: Color

    var preview_start: Vector2i
    var preview_end: Vector2i
    var label_start: Vector2i
    var label_end: Vector2i

    var small_min_size: Vector2i
    var large_min_size: Vector2i

class ThemeItem extends ThemeEntity:
    var theme_type : StringName = StringName()
    var data_type : int = -1
    var item_name : StringName = StringName()

    var selected: bool = false
    var index: int = -1
    var grid_coordinates: Vector2i


    func filter(filter : String) -> bool:
        return true


    func _get_fields() -> Dictionary:
        return Dictionary()


    func _get_options() -> PackedStringArray:
        return PackedStringArray()


    func _handle_option(idx: int) -> void:
        print(tr("Not implemented!"))


    func _get_list_preview() -> Control:
        return Control.new()


    func _get_detail_preview() -> Control:
        return Control.new()


    func _get_tooltip_preview() -> Control:
        return Control.new()


class ColorItem extends ThemeItem:
    pass


class ConstantItem extends ThemeItem:
    pass


class FontItem extends ThemeItem:
    pass


class FontSizeItem extends ThemeItem:
    pass


class IconItem extends ThemeItem:
    pass


class StyleboxItem extends ThemeItem:
    pass
