word_set = set()

def make_word_set():
    with open('pylib/word_list.csv') as f:
        for l in f.readlines():
            if l.strip():
                word_set.add(l.strip())

def letters_on_places(word, locked_positions):
    for idx, letter in enumerate(locked_positions):
        if letter.strip():
            if word[idx] == letter:
                continue
            else:
                return
    return word


def filter_words(not_containing=None, containing=None, locked_positions=None):
    """
    not containing: string of letters
    containing:     string of letters
    locked:         string of letters , like: "A  E "
                    where space indicates not yet locked.
    """
    potentials = set()
    for w in word_set:
        if not (set(w) & set(not_containing)):
            if containing:
                if set(w) > set(containing):
                     potentials.add(w)
            else:
                potentials.add(w)
    
    possible_locked = []
    sorted_potentials = sorted(list(potentials))
    for word in sorted_potentials:
        if locked_positions:
            result = letters_on_places(word, locked_positions)
            if result:
                possible_locked.append(result)


    return possible_locked


make_word_set()
# potentials = filter_words(
#     not_containing="sparkwige",
#     containing="toc",
#     locked_positions="     ")
# print(potentials)
