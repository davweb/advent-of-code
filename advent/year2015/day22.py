# -*- coding: utf-8 -*-
# pylint: disable=too-many-instance-attributes

HIT_POINTS = 51
DAMAGE = 9


class State:
    def __init__(self, hard_mode):
        self.hard_mode = hard_mode
        self.player_hp = 50
        self.mana = 500
        self.boss_hp = HIT_POINTS
        self.shield_turns = 0
        self.poison_turns = 0
        self.recharge_turns = 0
        self.spend = 0

    def copy(self):
        other = State(self.hard_mode)
        other.player_hp = self.player_hp
        other.mana = self.mana
        other.boss_hp = self.boss_hp
        other.shield_turns = self.shield_turns
        other.poison_turns = self.poison_turns
        other.recharge_turns = self.recharge_turns
        other.spend = self.spend

        return other

    def start_turn(self):
        if self.shield_turns > 0:
            self.shield_turns -= 1

        if self.poison_turns > 0:
            self.boss_hp -= 3
            self.poison_turns -= 1

        if self.recharge_turns > 0:
            self.mana += 101
            self.recharge_turns -= 1

        return self.boss_hp > 0

    def boss_turn(self):
        if not self.start_turn():
            return False

        armour = 7 if self.shield_turns > 0 else 0
        self.player_hp -= (DAMAGE - armour)

        return True

    def cast(self, cost):
        if self.mana < cost:
            return False

        self.mana -= cost
        self.spend += cost
        return True

    def missile(self):
        if self.cast(53):
            self.boss_hp -= 4
            return True

        return False

    def drain(self):
        if self.cast(73):
            self.boss_hp -= 2
            self.player_hp += 2
            return True

        return False

    def shield(self):
        if self.shield_turns == 0 and self.cast(113):
            self.shield_turns = 6
            return True

        return False

    def poison(self):
        if self.poison_turns == 0 and self.cast(173):
            self.poison_turns = 6
            return True

        return False

    def recharge(self):
        if self.recharge_turns == 0 and self.cast(229):
            self.recharge_turns = 5
            return True

        return False

    def next_turns(self):
        turns = []

        for action in (State.missile, State.drain, State.shield, State.poison, State.recharge):
            next_turn = self.copy()

            if next_turn.hard_mode:
                next_turn.player_hp -= 1

                if next_turn.player_hp <= 0:
                    continue

            if next_turn.start_turn() and not action(next_turn):
                continue

            next_turn.boss_turn()

            if next_turn.player_hp > 0:
                turns.append(next_turn)

        return turns


def play_game(hard_mode):
    best = None
    queue = [State(hard_mode)]

    while queue:
        turn = queue.pop()

        if best is not None and best <= turn.spend:
            continue

        if turn.boss_hp <= 0:
            if best is None or best > turn.spend:
                best = turn.spend
            continue

        for next_turn in turn.next_turns():
            queue.append(next_turn)

    return best


def part1():
    """
    >>> part1()
    900
    """

    return play_game(False)


def part2():
    """
    >>> part2()
    1216
    """

    return play_game(True)


def main():
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
