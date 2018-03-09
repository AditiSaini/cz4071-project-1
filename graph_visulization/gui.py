from __future__ import division
from tkinter import *
from PIL import ImageTk, Image

APP_NAME = "CZ4071 graph visualization"

# global properties
current_graph = "tpch"
current_property = "d-dist"

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
    if current_graph == "tpch":
        display_image(graph_canvas, "tpch_graph.png", graph_width, graph_height)
    elif current_graph == "random":
        display_image(graph_canvas, "test.png", graph_width, graph_height)
    elif current_graph == "scale":
        display_image(graph_canvas, "test2.png", graph_width, graph_height)
    print("Updated graph to " + current_graph)


def update_property():
    global plot_canvas1, plot_canvas2, plot_canvas3, plot_width, plot_height
    if current_property == "bc":
        display_image(plot_canvas1, "tpch_graph.png", plot_width, plot_height)
        display_image(plot_canvas2, "test.png", plot_width, plot_height)
        display_image(plot_canvas3, "test2.png", plot_width, plot_height)
    elif current_property == "close":
        display_image(plot_canvas1, "test.png", plot_width, plot_height)
        display_image(plot_canvas2, "tpch_graph.png", plot_width, plot_height)
        display_image(plot_canvas3, "test2.png", plot_width, plot_height)
    elif current_property == "d-dist":
        display_image(plot_canvas1, "tpch_graph.png", plot_width, plot_height)
        display_image(plot_canvas2, "test2.png", plot_width, plot_height)
        display_image(plot_canvas3, "test.png", plot_width, plot_height)
    elif current_property == "bc-close":
        display_image(plot_canvas1, "test2.png", plot_width, plot_height)
        display_image(plot_canvas2, "test.png", plot_width, plot_height)
        display_image(plot_canvas3, "tpch_graph.png", plot_width, plot_height)
    elif current_property == "close-d":
        display_image(plot_canvas1, "tpch_graph.png", plot_width, plot_height)
        display_image(plot_canvas2, "test.png", plot_width, plot_height)
        display_image(plot_canvas3, "test2.png", plot_width, plot_height)
    elif current_property == "bc-d":
        display_image(plot_canvas1, "tpch_graph.png", plot_width, plot_height)
        display_image(plot_canvas2, "test.png", plot_width, plot_height)
        display_image(plot_canvas3, "test2.png", plot_width, plot_height)
    elif current_property == "d-corr":
        display_image(plot_canvas1, "tpch_graph.png", plot_width, plot_height)
        display_image(plot_canvas2, "test.png", plot_width, plot_height)
        display_image(plot_canvas3, "test2.png", plot_width, plot_height)
    print("Updated property to " + current_property)

def set_property(prop):
    global current_property
    current_property = prop
    update_property()

def set_graph(g):
    global current_graph
    current_graph = g
    update_graph()

if __name__ == "__main__":
    # the app window
    root = Tk()
    root.title(APP_NAME)
    screen_width = root.winfo_screenwidth() - 50
    screen_height = root.winfo_screenheight() - 100
    root.geometry(str(screen_width) + "x" + str(screen_height))
    #root.resizable(width=False, height=False)

    # the graph visualization region
    graph_width = int(screen_width * 0.73)
    graph_height = screen_height - 60
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
    button_region = Frame(root, width=screen_width, height=60)
    button_region.grid(row=3, column=0, columnspan=2)

    Label(button_region, text="Choose graph:").pack(side=LEFT)
    Button(button_region, text="TPC-H", command=(lambda: set_graph("tpch"))).pack(side=LEFT)
    Button(button_region, text="Random", command=(lambda: set_graph("random"))).pack(side=LEFT)
    Button(button_region, text="Scale-free", command=(lambda: set_graph("scale"))).pack(side=LEFT)

    Label(button_region, text="Choose property:").pack(side=LEFT)
    Button(button_region, text="Betweenness (BC)", command=(lambda: set_property("bc"))).pack(side=LEFT)
    Button(button_region, text="Closeness", command=(lambda: set_property("close"))).pack(side=LEFT)
    Button(button_region, text="Degree dist.", command=(lambda: set_property("d-dist"))).pack(side=LEFT)
    Button(button_region, text="BC v.s. Closeness", command=(lambda: set_property("bc-close"))).pack(side=LEFT)
    Button(button_region, text="BC v.s. Degree", command=(lambda: set_property("bc-d"))).pack(side=LEFT)
    Button(button_region, text="Closeness v.s. Degree", command=(lambda: set_property("close-d"))).pack(side=LEFT)
    Button(button_region, text="Degree correlation", command=(lambda: set_property("d-corr"))).pack(side=LEFT)

    root.mainloop()
