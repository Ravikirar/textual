try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'pip install httpx' ")

from rich.json import JSON

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Static


class DictionaryApp(App):
    """Searches a dictionary API as-you-type."""

    CSS_PATH = "dictionary.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a word")
        yield VerticalScroll(Static(id="results"), id="results-container")

    def on_input_changed(self, message: Input.Changed) -> None:
        """Handle a changed input value."""
        self.lookup_word(message.value)

    @work(exclusive=True)
    async def lookup_word(self, word: str) -> None:
        """Look up a word in a worker."""
        results_widget = self.query_one("#results", Static)
        if not word:
            results_widget.update()
            return

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        async with httpx.AsyncClient() as client:
            results = (await client.get(url)).text

        results_widget.update(JSON(results))


if __name__ == "__main__":
    app = DictionaryApp()
    app.run()
