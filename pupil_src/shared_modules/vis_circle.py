"""
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2022 Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
"""

from player_methods import transparent_circle
from plugin import Plugin
from pyglui import ui

from methods import denormalize


class Vis_Circle(Plugin):
    uniqueness = "not_unique"
    icon_chr = chr(0xE061)
    icon_font = "pupil_icons"

    def __init__(
        self, g_pool, radius=20, color=(0.0, 0.7, 0.25, 0.2), thickness=2, fill=True
    ):
        super().__init__(g_pool)
        self.order = 0.9

        # initialize empty menu
        self.menu = None

        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.a = color[3]
        self.radius = radius
        self.thickness = thickness
        self.fill = fill

    def recent_events(self, events):
        frame = events.get("frame")
        if not frame:
            return
        if self.fill:
            thickness = -1
        else:
            thickness = self.thickness

        frame_width_height = frame.img.shape[:-1][::-1]
        pts = [
            denormalize(pt["norm_pos"], frame_width_height, flip_y=True)
            for pt in events.get("gaze", [])
            if pt["confidence"] >= self.g_pool.min_data_confidence
        ]

        for pt in pts:
            transparent_circle(
                frame.img,
                pt,
                radius=self.radius,
                color=(self.b, self.g, self.r, self.a),
                thickness=thickness,
            )

    def init_ui(self):
        self.add_menu()
        self.menu.label = "Gaze Circle"
        self.menu.append(
            ui.Slider("radius", self, min=1, step=1, max=100, label="Radius")
        )
        self.menu.append(
            ui.Slider("thickness", self, min=1, step=1, max=15, label="Stroke width")
        )
        self.menu.append(ui.Switch("fill", self, label="Fill"))

        color_menu = ui.Growing_Menu("Color")
        color_menu.collapsed = True
        color_menu.append(
            ui.Info_Text("Set RGB color components and alpha (opacity) values.")
        )
        color_menu.append(
            ui.Slider("r", self, min=0.0, step=0.05, max=1.0, label="Red")
        )
        color_menu.append(
            ui.Slider("g", self, min=0.0, step=0.05, max=1.0, label="Green")
        )
        color_menu.append(
            ui.Slider("b", self, min=0.0, step=0.05, max=1.0, label="Blue")
        )
        color_menu.append(
            ui.Slider("a", self, min=0.0, step=0.05, max=1.0, label="Alpha")
        )
        self.menu.append(color_menu)

    def deinit_ui(self):
        self.remove_menu()

    def get_init_dict(self):
        return {
            "radius": self.radius,
            "color": (self.r, self.g, self.b, self.a),
            "thickness": self.thickness,
            "fill": self.fill,
        }
