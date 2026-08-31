import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from system import detection, create_neightbors
from buttons import game_mode
from matplotlib.widgets import Button
from minmaxbot import minmax_bot



# dorob class pre hexagons

hexagons = []
susedia_map = {}
swapper = True
menu_open = False
mode = "PvP"


farby = {
    "red":     (1.0, 0.0, 0.0),
    "green":   (0.0, 1.0, 0.0),
    "blue":    (0.0, 0.0, 1.0),
    "yellow":  (1.0, 1.0, 0.0),
    "cyan":    (0.0, 1.0, 1.0),
    "magenta": (1.0, 0.0, 1.0),
    "orange":  (1.0, 0.5, 0.0),
    "purple":  (0.5, 0.0, 0.5),
    "pink":    (1.0, 0.0, 0.5),
    "brown":   (0.6, 0.3, 0.0),
    "lime":    (0.5, 1.0, 0.0),
    "teal":    (0.0, 0.5, 0.5),
    "navy":    (0.0, 0.0, 0.5),
    "gray":    (0.5, 0.5, 0.5)
}
farba_1 = [ "red", (1.0, 0.0, 0.0)]
farba_2 = ["blue", (0.0, 0.0, 1.0)]

def reset_board(fig):

    global swapper, menu_open

    for h in hexagons:
        h.set_facecolor("white")
        h.player = None

    swapper = True
    menu_open = False

    fig.canvas.draw_idle()

def vyber_farby(fig, okraje):

    global menu_open

    farby_list = list(farby.keys())

    ax1 = fig.add_axes([0.25, 0.95, 0.18, 0.05])
    ax2 = fig.add_axes([0.48, 0.95, 0.18, 0.05])

    b1 = Button(ax1, f"Player 1: {farba_1[0]} ▼")
    b2 = Button(ax2, f"Player 2: {farba_2[0]} ▼")

    menu1 = []
    menu2 = []

    def vytvor_menu (player):
        menu = []  

        lenght = 14

        #sedlacky bugfix
        if player == 2:
            lenght = 15

        for i in range(lenght):
            ax = fig.add_axes([
                0.25 if player == 1 else 0.48,
                0.91 - i * 0.035,
                0.18,
                0.035
            ])
            if i == 14:
                i=13
            
            btn = Button(ax, farby_list[i])
            
            ax.set_visible(False)
            menu.append((ax, btn))

        #sedlacky bugfix
        if player == 2:
            menu.pop(-1)
        
        return menu

    menu1 = vytvor_menu(1)
    menu2 = vytvor_menu(2)

    def otvor(menu):
        global menu_open

        stav = not menu[0][0].get_visible()
        
        for ax, _ in menu1 + menu2:
            ax.set_visible(False)

        for ax, _ in menu:
            ax.set_visible(stav)

        menu_open = stav

        fig.canvas.draw_idle()

        menu_open == False

    def zmen1(event, color):
        global menu_open

        if menu_open == False:
            return 

        farba_1[0] = color
        farba_1[1] = farby[color]

        for h in hexagons:
            if getattr(h, "player", None) == 1:
                h.set_facecolor(color)

        for line in okraje["red"]:
            line.set_color(color)

        b1.label.set_text(f"Player 1: {color} ▼")

        for ax, _ in menu1:
            ax.set_visible(False)

        fig.canvas.draw_idle()
        menu_open = False

    def zmen2(event, color):
        global menu_open

        if menu_open == False:
            return 
        
        farba_2[0] = color
        farba_2[1] = farby[color]

        for h in hexagons:
            if getattr(h, "player", None) == 2:
                h.set_facecolor(color)

        for line in okraje["blue"]:
            line.set_color(color)

        b2.label.set_text(f"Player 2: {color} ▼")

        for ax, _ in menu2:
            ax.set_visible(False)

        fig.canvas.draw_idle()

        menu_open = False

    b1.on_clicked(lambda e: otvor(menu1))
    b2.on_clicked(lambda e: otvor(menu2))

    for (ax, btn), color in zip(menu1, farby_list):
        btn.on_clicked(lambda e, c=color: zmen1(e, c))

    for (ax, btn), color in zip(menu2, farby_list):
        btn.on_clicked(lambda e, c=color: zmen2(e, c))

def regime(n):
    global mode
    mode = n

def farbenie(event):

    global swapper

    if event.inaxes is None or menu_open is True:
        return
    
    for hexagon in hexagons:
        contains, _ = hexagon.contains(event)

        if not contains:
            continue

        if contains and hexagon.get_facecolor()[:3] == (1, 1, 1):

            if swapper:
                hexagon.set_facecolor(farba_1[0])
                hexagon.player = 1
                swapper = False

                if mode == "PvC":
                    tah = minmax_bot(hexagons, 11, susedia_map)

                    if tah is not None:
                        hexagons[tah].set_facecolor(farba_2[0])
                        hexagons[tah].player = 2

                    swapper = True

                else:
                    swapper = False

            else:
                hexagon.set_facecolor(farba_2[0])
                hexagon.player = 2
                swapper = True

            event.canvas.draw_idle()
            detection(11, hexagons, farba_1[0], farba_2[0], susedia_map)
            break

def hex_grid(pocet, velkost_hex=1):

    global susedia_map

    fig, ax = plt.subplots(figsize=(8, 8))

    dx = 1.5 * velkost_hex + 0.23
    dy = np.sqrt(3) * velkost_hex 

    okraje = {
        "blue": [],
        "red": []
    }

    for riadok in range(pocet):
        for stlpec in range(pocet):
            x = stlpec * dx + 0.85 * riadok
            y = riadok * dy - 0.24 * riadok

            hexagon = RegularPolygon(
                (x, y),
                numVertices=6,
                radius=velkost_hex,
                orientation=0,
                edgecolor="black",
                facecolor="white",
                picker=True          
            )

            ax.add_patch(hexagon)
            hexagons.append(hexagon)
            uhly = np.radians(
                np.arange(6) * 60 + 30
            )

            vrcholy = [
                (
                    x + velkost_hex * np.cos(uhol),
                    y + velkost_hex * np.sin(uhol)
                )
                for uhol in uhly
            ]

            for strana in range(6):

                useless = False

                x1, y1 = vrcholy[strana]
                x2, y2 = vrcholy[(strana + 1) % 6]

                if stlpec == 0 and strana in [1, 2]:
                    farba = "blue"

                elif stlpec == pocet - 1 and strana in [4, 5]:
                    farba = "blue"

                elif riadok == 0 and strana in [3, 4]:
                    farba = "red"

                elif riadok == pocet - 1 and strana in [0, 1]:
                    farba = "red"

                else:
                    useless = True

                if not useless:
                    line, = ax.plot(
                        [x1, x2],
                        [y1, y2],
                        color=farba,
                        linewidth=2
                    )
                    okraje[farba].append(line)

    susedia_map = create_neightbors(pocet, velkost_hex)
    rezim = game_mode(fig, regime)
    vyber_farby(fig, okraje)

    ax_reset = fig.add_axes([0.72, 0.95, 0.12, 0.05])
    reset = Button(ax_reset, "Reset")
    reset.on_clicked(lambda event: reset_board(fig))
    
    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.axis("off")

    fig.canvas.mpl_connect("button_press_event", farbenie)

    plt.axis("off")
    plt.show()
