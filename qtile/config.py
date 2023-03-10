import os
import subprocess

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy


mod = "mod4"
terminal = "kitty"
browser = "brave-browser"
filemanager = "kitty -T -x ranger"


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [mod, "control"], "h",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide", "monadthreecol"]),
        desc="Grow window to the left"
    ),
    Key(
        [mod, "control"], "l",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide", "monadthreecol"]),
        desc="Grow window to the right"
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.grow_down().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide", "monadthreecol"]),
        desc="Grow window down"
    ),
    Key(
        [mod, "control"], "k",
        lazy.layout.grow_up().when(layout=["bsp", "columns"]), 
        lazy.layout.shrink().when(layout=["monadtall", "monadwide", "monadthreecol"]),
        desc="Grow window up"
    ),
    Key([mod], "n", lazy.layout.reset(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Apps
    Key(
        [mod], "b",
        lazy.spawn(browser),
        desc="Browser"
    ),
    Key(
        [mod], "f",
        lazy.spawn(filemanager),
        desc="Filemanager"
    ),

    # Sys
    Key([], "XF86AudioRaiseVolume",lazy.spawn("amixer set Master 3%+")),
    Key([], "XF86AudioLowerVolume",lazy.spawn("amixer set Master 3%-")),
    Key([], "XF86AudioMute",lazy.spawn("amixer set Master toggle")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight +5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -5")),
    Key(
        ["shift"], "alt_l",
        lazy.widget["keyboardlayout"].next_keyboard(),
        desc="Next keyboar layout"
    )
]


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )


border_focus = "5b2e99"
border_normal = "1f1232"

layout_settings = {
    "border_width": 1,
    "margin": 0,
    "border_focus": border_focus,
    "border_normal": border_normal,
}

layouts = [
    layout.MonadTall(**layout_settings),
    layout.Max(**layout_settings),
    layout.Columns(**layout_settings),
    # layout.Stack(num_stacks=2, **layout_settings),
    # layout.Bsp(**layout_settings),
    # layout.Matrix(**layout_settings),
    # layout.MonadWide(**layout_settings),
    # layout.RatioTile(**layout_settings),
    # layout.Tile(**layout_settings),
    # layout.TreeTab(**layout_settings),
    # layout.VerticalTile(**layout_settings),
    # layout.Zoomy(**layout_settings),
    layout.Floating(**layout_settings),
]

widget_defaults = dict(
    font="Jet Brains Mono",
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()

sep_config = {
    "foreground": border_focus,        
    "size_percent": 100
}

widgets = [
    widget.CurrentLayoutIcon(scale=0.7),
    widget.Sep(**sep_config),
    widget.GroupBox(
        margin_x=3,
        padding_y=0.7,
        rounded=True,
        this_current_screen_border="5b2e99",
        highlight_method="border",
        hide_unused=True,
    ),

    widget.Sep(**sep_config),
    widget.Prompt(),
    widget.WindowName(format="{name}", empty_group_string="no active windows"),

    widget.Sep(**sep_config),
    widget.Systray(
        icon_size=20,
        padding = 4
    ),
    widget.Volume(fmt=" Vol: {} "),
    widget.Battery(format="Bat: {percent:2.0%} "),

    widget.Sep(**sep_config),
    widget.TextBox(text = " CPU:"),
    widget.CPUGraph(
        line_width=1,
        border_color="5b2e99",
        border_width=1,
        graph_color="abaaab",
        type="line",
    ),
    widget.TextBox(text = " RAM:"),
    widget.MemoryGraph(
        line_width=1,
        border_color="5b2e99",
        border_width=1,
        graph_color="abaaab",
        type="line",
    ),

    widget.Sep(**sep_config),
    widget.KeyboardLayout(
        configured_keyboards=["de qwerty", "ru"],
        fmt=" Lay: {} "
    ),

    widget.Sep(**sep_config),
    widget.Clock(format=" %b %d - %H:%M "),
]

screens = [
    Screen(
        bottom=bar.Bar(
            widgets,
            22,
            background="#111213",
            border_width=[1, 1, 1, 1],  # Draw top and bottom borders
            border_color=[border_focus for _ in range(4)] # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
