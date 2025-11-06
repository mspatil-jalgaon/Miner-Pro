import tkinter as tk
import pyperclip
import keyboard
import threading
import time

class BulkCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📋 Miner Pro")
        self.root.geometry("520x520")
        self.root.minsize(400, 350)
        self.root.configure(bg="#f7f9fc")
        self.root.attributes("-topmost", True)

        self.items = []
        self.last_copied = ""

        # --- Colors ---
        self.primary = "#1976d2"     # Blue
        self.light_blue = "green"
        self.text_color = "#0d47a1"

        # --- Top Bar ---
        top_frame = tk.Frame(root, bg=self.primary)
        top_frame.pack(fill="x")

        title = tk.Label(
            top_frame, text="🧾 Miner Pro",
            bg=self.primary, fg="white",
            font=("Segoe UI", 12, "bold"), pady=8
        )
        title.pack(side="left", padx=10)

        tk.Button(
            top_frame, text="Clear All", command=self.clear_all,
            bg="#ef5350", fg="white", activebackground="#e53935",
            relief="flat", font=("Segoe UI", 10, "bold"), padx=10
        ).pack(side="right", padx=10, pady=5)

        # --- Message Label ---
        self.message_label = tk.Label(
            root, text="", bg="#f7f9fc", fg="green", font=("Segoe UI", 10, "bold")
        )
        self.message_label.pack(pady=(5, 0))

        # --- Listbox Area ---
        list_frame = tk.Frame(root, bg="white", highlightbackground="#bbdefb", highlightthickness=2)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 11),
            yscrollcommand=scrollbar.set,
            selectbackground=self.light_blue,
            bg="white",
            fg=self.text_color,
            relief="flat",
            activestyle="none",
            highlightthickness=0
        )
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=self.listbox.yview)

        # --- Info Label ---
        tk.Label(
            root,
            text="💡 Copy with Ctrl+C → Double-click any entry to copy again",
            bg="#f7f9fc", fg="#555", font=("Segoe UI", 9)
        ).pack(pady=(0, 5))

        # --- Footer label ---
        footer = tk.Label(
            root,
            text="Developed by Er. Mukesh Patil",
            bg="#f7f9fc", fg="#1565c0",
            font=("Segoe UI", 9, "italic")
        )
        footer.pack(side="bottom", pady=(0, 8))

        # --- Bind double-click ---
        self.listbox.bind("<Double-Button-1>", self.on_double_click)

        # --- Start clipboard monitoring ---
        threading.Thread(target=self.watch_clipboard, daemon=True).start()

    # --- Clipboard watcher ---
    def watch_clipboard(self):
        while True:
            try:
                if keyboard.is_pressed("ctrl") and keyboard.is_pressed("c"):
                    time.sleep(0.25)
                    text = pyperclip.paste().strip()
                    if text and text != self.last_copied:
                        self.last_copied = text
                        self.items.append(text)
                        display = (text[:100] + "...") if len(text) > 100 else text
                        self.listbox.insert(tk.END, f"{len(self.items)}. {display}")
                        self.show_temp_message("✅ Copied & saved")
                    time.sleep(0.6)
            except Exception:
                pass
            time.sleep(0.1)

    # --- Double-click copy ---
    def on_double_click(self, event):
        index = self.listbox.curselection()
        if not index:
            return
        pyperclip.copy(self.items[index[0]])
        self.show_temp_message(f"📋 Copied item {index[0] + 1}")

    # --- Show short message ---
    def show_temp_message(self, text, duration=1):
        self.message_label.config(text=text)
        self.root.after(int(duration * 1000), lambda: self.message_label.config(text=""))

    # --- Clear all ---
    def clear_all(self):
        self.items.clear()
        self.listbox.delete(0, tk.END)
        self.last_copied = ""
        self.show_temp_message("🧹 Cleared all entries!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BulkCopyApp(root)
    root.mainloop()
