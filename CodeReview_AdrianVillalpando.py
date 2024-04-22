import sys

def main():
    users = {}
    posts = {}
    
    while True:
        print("\nMenu Options:")
        print("1. Load input data")
        print("2. Check visibility")
        print("3. Retrieve posts")
        print("4. Search users by location")
        print("5. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            user_file_path = input("Enter the path for the user info file: ")
            post_file_path = input("Enter the path for the post info file: ")
            users, posts = load_data(user_file_path, post_file_path)
        elif choice == '2':
            post_id = input("Enter post ID: ")
            username = input("Enter username: ")
            check_visibility(posts, users, post_id, username)
        elif choice == '3':
            username = input("Enter username: ")
            retrieve_posts(posts, users, username)
        elif choice == '4':
            state = input("Enter state location: ")
            search_users_by_location(users, state)
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def load_data(user_file_path, post_file_path):
    users = {}
    posts = {}
    with open(user_file_path) as file:
        for line in file:
            parts = line.strip().split(';')
            username = parts[0]
            display_name = parts[1]
            state = parts[2]
            friends_list = parts[3].strip()[1:-1]
            if friends_list:
                friends = [friend.strip() for friend in friends_list.split(',')]
            else:
                friends = []
            users[username] = {'display_name': display_name, 'state': state, 'friends': friends}
        
    with open(post_file_path) as file:
        for line in file:
            parts = line.strip().split(';')
            post_id = parts[0]
            user_id = parts[1]
            visibility = parts[2]
            posts[post_id] = {'user_id': user_id, 'visibility': visibility}
    
    # print("User data:")
    # for user, user_info in users.items():
    #     print(user, user_info)

    # print("\nPost data:")
    # for post, post_info in posts.items():
    #     print(post, post_info)

    return users, posts

def check_visibility(posts, users, post_id, username):
    if post_id not in posts:
        print("Post ID does not exist.")
        return
    if username not in users:
        print("Username does not exist.")
        return
    
    post = posts[post_id]
    if post['visibility'] == 'public':
        print("Access Permitted")
    elif post['visibility'] == 'friend':
        post_owner = post['user_id']
        if post_owner == username or username in users[post_owner]['friends']:
            print("Access Permitted")
        else:
            print("Access Denied")

def retrieve_posts(posts, users, username):
    if username not in users:
        print("Username does not exist.")
        return
    
    visible_posts = []
    for post_id, post_info in posts.items():
        if post_info['user_id'] != username:
            if post_info['visibility'] == 'public':
                visible_posts.append(post_id)
            elif post_info['visibility'] == 'friend' and username in users[post_info['user_id']]['friends']:
                visible_posts.append(post_id)
    
    if visible_posts:
        print("Visible posts:", ', '.join(visible_posts))
    else:
        print("No posts available.")

def search_users_by_location(users, state):
    found = False
    for user_info in users.values():
        if user_info['state'] == state:
            print(user_info['display_name'])
            found = True
    if not found:
        print("No users found in the specified state.")

if __name__ == "__main__":
    main()
