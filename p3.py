import streamlit as st

# Helper functions
def initialize_session_state():
    if "page" not in st.session_state:
        st.session_state["page"] = "Login"
    if "users" not in st.session_state:
        st.session_state["users"] = {}
    if "logged_in_user" not in st.session_state:
        st.session_state["logged_in_user"] = None
    if "cart" not in st.session_state:
        st.session_state["cart"] = []
    if "wishlist" not in st.session_state:
        st.session_state["wishlist"] = []
    if "gifts" not in st.session_state:
        st.session_state["gifts"] = generate_gifts()
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""
    if "sort_by" not in st.session_state:
        st.session_state["sort_by"] = "Name"
    if "filter_price" not in st.session_state:
        st.session_state["filter_price"] = 3000
    if "filter_category" not in st.session_state:
        st.session_state["filter_category"] = []

def generate_gifts():
    categories = ["Electronics", "Books", "Toys", "Home Decor", "Fashion", "Gourmet"]
    descriptions = [
        "This gadget will revolutionize your life. Or at least make it more fun!",
        "A page-turner that will keep you hooked until the last word.",
        "Perfect for kids—or adults who are kids at heart!",
        "Add a touch of elegance to any room with this masterpiece.",
        "Step out in style with this trendy must-have accessory.",
        "For the foodies who deserve the finest flavors in life."
    ]
    gifts = []
    for i in range(1, 31):
        category = categories[i % len(categories)]
        description = descriptions[i % len(descriptions)]
        gifts.append({
            "id": i,
            "name": f"Gift {i} ({category})",
            "price": 500 + i * 50,
            "category": category,
            "description": description
        })
    return gifts

def login_user(username, password):
    users = st.session_state["users"]
    if username in users and users[username]["password"] == password:
        st.session_state["logged_in_user"] = username
        st.session_state["page"] = "Home"
    else:
        st.error("Invalid username or password!")

def register_user(username, password, display_name):
    users = st.session_state["users"]
    if username in users:
        st.error("Username already exists!")
    else:
        users[username] = {"password": password, "display_name": display_name}
        st.success("Registration successful! Please log in.")
        if st.button("Go to Login Page"):
            st.session_state["page"] = "Login"

def logout_user():
    st.session_state["logged_in_user"] = None
    st.session_state["page"] = "Login"

def add_to_cart(item_id):
    item = next((gift for gift in st.session_state["gifts"] if gift["id"] == item_id), None)
    if item:
        st.session_state["cart"].append(item)
        st.success(f"{item['name']} added to your cart!")

def add_to_wishlist(item_id):
    item = next((gift for gift in st.session_state["gifts"] if gift["id"] == item_id), None)
    if item:
        st.session_state["wishlist"].append(item)
        st.success(f"{item['name']} added to your wishlist!")

def remove_from_cart(item_id):
    st.session_state["cart"] = [item for item in st.session_state["cart"] if item["id"] != item_id]

def remove_from_wishlist(item_id):
    st.session_state["wishlist"] = [item for item in st.session_state["wishlist"] if item["id"] != item_id]

def apply_search_sort_filter(gifts):
    query = st.session_state["search_query"].lower()
    sort_by = st.session_state["sort_by"]
    filter_price = st.session_state["filter_price"]
    filter_category = st.session_state["filter_category"]

    # Filter by search query
    if query:
        gifts = [gift for gift in gifts if query in gift["name"].lower()]

    # Filter by price
    if filter_price is not None:
        gifts = [gift for gift in gifts if gift["price"] <= filter_price]

    # Filter by category (multiple categories can be selected)
    if filter_category:
        gifts = [gift for gift in gifts if gift["category"] in filter_category]

    # Sort gifts
    if sort_by == "Name":
        gifts = sorted(gifts, key=lambda x: x["name"])
    elif sort_by == "Price (Low to High)":
        gifts = sorted(gifts, key=lambda x: x["price"])
    elif sort_by == "Price (High to Low)":
        gifts = sorted(gifts, key=lambda x: x["price"], reverse=True)

    return gifts

