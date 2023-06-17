@tool
extends Object

class ListEntity extends Object:
    var rect: Rect2i

    func is_valid() -> bool:
        return false

    func filter(filter : String) -> bool:
        return false

class ListGroup extends ListEntity:
    var _children: Array[ListEntity] = []
    var _valid_children: int = 0

    func _notification(what: int) -> void:
        match what:
            NOTIFICATION_PREDELETE:
                clear()

    func clear() -> void:
        while not _children.is_empty():
            var child: ListEntity = _children.pop_back()
            child.free()

    func get_child_count() -> int:
        return _children.size()

    func is_valid() -> bool:
        return _valid_children > 0

    func get_valid_child_count() -> int:
        return _valid_children

    func filter(filter: String) -> bool:
        _valid_children = 0
        for child in _children:
            if child.filter(filter):
                _valid_children += 1
        return _valid_children > 0

class ThemeTypeGroup extends ListGroup:
    var theme_type: StringName = StringName()
    var base_type: StringName = StringName()

    func push(child: DataTypeGroup) -> void:
        _children.push_back(child)

class DataTypeGroup extends ListGroup:
    var data_type: int = -1

    var header_rect: Rect2i
    var icon_rect: Rect2i

    func push(child: ThemeItemEntity) -> void:
        _children.push_back(child)

class ThemeItemEntity extends ListEntity:
    var theme_type : StringName = StringName()
    var data_type : int = -1
    var item_name : StringName = StringName()

    var selected: bool = false
    var index: int = -1
    var grid_coordinates: Vector2i
