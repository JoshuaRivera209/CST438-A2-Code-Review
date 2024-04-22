class Assignment2:
    # Initializes dictionaries where data will be stored
    def __init__(self):
        self.user_data = {}
        self.post_data = {}

    # Function that loads user data based on provided text files
    # Note: Data will only be loaded properly when the file is formatted correctly
    def load_data(self):
        while True:
            # Try-Catch block to properly catch any errors that may arise when opening and reading the files
            try:
                # Note: These files must be the absolute path. This is reflected in the print statement
                user_path = input("Enter the absolute file path for user data: ")
                post_path = input("Enter the absolute path for post data: ")

                # The data for users will only be loaded properly if it is split using ";" in the text file containing the data.
                with open(user_path, 'r') as user_data:
                    for line in user_data:
                        user_id, display_name, state, friends_list = line.strip().split(';')
                        self.user_data[user_id] = {"user_id": user_id, "display_name": display_name, "state": state,
                                                   "friends_list": friends_list}

                with open(post_path, 'r') as post_data:
                    for line in post_data:
                        post_id, user_id, visibility = line.strip().split(';')
                        self.post_data[post_id] = {"post_id": post_id, "user_id": user_id, "visibility": visibility}

                # Show the user that the data was loaded properly
                print("Data loaded successfully!")
            except (FileNotFoundError, IOError) as e:
                # Print error that was caught
                print("Error getting data: " + str(e))
                # Use a while loop to ensure that the user provides a valid input
                while True:
                    try_again = input("Would you like to retry? (y/n): ").lower()
                    if try_again != "n" and try_again != "y":
                        print("Invalid input")
                    else:
                        break

                if try_again == "n":
                    break


    # Function to view the visibility of a post based on the post_id and user_id
    def view_visibility(self):

        # Ensures that there is data loaded so that the user can interact with this functionality
        if len(self.user_data) == 0 and len(self.post_data) == 0:
            print("You must load data in order to perform other actions.")
            return

        # Takes in user input for post_id and user_id to check visibility of post
        post_id_input = input("Enter post ID: ")
        username = input("Enter username: ")

        # First checks if the post visibility is set to public
        # This will eliminate the need to check the post owner's friends at all
        if post_id_input in self.post_data and self.post_data[post_id_input]["visibility"] == "public":
            print("Access permitted")
        # If the visibility is set to friends, we check if the provided username is found in the post
        # owner's friends list
        elif post_id_input in self.post_data and self.post_data[post_id_input]["visibility"] == "friend":
            post_owner = self.post_data[post_id_input]["user_id"]
            # Print out that the provided username has access to the post if said username is
            # found in the post owner's friends list
            if username in self.user_data[post_owner]["friends_list"]:
                print("Access Permitted")
            # Otherwise the username does not have access to the post
            else:
                print("Access Denied")
        # Prints if the post_id provided does not exist in the post data that was loaded
        else:
            print("Post not found")

    # Function to display posts that the provided user_id has created
    def retrieve_posts(self):
        # Ensures there is data loaded in order for the user to properly interact with this functionality
        if len(self.user_data) == 0 and len(self.post_data) == 0:
            print("You must load data in order to perform other actions.")
            return

        # Takes in a user_id to fetch the corresponding posts
        username = input("Enter user ID: ")
        # Array to store the found posts
        posts = []

        # Checks to ensure that the user_id provided is valid
        if username not in [post["user_id"] for post in self.post_data.values()]:
            print("User not found")
        # Otherwise we check the posts for the provided user_id
        else:
            for post in self.post_data.values():
                # If there is a match we add the post_id to the list of matches
                if post["user_id"] == username:
                    posts.append(post["post_id"])

        # If there are no posts found for the user_id, we show this to the user
        if len(posts) == 0:
            print("No posts found for this user")
        # Otherwise, we print out the posts that were found
        else:
            for post in posts:
                print(post + " ")


    # Function to display display_names based on a provided state inputted by the user
    def search_location(self):
        # Checks that there is data to ensure proper user interaction
        if len(self.user_data) == 0 and len(self.post_data) == 0:
            print("You must load data in order to perform other actions.")
            return

        # Takes a state abbreviation as an input
        # Note: This will not check for valid or invalid inputs, it will
        # simply print "No users found" if there are no matches for the provided
        # input.
        input_state = input("Enter a state abbreviation: ")
        # Set found_users to False in order to handle the case where no users are found
        found_users = False

        # Check the user data for matches with the provided input
        for user in self.user_data.values():
            if user["state"] == input_state:
                # Print out matches as they are found
                print(user["display_name"] + " ")
                # Set found_users to True to show there was a match
                found_users = True

        # If there are no users found then we provide that feedback
        if not found_users:
            print("No users found")

    # Main driver function of program
    def main(self):
        # Uses a while loop to make sure the program runs until the user
        # tells it not to
        while True:
            # Print out all options of functionality
            # Note: Functions 2-4 will not work unless there is data loaded
            print("1: Load Data")
            print("2: Check post visibility")
            print("3: Retrieve user posts")
            print("4: Find a user by location")
            print("5: Exit")

            # Takes user input to decide which functions to call
            user_input = input("Enter a number to perform an action: ")

            # if-elif chains to determine what the user input was.
            # Calls appropriate function based on user input
            if user_input == "1":
                self.load_data()
            elif user_input == "2":
                self.view_visibility()
            elif user_input == "3":
                self.retrieve_posts()
            elif user_input == "4":
                self.search_location()
            # This loop will only break out and end the program
            # if the user types 5 to exit the program.
            elif user_input == "5":
                print("Exiting...")
                return
            # Default will be an invalid input
            else:
                print("Invalid input")

# Instantiate class and call main function to start program
A2 = Assignment2()
A2.main()
