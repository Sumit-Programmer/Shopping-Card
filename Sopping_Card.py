import customtkinter as ctk
from tkinter import messagebox
import json

# Functions for loading and saving the cart
def search_item():
    search_term = entry_search.get().lower()
    if not search_term:
        messagebox.showerror("Invalid input", "Please enter an item name to search.")
        return

    for widget in frame_cart.winfo_children():
        widget.destroy()

    results = [item for item in cart if search_term in item['name'].lower()]

    if not results:
        label = ctk.CTkLabel(frame_cart, text="No items found.")
        label.pack()
    else:
        total_price = 0
        for i, item in enumerate(results, start=1):
            item_label = ctk.CTkLabel(frame_cart, text=f"{i}. {item['name']} (x{item['quantity']}): ${item['price'] * item['quantity']}")
            item_label.pack()
            total_price += item['price'] * item['quantity']

        total_label = ctk.CTkLabel(frame_cart, text=f"Total: ${total_price}")
        total_label.pack()

def edit_item():
    try:
        index = int(entry_edit_index.get()) - 1
        if 0 <= index < len(cart):
            name = entry_edit_name.get()
            price = float(entry_edit_price.get())
            quantity = int(entry_edit_quantity.get())

            cart[index] = {"name": name, "price": price, "quantity": quantity}
            messagebox.showinfo("Item edited", f"Item {index + 1} has been updated.")
            entry_edit_index.delete(0, ctk.END)
            entry_edit_name.delete(0, ctk.END)
            entry_edit_price.delete(0, ctk.END)
            entry_edit_quantity.delete(0, ctk.END)
            display_cart()
        else:
            messagebox.showerror("Invalid index", "Please enter a valid item number.")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid details.")

def sort_items(by):
    if by == "name":
        cart.sort(key=lambda x: x["name"].lower())
    elif by == "price":
        cart.sort(key=lambda x: x["price"])
    elif by == "quantity":
        cart.sort(key=lambda x: x["quantity"])
    display_cart()

def clear_cart():
    cart.clear()
    display_cart()
    messagebox.showinfo("Cart cleared", "All items have been removed from the cart.")

def save_cart(cart):
    with open('cart.json', 'w') as f:
        json.dump(cart, f)

