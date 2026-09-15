import pytest
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import RichLog

async def test_make_renderable_expand_tabs():
    # Regression test for https://github.com/Textualize/textual/issues/3007
    text_log = RichLog()
    renderable = text_log._make_renderable("\tfoo")
    assert isinstance(renderable, Text)
    assert renderable.plain == "        foo"
@pytest.mark.asyncio
async def test_rich_log_virtual_size_shrinks_on_eviction():
    class LogApp(App):
        def compose(self) -> ComposeResult:
            yield RichLog(max_lines=2, wrap=False)

    app = LogApp()
    async with app.run_test() as pilot:
        log = app.query_one(RichLog)

        # Write an initial very wide line (width = 100)
        log.write("A" * 100)
        await pilot.pause()
        assert log.virtual_size.width >= 100

        # Push two short lines; this evicts the wide line from the buffer
        log.write("Short 1")
        log.write("Short 2")
        await pilot.pause()

        # The ghost scrollbar bug: virtual_size remains 100+ even after wide line is evicted
        # This assert should FAIL right now because the width doesn't shrink back
        assert log.virtual_size.width < 100
        assert log.virtual_size.width == len("Short 1")