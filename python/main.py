from browser import document, svg, html
import sv_easing_functions

doc_box = """
The graphs below represent the easing functions implemented in the Easing node, they are calculated from
the same functions used in Sverchok. If you hover your mouse over a graph, the codebox will show the python 
function for that graph.
"""


num_points_high = 80
num_points_low = 20
deltas_high = [i/num_points_high for i in range(num_points_high+1)]
deltas_low = [i/num_points_low for i in range(num_points_low+1)]

scale = 150

path_y_offset = 210
rect_y_offset = path_y_offset - scale 
g_x_offset, g_y_offset = 25, 0

def get_points(name, idx):
    """ some functions only need few points so we speed up this function by switching after 21 """
    func = getattr(sv_easing_functions, name)
    points = deltas_high if idx > 21 else deltas_low 
    results = [(delta, -func(delta)) for delta in points]
    return "M " + " ".join([f"{r[0]:.4f},{r[1]:.4f}" for r in results])

for idx, easing_func in sv_easing_functions.easing_dict.items():
    if idx == 0:
        continue
        
    easing_name = easing_func.__name__

    svg_tag = html.SVG(xmlns="http://www.w3.org/2000/svg", width=200, height=280, style={})
    svg_tag <= svg.g(id=easing_name, transform=f"translate({g_x_offset} {g_y_offset})")
    document <= svg_tag

    title = svg.text(easing_name, x=70, y=25, font_size=17, text_anchor="middle")
    bg = svg.rect(x=0, y=rect_y_offset, width=150, height=150, stroke="#999", fill="#cdcdcd")
    path = svg.path(
        transform=f"translate(0, {path_y_offset})\nscale(150, 150)", fill="none", stroke="#333", vector_effect="non-scaling-stroke",
        stroke_width="2", d=get_points(easing_name, idx))
    panel = document[easing_name]
    panel <= title
    panel <= bg
    panel <= path
