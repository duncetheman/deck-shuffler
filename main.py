from dataclasses import dataclass
import random
from bakery import assert_equal
from drafter import *
from deckfunctions import *

set_website_title("SUPER DUPER DECK SHUFFLER")
set_site_information(
    author="Henry Parker",
    description="Shuffle, modify, and deal from a virtual deck.",
    sources="Drafter docs and my cisc class",
    planning=[],
    links=[]
)
hide_debug_information()
set_website_framed(False)



@dataclass
class State:
    current_deck: list[Card]
    current_hand: list[Card]
    card_view_index: int
    operations_tally: int
    status: str
    
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("SUPER DUPER DECK SHUFFLER !!!!"),
        Button("Begin", "deck_screen"),
        Button("Info", "info"),
        ])

@route
def info(state: State) -> Page:
    return Page(state, [
        Header("About this site"),
        "info goes here or smtn",
        "\n",
        Button("Homepage", "index"),
        Button("Deck screen", "deck_screen")
        ])

@route
def deck_screen(state: State) -> Page:
    return Page(state, [
        Button("Info","info"),
        #Button("Overview","overview"),
        Button("Simple shuffle","simple_shuffle_b"),
        Button("Complex shuffle","complex_shuffle_b"),
        Button("Reset deck", "reset"),
        "\n",
        str(state.card_view_index + 1) + " / " + str(len(state.current_deck)),
        "\n",
        str(get_name(state.current_deck[state.card_view_index]))
        #create_ascii_art(state.current_deck[state.card_view_index]),
        "\n",
        TextBox("new_index",state.card_view_index+1),
        Button("Go to card", "go_to_card"),
        Button("<---","prevcard"),
        Button("--->","nextcard"),
        #TextBox("# cards to deal", hand_size),
        #Button("Deal cards","hand"),
        ])

@route
def reset(state:State) -> Page:
    state.current_deck = generate_standard_deck()
    state.operations_tally = 0
    return deck_screen(state)

@route
def overview(state:State) -> Page:
    return index(state)

@route
def hand(state:State) -> Page:
    return index(state)

@route
def simple_shuffle_b(state:State) -> Page:
    state.current_deck = simple_shuffle(state.current_deck)
    return deck_screen(state)

@route
def complex_shuffle_b(state:State) -> Page:
    state.current_deck = complex_shuffle(state.current_deck)
    return deck_screen(state)

@route
def prevcard(state:State) -> Page:
    state.card_view_index -= 1
    if state.card_view_index < 1:
        state.card_view_index = len(state.current_deck) - 1
    return deck_screen(state)

@route
def nextcard(state:State) -> Page:
    state.card_view_index += 1
    if state.card_view_index > len(state.current_deck) - 1:
        state.card_view_index = 0
    return deck_screen(state)

@route
def go_to_card(state:State, new_index: str) -> Page:
    #use try/except here to test if the given new index value is actually an int
    #best way i found to restrict a text field to only ints
    try:
        print(int(new_index))
    except ValueError:
        state.status = "Error: not a number!"
        return deck_screen(state)
    new_index = int(new_index)
    if isinstance(new_index, int):
        if len(state.current_deck) < new_index-1:
            state.card_view_index = len(state.current_deck)-1
        elif new_index-1 < 0:
            state.card_view_index = 0
        else:
            state.card_view_index = new_index-1
    return deck_screen(state)
    



start_server(State(generate_standard_deck(), [], 0, 0, ""))
