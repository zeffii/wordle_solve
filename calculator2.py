from browser import document, html
from wordle_functions import filter_words

ARK = """\
ABCD|ABCD|ABCD|ABCD|ABCD
EFGH|EFGH|EFGH|EFGH|EFGH
IJKL|IJKL|IJKL|IJKL|IJKL
MNOP|MNOP|MNOP|MNOP|MNOP
QRST|QRST|QRST|QRST|QRST
UVWX|UVWX|UVWX|UVWX|UVWX
YZ..|YZ..|YZ..|YZ..|YZ..
.
ABCD|ABCD|ABCD|ABCD|ABCD
EFGH|EFGH|EFGH|EFGH|EFGH
IJKL|IJKL|IJKL|IJKL|IJKL
MNOP|MNOP|MNOP|MNOP|MNOP
QRST|QRST|QRST|QRST|QRST
UVWX|UVWX|UVWX|UVWX|UVWX
YZ..|YZ..|YZ..|YZ..|YZ..
.
ABCDEFGHIJKLMNOPQRSTUVWX
YZ
.
"""

inner_config = {'info': []}

calc = html.TABLE()
lines = ARK.split('\n')

calc <= (html.TR(html.TD(x) for x in line) for line in lines)
calc <= html.TR(html.TH(html.DIV("...", id="result"), colspan=24, rowspan=20))  # word-wrap: break-word;


compute = html.BUTTON("engage")

def replace_at_index(my_str, index, new_char):
    return my_str[:index] + new_char + my_str[index + 1:]


for r in calc.rows:
    for c in r.cells:

        if c.textContent == "|":
            c.classList.add("divider")
            continue
        elif c.textContent == ".":
            c.classList.add("empty_cell")
            continue

        if r.rowIndex < 7:
            c.classList.add("locked")
        elif 8 <= r.rowIndex <= 14:
            c.classList.add("present_but_not_locked")
        else:
            c.classList.add("not_present")
        
        if r.rowIndex <= 14:
            if c.cellIndex in {0, 1, 2, 3}:
                c.classList.add("char_1")
            elif c.cellIndex in {5, 6, 7, 8}:
                c.classList.add("char_2")
            elif c.cellIndex in {10, 11, 12, 13}:
                c.classList.add("char_3")
            elif c.cellIndex in {15, 16, 17, 18}:
                c.classList.add("char_4")
            elif c.cellIndex in {20, 21, 22, 23}:
                c.classList.add("char_5")


document <= calc
document <= compute
result = document["result"]

def set_one_element_active(element, kind):
    char_index = [cl for cl in element.classList if 'char_' in cl][0]
    for r in calc.rows:
        for c in r.cells:
            if char_index in c.classList and kind in c.classList:
                if 'pressed' in c.classList:
                    c.classList.remove("pressed")
                
    element.classList.add("pressed")

def toggle_element(element):
    if not 'pressed' in element.classList:
        element.classList.add("pressed")
    else:
        element.classList.remove("pressed")

def get_letter_config():
    # any letter found in the not_present class.
    not_containing = ""
    for r in calc.rows:
        for c in r.cells:
            if "not_present" in c.classList and 'pressed' in c.classList:
                not_containing += c.text.lower()
    # print("not containing:", not_containing)

    # find all letters found in "present_but_not_locked"
    containing = ""
    for r in calc.rows:
        for c in r.cells:
            if "present_but_not_locked" in c.classList and 'pressed' in c.classList:
                containing += c.text.lower()
    containing = ''.join(set(containing))
    # print("containing:", containing)

    # for ch in "locked" if "pressed" in classList.
    locked_positions = [" ", " ", " ", " ", " "]
    for r in calc.rows:
        for c in r.cells:
            if "locked" in c.classList and 'pressed' in c.classList:
                if "char_1" in c.classList:
                    locked_positions[0] = c.text.lower()
                if "char_2" in c.classList:
                    locked_positions[1] = c.text.lower()
                if "char_3" in c.classList:
                    locked_positions[2] = c.text.lower()
                if "char_4" in c.classList:
                    locked_positions[3] = c.text.lower()
                if "char_5" in c.classList:
                    locked_positions[4] = c.text.lower()                                                            
    locked_positions = "".join(locked_positions)
    # print("locked positions:", f'|{locked_positions}|')

    extra_filter = {} # <-- for char of wordle, which char is present but definitely not at this location.

    return not_containing, containing, locked_positions, extra_filter



def action(event):
    element = event.target
    value = element.text

    if "locked" in element.classList:
        set_one_element_active(element, "locked")
    elif "present_but_not_locked" in element.classList:
        toggle_element(element)
    elif "not_present" in element.classList:
        toggle_element(element)
    
    # not_containing, containing, locked_positions, extra_filter = get_letter_config()
    inner_config['info'] = get_letter_config()

def chap(event):
    not_containing, containing, locked_positions, extra_filter = inner_config['info']    
    potential_word_list = filter_words(
        not_containing=not_containing, 
        containing=containing, 
        locked_positions=locked_positions) or []

    if len(potential_word_list) > 20:
        result.text = "word list too long.."
        return

    try:
        result.text = str(potential_word_list)
    except:
        result.text = "something happened.. why are you cheating anyway..?"


for button in document.select("td"):
    button.bind("click", action)

compute.bind("click", chap)