def load_cart():
    try:
        with open('cart.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Functions for managing the cart
def add_item():
    name = entry_name.get()
    try:
        price = float(entry_price.get())
        quantity = int(entry_quantity.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid price and quantity.")
        return
    
    if name and price > 0 and quantity > 0:
        cart.append({"name": name, "price": price, "quantity": quantity})
        messagebox.showinfo("Item added", f"{name} added to cart.")
        entry_name.delete(0, ctk.END)
        entry_price.delete(0, ctk.END)
        entry_quantity.delete(0, ctk.END)
        display_cart()
    else:
        messagebox.showerror("Invalid input", "Please enter valid name, price, and quantity.")

def remove_item():
    try:
        index = int(entry_remove.get()) - 1
        if 0 <= index < len(cart):
            removed_item = cart.pop(index)
            messagebox.showinfo("Item removed", f"{removed_item['name']} removed from cart.")
            entry_remove.delete(0, ctk.END)
            display_cart()
        else:
            messagebox.showerror("Invalid index", "Please enter a valid item number.")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid item number.")

def display_cart():
    for widget in frame_cart.winfo_children():
        widget.destroy()

    if not cart:
        label = ctk.CTkLabel(frame_cart, text="Your cart is empty.")
        label.pack()
    else:
        total_price = 0
        for i, item in enumerate(cart, start=1):
            item_label = ctk.CTkLabel(frame_cart, text=f"{i}. {item['name']} (x{item['quantity']}): ${item['price'] * item['quantity']}")
            item_label.pack()
            total_price += item['price'] * item['quantity']

        total_label = ctk.CTkLabel(frame_cart, text=f"Total: ${total_price}")
        total_label.pack()

def on_closing():
    save_cart(cart)
    root.destroy()

# Main GUI setup
cart = load_cart()
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

root = ctk.CTk()
root.geometry("550x700")
root.resizable(False, False)
root.title("Shopping Cart BY 'Sumit-Progrmmer' ")

# Add item section
frame_add = ctk.CTkFrame(root)
frame_add.pack(pady=10)

label_name = ctk.CTkLabel(frame_add, text="Item name:")
label_name.grid(row=0, column=0)
entry_name = ctk.CTkEntry(frame_add, placeholder_text="Item name", text_color="#FFCC70")
entry_name.grid(row=0, column=1)

label_price = ctk.CTkLabel(frame_add, text="Item price:")
label_price.grid(row=1, column=0)
entry_price = ctk.CTkEntry(frame_add, placeholder_text="$0.00", text_color="#FFCC70")
entry_price.grid(row=1, column=1)

label_quantity = ctk.CTkLabel(frame_add, text="Item quantity:")
label_quantity.grid(row=2, column=0)
entry_quantity = ctk.CTkEntry(frame_add, placeholder_text="0", text_color="#FFCC70")
entry_quantity.grid(row=2, column=1)

button_add = ctk.CTkButton(frame_add, text="Add item", border_color="#7605FF", fg_color='transparent', border_width=2.5, hover_color='#013AC0', command=add_item)
button_add.grid(row=3, columnspan=2, pady=10)

# Display cart section
frame_cart = ctk.CTkFrame(root)
frame_cart.pack(pady=10)
display_cart()

# Remove item section
frame_remove = ctk.CTkFrame(root)
frame_remove.pack(pady=10)

label_remove = ctk.CTkLabel(frame_remove, text="Item number to remove:")
label_remove.grid(row=0, column=0)
entry_remove = ctk.CTkEntry(frame_remove, placeholder_text="1", text_color="red")
entry_remove.grid(row=0, column=1)

button_remove = ctk.CTkButton(frame_remove, text="Remove item", border_color="red", fg_color='transparent', border_width=2.5, hover_color='red', command=remove_item)
button_remove.grid(row=1, columnspan=2, pady=10)

frame_search = ctk.CTkFrame(root)
frame_search.pack(pady=10)

label_search = ctk.CTkLabel(frame_search, text="Search item by name:")
label_search.grid(row=0, column=0)
entry_search = ctk.CTkEntry(frame_search, placeholder_text="Item name", text_color="#FFCC70")
entry_search.grid(row=0, column=1)

button_search = ctk.CTkButton(frame_search, text="Search", border_color="#7605FF", fg_color='transparent', border_width=2.5, hover_color='#013AC0', command=search_item)
button_search.grid(row=1, columnspan=2, pady=10)

frame_edit = ctk.CTkFrame(root)
frame_edit.pack(pady=10)

label_edit_index = ctk.CTkLabel(frame_edit, text="Item number to edit:")
label_edit_index.grid(row=0, column=0)
entry_edit_index = ctk.CTkEntry(frame_edit, placeholder_text="1", text_color="#FFCC70")
entry_edit_index.grid(row=0, column=1)

label_edit_name = ctk.CTkLabel(frame_edit, text="New item name:")
label_edit_name.grid(row=1, column=0)
entry_edit_name = ctk.CTkEntry(frame_edit, placeholder_text="Item name", text_color="#FFCC70")
entry_edit_name.grid(row=1, column=1)

label_edit_price = ctk.CTkLabel(frame_edit, text="New item price:")
label_edit_price.grid(row=2, column=0)
entry_edit_price = ctk.CTkEntry(frame_edit, placeholder_text="$0.00", text_color="#FFCC70")
entry_edit_price.grid(row=2, column=1)

label_edit_quantity = ctk.CTkLabel(frame_edit, text="New item quantity:")
label_edit_quantity.grid(row=3, column=0)
entry_edit_quantity = ctk.CTkEntry(frame_edit, placeholder_text="0", text_color="#FFCC70")
entry_edit_quantity.grid(row=3, column=1)

button_edit = ctk.CTkButton(frame_edit, text="Edit item", border_color="#7605FF", fg_color='transparent', border_width=2.5, hover_color='#013AC0', command=edit_item)
button_edit.grid(row=4, columnspan=2, pady=10)

frame_sort = ctk.CTkFrame(root)
frame_sort.pack(pady=10)

label_sort = ctk.CTkLabel(frame_sort, text="Sort items by:")
label_sort.grid(row=0, column=0)

button_sort_name = ctk.CTkButton(frame_sort, text="Name", border_color="#05FFFF", fg_color='transparent', border_width=2.5, hover_color='#A805FF', command=lambda: sort_items("name"))
button_sort_name.grid(row=0, column=1)

button_sort_price = ctk.CTkButton(frame_sort, text="Price", border_color="#05FFFF", fg_color='transparent', border_width=2.5, hover_color='#A805FF', command=lambda: sort_items("price"))
button_sort_price.grid(row=0, column=2)

button_sort_quantity = ctk.CTkButton(frame_sort, text="Quantity", border_color="#05FFFF", fg_color='transparent', border_width=2.5, hover_color='#A805FF', command=lambda: sort_items("quantity"))
button_sort_quantity.grid(row=0, column=3)

# Clear cart button
button_clear_cart = ctk.CTkButton(root, text="Clear cart", border_color="red", fg_color='transparent', border_width=2.5, hover_color='red', command=clear_cart)
button_clear_cart.pack(pady=10)

# Main event loop
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
