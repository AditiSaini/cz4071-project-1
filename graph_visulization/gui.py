from __future__ import division
from tkinter import *
from PIL import ImageTk, Image
import os

APP_NAME = "CZ4071 graph visualization"

def display_image(widget, image_file, width, height):
    """
    Put image into label
    """
    img_ori = Image.open(image_file)
    img_ori = img_ori.resize((width, height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img_ori)
    widget.configure(image=img)
    widget.image = img

def update_graph():
    global graph_canvas, graph_width, graph_height
    graph_str = current_graph.get()
    overlay_str = current_overlay.get()
    base_dir = os.path.join(result_dir, graph_str)
    if overlay_str == "none":
        display_image(graph_canvas, os.path.join(base_dir, "graph.png"), graph_width, graph_height)
    elif overlay_str == "bc":
        display_image(graph_canvas, os.path.join(base_dir, "betweenness.png"), graph_width, graph_height)
    elif overlay_str == "close":
        display_image(graph_canvas, os.path.join(base_dir, "closeness.png"), graph_width, graph_height)
    print("Updated graph to " + graph_str + " with overlay " + overlay_str)

def update_property():
    global plot_canvas1, plot_canvas2, plot_canvas3, plot_width, plot_height
    prop_str = current_property.get()
    g_with_canvas = [
        ("tpch", plot_canvas1),
        ("random", plot_canvas2),
        ("scale_free", plot_canvas3),
    ]
    for g, canvas in g_with_canvas:
        base_dir = os.path.join(result_dir, g)
        if prop_str == "d_dist":
            display_image(canvas, os.path.join(base_dir, "degree_distribution.png"), plot_width, plot_height)
        elif prop_str == "bc_close":
            display_image(canvas, os.path.join(base_dir, "test2.png"), plot_width, plot_height)
        elif prop_str == "close_deg":
            display_image(canvas, os.path.join(base_dir, "tpch_graph.png"), plot_width, plot_height)
        elif prop_str == "bc_deg":
            display_image(canvas, os.path.join(base_dir, "tpch_graph.png"), plot_width, plot_height)
        elif prop_str == "d_corr":
            display_image(canvas, os.path.join(base_dir, "degree_corr.png"), plot_width, plot_height)
    print("Updated property to " + prop_str)

def set_property(prop):
    global current_property
    current_property = prop
    update_property()

def set_graph(g):
    global current_graph
    current_graph = g
    update_graph()

if __name__ == "__main__":
    result_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "results")
    print(result_dir)
    # the app window
    root = Tk()
    root.title(APP_NAME)
    screen_width = root.winfo_screenwidth() - 50
    screen_height = root.winfo_screenheight() - 80
    root.geometry(str(screen_width) + "x" + str(screen_height))
    #root.resizable(width=False, height=False)

    # the graph visualization region
    graph_width = int(screen_width * 0.73)
    graph_height = screen_height - 80
    graph_region = Frame(root, width=graph_width, height=graph_height)
    graph_region.grid(row=0, rowspan=3, column=0)
    Label(graph_region, text="Graph").pack()
    img_ori = Image.open("tpch_graph.png")
    img_ori = img_ori.resize((graph_width, graph_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img_ori)
    graph_canvas = Label(graph_region, image=img, width=graph_width, height=graph_height, borderwidth=2)
    graph_canvas.pack(side=BOTTOM)

    # the plot region
    plot_width = screen_width - graph_width
    plot_height = int(graph_height / 3) - 20

    # plot for TPC-H graph
    plot_region1 = Frame(root, width=plot_width, height=plot_height)
    plot_region1.grid(row=0, column=1)
    Label(plot_region1, text="TPC-H graph property").pack()
    img_ori2 = Image.open("tpch_graph.png")
    img_ori2 = img_ori2.resize((plot_width, plot_height), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img_ori2)
    plot_canvas1 = Label(plot_region1, image=img2, width=plot_width, height=plot_height)
    plot_canvas1.pack(side=BOTTOM)

    # plot for random graph
    plot_region2 = Frame(root, width=plot_width, height=plot_height)
    plot_region2.grid(row=1, column=1)
    Label(plot_region2, text="Random graph property").pack()
    img_ori3 = Image.open("tpch_graph.png")
    img_ori3 = img_ori3.resize((plot_width, plot_height), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(img_ori3)
    plot_canvas2 = Label(plot_region2, image=img3, width=plot_width, height=plot_height)
    plot_canvas2.pack(side=BOTTOM)

    # plot for scale-free graph
    plot_region3 = Frame(root, width=plot_width, height=plot_height)
    plot_region3.grid(row=2, column=1)
    Label(plot_region3, text="Scale-free graph property").pack()
    img_ori4 = Image.open("tpch_graph.png")
    img_ori4 = img_ori4.resize((plot_width, plot_height), Image.ANTIALIAS)
    img4 = ImageTk.PhotoImage(img_ori4)
    plot_canvas3 = Label(plot_region3, image=img4, width=plot_width, height=plot_height)
    plot_canvas3.pack(side=BOTTOM)

    # button region
    button_region_1 = Frame(root, width=screen_width, height=60)
    button_region_1.grid(row=3, column=0, columnspan=2)
    current_graph = StringVar()
    current_overlay = StringVar()
    current_property = StringVar()

    Label(button_region_1, text="Choose graph:").pack(side=LEFT)
    GRAPHS = [
        ("TPC-H", "tpch"),
        ("Random", "random"),
        ("Scale-free", "scale_free")
    ]
    current_graph.set("tpch")
    for text, val in GRAPHS:
        Radiobutton(button_region_1, text=text, variable=current_graph, value=val, command=update_graph).pack(side=LEFT)

    Label(button_region_1, text="Choose overlay:").pack(side=LEFT, padx=(20, 0))
    OVERLAYS = [
        ("None", "none"),
        ("Betweenness centrality (BC)", "bc"),
        ("Closeness centrality", "close")
    ]
    current_overlay.set("none")
    for text, val in OVERLAYS:
        Radiobutton(button_region_1, text=text, variable=current_overlay, value=val, command=update_graph).pack(side=LEFT)

    button_region_2 = Frame(root, width=screen_width, height=60)
    button_region_2.grid(row=4, column=0, columnspan=2)
    Label(button_region_2, text="Choose property:").pack(side=LEFT)
    PROPERTIES = [
        ("Degree Distribution", "d_dist"),
        ("Degree Correlation", "d_corr"),
        ("Degree BC v.s. Closeness", "bc_close"),
        ("Degree BC v.s. Degree", "bc_deg"),
        ("Degree Close v.s. Degree", "close_deg"),
    ]
    current_property.set("d_dist")
    for text, val in PROPERTIES:
        Radiobutton(button_region_2, text=text, variable=current_property, value=val, command=update_property).pack(side=LEFT)

    update_graph()
    update_property()
    root.mainloop()
