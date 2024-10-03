from PIL import ImageGrab
import tkinter as tk
import threading
from pynput.mouse import Listener

# Fonction pour convertir le RVB en HEX (utilistation du module pynput)
def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# Fonction pour avoir la couleur du pixel à une position exacte
def get_pixel_color(x, y):
    # Capture l'écran (pas la fenêtre overlay(utilisation du module ImageGrab)
    screen = ImageGrab.grab()
    # Trouve la valeur RVB à la position (x, y)
    color = screen.getpixel((x, y))
    return color

# Fonction qui gère le cliquage de cte souris à la con
def on_click(x, y, button, pressed):
    if pressed:  # là c'est cliqué
        # définis la couleur sur celle du pixel cliqué (en gros)
        color = get_pixel_color(x, y)
        # convertis de RVB à HEX
        hex_color = rgb_to_hex(*color)
        # Mets à jour le GUI avec l'information HEX
        update_gui(x, y, hex_color, color)

# Fonction pour démarrer le mouse_listener (suit la souris)
def start_listener():
    # commence à enregistrer les clics de la souris
    with Listener(on_click=on_click) as listener:
        listener.join()

# Fonction pour mettre à jour le GUI du tkinter
def update_gui(x, y, hex_color, rgb_color):
    coord_label.config(text=f"Coordonnées: ({x}, {y})")
    hex_label.config(text=f"HEX: {hex_color}")
    # Mets à jour la boîte de prévisualisation de la couleur
    color_preview.config(bg=hex_color)
    rgb_label.config(text=f"RVB: {rgb_color}")

# Fonction pour gérér la transparence de l'overlay et si il est en plein écran, c'est écrit en dessous je me fais chier pour rien à écrire ce commentaire inutile je connais mon code bordel (non)
def make_overlay(window):
    window.attributes("-alpha", 1)  # Transparence (0 = totalement transparent, 1 = opaque)
    window.attributes("-fullscreen", True)  # Gère le plein écran
    window.attributes("-topmost", False)  # fais en sorte que l'overlay soit tout le temps au premier plan
    window.config(bg="")  # gère l'arrière plan (pas vraiment important vu qu'il est censé être transparent)

# Setup de l'environnement graphique de l'appli (ça rend le truc un peu moins moche je crois)
def setup_gui():
    global coord_label, hex_label, color_preview, rgb_label
    
    root = tk.Tk()
    make_overlay(root)  # Transforme la fenêtre en Overlay
    
    # Instructions du label
    label = tk.Label(root, text="Clique n'importe où pour avoir la couleur (Mode Overlay)", font=('Arial', 12), bg="black", fg="white")
    label.pack(pady=10)
    
    # Coordonnées du label
    coord_label = tk.Label(root, text="Coordonnées: (---, ---)", font=('Arial', 10), bg="black", fg="white")
    coord_label.pack(pady=5)
    
    # couleur HEX du label
    hex_label = tk.Label(root, text="HEX: #------", font=('Arial', 10), bg="black", fg="white")
    hex_label.pack(pady=5)
    
    # couleur RVB du label
    rgb_label = tk.Label(root, text="RVB: (---, ---, ---)", font=('Arial', 10), bg="black", fg="white")
    rgb_label.pack(pady=5)
    
    # boîte de prévisualisation de la couleur
    color_preview = tk.Label(root, text="", width=20, height=3, relief="solid", bg="black")
    color_preview.pack(pady=10)
    
    # bouton quitter (Assez explicite je pense)
    exit_button = tk.Button(root, text="Quitter", command=root.quit, bg="red", fg="white")
    exit_button.pack(pady=20)
    
    # Démarre l'écouteur de la souris en arrière plan  (dans un thread)
    listener_thread = threading.Thread(target=start_listener, daemon=True)
    listener_thread.start()

    root.mainloop()

# Lance ce programme (qui pue un peu on peut se l'avouer)
setup_gui()
