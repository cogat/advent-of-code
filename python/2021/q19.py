import aocd
from dataclasses import dataclass, field
import typing as t
import numpy as np
import re
from ast import literal_eval


class Beacon:
    coords: np.array

    def __init__(self, coords):
        self.coords = np.array(coords, int)

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def z(self):
        return self.coords[2]

    def __eq__(self, other):
        return tuple(self.coords) == tuple(other.coords)

    def __str__(self):
        return str(tuple(self.coords))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(tuple(self.coords))

    def __add__(self, other):
        return Beacon(self.coords + other.coords)

    def __sub__(self, other):
        return Beacon(self.coords - other.coords)

    def normalize(self, origin: "Beacon"):
        return self - origin


@dataclass
class Scanner:
    id: int
    is_normalized = False
    beacons: t.Set[Beacon] = field(default_factory=set)
    origin = None

    def reoriented_beacon_sets(
        self,
    ):
        # return sets of beacons rotated according to all possible orientations
        rotmatrices = [
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
            ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
            ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
            ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
            ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
            ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
            ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
            ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
            ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
            ((0, 0, 1), (0, -1, 0), (1, 0, 0)),
            ((0, 0, 1), (-1, 0, 0), (0, -1, 0)),
            ((0, 0, -1), (1, 0, 0), (0, -1, 0)),
            ((0, 0, -1), (0, 1, 0), (1, 0, 0)),
            ((0, 0, -1), (0, -1, 0), (-1, 0, 0)),
            ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
            ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
            ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
            ((0, -1, 0), (0, 0, -1), (1, 0, 0)),
            ((0, -1, 0), (-1, 0, 0), (0, 0, -1)),
            ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),
            ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
            ((-1, 0, 0), (0, 0, -1), (0, -1, 0)),
            ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),
        ]
        for matrix in rotmatrices:
            yield [Beacon(np.round(np.dot(matrix, b.coords))) for b in self.beacons]

    def try_to_align(self, other: "Scanner", threshold=12, test=False):
        assert (
            other.is_normalized
        ), "This scanner should only be aligned with already normalised scanners"
        assert not self.is_normalized, "This scanner should not already be normalized"

        for beacon_set in self.reoriented_beacon_sets():
            for origin_beacon in other.beacons:
                for test_beacon in beacon_set:
                    normalised_beacons = {
                        b.normalize(test_beacon - origin_beacon) for b in beacon_set
                    }
                    num_overlaps = len(other.beacons & normalised_beacons)

                    if num_overlaps >= threshold:
                        if not test:
                            self.beacons = normalised_beacons
                            self.is_normalized = True
                            self.origin = test_beacon - origin_beacon
                        return num_overlaps
        return 0


def create_scanners_from_input(input):
    scanners = []
    scanner = None
    scanner_id = 0
    for line in input.splitlines():
        if not line:
            scanners.append(scanner)
            scanner_id += 1
            continue
        start_scanner = re.match(r"--- scanner (\d+) ---", line)
        if start_scanner:
            scanner = Scanner(id=scanner_id)
        else:
            coords = literal_eval(f"({line})")
            scanner.beacons.add(Beacon(coords))
    scanners.append(scanner)
    return scanners


def align_scanners(scanners):
    assert any(
        scanner.is_normalized for scanner in scanners
    ), "At least one scanner must be normalized by default"

    normalized_points = beacon_union([s for s in scanners if s.is_normalized])
    normalized_megascanner = Scanner(id=-1, beacons=normalized_points)
    normalized_megascanner.is_normalized = True
    normalized_megascanner.origin = Beacon([0, 0, 0])

    while any(not scanner.is_normalized for scanner in scanners):
        for scanner in [s for s in scanners if not s.is_normalized]:
            print(f"Align {scanner.id}")
            possibly_aligned = scanner.try_to_align(normalized_megascanner)
            if possibly_aligned:  # have a closer look
                print("...aligned")
                normalized_megascanner.beacons |= scanner.beacons


def beacon_union(aligned_scanners):
    united_beacons = set()
    for scanner in aligned_scanners:
        united_beacons |= scanner.beacons

    return united_beacons


def tasks(input):
    scanners: t.List[Scanner] = create_scanners_from_input(input)
    scanners[0].is_normalized = True
    scanners[0].origin = Beacon([0, 0, 0])
    align_scanners(scanners)
    return len(beacon_union(scanners)), manhattan(scanners)


def manhattan(scanners):
    MM = 0
    for i in range(len(scanners)):
        b = scanners[i]
        for j in range(i):
            b2 = scanners[j]
            mm = (
                abs(b.origin.x - b2.origin.x)
                + abs(b.origin.y - b2.origin.y)
                + abs(b.origin.z - b2.origin.z)
            )
            MM = max(MM, mm)
    return MM


def test():
    s = Scanner(id=0, beacons={Beacon([1, 2, 3])})
    rots = list(s.reoriented_beacon_sets())
    assert len(rots) == 24, rots

    s1 = Scanner(id=1, beacons={Beacon([1, 2, 3]), Beacon([3, 2, 1])})
    s1.is_normalized = True
    s2 = Scanner(id=2, beacons={Beacon([2, 3, 4]), Beacon([4, 3, 2]), Beacon([0, 0, 0])})
    alignments = s2.try_to_align(s1, threshold=2)
    assert alignments == 2, alignments
    # s2 is now normalised:
    assert s2.is_normalized
    assert Beacon([1, 2, 3]) in s2.beacons
    assert Beacon([3, 2, 1]) in s2.beacons
    s3 = Scanner(id=3, beacons={Beacon([-2, 3, -4]), Beacon([-4, 3, -2])})
    alignments = s3.try_to_align(s1, threshold=2)
    assert alignments == 2, alignments

    input = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
    part1, part2 = tasks(input)
    assert part1 == 79, part1
    assert part2 == 3621, part2


if __name__ == "__main__":
    test()
    input = aocd.get_data(day=19, year=2021)
    print(tasks(input))
