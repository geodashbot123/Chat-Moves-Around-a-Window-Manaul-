import pytchat
import tkinter as tk
from tkinter import messagebox
import sys

chat = None
window_width = 400
window_height = 300

move_speed = 100     
resize_speed = 100   

MIN_WIDTH, MIN_HEIGHT = 150, 100
MAX_WIDTH, MAX_HEIGHT = 1200, 900

root = tk.Tk()
root.title("YouTube ID Setup")
root.configure(bg="gray")
root.attributes("-topmost", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

setup_frame = tk.Frame(root, bg="gray")
setup_frame.pack(expand=True)

instruction_label = tk.Label(
    setup_frame, 
    text="Enter your YouTube Live Video ID:", 
    font=("Arial", 12, "bold"), 
    fg="white", 
    bg="gray"
)
instruction_label.pack(pady=10)

id_entry = tk.Entry(setup_frame, font=("Arial", 12), width=20, justify="center")
id_entry.pack(pady=5)
id_entry.focus_set()

def connect_stream():
    global chat
    video_id = id_entry.get().strip()
    
    if not video_id:
        messagebox.showwarning("Warning", "Please enter a valid Video ID!")
        return
        
    try:
        chat = pytchat.create(video_id=video_id)
        setup_frame.pack_forget()
        root.title("Chat Controls Moves around my desktop")
        status_label.config(text=f"Connected to ID: {video_id}\nWaiting for chat commands...")
        status_label.pack(expand=True)
        update_and_move()
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to YouTube: {e}")

submit_btn = tk.Button(setup_frame, text="Start Blocker Game", font=("Arial", 10, "bold"), command=connect_stream)
submit_btn.pack(pady=15)

status_label = tk.Label(root, text="", font=("Arial", 14, "bold"), fg="white", bg="gray", wraplength=350)

def update_and_move():
    global window_x, window_y, window_width, window_height
    
    if chat and chat.is_alive():
        for c in chat.get().sync_items():
            raw_msg = c.message.strip()
            msg = raw_msg.lower()
            
            if msg.startswith("!"):
                msg = "." + msg[1:]
                
            current_screen_width = root.winfo_screenwidth()
            current_screen_height = root.winfo_screenheight()
            
            success_msg = ""
            
            # --- 1. NEW !TALK / .TALK COMMAND ---
            if msg.startswith(".talk "):
                # Extract the actual words typed after the command
                talk_text = raw_msg[6:].strip() 
                if talk_text:
                    success_msg = f"{c.author.name}: {talk_text}"
            
            # --- 2. MOVEMENT COMMANDS ---
            elif msg == ".up":
                window_y -= move_speed
                success_msg = f"{c.author.name} moved the window UP!"
            elif msg == ".down":
                window_y += move_speed
                success_msg = f"{c.author.name} moved the window DOWN!"
            elif msg == ".left":
                window_x -= move_speed
                success_msg = f"{c.author.name} moved the window LEFT!"
            elif msg == ".right":
                window_x += move_speed
                success_msg = f"{c.author.name} moved the window RIGHT!"
            elif msg == ".center":
                window_x = (current_screen_width - window_width) // 2
                window_y = (current_screen_height - window_height) // 2
                success_msg = f"{c.author.name} RESET the window to center!"
            elif msg == ".big":
                window_width = min(window_width + resize_speed, MAX_WIDTH, current_screen_width)
                window_height = min(window_height + resize_speed, MAX_HEIGHT, current_screen_height)
                success_msg = f"{c.author.name} made the window BIGGER!"
            elif msg == ".small":
                window_width = max(window_width - resize_speed, MIN_WIDTH)
                window_height = max(window_height - resize_speed, MIN_HEIGHT)
                success_msg = f"{c.author.name} made the window SMALLER!"
            elif msg.startswith("."):
                color_choice = msg[1:]
                try:
                    root.configure(bg=color_choice)
                    status_label.configure(bg=color_choice) 
                    success_msg = f"{c.author.name} changed the color to {color_choice}!"
                except tk.TclError:
                    pass  
            
            if success_msg:
                status_label.config(text=success_msg)
            
            # Make sure text wrapping scales with window width
            status_label.config(wraplength=max(100, window_width - 40))
            
            window_x = max(0, min(window_x, current_screen_width - window_width))
            window_y = max(0, min(window_y, current_screen_height - window_height))
                
            root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    root.after(100, update_and_move)

root.mainloop()
