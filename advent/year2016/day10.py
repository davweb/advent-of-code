# -*- coding: utf-8 -*-

import re

PATTERN_BOT = re.compile(r'bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)')
PATTERN_VALUE = re.compile(r'value (\d+) goes to bot (\d+)')

def read_input():
    output = []

    with open('input/2016/day10-input.txt', encoding='utf8') as file:
        for line in file.readlines():
            if match := PATTERN_BOT.match(line):
                output.append((
                    'bot', int(match.group(1)),
                    match.group(2), int(match.group(3)),
                    match.group(4), int(match.group(5))
                ))
            elif match := PATTERN_VALUE.match(line):
                output.append(('value', int(match.group(1)), int(match.group(2))))
            else:
                raise ValueError(f'Did not match "{line}"')

    return output


class Bot:
    all_bots = {}
    outputs = {}

    @classmethod
    def get(_, bot_id):
        if bot_id in Bot.all_bots:
            return Bot.all_bots[bot_id]

        bot = Bot()
        Bot.all_bots[bot_id] = bot
        return bot

    def __init__(self):
        self.values = []
        self.low = None
        self.low_id = None
        self.high = None
        self.high_id = None

    def route(self, low, low_id, high, high_id):
        self.low = low
        self.low_id = low_id
        self.high = high
        self.high_id = high_id
        self.__process()

    def add_value(self, value):
        self.values.append(value)
        self.__process()

    @classmethod
    def __send(_, destination, destination_id, value):
        match destination:
            case 'output':
                Bot.outputs[destination_id] = value
            case 'bot':
                Bot.get(destination_id).add_value(value)
            case _:
                raise ValueError(destination)

    def __process(self):
        if len(self.values) != 2 or self.low is  None or self.high is None:
            return

        self.values = sorted(self.values)
        Bot.__send(self.low, self.low_id, self.values[0])
        Bot.__send(self.high, self.high_id, self.values[1])

    @classmethod
    def find_by_values(_, *values):
        for bot_id, bot in Bot.all_bots.items():
            if all(v in bot.values for v in values):
                return bot_id

        return None


def part1and2(data):
    """
    >>> part1and2(read_input())
    (56, 7847)
    """

    for line in data:
        if line[0] == 'value':
            (value, bot_id) = line[1:3]
            Bot.get(bot_id).add_value(value)
        elif line[0] == 'bot':
            Bot.get(line[1]).route(*line[2:6])
        else:
            raise ValueError(line)

    return (Bot.find_by_values(61, 17), Bot.outputs[0] * Bot.outputs[1] * Bot.outputs[2])


def main():
    data = read_input()
    print(part1and2(data))


if __name__ == "__main__":
    main()