def display_navbar():
    st.sidebar.title("🎁 Gift Galaxy")
    if st.session_state["logged_in_user"]:
        display_name = st.session_state["users"][st.session_state["logged_in_user"]]["display_name"]
        st.sidebar.write(f"Welcome, {display_name} 🌟")
        st.sidebar.button("Home", on_click=lambda: switch_page("Home"))
        st.sidebar.button(f"Cart ({len(st.session_state['cart'])})", on_click=lambda: switch_page("Cart"))
        st.sidebar.button("Wishlist", on_click=lambda: switch_page("Wishlist"))
        st.sidebar.button("Profile", on_click=lambda: switch_page("Profile"))
        st.sidebar.button("Logout", on_click=logout_user)

def switch_page(page):
    st.session_state["page"] = page

def login_page():
    st.title("Login to Gift Galaxy")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login_user(username, password)
    st.write("Don't have an account?")
    if st.button("Register"):
        st.session_state["page"] = "Register"

def register_page():
    st.title("Register at Gift Galaxy")
    username = st.text_input("Create a Username")
    password = st.text_input("Create a Password", type="password")
    display_name = st.text_input("Enter your Display Name")
    if st.button("Register"):
        register_user(username, password, display_name)
    st.write("Already have an account?")
    if st.button("Go to Login"):
        st.session_state["page"] = "Login"

def home_page():
    st.title("Welcome to Gift Galaxy 🎁")
    st.subheader("Find the perfect gift for your loved ones!")

    # Search, Sort, and Filter
    st.text_input("Search by Name", key="search_query")
    st.selectbox("Sort By", ["Name", "Price (Low to High)", "Price (High to Low)"], key="sort_by")
    st.slider("Filter by Maximum Price", min_value=500, max_value=3000, step=100, value=3000, key="filter_price")
    
    # Multi-select for categories
    categories = ["All Categories"] + list(set(gift["category"] for gift in st.session_state["gifts"]))
    st.multiselect("Filter by Categories", categories, default=["All Categories"], key="filter_category")

    gifts = apply_search_sort_filter(st.session_state["gifts"])
    if not gifts:
        st.write("No gifts match your criteria.")
    else:
        for gift in gifts:
            st.write(f"**{gift['name']}** - ₹{gift['price']}")
            st.write(f"*Category:* {gift['category']}")
            st.write(gift["description"])
            col1, col2 = st.columns(2)
            with col1:
                st.button("Add to Cart", key=f"cart_{gift['id']}", on_click=lambda g=gift["id"]: add_to_cart(g))
            with col2:
                st.button("Add to Wishlist", key=f"wishlist_{gift['id']}", on_click=lambda g=gift["id"]: add_to_wishlist(g))

def cart_page():
    st.title("🛒 Your Cart")
    if not st.session_state["cart"]:
        st.write("Your cart is empty!")
        return
    for idx, item in enumerate(st.session_state["cart"]):
        st.write(f"**{item['name']}** - ₹{item['price']}")
        st.button("❌ Remove", key=f"cart_remove_{idx}", on_click=lambda i=item["id"]: remove_from_cart(i))
    st.button("Proceed to Checkout", on_click=lambda: st.success("Checkout not implemented yet!"))

def wishlist_page():
    st.title("💖 Your Wishlist")
    if not st.session_state["wishlist"]:
        st.write("Your wishlist is empty!")
        return
    for idx, item in enumerate(st.session_state["wishlist"]):
        st.write(f"**{item['name']}** - ₹{item['price']}")
        st.button("❌ Remove", key=f"wishlist_remove_{idx}", on_click=lambda i=item["id"]: remove_from_wishlist(i))

def profile_page():
    st.title("Your Profile")
    user = st.session_state["logged_in_user"]
    if user:
        display_name = st.session_state["users"][user]["display_name"]
        st.write(f"**Display Name:** {display_name}")
        new_display_name = st.text_input("Change Display Name", value=display_name)
        new_password = st.text_input("Change Password", type="password")
        if st.button("Save Changes"):
            if new_display_name != display_name:
                st.session_state["users"][user]["display_name"] = new_display_name
            if new_password:
                st.session_state["users"][user]["password"] = new_password
            st.success("Profile updated successfully!")

def run():
    initialize_session_state()
    display_navbar()
    
    page = st.session_state["page"]
    if page == "Login":
        login_page()
    elif page == "Register":
        register_page()
    elif page == "Home":
        home_page()
    elif page == "Cart":
        cart_page()
    elif page == "Wishlist":
        wishlist_page()
    elif page == "Profile":
        profile_page()

if __name__ == "__main__":
    run()
