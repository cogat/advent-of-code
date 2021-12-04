import utils
from typing import List, Optional
import aocd
from dataclasses import dataclass, field


@dataclass
class BingoNumber:
    number: int
    picked: bool = False


@dataclass
class BingoBoard:
    last_number_picked: Optional[int] = None
    has_won: bool = False
    numbers: List[List[BingoNumber]] = field(default_factory=list)  # row, col

    def is_winner(self) -> bool:
        for row in range(5):
            if all(self.numbers[row][x].picked for x in range(5)):
                self.has_won = True
                return True
        for col in range(5):
            if all(self.numbers[x][col].picked for x in range(5)):
                self.has_won = True
                return True

        return False

    def add_row(self, row: str):
        self.numbers.append([BingoNumber(number=int(n)) for n in row.split()])

    def pick_number(self, number: int) -> bool:
        for row in range(5):
            for col in range(5):
                if self.numbers[row][col].number == number:
                    self.numbers[row][col].picked = True
                    self.last_number_picked = number
                    return True
        return False

    def unmarked_numbers(self):
        for row in range(5):
            for col in range(5):
                if self.numbers[row][col].picked == False:
                    yield self.numbers[row][col].number


def part_one(data) -> int:
    picked_numbers = [int(d) for d in data[0].split(",")]
    boards: List[BingoBoard] = []
    for line in data[1:]:
        if line.strip() == "":
            boards.append(BingoBoard())
        else:
            boards[-1].add_row(line)

    for number in picked_numbers:
        for board in boards:
            board.pick_number(number)
            if board.is_winner():
                return number * sum(board.unmarked_numbers())


def part_two(data) -> int:
    picked_numbers = [int(d) for d in data[0].split(",")]
    boards: List[BingoBoard] = []
    for line in data[1:]:
        if line.strip() == "":
            boards.append(BingoBoard())
        else:
            boards[-1].add_row(line)

    last_board_to_win = None
    for number in picked_numbers:
        for board in boards:
            if board.has_won:
                continue
            board.pick_number(number)
            if board.is_winner():
                last_board_to_win = board

    return last_board_to_win.last_number_picked * sum(last_board_to_win.unmarked_numbers())


if __name__ == "__main__":
    data = aocd.get_data(day=4, year=2021).splitlines()
    print(part_one(data))
    print(part_two(data))
