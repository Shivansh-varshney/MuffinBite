from prompt_toolkit.completion import WordCompleter, PathCompleter, Completer

command_completer = WordCompleter(['build', 'send', 'init', 'exit', 'help', 'reset', 'camp', 'config'])
path_completer = PathCompleter()

class HybridCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        if text.startswith('!'):
            yield from path_completer.get_completions(document, complete_event)
        else:
            yield from command_completer.get_completions(document, complete_event)