import game_board
import game_rules
import random
import game_ai_player
import time
import threading


def move_to_str(n1, n2):
    return game_rules._to_str(n1) + game_rules._to_str(n2)


def set_bit(bitmap, i):
    return bitmap | game_board._mask[i]


def is_empty(rules, bitmap, i):
    return rules._valid(i) and ((bitmap & game_board._mask[i]) == 0)

def get_distance(rules, n, direction):
    d = 0
    assert (rules._valid(n))
    while rules._valid(rules.way[n][direction]):
        n = rules.way[n][direction]
        d += 1
    return d

def get_n_at(rules, n, distance, direction):
    while distance > 0:
        assert(rules._valid(n))
        n = rules.way[n][direction]
        distance -= 1
    return n


def dam_hit_dir(rules, enemy_bmp, way_bmp, n, direction):
    d = get_distance(rules, n, direction)
    for ei in xrange(1, d):
        y = get_n_at(rules, n, ei, direction)
        if is_empty(rules, enemy_bmp, y) and is_empty(rules, way_bmp, y):
            new_enemy_bmp = set_bit(enemy_bmp, y)
            new_way_bmp = way_bmp
            for wi in xrange(1, ei):
                x = get_n_at(rules, n, wi, direction)
                new_way_bmp = set_bit(new_way_bmp, x)
            for wi in xrange(ei, d):
                x = get_n_at(rules, y, wi - ei + 1, direction)
                if is_empty(rules, enemy_bmp, x):
                    new_way_bmp = set_bit(new_way_bmp, x)
                    '''
                    bx = game_board.Board()
                    bx.full = new_enemy_bmp | new_way_bmp
                    bx.black = new_enemy_bmp
                    bx.dam = 0
                    print("Yield", n, game_rules._to_str(n), direction, move_to_str(y, x))
                    print(bx)
                    '''
                    yield new_enemy_bmp, new_way_bmp, move_to_str(y, x)
                else:
                    break
        else:
            break


def unit_hit_dir(rules, enemy_bmp, way_bmp, n, direction):
    n1 = rules.way[n][direction]  # try place black here
    if is_empty(rules, enemy_bmp, n1) and is_empty(rules, way_bmp, n1):
        n2 = rules.way[n1][direction]
        if is_empty(rules, enemy_bmp, n2):
            enemy = set_bit(enemy_bmp, n1)
            empty = set_bit(way_bmp, n2)
            yield enemy, empty, move_to_str(n1, n2)


def unit_hit_way(rules, enemy_bmp, way_bmp, n, is_dam, way, last_dir):
    deep_end = True  # TBD
    white_turn = True
    directions = list(game_rules._all_directions)
    if last_dir is not None:
        directions.remove(game_rules._opposite_direction[last_dir])
        #print "last dir", last_dir, "opposite", game_rules._opposite_direction[last_dir], directions
    for d in directions:
        hit_dir_generator = dam_hit_dir if is_dam else unit_hit_dir
        for hit in hit_dir_generator(rules, enemy_bmp, way_bmp, n, d):
            new_enemy_bmp = hit[0]
            new_empty_bmp = hit[1]
            move = hit[2]
            if move[0] not in way:
                new_n = game_rules._from_str(move[1])
                deep_end = False
                new_is_dam = is_dam or rules._dam_field(white_turn, new_n) #russian rule
                # way_generator = rules._hit_dam_way if self._dam_field(white_turn, new_n) else self.unit_hit_way  # russian rule
                # way_generator = unit_hit_way  # international rule
                for a_way in unit_hit_way(rules, new_enemy_bmp, new_empty_bmp, new_n, new_is_dam, way + move, d):
                    yield a_way
                yield new_enemy_bmp, new_empty_bmp, way + move
    if deep_end:
        yield enemy_bmp, way_bmp, way


b = game_board.Board()
r = game_rules.Rules(game_board._n)

'''
n = 0
d = 1
own_bitmap = game_board._mask[n]
b.set(n, True, True)
for h in dam_hit_dir(r, 0, own_bitmap, n, d):
    bx = game_board.Board()
    bx.full = h[0] | h[1] | own_bitmap
    bx.black = h[0]
    bx.dam = own_bitmap
    print str(bx)
'''


grand_total = 0
grand_same = 0
assert_cnt = 0
for i in xrange(0, game_board._N):
    total = 0
    duplicated = 0
    is_dam = True   # r._dam_field(True, i)
    b.clear()
    way = ""
    own_bitmap = game_board._mask[i]
    print(i, "****************************************")
    hit_list = []
    for h in unit_hit_way(r, 0, own_bitmap, i, is_dam, way, None):
        total += 1
        grand_total += 1
        bx = game_board.Board()
        bx.full = h[0] | h[1] | own_bitmap
        bx.black = h[0]
        bx.dam = own_bitmap
        if bx in hit_list:
            duplicated += 1
        else:
            hit_list.append(bx)
            print str(bx)
            bx_full_move = h[2]+game_rules._to_str(i)
            print bx_full_move

            dut = game_board.Board()
            dut.full = h[0] | game_board._mask[i]
            dut.black = h[0]
            dut.dam = game_board._mask[i] if is_dam else 0
            dut_hit_list = []
            print dut
            for dut_hit in r.hits(dut, True):
                dut_hit_list.append(dut_hit)
                if dut_hit == bx_full_move:
                    print dut_hit, "  <-- OK"
                else:
                    print(dut_hit)

            # print("OK" if bx_full_move in dut_hit_list else "not found");

            if len(dut_hit_list) == 0 or bx_full_move not in dut_hit_list:
                print("ASSERT", i)
                print(game_board.Board.notation())
                assert_cnt += 1
                #exit(0)

    print(i, "************************************* unique", total - duplicated, "duplicated", duplicated, "total", total, "asserts", assert_cnt)
print("grand_total", grand_total)

'''
b.load(" . . . ."
       ". . . . "
       " x x x ."
       ". . . . "
       " x x x ."
       ". . . . "
       " x x x ."
       ". . . o ")

for h1 in r.hits(b, True):
    print(h1)
'''