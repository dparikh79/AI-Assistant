import time
import random

def human_like_typing(response_text, max_delay=0.1, typo_chance=0.02):
    """
    Simulate human-like typing.
    
    Parameters:
    - response_text: The text to be "typed out".
    - max_delay: The maximum delay between characters.
    - typo_chance: Probability of making a typo.
    """
    
    i = 0
    while i < len(response_text):
        char = response_text[i]
        
        # Introduce a typo with a given probability
        if random.random() < typo_chance:
            typo = random.choice('abcdefghijklmnopqrstuvwxyz')
            print(typo, end='', flush=True)
            time.sleep(max_delay)
            
            # Simulate backspacing to correct the typo
            print('\b \b', end='', flush=True)
            time.sleep(max_delay)
        else:
            print(char, end='', flush=True)
            i += 1
        
        # Variable delay based on character and context
        if char in [',', ';', ':']:
            time.sleep(max_delay * 2)
        elif char == '.':
            time.sleep(max_delay * 3)
        else:
            time.sleep(random.uniform(0.01, max_delay))
    
    print()  # Move to the next line after typing

response = ("This is a sample response to demonstrate human-like typing. "
            "Notice the variable speed, occasional typos, and contextual pauses.")
human_like_typing(response)
