import ascii_magic

from typing import Optional


def ascii_icon(icon_url: str) -> Optional[str]:
    '''
    Takes icon(png) url as params and return ascii art of the png
    '''
    try:
        art = ascii_magic.from_url('https:' + icon_url)

        if not art:
            print('Error occured, ASCII art could not be generated')

        return art.to_terminal(columns=50)
    
    except OSError as e:
        print(f'Error occured {e} ')
        return None