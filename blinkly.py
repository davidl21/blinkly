import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Timer
import sys

class Blinkly:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blinkly")
        self.root.geometry("400x200")
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.bind("<Command-q>", lambda event: self.close_app())

        self.interval = tk.IntVar(value=20)

        # GUI
        self.build_gui()

        self.reminder_window = None
        self.root.mainloop()
    
    def build_gui(self):
        # Main window label
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=10, fill='both', expand=True)
        
        ttk.Label(
            main_frame, 
            text="Set Reminder Interval in Minutes:", 
            font=("Helvetica", 16)
        ).pack(pady=10)
        
        self.interval_entry = ttk.Entry(
            main_frame, 
            textvariable=self.interval, 
            font=("Helvetica", 16), 
            width=10
        )
        self.interval_entry.pack(pady=5)

        # start button
        start_button = ttk.Button(main_frame, text="Start Blinkly", command=self.start_timer)
        start_button.pack(pady=10)

        # close button
        close_button = ttk.Button(main_frame, text="Close Blinkly", command=self.close_app)
        close_button.pack(pady=5)

    def start_timer(self):
        try:
            minutes = int(self.interval.get())
            if minutes <= 0:
                raise ValueError("Interval must be greater than 0")
            
            messagebox.showinfo("Blink Reminder", f"Blinkly set for {minutes} minutes.")
            print(f"Blinkly timer started for {minutes} minutes.")
            self.schedule_reminder(minutes * 60)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of minutes.")
    
    def schedule_reminder(self, seconds):
        self.timer = Timer(seconds, self.show_reminder)
        self.timer.start()
    
    def show_reminder(self):
        self.reminder_window = tk.Toplevel(self.root)
        self.reminder_window.title("Blinkly")
        self.reminder_window.attributes("-fullscreen", True)
        self.reminder_window.attributes("-topmost", True)
        
        reminder_frame = ttk.Frame(self.reminder_window)
        reminder_frame.pack(fill="both", expand=True)
        
        style = ttk.Style()
        style.configure('Reminder.TLabel', 
                       font=("Helvetica", 30),
                       foreground='black',
                       background='white')
        
        ttk.Label(
            reminder_frame, 
            text="Time to blink!", 
            style='Reminder.TLabel'
        ).pack(expand=True)

        dismiss_button = ttk.Button(
            reminder_frame,
            text="Dismiss Timer", 
            command=self.dismiss_reminder
        )
        dismiss_button.pack(pady=20)

        self.reminder_window.bind("<Escape>", lambda e: self.dismiss_reminder())

    def dismiss_reminder(self):
        if self.reminder_window:
            self.reminder_window.destroy()
            self.reminder_window = None
            print("Reminder dismissed.")

            self.schedule_reminder(self.interval.get() * 60)

    def close_app(self):
        if messagebox.askyesno("Exit Blinkly", "Are you sure you want to exit Blinkly?"):
            print("Closing Blinkly...")
            if hasattr(self, "timer") and self.timer.is_alive():
                self.timer.cancel()
            self.root.quit()
            sys.exit()

if __name__ == "__main__":
    Blinkly()