from dataclasses import dataclass
from collections import Counter
import typing as t


## PART ONE


class Game:
    num_rolls = 0

    def dice_roll(self) -> int:
        self.num_rolls += 1
        return self.num_rolls

    def play(self, players):
        while True:
            for p in players:
                total_roll = sum(self.dice_roll() for _ in range(3))
                p.position = (p.position + total_roll) % 10 or 10
                p.score += p.position
                if p.score >= 1000:
                    return


@dataclass
class Player:
    position: int
    score: int = 0

    def __hash__(self):
        return hash((self.position, self.score))


def part_one():
    g = Game()
    p1 = Player(position=10)
    p2 = Player(position=9)
    g.play(players=(p1, p2))
    min_score = min((p1.score, p2.score))
    result = min_score * g.num_rolls
    assert result == 918081
    return result


# PART TWO


def dice_frequencies():
    freqs = []
    for r1 in (1, 2, 3):
        for r2 in (1, 2, 3):
            for r3 in (1, 2, 3):
                freqs.append(r1 + r2 + r3)
    return Counter(freqs)


DICE_FREQS = dice_frequencies()


@dataclass
class GameState:
    players: t.Tuple

    def __hash__(self):
        return hash(self.players)

    def is_complete(self):
        return self.winner() is not None

    def winner(self):
        for i, player in enumerate(self.players):
            if player.score >= 21:
                return i
        return None


def dirac_player_round(player: Player):
    outcomes = Counter()
    for roll, freq in DICE_FREQS.items():
        new_pos = ((player.position + roll) % 10) or 10
        new_score = player.score + new_pos
        new_player = Player(position=new_pos, score=new_score)
        outcomes[new_player] += freq
    return outcomes


def dirac_round(game_state):
    possible_outcomes_p0 = dirac_player_round(game_state.players[0])
    possible_outcomes_p1 = dirac_player_round(game_state.players[1])
    possible_game_states = Counter()
    for p0_state, freq0 in possible_outcomes_p0.items():
        if p0_state.score >= 21:  # player 0 wins, halt the round
            gs = GameState(players=(p0_state, game_state.players[1]))
            possible_game_states[gs] += freq0
        else:
            for p1_state, freq1 in possible_outcomes_p1.items():
                gs = GameState(players=(p0_state, p1_state))
                possible_game_states[gs] += freq0 * freq1
    return possible_game_states


def dirac(players):
    initial_game_state = GameState(players=players)
    uncompleted_games = Counter({initial_game_state: 1})
    completed_games = Counter()
    while uncompleted_games:
        # print(len(uncompleted_games), len(completed_games))
        new_uncompleted_games = Counter()
        for prior_game_state, prior_game_freq in uncompleted_games.items():
            outcomes = dirac_round(prior_game_state)
            for new_game_state, new_game_freq in outcomes.items():
                if new_game_state.is_complete():
                    completed_games[new_game_state] += prior_game_freq * new_game_freq
                else:
                    new_uncompleted_games[new_game_state] += prior_game_freq * new_game_freq
        uncompleted_games = new_uncompleted_games
    return completed_games


def count_wins(games: Counter) -> Counter:
    wins = Counter()
    for game, freq in games.items():
        wins[game.winner()] += freq
    return wins


def part_two():
    p1 = Player(position=10)
    p2 = Player(position=9)

    completed_games = dirac(players=(p1, p2))
    wins = count_wins(completed_games)
    return max(wins.values())


def test():
    g = Game()
    p1 = Player(position=4)
    p2 = Player(position=8)
    g.play(players=(p1, p2))
    min_score = min((p1.score, p2.score))
    assert min_score == 745, min_score
    assert g.num_rolls == 993, g.num_rolls

    p1 = Player(position=4)
    p2 = Player(position=8)
    completed_games = dirac(players=(p1, p2))
    wins = count_wins(completed_games)
    assert max(wins.values()) == 444356092776315, max(wins.values())


if __name__ == "__main__":
    test()
    print("Part One:", part_one())
    print("Part Two:", part_two())
#
