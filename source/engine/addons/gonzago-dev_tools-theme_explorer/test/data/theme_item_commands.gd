@tool
extends RefCounted

const ThemeItem := preload("./theme_item.gd")

enum CommandFlags {
    SHOW_IN_CONTEXT = 1,
    SHOW_IN_DETAIL = 2,
    DEFERRED = 4,
    DEFAULT = 3
}

enum CommandIcon {
    NONE = 0,
    COPY = 1
}

class Command extends RefCounted:
    var _label: String
    var _icon: CommandIcon
    var _flags: CommandFlags

    var label: String:
        get: return _label
    var icon: CommandIcon:
        get: return _icon
    var flags: CommandFlags:
        get: return flags

    func _init(
        label: String,
        icon: CommandIcon = CommandIcon.NONE,
        flags: CommandFlags = CommandFlags.DEFAULT
    ) -> void:
        _label = label
        _icon = icon
        _flags = flags

    func execute() -> void:
        print("Not implemented!")

    func has_flags(flags: CommandFlags) -> bool:
        return (_flags & flags) == flags

class CallableCommand extends Command:
    var _callable: Callable

    func _init(
        label: String,
        callable: Callable,
        icon: CommandIcon = CommandIcon.NONE,
        flags: CommandFlags = CommandFlags.DEFAULT
    ) -> void:
        super._init(label, icon, flags)
        _callable = callable

    func execute() -> void:
        if not is_instance_valid(_callable) or not _callable.is_valid():
            print("Whoopsie!")
        _callable.call()

class CopyCommand extends Command:
    var _copy_buffer: String

    func _init(
        label: String,
        copy_buffer: String,
        flags: CommandFlags = CommandFlags.DEFAULT
    ):
        super._init(label, CommandIcon.COPY, flags)
        _copy_buffer = copy_buffer

    func execute() -> void:
        DisplayServer.clipboard_set(_copy_buffer)
        print('Copied to clipboard: %s' % _copy_buffer)

class SnippetCommand extends CopyCommand:
    func _init(
        snippet: String,
        prefix: String = "Copy ",
        flags: CommandFlags = CommandFlags.DEFAULT
    ):
        super._init(tr(prefix) + snippet, snippet, flags)

static func get_command_list(
    theme: Theme,
    theme_item: ThemeItem,
    flags: CommandFlags = CommandFlags.DEFAULT
) -> Array[Command]:
    if is_instance_valid(theme_item):
        return []
    match theme_item._data_type:
        Theme.DATA_TYPE_COLOR:
            return get_color_command_list(
                theme,
                theme_item.name,
                theme_item.theme_type,
                flags
            )
        Theme.DATA_TYPE_CONSTANT:
            return get_constant_command_list(
                theme,
                theme_item.name,
                theme_item.theme_type,
                flags
            )
        Theme.DATA_TYPE_FONT:
            return get_font_command_list(
                theme,
                theme_item.name,
                theme_item.theme_type,
                flags
            )
        Theme.DATA_TYPE_FONT_SIZE:
            return get_font_size_command_list(
                theme,
                theme_item.name,
                theme_item.theme_type,
                flags
            )
        Theme.DATA_TYPE_ICON:
            return get_icon_command_list(
                theme,
                theme_item.name,
                theme_item.theme_type,
                flags
            )
        Theme.DATA_TYPE_STYLEBOX:
            return get_stylebox_command_list(
                theme,
                theme_item.name,
                theme_item.theme_type,
                flags
            )
        _:
            return []

static func get_color_command_list(
    theme: Theme,
    name: StringName,
    theme_type: StringName,
    flags: CommandFlags = CommandFlags.DEFAULT
) -> Array[Command]:
    if (
        flags == 0
        or not is_instance_valid(theme)
        or not theme.has_theme_item(
            Theme.DATA_TYPE_COLOR,
            name,
            theme_type
        )
    ):
        return []

    var result: Array[Command] = []
    return result

static func get_constant_command_list(
    theme: Theme,
    name: StringName,
    theme_type: StringName,
    flags: CommandFlags = CommandFlags.DEFAULT
) -> Array[Command]:
    if (
        flags == 0
        or not is_instance_valid(theme)
        or not theme.has_theme_item(
            Theme.DATA_TYPE_CONSTANT,
            name,
            theme_type
        )
    ):
        return []

    var result: Array[Command] = []
    return result

static func get_font_command_list(
    theme: Theme,
    name: StringName,
    theme_type: StringName,
    flags: CommandFlags = CommandFlags.DEFAULT
) -> Array[Command]:
    if (
        flags == 0
        or not is_instance_valid(theme)
        or not theme.has_theme_item(
            Theme.DATA_TYPE_FONT,
            name,
            theme_type
        )
    ):
        return []

    var result: Array[Command] = []
    return result

static func get_font_size_command_list(
    theme: Theme,
    name: StringName,
    theme_type: StringName,
    flags: CommandFlags = CommandFlags.DEFAULT
) -> Array[Command]:
    if (
        flags == 0
        or not is_instance_valid(theme)
        or not theme.has_theme_item(
            Theme.DATA_TYPE_FONT_SIZE,
            name,
            theme_type
        )
    ):
        return []

    var result: Array[Command] = []
    return result

static func get_icon_command_list(
    theme: Theme,
    name: StringName,
    theme_type: StringName,
    flags: CommandFlags = CommandFlags.DEFAULT
) -> Array[Command]:
    if (
        flags == 0
        or not is_instance_valid(theme)
        or not theme.has_theme_item(
            Theme.DATA_TYPE_ICON,
            name,
            theme_type
        )
    ):
        return []

    var result: Array[Command] = []
    return result

static func get_stylebox_command_list(
    theme: Theme,
    name: StringName,
    theme_type: StringName,
    flags: CommandFlags = CommandFlags.DEFAULT
) -> Array[Command]:
    if (
        flags == 0
        or not is_instance_valid(theme)
        or not theme.has_theme_item(
            Theme.DATA_TYPE_STYLEBOX,
            name,
            theme_type
        )
    ):
        return []

    var result: Array[Command] = []
    return result
