from __future__ import annotations

from typing import TYPE_CHECKING

import ba
from bastd.ui.popup import PopupWindow

if TYPE_CHECKING:
    from typing import Any, Sequence


class HubCheatWindow(PopupWindow):
    """A mini window that assists players on spawning random stuff"""

    def __init__(
        self,
        parent: ba.Widget,
        position: tuple[float, float],
        delegate: Any = None,
        scale: float | None = None,
        offset: tuple[float, float] = (0.0, 0.0),
        bgcolor: tuple[float, float, float] = (0, 0, 0),
    ):
        uiscale = ba.app.ui.uiscale
        if scale is None:
            scale = (
                2.3
                if uiscale is ba.UIScale.SMALL
                else 1.65 if uiscale is ba.UIScale.MEDIUM else 1.23
            )
        self._parent = parent
        self._position = position
        self._scale = scale
        self._offset = offset
        self._delegate = delegate
        self._transitioning_out = False

        # Create our _root_widget.
        PopupWindow.__init__(
            self,
            position=position,
            size=(210, 240),
            scale=scale,
            focus_position=(10, 10),
            focus_size=(190, 220),
            bg_color=bgcolor,
            offset=offset,
            bypassbse=True,
        )

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            if self._delegate is not None:
                self._delegate.color_picker_closing(self)
            ba.containerwidget(edit=self.root_widget, transition="out_scale")

    def on_popup_cancel(self) -> None:
        if not self._transitioning_out:
            ba.playsound(ba.getsound("swish"))
        self._transition_out()
