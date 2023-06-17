@tool
extends "./entity.gd"

const ThemeEntity := preload("./entity.gd")

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

func child_count() -> int:
    return _children.size()

func is_valid() -> bool:
    return _valid_children > 0

func valid_child_count() -> int:
    return _valid_children

func filter(filter : String) -> bool:
    _valid_children = 0
    for child in _children:
        if child.filter(filter):
            _valid_children += 1
    return _valid_children > 0
