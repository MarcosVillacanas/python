from collections import defaultdict
from collections import Counter
from functools import reduce
import operator

merge_points = defaultdict(list)


def detect_connexions(edges, identifier):
    global merge_points
    for e in edges:
        if e in merge_points:
            merge_points[e].append(identifier)
        else:
            merge_points[e] = [identifier]


line = input()
while line != "":
    title = ""
    tile = ""
    while line != "":
        if "Tile" in line:
            title = line
        else:
            tile += line
        line = input()

    top = tile[:10]
    reverse_top = top[::-1]
    bottom = tile[-10:]
    reverse_bottom = bottom[::-1]
    left = "".join([x for i, x in enumerate(tile) if i % 10 == 0])
    reverse_left = left[::-1]
    right = "".join([x for i, x in enumerate(tile) if i % ((i // 10) * 10 + 9) == 0 and i != 0])
    reverse_right = right[::-1]
    detect_connexions([top, reverse_top, bottom, reverse_bottom, left, reverse_left, right, reverse_right], title[5:9])
    line = input()

unique_connexions = {'-'.join(x) for x in dict(merge_points).values() if len(x) >= 2}
extreme_points = [int(y) for x in unique_connexions for y in x.split("-")]
edges_n_links = dict(Counter(extreme_points))
print(reduce(operator.mul, (list(filter(lambda x: edges_n_links[x] == min(edges_n_links.values()), edges_n_links))), 1))

"""
Advent of Code, day 20

The high-speed train leaves the forest and quickly carries you south. You can even see a desert in the distance! 
Since you have some spare time, you might as well see if there was anything interesting in the image the Mythical
 Information Bureau satellite captured.

After decoding the satellite messages, you discover that the data actually contains many small images created by the
 satellite's camera array. The camera array consists of many cameras; rather than produce a single square image,
  they produce many smaller square image tiles that need to be reassembled back into a single image.

Each camera in the camera array returns a single monochrome image tile with a random unique ID number.
 The tiles (your puzzle input) arrived in a random order.

Worse yet, the camera array appears to be malfunctioning: each image tile has been rotated and flipped to a random
 orientation. Your first task is to reassemble the original image by orienting the tiles so they fit together.

To show how the tiles should be reassembled, each tile's image data includes a border that should line up exactly with
 its adjacent tiles. All tiles have this border, and the border lines up exactly when the tiles are both oriented
  correctly. Tiles at the edge of the image also have border, but the outermost edges will line up with no other tiles.

For example, suppose you have the following nine tiles:

Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...

By rotating, flipping, and rearranging them, you can find square arrangement that causes all adjacent borders to line up

#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##.....

For reference, the IDs of the above tiles are:

1951    2311    3079
2729    1427    2473
2971    1489    1171

To check that you've assembled the image correctly, multiply the IDs of the four corner tiles together. If you do this
 with the assembled tiles from the example above, you get 1951 * 3079 * 2971 * 1171 = 20899048083289.

Assemble the tiles into an image. What do you get if you multiply together the IDs of the four corner tiles?

Your puzzle answer was 17148689442341.

Input:

Tile 1471:
.#...##.##
#...#.#..#
##.......#
#..#.....#
#..##....#
.#.#..#...
##.##.#..#
...###..#.
......##..
.##..##.#.

Tile 1699:
.##..#..##
#....#....
.##..#....
##......##
#...#....#
#.#......#
...#...##.
#.........
#..#..#...
.#..###.##

Tile 2909:
##...####.
.......#..
.....#...#
#...#..###
..........
##.......#
#..#.#..#.
.#..#.....
#......##.
.#...##...

Tile 2297:
.#.##.....
#..###.#.#
....###..#
..#...##.#
...#...##.
#........#
#........#
##.....#.#
.#....#..#
...#.##.#.

Tile 3109:
#...#.##.#
....#.....
......#..#
#.####.#..
###..##...
........##
#..####..#
##..#.....
.#.#..#..#
####.###.#

Tile 3767:
##..###.#.
##........
..#.....##
...#.....#
#..#.....#
#..#..##.#
.#......#.
..........
.......#..
#.#..##.##

Tile 1061:
..###.#...
.....#..#.
.#........
..#..##...
#.........
#...#.....
...#....##
#.#....#.#
........#.
...##.#.##

Tile 2953:
#..##.#.##
#.....#...
...##.....
#.#.......
..#.#....#
#.....#...
...#..#..#
.#.#....#.
#........#
..##.##...

Tile 3659:
###...#.##
..#.#....#
#.#...#...
#........#
#.#.##..##
#.###.##..
..#.......
.#.##.....
#..#.....#
.#..##..##

Tile 3733:
.##.##..#.
.#...##...
#........#
#.###.....
##...#...#
.##.......
..#...#..#
#.#.#..#.#
.#.#......
....#....#

Tile 1741:
#.#.......
#.......#.
.....#..##
......#..#
##.#.....#
#.........
#.#......#
#..##.#.#.
...##....#
###..##.#.

Tile 2053:
..#..##.#.
#...#...##
..#....##.
..#.#..#..
#.##......
#...##.#.#
...##.....
###.#...##
#....#....
.####.#..#

Tile 3391:
.#.#.#.###
....###...
...#.#.#.#
..#..#..##
.....##...
......#...
....#..#.#
.......#..
#..#..#...
#.#######.

Tile 2969:
#...#.#..#
###.##...#
.###..##..
#.........
##........
.#..#.....
#.....#...
#..#..#..#
.........#
...#....##

Tile 3167:
#..#.#.###
###.#....#
.#...#...#
...#.#...#
..#.##....
#....#..#.
#.##.....#
#...#...##
...####..#
..##..###.

Tile 3719:
...###.##.
...#....#.
#.#.##....
#...##...#
#.....##..
#.#....#..
#.#.#.....
#...#....#
...#....##
#.#.#.#..#

Tile 1531:
####.#.#.#
##....###.
..#...#...
#.##......
#........#
#.#....##.
......#.#.
..##.###..
..##..#..#
###...####

Tile 1361:
#....#...#
#..#.....#
##....###.
#........#
##.....#..
#...#..#.#
#...#.#.##
..#...##..
..........
#.##..##..

Tile 2393:
.###....#.
.........#
#.......#.
....#.....
......#..#
....###...
##.#.....#
##...###.#
#..##.....
##..######

Tile 1481:
####.#.#.#
...#......
#....#.###
.....#...#
..........
#.#....#.#
###.##....
##.......#
#.......#.
.##.#.###.

Tile 2851:
.##.....##
#..#.#....
.#...#...#
#.....#...
..#.......
.#........
...#.##...
...#..##.#
##...#....
.####..#..

Tile 3833:
.#.##.#.##
#.....#...
##.....##.
..#.......
..#.#....#
##.....#.#
#..##...#.
#.#.......
..........
#..#####..

Tile 2971:
##.#.#....
......#...
#.#.#.....
.........#
.....#...#
#....##..#
...#..##.#
..#.......
#..#..#..#
..#..#..##

Tile 3203:
###.###...
...#####.#
...#.#...#
#..##.....
.........#
#.#..#....
#.#..##.##
###...###.
###.#.#..#
##.#..##.#

Tile 3067:
...#.###.#
......##.#
.#...#...#
###...##.#
#........#
..........
#.........
#.#....#.#
.....#.#..
.#...#.###

Tile 1993:
.#...#...#
.##...#..#
#....#...#
.#..###...
...#..###.
#.#....#..
##...#...#
.....#..#.
.......#.#
...#....##

Tile 2903:
##.#..###.
###.....##
.#...##..#
...#.....#
###...#.#.
#...##...#
..#..#..#.
...##...##
..###.....
#.#...##.#

Tile 1439:
....##.#.#
###.......
##......##
#...#.#...
..........
........##
.#......##
#.......#.
.#......##
.####.##..

Tile 3023:
..#..#..#.
##....####
##....#..#
...#.#..##
.....##...
......#.##
##...#..#.
...##.##.#
#.....#...
#.#..#.##.

Tile 2503:
##.###.#..
..........
#.#..#..#.
#####.#..#
##....#.#.
#..#.#.#..
#..#...#..
.#........
#.#.##....
.#####..#.

Tile 1277:
#.#....##.
...##.#...
###....#..
#.#.#....#
#....#.##.
.....#..##
#...#...#.
#.......#.
#...##..##
#..#.#.###

Tile 2027:
..###..#..
#.........
...#..##..
..#.....##
#.#......#
...###.#.#
...#....#.
...###...#
##.#.....#
##.#####.#

Tile 2333:
#.#.#.#..#
..##......
.........#
.#.#.....#
#...####.#
.##......#
#....####.
...#.....#
###..#.##.
.######.#.

Tile 2069:
#.#.##..#.
..#.....#.
..#...##..
.......#..
..#####.#.
.#####...#
..#....#..
...##.####
.......#.#
.#...###.#

Tile 1999:
#.#.##.#..
#.....#.##
..#.#.....
..#......#
..###....#
...#.....#
#.#...##..
#....#.#.#
##......#.
#..#..#.#.

Tile 3181:
...#####..
....##.#..
......#..#
.#.#......
#......#..
#........#
.#.....###
....##.###
#..#..#.##
########.#

Tile 1321:
.#..#.....
..#...##.#
#.#.....##
....#.....
#....#..#.
.....#....
#...#.....
#.#.#..#.#
#..#..#...
...#......

Tile 2549:
.##....###
#...####..
##.......#
#.###...##
..#####...
#.#..##.#.
#..##.....
#....#...#
#.###...#.
#...#.##.#

Tile 1951:
.#.#...#..
##..#..#..
..#.....##
.#.#..#..#
#...#.....
...#...#.#
.#.......#
.#...#.#.#
.#......#.
#..#.#####

Tile 2111:
.##.#....#
#.#.....##
#.#...#..#
#......###
#....##.##
.......#..
#....#...#
.##.##.#.#
#...#..#..
.##.##.###

Tile 1447:
..#.#.....
##..####..
##...#...#
.##..##.#.
.....#...#
...#......
.....##..#
..#..#..#.
.#.......#
#.#.#.#...

Tile 2707:
.#.#####.#
###.#.....
.#.##.##..
......#...
#.#...##..
.#...#.###
....#.##.#
...#..#...
.#.....#.#
#.#####.##

Tile 2437:
..#.#...#.
..#.......
.##..##..#
#..#...#..
..#....#..
##.....#.#
##........
...##...#.
.....#...#
.#...#.###

Tile 2699:
.##.#..###
.........#
...#..#..#
...#.#....
#......###
##......##
...#.....#
.....#...#
#....#...#
..###.###.

Tile 1913:
.#######.#
.#.##.#..#
#.##.....#
####..#..#
.##..#.##.
#.....#..#
...#.#....
..#..#....
##......##
.#########

Tile 3361:
.....##...
#.####...#
#.#..#...#
.#.###.##.
....##...#
......#...
.#.#....#.
#........#
#..#..#...
#.#...#...

Tile 3359:
.####.#..#
#.......#.
..........
..#..#....
#...##.##.
....#.....
..#..#..#.
...#.#....
#..#...#.#
#######...

Tile 2731:
###.##.##.
......##..
#........#
..........
.........#
###....#.#
...#..#..#
##...#.#..
.#.#.#.#..
#.#....#..

Tile 1543:
.#..###.##
#........#
#...#.#...
..#..##.##
#...#...#.
.......#.#
..#...##.#
....#..###
......#.##
###.#..###

Tile 2861:
##..####.#
##......##
...##...##
.#......##
...#.#....
..##.###.#
##.#.#.#..
#..#...#.#
##......##
##.#...##.

Tile 3559:
.#..#.#...
......###.
.#...#...#
#...###.##
#...#..#.#
#..##.....
####....##
......#..#
...###.#..
#.#.....#.

Tile 2819:
.#..#..#.#
#...#.#..#
....#....#
.#.#...#..
....####.#
.#...#.#.#
...#.....#
#........#
#..###.#..
.###...#..

Tile 1613:
.##.#..###
#.....#...
#...##..##
.##......#
#.##......
.#..#.#..#
#..#.##...
.#.#......
#....#....
.#####....

Tile 1213:
...#.#..#.
#.....#..#
...#####.#
.##..#.##.
.##.......
##.......#
#........#
###......#
....#...##
######.##.

Tile 2161:
###.#.#...
.##..#...#
#.##......
.....#.#..
.......##.
#.#....##.
##....#...
.#..#....#
#.........
....#...#.

Tile 3041:
....#.#...
.##.##...#
....#.....
##.##..#..
#.......#.
#...#.....
.##....###
...#....##
#.....#...
..##.####.

Tile 1871:
#.#.....##
##.....#..
..###...##
.......#.#
........#.
..#.....#.
.#.#......
.#..#....#
.##.#..###
..##.#....

Tile 2687:
.#...#....
...#.#..##
..#.......
#.#.......
...#..#.##
...#....##
##.......#
#..#...#..
#.######..
.##.##.#..

Tile 2269:
#......##.
...#..#.#.
#.#.....#.
#.#.##...#
.#.#.....#
##.......#
#....##..#
#..#..#...
#...##...#
.###....#.

Tile 2089:
##.#.#....
..#.#..##.
.#.......#
#.....#..#
........##
.....#.###
#.......##
.#.......#
..##.##..#
...#..##.#

Tile 1097:
##.##.##.#
.....##..#
..#.....##
##......#.
....#..#.#
..#..#..#.
.#.......#
..####.#..
#...#...##
##...####.

Tile 3001:
.....#..#.
#..#...#.#
..#...####
..#.#...#.
..#..#.###
#.........
#...#.###.
#...##..#.
#......#..
......#.#.

Tile 2803:
.####.###.
##........
..#......#
#.#..#.#.#
##..#...##
#.#......#
.##..##...
.###.....#
###....##.
#..#.#..#.

Tile 3407:
#.........
........#.
.........#
#.##.##..#
###....###
..........
.........#
.#..##..##
#..##.#...
.##...##..

Tile 2423:
#####.##.#
......##.#
..#.#.#..#
#...##....
#...#.#.#.
..##......
#........#
.........#
..##.....#
#..##...#.

Tile 2213:
.##.#.#..#
#...#.#..#
........##
.#......##
#...#....#
.....#..#.
.......#..
.........#
#.........
...####.##

Tile 2879:
.##.#.###.
.#........
..#......#
#..#.#....
..#.......
#......###
.#...#.#.#
#.......#.
#.#....#.#
.##...#...

Tile 3779:
.#####.#.#
.........#
.#....##..
##...##..#
#..####...
..#..##.#.
.#....#.##
####...#.#
#.#.......
......#..#

Tile 2647:
.###.##.#.
#.####.###
#........#
#.#.###..#
...#......
.....#....
##..###.##
..#.....#.
#..#..#..#
#..#.#..#.

Tile 3623:
...##.#...
#.#.......
....##.#.#
......#..#
#.....#.##
.....##...
#.#.#....#
.#..#.....
#..#.#.###
#.##.....#

Tile 1733:
.##.#.##..
###....###
...#.###.#
#.#.#.....
#....#.#.#
######..##
#####....#
#..#.#.###
........#.
.#.....#.#

Tile 1601:
##...#.###
#...###..#
...##.#..#
.##.#..#.#
#.##....##
#.#.##...#
....#.#..#
##....#...
.#.#.#...#
#####..##.

Tile 2203:
#..#.#.#..
...#.....#
#...#...##
#......#.#
...#..#..#
#.....#...
...##.#..#
.#........
........##
...###...#

Tile 1051:
##...#...#
.....#..#.
#....#....
...#......
..##..#...
..#......#
.#.#####..
##.#......
#...##....
##.#.#.##.

Tile 3823:
.######...
...#.....#
.#........
........##
..#......#
.#...#...#
..#.......
.......###
#..#.....#
.#.#.####.

Tile 3121:
.##.##....
.#.....###
..#.#.#..#
.##....#..
...#.#..##
#..##.###.
.#...#....
###....#.#
#...#....#
#..#..##..

Tile 3347:
#..##.#.##
#.#.#.#...
.##......#
#..#..#..#
#.###....#
#......#.#
..##.#...#
###..#...#
#.#....#..
.##..####.

Tile 1609:
#...#.###.
#.#......#
#..#.#.#..
..#.....#.
#......##.
..###.....
..........
...#.#..##
#.....#...
#..#...##.

Tile 1283:
..#.##....
.#.#.....#
.#..#..#.#
...#.#####
.##...#.#.
#........#
#....#...#
##...###.#
#.#....#..
..#.##.##.

Tile 2543:
#####...##
#....##...
..#.......
.......#.#
.#........
...#....##
#........#
....#..#..
#.#.#....#
#####.##..

Tile 1019:
###..##.##
..#.......
.#...#....
##.......#
#........#
#.#..##...
...#......
.....#...#
#..##.#.##
#####.#.##

Tile 3433:
.##.....##
#..#......
.###......
...#......
.#.#.#.#..
##.#...#.#
...##....#
#.###....#
######...#
.#...##.##

Tile 2207:
.##.#..#..
....#..#.#
..#....#..
....#....#
...##...##
....#.####
#..#...###
..#.....##
#.#.#....#
.#.##....#

Tile 1861:
#.#.#..#.#
.#..#....#
.....#...#
...#..#...
........#.
#..#......
#....#.#.#
#......#.#
#.....#..#
#...#.....

Tile 3163:
####.#..##
...#.##...
##..#.....
.........#
.#.....#.#
.#..#..#.#
.........#
..#....#.#
#.......##
#.###.#.##

Tile 1453:
###.#....#
#.......##
..#.......
..#...##..
#.....###.
.........#
..##...#.#
#......#..
....#....#
##.....###

Tile 1987:
.#.#.##...
##.##..#..
##.#.#...#
..........
....#....#
##...##..#
.........#
##.#.....#
.#........
.#.#..##..

Tile 2441:
..#.#.#.#.
..#.......
#.......##
.##.#.####
..........
.#..##...#
#..#.####.
.#.......#
##.#..##..
.#####..#.

Tile 1499:
..#######.
##...###.#
.........#
##......##
.#....#...
###....#.#
...#..#...
......###.
#..##.....
.#.##....#

Tile 1151:
#..###..#.
#.#.##...#
.......#..
#......##.
..#..#.#..
#.##....#.
#........#
##........
..####....
..##..####

Tile 2939:
..#####.#.
...##...#.
#..#.#.#..
#.#......#
......#.#.
........##
.......#.#
#...#....#
#.#..###.#
.....#...#

Tile 1571:
..#..#####
..........
##.#.#.##.
........#.
#.###....#
..#.###..#
.#..#.#.##
#.#.#....#
#..#......
.##..###.#

Tile 3863:
#..#..#...
##.##.#...
#.#...##.#
..#..##.##
#..###....
#..#.....#
##......#.
#.........
....#....#
..##....#.

Tile 3881:
#.#.#..#..
##.......#
.........#
.#.#..#...
#.#.##.###
#..#......
.....#...#
#.#...#...
..#....#.#
##.#..#...

Tile 1307:
.....#....
###.##...#
.###.#....
....#.....
..#.......
..##.....#
#....#....
..#..##..#
#.#.#.#.#.
.......###

Tile 3739:
...#.##.#.
#...###...
##.#..#..#
#..#.#..##
....#.##.#
........##
..#..#.#..
.#...#....
.#..#.....
.##....#.#

Tile 1621:
##.#.#.#..
#.##..#..#
...##.....
..#..#....
.........#
#..##.....
..#..#....
#..#.....#
#..#..#..#
....##.#.#

Tile 3011:
.#...####.
..#.#.....
..........
#.##.#...#
#..#...###
#......##.
..#.#.....
#...#...#.
........#.
#.##....#.

Tile 2309:
#......#..
..#.......
#...#....#
##.#..#..#
..........
.#...#..#.
.###.#..##
##..#.....
..#.#.....
.#.####...

Tile 2383:
.###.##.#.
###....#..
#..#.#...#
#.........
..#......#
##..##.#.#
.#..#.....
###.#.#...
#....#...#
##.#..#...

Tile 2273:
.##.#...#.
..........
#....#....
#.#..#....
#.#....#..
#.........
.#....#...
..#.#....#
#...#..#.#
.#.......#

Tile 1549:
#..#.###.#
.#.#.#.#..
#..#....##
#..#.##..#
#....##..#
....#.#...
#...#..##.
.....#...#
#......#.#
.#..####.#

Tile 1867:
.#.#..#..#
#.##.###..
.#...#...#
#.#...##..
......#...
#.#..#..##
...##.....
.......#.#
#........#
.....#.##.

Tile 3061:
...#######
#...#....#
.....##...
#....#...#
..#.#...##
..........
........#.
.#..##..#.
...###.#..
#.##.###.#

Tile 2447:
#.#.####..
#.......##
......#.##
#........#
......#...
####..#...
#...#....#
.#........
#.#..#..##
.#.#.##...

Tile 2243:
###.#..#.#
..#.......
...##....#
#..###..##
.##...#.#.
#.#..#.#.#
#....#.#..
#....#..#.
..#...##.#
#.##...#..

Tile 2551:
.#.#.....#
#..#....##
..#....#.#
.###....##
#...#..#..
#........#
#.....#.#.
##...##.##
......#...
.####.#...

Tile 3037:
#...##.#.#
#...##...#
#...###.#.
...#...#.#
#.....#.##
#....#.#.#
#..##..###
....##...#
##...#.#.#
......####

Tile 2389:
###..##.#.
##..####..
....#....#
.........#
.#..#..#..
#..#.....#
...#......
#...#....#
..#.....##
.##..##.#.

Tile 2791:
.###.#.###
#....#...#
##...#.#.#
##.####.##
........##
##.#.#....
.##...#...
#.#..#####
.#...#.#.#
#.#...#...

Tile 1229:
.#.###.#..
#.##..#...
.#.....###
.##.....##
#.#......#
..#.#....#
.........#
##.#.....#
###.....##
###.#.#...

Tile 2579:
#..#.#.#..
##.....#..
####....#.
....#.##..
#....#.#.#
###....#..
#.#.#.#...
#..#...#.#
#..#.....#
..###.#...

Tile 2837:
##.#####..
....##...#
#.#......#
..........
.......#..
.#........
#......###
#.#.....#.
##....#...
.....#....

Tile 2957:
#########.
..........
###..#.##.
##....#.##
...#.#.##.
.......#.#
#....#....
#...##.#..
.#......#.
.....####.

Tile 3083:
..#..#..#.
......#...
....#..###
#....##...
.#.......#
.......#.#
.....#...#
.......#..
.....###.#
#.##.###.#

Tile 3533:
...#.###.#
#..#..##.#
#.#..#.#..
##..##....
#....#....
#.#.......
##...#....
.........#
#.......#.
....###.#.

Tile 1289:
#..##.##.#
......#..#
#..##.....
#.........
....#..##.
##...##.##
#..#.#...#
....#..###
#.........
......##..

Tile 1559:
.#..##.#.#
###.......
##....#.#.
.##......#
#.#...#...
.##.#....#
##.....###
#.........
.....#....
###..#.###

Tile 2693:
.#........
.......#..
#.#.......
..........
#.......#.
#.........
#.#.......
....##.#.#
.....#....
.#.##...#.

Tile 1669:
###.###.#.
#........#
..........
#..#.#....
#...#...##
.#....#...
#..#......
##....#...
.##.#..#.#
########..

Tile 3541:
#..####.#.
.#.......#
#......#.#
..#...####
#.....#...
......#...
#......##.
..#.....#.
.......#.#
.###..#..#

Tile 3389:
#..####...
#.##.....#
.#.##....#
#...##....
.####...##
#.#..##..#
....##.#.#
.###..#...
#..#.....#
#.....##.#

Tile 1889:
#.#.#####.
.##..##.#.
#..#.....#
#..##....#
##..#...#.
...#.#..#.
#..#..##.#
#.#.#...#.
...#..##..
.....#.#..

Tile 3343:
##...#.#..
#..##...#.
##.......#
#......#..
..#...##.#
##..##.#..
.###....##
#.##...#.#
##.......#
...#.....#

Tile 1231:
......##..
#..#.#####
.##...###.
#.....#...
#..#.##.##
#....#.#..
#.#.....##
...#.#.###
.......#.#
#.##.####.

Tile 3637:
.#...#...#
###.###..#
##..#....#
.....#..#.
....#.....
#.#.#..###
#....#.#.#
.##..#...#
.#..##..#.
..#......#

Tile 3499:
.#....#.##
.##...##.#
#..#..#..#
...#.....#
.#....#...
...####...
....#.....
..........
#.........
#..#.#.##.

Tile 1009:
..####..##
.#.....#..
..........
.........#
#.#.#....#
#.##..#..#
.#..#.#.#.
#.....#...
#......#.#
.##.#.##.#

Tile 2473:
#.#.##.#..
.##..#....
#...#....#
...#....#.
..##..#..#
..........
...#....##
.#......#.
.....#...#
.#....#..#

Tile 2137:
##.##.##..
.........#
#..#.#...#
#........#
.........#
###.##.#.#
.........#
#.#.##....
...#.#....
###...####

Tile 1489:
.##.####.#
#.##.##..#
...#.##.#.
#.##...#.#
.##.#.#.#.
###......#
##.#...#..
#.#...#.#.
.##...#.##
.#..###..#

Tile 1291:
..##..#..#
.#....#..#
.........#
#......#.#
.........#
...#...#.#
#.........
...#.....#
###....###
.##.###...

Tile 1483:
#.##....#.
#...####.#
..#...#..#
.........#
..#####...
.#..#..#.#
#....##..#
#..#.....#
#....#...#
.#.##.##.#

Tile 3119:
..##.#.#..
#....##.#.
##.......#
#....#....
......#...
..#....##.
#...#.....
.........#
...##....#
#.#.###...

Tile 2609:
.....##.#.
.....#..##
#.#.#.....
#.##...##.
...##..#.#
..##..##.#
#.##...###
......#.#.
#..#.....#
..#####...

Tile 2399:
..#.#...#.
........##
#.##......
#..##..#..
..........
..#.#..#..
#.........
#...#...##
#........#
##...#.##.

Tile 3847:
#..#....##
...####.##
...#....#.
..#...#...
##..#.##..
#.##.#...#
...##....#
#.###....#
..#.#....#
###.#.##.#

Tile 2531:
.###.#..#.
....#..#..
#......#.#
.........#
....#..#..
.###..###.
#.#......#
##...#..##
#...#.####
#..#...#..

Tile 1627:
..#.##..#.
.........#
###....###
#....#.#.#
#..#...#.#
#......###
...##.....
##..##.#..
....#.#...
#....##...

Tile 2719:
#...#.#...
......#.##
#..##.....
.....#.#..
.#...#..#.
...##....#
#........#
##......#.
#.#..#...#
.####..#..

Tile 3169:
#.#.#..#..
..#.#.....
......#...
#.#.##....
....#....#
...#...#.#
...#...##.
#...#.....
#..#.#...#
...#..###.

Tile 1193:
#.#....###
...#.#..#.
..#..#..#.
#........#
#.........
#.#.....#.
##........
#.........
#.........
...##..#..

Tile 1459:
###..##..#
.........#
.........#
.##.......
##.#......
###......#
#.#.....##
........##
...###..##
#...##.###

Tile 3943:
...##....#
........#.
..#.......
#.##.#....
##.#.....#
#.......##
.#..#.#...
..........
.......##.
##.##.###.


"""