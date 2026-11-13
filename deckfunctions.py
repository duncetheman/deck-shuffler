from dataclasses import dataclass
import random
from bakery import assert_equal



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


print(create_ascii_art(Card("spades",12)))
