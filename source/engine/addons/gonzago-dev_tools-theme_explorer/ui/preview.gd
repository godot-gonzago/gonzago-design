@tool
extends RefCounted


static func get_list_item_preview() -> Control:
    return PanelContainer.new()


static func get_tooltip_preview() -> Control:
    return PanelContainer.new()


static func get_detail_preview() -> Control:
    return PanelContainer.new()
