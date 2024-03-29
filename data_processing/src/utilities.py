def fill_hole(l, null_char=0):
    if not has_hole(l):
        return l
    l = l.copy()
    num_1 = null_char
    num_1_index = 0
    num_2 = null_char
    num_2_index = 0
    done = False
    encountered_first = False
    i = 0
    while i < len(l):
        if l[i] != null_char:
            encountered_first = True
        if l[i] == null_char and encountered_first:
            if num_1_index == 0:
                num_1 = l[i - 1]
                num_1_index = i - 1
            j = 1
            while i + j < len(l):
                if l[i + j] != null_char:
                    num_2 = l[i + j]
                    num_2_index = i + j
                    done = True
                    break
                j += 1
            if done:
                break
        i += 1
    slope = (num_2 - num_1) / (num_2_index - num_1_index)
    i = num_1_index + 1
    while i < num_2_index:
        l[i] = num_1 + slope * (i - num_1_index)
        i += 1
    return l

def has_hole(l, null_char=0):
    l = l.copy()
    i = 0
    new_start = 0
    new_end = 0
    while i < len(l):
        if l[i] != null_char:
            new_start = i
            break
        i += 1
    i = len(l) - 1
    while i >= 0:
        if l[i] != null_char:
            new_end = i + 1
            break
        i -= 1

    l = l[new_start:new_end + 1]
    i = 0
    while i < len(l):
        if l[i] == null_char:
            if i != 0 and i != len(l) - 1:
                return True
        i += 1
    return False

def fill_left_end(l, null_char=0):
    l = l.copy()
    index = 0
    while index < len(l):
        if l[index] != null_char:
            max_index = index
            break
        index += 1
    i = 0
    while i < max_index:
        l[i] = l[max_index]
        i += 1
    return l

def fill_right_end(l, null_char=0):
    l = l.copy()
    index = len(l) - 1
    while index > 0:
        if l[index] != null_char:
            min_index = index + 1
            break
        index -= 1
    i = min_index
    while i < len(l):
        l[i] = l[min_index - 1]
        i += 1
    return l

def lin_interp(l, null_char=0):
    l = l.copy()
    num_non_null = 0
    last_non_null = 0
    null_pos = []

    j = 0
    for i in l:
        if i != null_char:
            last_non_null = i
            num_non_null += 1
        else:
            null_pos.append(j)
        j += 1

    if num_non_null == 1:
        j = 0
        while j < len(l):
            if l[j] == null_char:
                l[j] = last_non_null
            j += 1
    elif num_non_null == 0:
        return l
    else:
        m = 0
        while has_hole(l):
            l = fill_hole(l)
        if l[0] == null_char:
            l = fill_left_end(l)
        if l[len(l) - 1] == null_char:
            l = fill_right_end(l)

    return l


def process_metrics(metrics):

    p_metrics = []

    for m in metrics:
        o_m = m
        m = m.lower()
        m = m.replace(' ', '')
        p_metrics.append(m)


    metrics = []
    for m in p_metrics:
        if '/' in m:
            a = m.split('/')
            for i in a:
                if i not in metrics:
                    metrics.append(i)
        else:
            if m not in metrics:
                metrics.append(m)

    return metrics
