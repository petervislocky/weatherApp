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
            return None

        full_ascii = art.to_ascii(columns=50)

        return full_ascii.split('\n')
    
    except OSError as e:
        print(f'Error occured {e} ')
        return None