from __future__ import annotations

from typing import TYPE_CHECKING

import _ba

if TYPE_CHECKING:
    from typing import Sequence
    import ba

def show_bottom_zoom_message(
    self,
    message: ba.Lstr,
    color: Sequence[float] = (0.9, 0.4, 0.0),
    trailcolor: Sequence[float] = (0.9, 0.4, 0.0),
    scale: float = 0.8,
    duration: float = 2.0,
    trail: bool = False,
) -> None:
    
    """ Shows a zooming text at the bottom side of the screen.
        Used for multiple silly things! """
    from bastd.actor.zoomtext import ZoomText
    
    i = 0
    cur_time = _ba.time()
    while True:
        if (
            i not in self._zoom_message_times
            or self._zoom_message_times[i] < cur_time
        ):
            self._zoom_message_times[i] = cur_time + duration
            break
        i += 1
    ZoomText(
        message,
        lifespan=duration,
        jitter=2.0,
        position=(0, -230 - i * 20),
        scale=scale,
        maxwidth=800,
        trail=trail,
        color=color,
    ).autoretain()