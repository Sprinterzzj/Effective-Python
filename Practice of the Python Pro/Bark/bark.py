from src.command import command


class Option(object):
    def __init__(self, name:str, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call # The optional preparation step to call before executing the command.
    
    def choose(self):
        data = self.prep_call() if self.prep_call is not None else None 

        if data is not None:
            message = self.command.execute(data)
        else:
            message = self.command.execute()
        print(message)
    
    def __str__(self):
        return self.name

def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) ({option})')
    print()

def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options

def get_option_choice(options):
    choice = input('Choose an option: ')
    while option_choice_is_valid(choice, options) != True:
        print('Invalid choice.')
        choice = input('Choose an option: ')
    return options[choice.upper()]

if __name__ == "__main__":
    command.CreateBookmarksTable().execute()
    options = {
        'A' : Option('Add a bookmark', command.AddBookmark()),
        'B' : Option('List bookmarks by date', command.ListBookmarks()),
        'T' : Option('List bookmarks by title', command.ListBookmarks(order_by='title')),
        'D' : Option('Delete a bookmark', command.DeleteBookmark()),
        'Q' : Option('Quit', command.Quit())

    }
    print_options(options)