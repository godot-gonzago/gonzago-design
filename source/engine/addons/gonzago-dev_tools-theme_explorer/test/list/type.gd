@tool
extends "./group.gd"

const DataType := preload("./data_type.gd")

var icon: Texture2D = null
var theme_type: StringName = StringName()
var base_type: StringName = StringName()

var header_rect: Rect2i
var icon_rect: Rect2i
var label_rect: Rect2i
var base_type_separator_rect: Rect2i
var base_type_rect: Rect2i

func push(child: DataType) -> void:
    _children.push_back(child)
