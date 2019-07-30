import random


ROLES = ('boomer', 'doomer', 'zoomer', 'bloomer')
STATS = ('finance', 'tech', 'social', 'sanity')
ACTIONS = (
    {'finance': 0, 'tech': 0, 'social': 0, 'sanity': -1},   # X
    {'finance': 0, 'tech': 0, 'social': 0, 'sanity': 1},    # A
    {'finance': 1, 'tech': 0, 'social': 0, 'sanity': 0},    # 2
    {'finance': 0, 'tech': 1, 'social': 0, 'sanity': 0},    # 3
    {'finance': 0, 'tech': 0, 'social': 1, 'sanity': 0},    # 4
    {'finance': -1, 'tech': 0, 'social': 1, 'sanity': 0},   # 5
    {'finance': -1, 'tech': 1, 'social': 0, 'sanity': 0},   # 6
    {'finance': 1, 'tech': 0, 'social': -1, 'sanity': 0},   # 7
    {'finance': 0, 'tech': 1, 'social': -1, 'sanity': 0},   # 8
    {'finance': 1, 'tech': -1, 'social': 0, 'sanity': 0},   # 9
    {'finance': 0, 'tech': -1, 'social': 1, 'sanity': 0},   # 10
    {'finance': 0, 'tech': 0, 'social': 0, 'sanity': 0},    # J
    {'finance': -1, 'tech': -1, 'social': -1, 'sanity': -1},    # Q
    {'finance': 1, 'tech': 1, 'social': 1, 'sanity': 1},    # K
)
TARGETS = {
    'boomer': [None, None, None, None, 'doomer', None, None, 'bloomer', 'zoomer', None, None, None, None, None],
    'doomer': [None, None, None, None, None, 'bloomer', None, 'boomer', None, None, None, None, None, None],
    'zoomer': [None, None, None, None, None, 'doomer', None, 'boomer', None, None, None, None, None, None],
    'bloomer': [None, None, None, None, None, 'zoomer', None, 'boomer', None, None, None, None, None, None],
}
MAX_STAT = 10


class Player(object):
    finance = 0
    tech = 0
    social = 0
    sanity = 0
    win = False
    win_by = 'n/a'
    out = False

    def __init__(self, finance, tech, social, sanity):
        self.finance = finance
        self.tech = tech
        self.social = social
        self.sanity = sanity

    def add_stat(self, stat, amount):
        self.__dict__[stat] += amount

    def get_stat(self, stat):
        return self.__dict__[stat]

    def set_stat(self, stat, amount):
        self.__dict__[stat] = amount


class PeakMillenial(object):
    def __init__(self, subtract_from_others=False):
        self.subtract_from_others = subtract_from_others
        self.draw = False
        self.turn = 0
        self.deck = [0, 0] + (list(range(0, 14)) * 4)
        random.shuffle(self.deck)
        self.players = {
            'boomer': Player(1, 0, 0, 1),
            'doomer': Player(0, 0, 0, -2),
            'zoomer': Player(0, 1, 0, 1),
            'bloomer': Player(0, 0, 1, 1),
        }
        for role in ROLES:
            for stat in STATS:
                self.players[role].add_stat(stat, random.randint(1, 13))
                if stat == 'sanity':
                    self.players[role].set_stat(stat, max(1, self.players[role].get_stat(stat)))
                else:
                    self.players[role].set_stat(stat, min(MAX_STAT - 1, self.players[role].get_stat(stat)))

    def run(self):
        curr = 0
        for self.turn in range(0, len(self.deck)):
            card = self.deck[self.turn]
            curr_action = ACTIONS[card]
            curr_player = self.players[ROLES[curr]]
            target_role = TARGETS[ROLES[curr]][card]
            curr = (curr + 1) % 4
            target = self.players[target_role if target_role is not None else ROLES[curr]]
            for stat in STATS:
                curr_player.add_stat(stat, curr_action[stat])
                if self.deck[self.turn] == 0:
                    continue
                if self.subtract_from_others and stat != 'sanity':
                    target.add_stat(stat, -curr_action[stat])
            target.add_stat('sanity', -1)
            if self.check_endgame():
                return
        self.draw = True

    def check_endgame(self):
        out_count = 0
        for role in ROLES:
            player = self.players[role]
            #if ((player.finance == 0 and player.social == 0) or
            #        (player.finance == 0 and player.tech == 0) or
            #        (player.social == 0 and player.tech == 0)):
            if (player.finance == 0 or player.social == 0 or player.tech == 0):
                player.out == True
            if player.out:
                out_count += 1
                continue
            if player.sanity == 0:
                if self.turn == 0:
                    player.out = True
                    continue
                player.win = True
                player.win_by = 'sanity'
                return True
            if ((player.finance == MAX_STAT and player.social == MAX_STAT) or
                    (player.finance == MAX_STAT and player.tech == MAX_STAT) or
                    (player.social == MAX_STAT and player.tech == MAX_STAT)):
                if self.turn == 0:
                    player.out = True
                    continue
                player.win_by = 'max_stat'
                player.win = True
                return True
                player.win = True
        if out_count == 3:
            self.draw = True
            return True
        return False


