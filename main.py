import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import RoutingSimulationGUI


def main():
    root = tk.Tk()
    app = RoutingSimulationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
