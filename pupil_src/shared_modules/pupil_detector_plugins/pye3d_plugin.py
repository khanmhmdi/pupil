"""
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2020 Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
"""
import logging

from pye3d.eyemodel import EyeModel_V2 as EyeModel
from pyglui import ui

from .detector_base_plugin import PupilDetectorPlugin
from .visualizer_2d import draw_eyeball_outline, draw_pupil_outline
from .visualizer_3d import Eye_Visualizer

logger = logging.getLogger(__name__)


class Pye3DPlugin(PupilDetectorPlugin):
    uniqueness = "by_class"
    icon_font = "pupil_icons"
    icon_chr = chr(0xEC19)

    label = "Pye3D"

    def __init__(self, g_pool):
        super().__init__(g_pool)
        self.detector = EyeModel()
        self.debugVisualizer3D = Eye_Visualizer(
            g_pool, self.detector.settings["focal_length"]
        )

    def detect(self, frame, pupil_data):
        for datum in pupil_data:
            if datum.get("method", "") == "2d c++":
                datum_2d = datum
                break
        else:
            return None

        return None

        datum_2d["raw_edges"] = []
        result = self.detector.update_and_detect(
            datum_2d, debug_toggle=self.is_debug_window_open
        )

        eye_id = self.g_pool.eye_id
        result["timestamp"] = frame.timestamp
        result["topic"] = f"pupil.{eye_id}"
        result["id"] = eye_id
        result["method"] = "3d c++"

        return result

    @classmethod
    def parse_pretty_class_name(cls) -> str:
        return "Pye3D Detector"

    def init_ui(self):
        super().init_ui()
        self.menu.label = self.pretty_class_name

        self.menu.append(ui.Button("Reset 3D model", self.reset_model))
        self.menu.append(ui.Button("Open debug window", self.debug_window_toggle))

        # self.menu.append(
        #     ui.Switch(TODO, label="Freeze model")
        # )

    def gl_display(self):
        self.debug_window_update()
        if self._recent_detection_result:
            draw_eyeball_outline(self._recent_detection_result)
            draw_pupil_outline(self._recent_detection_result)

    def cleanup(self):
        self.debug_window_close()  # if we change detectors, be sure debug window is also closed

    # Public

    def reset_model(self):
        self.detector.reset_model()

    # Debug window management

    @property
    def is_debug_window_open(self) -> bool:
        return self.debugVisualizer3D.window is not None

    def debug_window_toggle(self):
        if not self.is_debug_window_open:
            self.debug_window_open()
        else:
            self.debug_window_close()

    def debug_window_open(self):
        if not self.is_debug_window_open:
            self.debugVisualizer3D.open_window()

    def debug_window_close(self):
        if self.is_debug_window_open:
            self.debugVisualizer3D.close_window()

    def debug_window_update(self):
        if self.is_debug_window_open:
            pass
            # TODO
            # self.debugVisualizer3D.update_window(
            #     self.g_pool, self.detector_3d.debug_result
            # )