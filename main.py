from dataclasses import dataclass
import random
from bakery import assert_equal
from drafter import *


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


@dataclass
class Card:
    suit: str
    number: int



def generate_standard_deck() -> list[Card]:
    # i considered writing this function easier than making a constant list of a standard deck myself.
    # i mean, i could probably just copy its output, make it said constant and delete this function
    # but this is probably shorter anyway
    deck = []
    for i in range(4):
        suit = ["diamonds", "hearts", "clubs", "spades"][i]
        for j in range(13):
            deck.append(Card(suit, j+1))
    return(deck)


    
def get_symbol(card: Card) -> str:
    if card.number == 1:
        return "Ace"
    if card.number >= 11:
        return ["Jack","Queen","King"][card.number-11]
    else:
        return str(card.number)
    
assert_equal(get_symbol(Card("diamonds",1)),"Ace")
assert_equal(get_symbol(Card("diamonds",12)),"Queen")
assert_equal(get_symbol(Card("diamonds",5)),"5")
    
def get_name(card: Card) -> str:
    return get_symbol(card) + " of " + card.suit.title()

assert_equal(get_name(Card("spades",1)),"Ace of Spades")

def get_color(card: Card) -> str:
    if card.suit.lower() in ["diamonds","hearts"]:
        return "red"
    else:
        return "black"
    
assert_equal(get_color(Card("diamonds",6)),"red")
assert_equal(get_color(Card("spades",6)),"black")
 
def remove_cards(deck: list[Card], amount: int, position:str) -> list[Card]:
    # position can be "start" or "end"
    if amount >= len(deck):
        return []
    if position == "start":
        return deck[amount:]
    if position == "end":
        return deck[:len(deck)-amount]
    
def simple_shuffle(deck:list[Card]) -> list[Card]:
    # totally randomizes location of cards in deck
    # impossible to unit test
    newDeck = deck
    random.shuffle(newDeck)
    return newDeck
                

def complex_shuffle(deck:list[Card]) -> list[Card]:
    # split the deck into two half-decks, and integrate the half-decks into each other one card after another
    if not deck:
        return []
    newDeck = []
    midpoint = len(deck) // 2
    half1 = deck[:midpoint]
    half2 = deck[midpoint:]
    for index, card in enumerate(half1):
        newDeck.append(card)
        if index <= len(half2) - 1:
            newDeck.append(half2[index])
    return newDeck

assert_equal(complex_shuffle([
    Card("spades",1),
    Card("spades",2),
    Card("spades",3),
    Card("spades",4),]),[
        Card("spades",1),
        Card("spades",3),
        Card("spades",2),
        Card("spades",4),])
    
def deal_cards(deck:list[Card],hand_size:int) -> list[Card]:
    # returns first the hand of how ever many cards, and second the new deck with said cards removed
    if not deck:
        return [], []
    hand = deck[:hand_size]
    newDeck = deck[hand_size:]
    return hand, newDeck
    
def remove_card(deck:list[Card], index:int) -> list[Card]:
    return deck[:index] + deck[index+1:]

def create_ascii_art(card:Card) -> str:
    
    CARD_ASCII_1 ="""┌-------------┐\n
|"""
    CARD_ASCII_2 ="""            |\n
|             |\n
|             |\n
|             |\n
|      """
    CARD_ASCII_3 ="""      |\n
|             |\n
|             |\n
|             |\n
|             |\n
|            """
    CARD_ASCII_4 = """|\n
└-------------┘"""
    
    
    number = get_symbol(card)[0]
    suit = ["♢","♡","♧","♤"][["diamonds", "hearts", "clubs", "spades"].index(card.suit)]
    return CARD_ASCII_1 + number + CARD_ASCII_2 + suit + CARD_ASCII_3 + number + CARD_ASCII_4

assert_equal(remove_card([Card("clubs",5),Card("clubs",8),Card("clubs",2),Card("clubs",13),],2),
             [Card("clubs",5),Card("clubs",8),Card("clubs",13),])



    
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
        str(get_name(state.current_deck[state.card_view_index])),
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
