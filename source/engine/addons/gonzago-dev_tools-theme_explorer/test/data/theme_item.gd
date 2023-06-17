@tool
extends RefCounted


var _data_type: int
var _name: StringName
var _theme_type: StringName


var data_type: int:
    get: return _data_type
var name: StringName:
    get: return _name
var theme_type: StringName:
    get: return _theme_type


func _init(data_type: int, name: StringName, theme_type: StringName) -> void:
    _data_type = data_type
    _theme_type = theme_type
    _name = name


func is_in_theme(theme: Theme) -> bool:
    return (
        is_instance_valid(theme)
        and theme.has_theme_item(_data_type, _name, _theme_type)
    )
