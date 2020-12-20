# -*- coding: utf-8 -*-

import regex as re


LETTER_RULE_PATTERN = re.compile(r'^(\d+): "([ab])"$', re.M)
SINGLE_RULE_PATTERN = re.compile(r"^(\d+): (\d+)$", re.M)
DOUBLE_RULE_PATTERN = re.compile(r"^(\d+): (\d+) (\d+)$", re.M)
TRIPLE_RULE_PATTERN = re.compile(r"^(\d+): (\d+) (\d+) (\d+)$", re.M)
OR_RULE_PATTERN = re.compile(r"^(\d+): (\d+) \| (\d+)$", re.M)
DOUBLE_OR_RULE_PATTERN = re.compile(r"^(\d+): (\d+) (\d+) \| (\d+) (\d+)$", re.M)
MESSAGE_PATTERN = re.compile(r"^([ab]+)$", re.M)


class RuleBook:
    """
    >>> rules = RuleBook('0: 4 1 5\\n1: 2 3 | 3 2\\n2: 4 4 | 5 5\\n3: 4 5 | 5 4\\n4: "a"\\n5: "b"\\n)')
    >>> str(rules[4])
    'a'
    >>> str(rules[5])
    'b'
    >>> str(rules[2])
    '(aa|bb)'
    >>> str(rules[3])
    '(ab|ba)'
    >>> str(rules[1])
    '((aa|bb)(ab|ba)|(ab|ba)(aa|bb))'
    >>> str(rules[0])
    'a((aa|bb)(ab|ba)|(ab|ba)(aa|bb))b'
    >>> messages = ['ababbb', 'bababa', 'abbbab', 'aaabbb', 'aaaabbb']
    >>> zero = rules[0]
    >>> sum(1 for message in messages if zero.matches_string(message))
    2
    """

    def __init__(self, text):
        self.rules = {}

        for groups in LETTER_RULE_PATTERN.findall(text):
            self.rules[int(groups[0])] = LetterRule(self, groups[1])

        for groups in SINGLE_RULE_PATTERN.findall(text):
            self.rules[int(groups[0])] = SingleRule(self, int(groups[1]))
        
        for groups in DOUBLE_RULE_PATTERN.findall(text):
            self.rules[int(groups[0])] = DoubleRule(self, int(groups[1]), int(groups[2]))
        
        for groups in TRIPLE_RULE_PATTERN.findall(text):
            self.rules[int(groups[0])] = TripleRule(self, int(groups[1]), int(groups[2]), int(groups[3]))

        for groups in OR_RULE_PATTERN.findall(text):
            self.rules[int(groups[0])] = OrRule(self, int(groups[1]), int(groups[2]))

        for groups in DOUBLE_OR_RULE_PATTERN.findall(text):
            self.rules[int(groups[0])] = DoubleOrRule(self, int(groups[1]), int(groups[2]), int(groups[3]), int(groups[4]))


    def __getitem__(self, item):
        return self.rules[item]


    def __setitem__(self, item, value):
        self.rules[item] = value

    
    def reset(self):
        for rule in self.rules.values():
            rule.reset()


class Rule:
    def __init__(self, rulebook):
        self.rulebook = rulebook
        self.value = None
        self.regex = None


    def reset(self):
        self.value = None
        self.regex = None


    def get_value(self):
        if self.value is None:
            self.value = self.resolve()

        return self.value


    def __str__(self):
        return self.get_value()


    def matches_string(self, string_value):
        if self.regex is None:
            self.regex = re.compile(self.get_value())

        return self.regex.fullmatch(string_value) is not None


class LetterRule(Rule):
    def __init__(self, rulebook, letter):
        super().__init__(rulebook) 
        self.letter = letter


    def resolve(self):
        return self.letter


class CombiningRule(Rule):
    def __init__(self, rulebook, format_string, rules):
        super().__init__(rulebook) 
        self.format_string = format_string
        self.rules = rules
    

    def resolve(self):
        values = [self.rulebook[rule].get_value() for rule in self.rules]
        return self.format_string.format(*values)


class SingleRule(Rule):
    def __init__(self, rulebook, rule_id):
        super().__init__(rulebook) 
        self.rule_id = rule_id


    def resolve(self):
        rule = self.rulebook[self.rule_id]
        return rule.get_value()


class DoubleRule(CombiningRule):
    def __init__(self, rulebook, *rules):
        super().__init__(rulebook, "{}{}", rules) 


class TripleRule(CombiningRule):
    def __init__(self, rulebook, *rules):
        super().__init__(rulebook, "{}{}{}", rules) 


class OrRule(CombiningRule):
    def __init__(self, rulebook, *rules):
        super().__init__(rulebook, "({}|{})", rules) 


class DoubleOrRule(CombiningRule):
    def __init__(self, rulebook, *rules):
        super().__init__(rulebook, "({}{}|{}{})", rules) 


def read_input():
    file = open('input/2020/day19-input.txt', 'r')
    text = file.read()
    rules = RuleBook(text)
    return (rules, MESSAGE_PATTERN.findall(text))


def part1(data):
    """
    >>> part1(read_input())
    203
    """

    (rules, messages) = data
    zero = rules[0] 
    return sum(1 for message in messages if zero.matches_string(message))


def part2(data):
    """
    >>> part2(read_input())
    304
    """
    
    (rules, messages) = data
    rules[8] = CombiningRule(rules, "(?P<eight>{}|{}(?&eight))", [42, 42])
    rules[11] = CombiningRule(rules, "(?P<eleven>{}{}|{}(?&eleven){})", [42, 31, 42, 31])
    zero = rules[0] 
    return sum(1 for message in messages if zero.matches_string(message))


def main():
    data = read_input()
    print(part1(data))
    data[0].reset()
    print(part2(data))


if __name__ == "__main__":
    main()
