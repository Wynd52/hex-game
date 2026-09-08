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
    ax3 = fig.add_axes([0.01, 0.85, 0.2, 0.05])
    pvp = Button(ax3, "PvP")
    ax2.set_visible(False)
    ax3.set_visible(False)

    # AI cast, vygeneroval templete a upravil som si ho podla potreby
    """
    Chcel som dropdown, ale nenapadal ma ako to spravit a nenašiel nič v manuali tkintera
    Pre pochopenie toho čo to urobilo je spustenie dropdownu pomocou prepinania setvisible
    Následne som si tam dodal resetovanie boardy a použil dalej ideu pri prepínaní farby
    """
    def toggle(event):
        swapper = not ax2.get_visible()
        ax2.set_visible(swapper)
        ax3.set_visible(swapper)
        button.label.set_text("Game mode: chose ▲")
        fig.canvas.draw_idle()

    def select_pvc(fig, event):
        regime("PvC", fig)
        button.label.set_text("Game mode: PvC ▼")
        ax2.set_visible(False)
        ax3.set_visible(False)
        fig.canvas.draw_idle()

    def select_pvp(fig, event):
        regime("PvP", fig)
        button.label.set_text("Game mode: PvP ▼")
        ax2.set_visible(False)
        ax3.set_visible(False)
        fig.canvas.draw_idle()
    

    button.on_clicked(toggle)
    pvc.on_clicked(lambda event: select_pvc(fig, event))
    pvp.on_clicked(lambda event: select_pvp(fig, event))
    # koniec AI casti
    return button, pvc, pvp
