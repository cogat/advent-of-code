from typing import Tuple


class Probe:
    target_x: Tuple[int, int]
    target_y: Tuple[int, int]

    def __init__(self, target_x: Tuple, target_y: Tuple):
        self.target_x = target_x
        self.target_y = target_y

    def is_in_target_x(self, position):
        return self.target_x[0] <= position[0] <= self.target_x[1]

    def is_in_target_y(self, position):
        return self.target_y[0] <= position[1] <= self.target_y[1]

    def is_in_target(self, position):
        return self.is_in_target_x(position) and self.is_in_target_y(position)

    def missed_target(self, position):
        return position[1] < self.target_y[0]

    def fire(self, x_vel: int, y_vel: int):
        max_y = 0
        position = [0, 0]
        while True:
            position[0] += x_vel
            position[1] += y_vel
            if x_vel > 0:
                x_vel -= 1
            elif x_vel < 0:
                x_vel += 1
            y_vel -= 1
            max_y = max(max_y, position[1])
            # print(position)
            if self.is_in_target(position):
                # print("HIT", position)
                return True, max_y
            if self.missed_target(position):
                # print("MISS", position)
                return False, max_y


def part_one():
    p = Probe(target_x=(241, 275), target_y=(-75, -49))
    # Max y height is aided by min x velocity
    max_y = 0

    for y_vel in range(72, 75):
        for x_vel in range(0, 1000):
            hit, my = p.fire(x_vel, y_vel)
            if hit:
                max_y = max(max_y, my)
                print(f"{y_vel} -> {max_y}")

    return max_y


def part_two():
    p = Probe(target_x=(241, 275), target_y=(-75, -49))
    velocities = set()

    for y_vel in range(-75, 75):
        for x_vel in range(1, 1000):
            vector = (x_vel, y_vel)
            hit, my = p.fire(*vector)
            if hit:
                print(vector)
                velocities.add(vector)

    return len(velocities)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
