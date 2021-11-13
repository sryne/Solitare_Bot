import pyautogui
import pandas as pd
import os

""" 
Scroll feature idea: Use blue selected cell from last unshare to scroll x numbers of scrolls. Stop after scroll_loops
 is satisfied. OR scroll until blue is gone?
"""


def solitaire():
    # Initialize deck
    df_cards = pd.DataFrame({'Card': ['As', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', 'Js', 'Qs', 'Ks',
                                      'Ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', 'Jc', 'Qc', 'Kc',
                                      'Ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', 'Jd', 'Qd', 'Kd',
                                      'Ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', 'Jh', 'Qh', 'Kh'],

                             'Color': ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',
                                       'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',
                                       'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',
                                       'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'],

                             'Value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                       1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                       1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                       1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],

                             'X-Coord': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

                             'Y-Coord': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

                             'Scored?': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    # Locate cards on screen
    for filename in os.listdir(r'C:\Deck of Cards'):
        if filename.endswith(".JPG"):
            file = 'C:/Deck of Cards/' + filename
            loc = pyautogui.locateOnScreen(file, grayscale=True, confidence=0.95)

        if loc is not None:
            located_card = filename.split('.', 1)[0]
            center_loc = pyautogui.locateCenterOnScreen(file, confidence=0.95, grayscale=True, region=loc)

            pyautogui.moveTo(center_loc)  # Debug assist

            df_cards.loc[df_cards['Card'] == located_card, 'X-Coord'] = center_loc.x
            df_cards.loc[df_cards['Card'] == located_card, 'Y-Coord'] = center_loc.y

            df_cards.loc[(df_cards['X-Coord'] > 850) & (df_cards['Y-Coord'] < 325), 'Scored?'] = 1

    df_cards = df_cards.sort_values(['X-Coord', 'Y-Coord'])  # Debug assist

    # Make all possible moves/scores
    for i, card in df_cards.iterrows():
        goal_sites = [[960, 210], [1130, 210], [1290, 210], [1450, 210]]

        # Don't touch cards that have scored
        if card['Scored?'] == 1 or card['X-Coord'] == 0:
            continue

        # Brute force score attempt
        for goal in goal_sites:
            pyautogui.moveTo(x=card['X-Coord'], y=card['Y-Coord'])
            pyautogui.dragTo(x=goal[0], y=goal[1], duration=1, button='left')
            pyautogui.leftClick(x=1800, y=200)

            file = 'C:/Deck of Cards/' + card['Card'] + '.JPG'
            new_loc = pyautogui.locateOnScreen(file, grayscale=True, confidence=0.95)
            new_center_loc = pyautogui.locateCenterOnScreen(file, confidence=0.95, grayscale=True, region=new_loc)

            # Has the card scored?
            if new_center_loc.y != card['Y-Coord']:
                card['Scored?'] = 1
                continue

        # Make a move
        for j, move in df_cards.iterrows():
            required_card = card['Value'] + 1
            if move['X-Coord'] != 0:
                if card['Color'] != move['Color']:
                    if move['Value'] == required_card:
                        pyautogui.moveTo(x=card['X-Coord'], y=card['Y-Coord'])
                        pyautogui.dragTo(x=move['X-Coord'], y=move['X-Coord'], duration=1, button='left')
                        pyautogui.leftClick(x=1800, y=200)


solitaire()
print("Done!")
