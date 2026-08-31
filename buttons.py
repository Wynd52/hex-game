import tkinter as tk
from matplotlib.widgets import Button

def vyherca(farba):

    root = tk.Tk()
    root.withdraw()

    tk.messagebox.showinfo(
        "End of game",
        f"Winner is {farba} player!"
    )

    root.destroy()

def game_mode(fig, regime):
    ax = fig.add_axes([0.01, 0.95, 0.2, 0.05])
    button = Button(ax, "Game mode: PvP ▼")

    ax2 = fig.add_axes([0.01, 0.9, 0.2, 0.05])
    pvc = Button(ax2, "PvC")
    ax2.set_visible(False)

    def toggle(event):
        ax2.set_visible(not ax2.get_visible())
        button.label.set_text(
            "Game mode: PvP ▲" if ax2.get_visible()
            else "Game mode: PvP ▼"
        )
        fig.canvas.draw_idle()

    def select_pvc(event):
        regime("PvC")
        button.label.set_text("Game mode: PvC ▼")
        ax2.set_visible(False)
        fig.canvas.draw_idle()

    button.on_clicked(toggle)
    pvc.on_clicked(select_pvc)

    return button, pvc
