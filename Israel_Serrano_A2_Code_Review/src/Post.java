public class Post {
    String postID;
    String username;
    String visibility;

    public Post(String postID, String username, String visibility) {
        this.postID = postID;
        this.username = username;
        this.visibility = visibility;
    }

    @Override
    public String toString() {
        return "postID:" + postID + " username:" + username + " visibility: " + visibility;
    }
}
