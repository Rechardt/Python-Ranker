# main.py
from tkinter import *
from tkinter import messagebox
import app

class RankerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ranker")
        self.root.geometry("300x400")
        self.root.eval('tk::PlaceWindow . top')

        self.ranker = app.Ranker()

        self.setup_ui()

    def setup_ui(self):
        # Create welcome message
        welcome_message = Label(self.root, text="Welcome to the ranker", width=22, font=('Helvetica', 12))
        welcome_message.pack(padx=10, pady=10)

        # Create entry box for items
        self.entry_box = Entry(self.root, width=10, font=('Helvetica', 15))
        self.entry_box.pack(padx=10, pady=10)
        self.entry_box.focus()
        
        # Create enter button
        submit_btn = Button(self.root, text="Add", width=13,command=lambda: self.enter_item(), font=('Helvetica', 12))
        submit_btn.pack(pady=5)

        # Create a rank button
        rank_btn = Button(self.root, text="Start Ranking", command=self.start_ranking, font=('Helvetica', 12), width=13)
        rank_btn.pack(pady=5)

        # Box to hold items entered
        self.list_box = Listbox(self.root, width=20)
        self.list_box.pack(padx=10)

        # Delete item button
        del_btn = Button(self.root, text="Delete Item", command=self.delete_item, font=('Helvetica', 12))
        del_btn.pack(pady=5)

        # Frame for ranking options
        self.ranking_frame = Frame(self.root)
        self.option_a_button = Button(self.ranking_frame, text="", command=lambda: self.record_vote(1), font=('Helvetica', 12), width=20)
        self.option_a_button.grid(column=0, row=0, padx=5, pady=5)
        self.option_b_button = Button(self.ranking_frame, text="", command=lambda: self.record_vote(0), font=('Helvetica', 12), width=20)
        self.option_b_button.grid(column=0, row=1, padx=5, pady=5)

        self.root.bind("<Return>", lambda event: self.enter_item())

    def enter_item(self):
        item = self.entry_box.get()
        if item:
            self.ranker.add_item(item)
            items = self.ranker.get_items()
            self.list_box.delete(0, END)
            for i in items:
                self.list_box.insert(END, i)
            self.entry_box.delete(0, END)
        else:
            messagebox.showwarning("Empty Input", "Please enter a valid item.")
        return
    
    def delete_item(self):
        selected_index = self.list_box.curselection()
        print(selected_index)
        if selected_index:
            item = self.list_box.get(selected_index)
            self.list_box.delete(selected_index)
            self.ranker.item_scores.pop(item, None)
        else:
            messagebox.showwarning("No Selection", "Please select an item to delete.")
    
    def start_ranking(self):
        items = self.ranker.get_items()
        if not items:
            messagebox.showwarning(title="No items entered", message="Enter items to start ranking")
            return
        elif len(items) == 1:
            messagebox.showwarning(title="Enter more than 1 item", message="Enter more items")
            return

        self.rounds = min(self.ranker.MAX_ROUNDS, (len(items) * (len(items) - 1)) / 2)
        self.last_option_a = None
        self.last_option_b = None
        self.list_box.pack_forget()
        self.ranking_frame.pack(pady=10)
        self.next_round()

    def next_round(self):
        if self.rounds <= 0:
            self.display_ranking()
            return

        self.option_a, self.option_b = self.ranker.get_next_pair(self.last_option_a, self.last_option_b)
        self.option_a_button.config(text=self.option_a)
        self.option_b_button.config(text=self.option_b)

    def record_vote(self, choice):
        if choice == 1:
            winner = self.option_a
            loser = self.option_b
        else:
            winner = self.option_b
            loser = self.option_a

        elo_change = self.ranker.update_elo(winner, loser)

        self.last_option_a = self.option_a
        self.last_option_b = self.option_b

        if elo_change <= self.ranker.THRESHOLD:
            self.display_ranking()
            return

        self.rounds -= 1
        self.next_round()

    def display_ranking(self):
        ranking_window = Toplevel(self.root)
        ranking_window.title("Final Ranking")

        sorted_items = self.ranker.get_sorted_items()
        Label(ranking_window, text="Final Ranking:", font=('Helvetica', 14, 'bold')).pack(pady=10)

        for count, (item, score) in enumerate(sorted_items, start=1):
            Label(ranking_window, text=f"{count}. {item}", font=('Helvetica', 12)).pack()

        self.ranking_frame.pack_forget()
        self.list_box.pack(pady=10)

        self.reset()

    def reset(self):
        self.ranker.reset()
        self.list_box.delete(0,'end')

if __name__ == "__main__":
    root = Tk()
    app = RankerApp(root)
    root.mainloop()