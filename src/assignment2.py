class Assignment2:
    def __init__(self):
        self.user_data = {}
        self.post_data = {}

    def load_data(self):
        while True:
            try:
                user_path = input("Enter the absolute file path for user data: ")
                post_path = input("Enter the absolute path for post data: ")

                with open(user_path, 'r') as user_data:
                    for line in user_data:
                        user_id, display_name, state, friends_list = line.strip().split(';')
                        self.user_data[user_id] = {"user_id": user_id, "display_name": display_name, "state": state,
                                                   "friends_list": friends_list}

                with open(post_path, 'r') as post_data:
                    for line in post_data:
                        post_id, user_id, visibility = line.strip().split(';')
                        self.post_data[post_id] = {"post_id": post_id, "user_id": user_id, "visibility": visibility}

                print("Data loaded successfully!")
            except (FileNotFoundError, IOError) as e:
                print("Error getting data: " + str(e))
                while True:
                    try_again = input("Would you like to retry? (y/n): ").lower()
                    if try_again != "n" and try_again != "y":
                        print("Invalid input")
                    else:
                        break

                if try_again == "n":
                    break


    def view_visibility(self):

        if len(self.user_data) == 0 and len(self.post_data) == 0:
            print("You must load data in order to perform other actions.")
            return

        post_id_input = input("Enter post ID: ")
        username = input("Enter username: ")

        if post_id_input in self.post_data and self.post_data[post_id_input]["visibility"] == "public":
            print("Access permitted")
        elif post_id_input in self.post_data and self.post_data[post_id_input]["visibility"] == "friend":
            post_owner = self.post_data[post_id_input]["user_id"]
            if username in self.user_data[post_owner]["friends_list"]:
                print("Access Permitted")
            else:
                print("Access Denied")
        else:
            print("Post not found")


    def retrieve_posts(self):
        if len(self.user_data) == 0 and len(self.post_data) == 0:
            print("You must load data in order to perform other actions.")
            return

        username = input("Enter user ID: ")
        posts = []

        if username not in [post["user_id"] for post in self.post_data.values()]:
            print("User not found")
        else:
            for post in self.post_data.values():
                if post["user_id"] == username:
                    posts.append(post["post_id"])

        for post in posts:
            print(post + " ")

    def search_location(self):
        if len(self.user_data) == 0 and len(self.post_data) == 0:
            print("You must load data in order to perform other actions.")
            return

        input_state = input("Enter a state: ")
        found_users = False

        for user in self.user_data.values():
            if user["state"] == input_state:
                print(user["display_name"] + " ")
                found_users = True

        if not found_users:
            print("No users found")

    def main(self):
        while True:
            print("1: Load Data")
            print("2: Check post visibility")
            print("3: Retrieve user posts")
            print("4: Find a user by location")
            print("5: Exit")

            user_input = input("Enter a number to perform an action: ")

            if user_input == "1":
                self.load_data()
            elif user_input == "2":
                self.view_visibility()
            elif user_input == "3":
                self.retrieve_posts()
            elif user_input == "4":
                self.search_location()
            elif user_input == "5":
                print("Exiting...")
                return
            else:
                print("Invalid input")


A2 = Assignment2()
A2.main()
