@tool
extends "./entity.gd"

var theme_type : StringName = StringName()
var data_type : int = -1
var item_name : StringName = StringName()

var selected: bool = false
var index: int = -1
var grid_coordinates: Vector2i
