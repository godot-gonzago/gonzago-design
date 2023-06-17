@tool
extends RefCounted


const _DATA_TYPES: Dictionary = {}


static func get_data_type_data(data_type: int) -> DataTypeData:
    if not _DATA_TYPES.has(data_type):
        Engine.get_main_loop().root
    return _DATA_TYPES[data_type]



class DataTypeData extends RefCounted:
    var data_type: int

    func _init() -> void:
        pass


class DataTypeUtil extends RefCounted:
    static func get_editor_icons_name(data_type: int) -> StringName:
        match data_type:
            Theme.DATA_TYPE_COLOR:
                return "Color"
            Theme.DATA_TYPE_CONSTANT:
                return "MemberConstant"
            Theme.DATA_TYPE_FONT:
                return "Font"
            Theme.DATA_TYPE_FONT_SIZE:
                return "FontSize"
            Theme.DATA_TYPE_ICON:
                return "ImageTexture"
            Theme.DATA_TYPE_STYLEBOX:
                return "StyleBoxFlat"
        return "Theme"

    static func get_tooltip_base_string(data_type: int) -> StringName:
        match data_type:
            Theme.DATA_TYPE_COLOR:
                return "Colors"
            Theme.DATA_TYPE_CONSTANT:
                return "Constants"
            Theme.DATA_TYPE_FONT:
                return "Fonts"
            Theme.DATA_TYPE_FONT_SIZE:
                return "Font sizes"
            Theme.DATA_TYPE_ICON:
                return "Icons"
            Theme.DATA_TYPE_STYLEBOX:
                return "Styleboxes"
        return ""


class ThemeItemFactory extends RefCounted:
    static func get_theme_item_data(
            theme: Theme,
            data_type: int,
            theme_type: StringName,
            name: StringName
    ) -> ThemeItem:
        return null


class ThemeItem extends RefCounted:
    var _theme: Theme
    var _type: StringName
    var _name: StringName

    func _init(theme: Theme, type: StringName, name: StringName) -> void:
        _theme = theme
        _type = type
        _name = name

    func get_theme() -> Theme:
        return _theme

    func get_type() -> StringName:
        return _type

    func get_name() -> StringName:
        return _name

    func get_data_type() -> int:
        return _get_data_type()

    func _get_data_type() -> int:
        return -1

    # TODO: Filtering?
    # TODO: Control generation?

    func has_item(theme: Theme) -> bool:
        return (
            is_instance_valid(theme)
            and theme.has_theme_item(_get_data_type(), _name, _type)
        )