def test(runs=100, subtract_from_others=False):
    games = []
    average_players = {
        'boomer': Player(0,0,0,0),
        'doomer': Player(0,0,0,0),
        'zoomer': Player(0,0,0,0),
        'bloomer': Player(0,0,0,0),
    }
    wins = {
        'boomer': 0,
        'doomer': 0,
        'zoomer': 0,
        'bloomer': 0,
    }
    wins_by = {
        'sanity': 0,
        'max_stat': 0,
    }
    outs = {
        'boomer': 0,
        'doomer': 0,
        'zoomer': 0,
        'bloomer': 0,
    }
    all_turns = 0
    max_turns = -1
    min_turns = 53
    draws = 0
    for i in range(0, runs):
        game = PeakMillenial(subtract_from_others=subtract_from_others)
        game.run()
        games.append(game)
        all_turns += game.turn + 1
        max_turns = max(game.turn + 1, max_turns)
        min_turns = min(game.turn + 1, min_turns)
        if game.draw:
            draws += 1
        for role in ROLES:
            player = game.players[role]
            for stat in STATS:
                average_players[role].add_stat(stat, player.get_stat(stat))
            if player.win:
                wins[role] += 1
                wins_by[player.win_by] += 1
            if player.out:
                outs[role] += 1
    turns = {
        'avg': all_turns / runs,
        'max': max_turns,
        'min': min_turns,
    }
    wins_by['sanity'] = float(wins_by['sanity']) / float(runs)
    wins_by['max_stat'] = float(wins_by['max_stat']) / float(runs)
    for role in ROLES:
        wins[role] = float(wins[role]) / float(runs)
        outs[role] = float(outs[role]) / float(runs)
        for stat in STATS:
            average_players[role].set_stat(stat, average_players[role].get_stat(stat) / runs)
    print('''
Peak Millenial play test results
================================

Settings
--------

* *Number of runs:* {runs}
* *Subtract from others:* {subtract_from_others}

Turns per game
----------------------

Min | Average | Max
----|---------|----
{turns[min]: >3} | {turns[avg]: >7} | {turns[max]: >3}

Draws
-----

*Draws:* {draws}

Wins
----

Boomer | Doomer | Zoomer | Bloomer
-------|--------|--------|--------
{wins[boomer]: >6.2%} | {wins[doomer]: >6.2%} | {wins[zoomer]: >6.2%} | {wins[bloomer]: >7.2%}

Wins by
-------

Sanity | Max stats
-------|----------
{wins_by[sanity]: >6.2%} | {wins_by[max_stat]: >9.2%}

Outs
----

Boomer | Doomer | Zoomer | Bloomer
-------|--------|--------|--------
{outs[boomer]: >6.2%} | {outs[doomer]: >6.2%} | {outs[zoomer]: >6.2%} | {outs[bloomer]: >7.2%}

Average stats
-------------

*Stat*        | Boomer | Doomer | Zoomer | Bloomer
--------------|--------|--------|--------|--------
Finances      | {avg[boomer].finance: >6} | {avg[doomer].finance: >6} | {avg[zoomer].finance: >6} | {avg[bloomer].finance: >7}
Technology    | {avg[boomer].tech: >6} | {avg[doomer].tech: >6} | {avg[zoomer].tech: >6} | {avg[bloomer].tech: >7}
Social credit | {avg[boomer].social: >6} | {avg[doomer].social: >6} | {avg[zoomer].social: >6} | {avg[bloomer].social: >7}
Sanity        | {avg[boomer].sanity: >6} | {avg[doomer].sanity: >6} | {avg[zoomer].sanity: >6} | {avg[bloomer].sanity: >7}
'''.format(
        runs=runs,
        subtract_from_others=subtract_from_others,
        turns=turns,
        draws=draws,
        wins=wins,
        wins_by=wins_by,
        outs=outs,
        avg=average_players))


if __name__ == '__main__':
    #test(runs=10000)
    test(runs=10000, subtract_from_others=True)
