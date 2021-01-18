from rich.console import Console, ConsoleOptions, RenderGroup, RenderResult
from rich.segment import Segment
from rich.color import Color
from rich.measure import Measurement
from rich.pretty import Pretty
from rich.style import Style
import colorsys


def __rich_console__(
        console: Console, options: ConsoleOptions
) -> RenderResult:
    for y in range(0, 1):
        for x in range(options.max_width):
            h = x / options.max_width
            l = 0.1 + ((y / 5) * 0.7)
            r1, g1, b1 = colorsys.hls_to_rgb(h, l, 1.0)
            r2, g2, b2 = colorsys.hls_to_rgb(h, l + 0.7 / 10, 1.0)
            bgcolor = Color.from_rgb(r1 * 255, g1 * 255, b1 * 255)
            color = Color.from_rgb(r2 * 255, g2 * 255, b2 * 255)
            yield Segment("▄", Style(color=color, bgcolor=bgcolor))
        yield Segment.line()


class ColorBox:

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        return Measurement(1, max_width)
