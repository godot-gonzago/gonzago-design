@tool
extends "./group.gd"

const ThemeItem := preload("./item.gd")

var data_type: int = -1
#var columns: int = -1
#var rows: int = -1

var header_rect: Rect2i
var icon_rect: Rect2i

func push(child: ThemeItem) -> void:
    _children.push_back(child)
