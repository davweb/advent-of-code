# -*- coding: utf-8 -*-


def read_input():
    file = open("input/2020/day22-input.txt", "r")
    text = file.read()
    data = []

    for player in text.split("\n\n"):
        cards = []

        for line in player.split("\n"):
            if line.startswith("Player") or line == "":
                continue

            cards.append(int(line))

        data.append(cards)

    return data


def score(deck):
    return sum((i + 1) * card for i, card in enumerate(reversed(deck)))


def part1(data):
    """
    >>> part1(read_input())
    31455
    """

    deck_one = list(data[0])
    deck_two = list(data[1])

    while len(deck_one) > 0 and len(deck_two) > 0:
        card_one = deck_one.pop(0)
        card_two = deck_two.pop(0)

        if card_one > card_two:
            deck_one.append(card_one)
            deck_one.append(card_two)
        else:
            deck_two.append(card_two)
            deck_two.append(card_one)

    winning_deck = deck_one if len(deck_two) == 0 else deck_two
    return score(winning_deck)


def combat(deck_one, deck_two):
    history = []

    while len(deck_one) > 0 and len(deck_two) > 0 and (deck_one, deck_two) not in history:
        history.append((deck_one, deck_two))

        card_one = deck_one[0]
        card_two = deck_two[0]
        deck_one = deck_one[1:]
        deck_two = deck_two[1:]

        if len(deck_one) >= card_one and len(deck_two) >= card_two:
            winner, _ = combat(deck_one[:card_one], deck_two[:card_two])
        elif card_one > card_two:
            winner = 1
        else:
            winner = 2

        if winner == 1:
            deck_one += (card_one, card_two)
        else:
            deck_two += (card_two, card_one)

    # This also handles the repeat case
    if len(deck_one) == 0:
        return(2, deck_two)
    else:
        return(1, deck_one)


def part2(data):
    """
    >>> part2([[43, 19], [2, 29, 14]])
    105
    >>> part2([[9, 2, 6, 3, 1], [5, 8, 4, 7, 10]])
    291
    >>> part2(read_input())
    32528
    """

    deck_one = tuple(data[0])
    deck_two = tuple(data[1])

    _, winning_deck = combat(deck_one, deck_two)
    return score(winning_deck)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
