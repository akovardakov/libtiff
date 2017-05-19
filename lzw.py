from itertools import cycle


def read_uneven_bit(data, size, position):
    # data = array of bytes
    # size = size in bits of int, supports 9-12 bits
    # position = start bit position (0 to 7)
    

    shift = size - 8 + position
    mask = 0xff >> position

    f_masked = data[0] & mask
    f_shifted = f_masked << shift

    # shifted bits may take 2 to 3 bytes
    if (size-9) < (8-position):
        s_shifted = data[1] >> 8-shift
        res = f_shifted | s_shifted
    else:
        s_shifted = data[1] << shift-8
        t_shifted = data[2] >> 16-shift
        res = f_shifted | s_shifted | t_shifted

    return res

def unpack_bits(data, size):
    pos = cycle(range(0,8))

    res = []

    cur_pos = next(pos)
    skipped = False
    for idx, elem in enumerate(data):
        if idx+2 == len(data):
            break
        if skipped:
            skipped = False
            continue
        tmp_list = [elem, data[idx+1], data[idx+2]]
        cur_bit = read_uneven_bit(tmp_list, size, cur_pos)
        cur_pos = next(pos)
        if cur_pos == 0:
            skipped = True
        res.append(cur_bit)

    return res

def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from io import StringIO
 
    # Build the dictionary.
    dict_size = 258
    init_dictionary = {i: [i] for i in range(dict_size)}
    dictionary = init_dictionary
 
    result = []
    last_entry = None

    for k in compressed:
        if k == 256:
            dictionary = init_dictionary
            continue
        elif k == 257:
            break
        elif k < dict_size:
            entry = dictionary[k]
        elif k == dict_size:
            entry = last_entry
            entry.append(last_entry[0])
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result += entry
 
        if last_entry is not None:
            curentry = last_entry
            curentry.append(entry[0])
            dictionary[dict_size] = curentry
            dict_size += 1
 
        last_entry = entry
    return result
 
