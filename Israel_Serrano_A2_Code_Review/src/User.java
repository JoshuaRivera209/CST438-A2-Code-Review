import java.util.ArrayList;

public class User {
    String username;
    String displayName;
    String state;
    ArrayList<String> friends;

    public User(String username, String display_name, String state, ArrayList<String> friends) {
        this.username = username;
        this.displayName = display_name;
        this.state = state;
        this.friends = friends;
    }

    @Override
    public String toString() {
        return "username:" + username + " display name:" + displayName + " state: " + state + " friends: " + friends.toString();
    }
}
