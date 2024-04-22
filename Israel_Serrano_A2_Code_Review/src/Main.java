import javax.xml.crypto.Data;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.InputMismatchException;
import java.util.Scanner;

public class Main {
    static String[] stateAbbreviations = {
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    };
    static String userFilePath = "user-info.txt";
    static String postFilePath = "post-info.txt";
    static ArrayList<User> users = new ArrayList<>();
    static ArrayList<Post> posts = new ArrayList<>();
    static int number = 0;
    static Scanner scanner = new Scanner(System.in);

    //DRIVER CODE
    public static void main(String[] args) {
        while (true) {
            System.out.println(
                    """    
                            +----------------------------+
                            | 1. Load input data         |
                            | 2. Check visibility        |
                            | 3. Retrieve post           |
                            | 4. Search user by location |
                            | 5. Exit                    |
                            +----------------------------+"""
            );

            getNumber();

            if (number == 5) {
                break;
            } else {
                runOption(number);
            }

        }
        scanner.close();
        System.out.println("Program Exited");
    }

    public static void runOption(int userChoice) {
        switch (userChoice) {
            case 1 -> getData();
            case 2 -> checkVisibility();
            case 3 -> getPosts();
            case 4 -> getUsersByLocation();
            default -> System.out.println("ERROR: Invalid Number");
        }
    }

    public static void getNumber() {
        try {
            System.out.print("Enter desired option: ");
            number = scanner.nextInt();
            scanner.nextLine();
        } catch (InputMismatchException e) {
            System.out.println("Invalid request.");
            e.printStackTrace();
        }
    }


    private static void getUsersByLocation() {
        String location = null;

        while(location == null || !validLocation(location)){
            System.out.print("Enter a state abbreviation (CA, NY, etc.): ");
            location = scanner.nextLine().trim().toUpperCase();
        }

        System.out.println("Users in state: " + location);
        for (User user : users){
            if(user.state.equals(location)){
                System.out.print(user.displayName + " ");
            }
        }
        System.out.print("\n");

    }

    private static boolean validLocation(String location) {
        if (location.length() > 2 || (!Arrays.asList(stateAbbreviations).contains(location))){
            System.out.println("INVALID INPUT");
            return false;
        }
        return true;
    }

    private static void getPosts() {
        String username = null;
        while(username == null || !validUsername(username)){
            System.out.print("Enter a username: ");
            username = scanner.nextLine().trim();
        }
        for (Post p : posts){
            if(validViewer(p.postID, username) && !p.username.equals(username)){
                System.out.print(p.postID + " ");
            }
        }
        System.out.print("\n");
    }

    private static boolean validUsername(String username) {
        for (User user : users){
            if(user.username.equals(username)){
                return true;
            }
        }
        return false;
    }

    private static void checkVisibility() {
        String postID, username;
        try {
            System.out.print("Enter a postID: ");
            postID =  scanner.nextLine().trim();

            System.out.print("Enter a username: ");
            username = scanner.nextLine().trim();
            if(validViewer(postID, username)){
                System.out.println("Access Granted\n");
            }else{
                System.out.println("Access Denied\n");
            }
        } catch (InputMismatchException e) {
            System.out.println("Invalid input.");
            e.printStackTrace();
        }
    }

    private static boolean validViewer(String postID, String username) {
        Post tempPost = null;
        User tempUser = null;

        //grab post object from posts list
        for (Post post:posts) {
            if(!post.postID.equals(postID)){
                continue;
            }
            //if post vis is public or username passed in is owner of post return true
            if(post.username.equals(username) || post.visibility.equals("public")){
                return true;
            }else{
                tempPost = post;
            }
            break;
        }

        //post not found
        if(tempPost == null){
            return false;
        }

        //get user object from username
        for (User user : users){
            if(tempPost.username.equals(user.username)){
                tempUser = user;
            }
        }

        //user not found
        if(tempUser == null){
            return false;
        }

        //if username is in friends list return true
        for (String friend : tempUser.friends){
            if (friend.equals(username)){
                return true;
            }
        }
        return false;
    }


    public static void getData() {
        getUserData();
        getPostData();
    }

    private static void getPostData() {
        try {
            System.out.print("Enter your posts filename: ");
            postFilePath = scanner.nextLine();

            File file = new File(postFilePath);
            Scanner scanner = new Scanner(file);
            while (scanner.hasNextLine()) {
                String data = scanner.nextLine().trim();
                parsePostData(data);
            }
            System.out.println("Post data parsed successfully.");
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("ERROR FILE NOT FOUND\n");
            getPostData();
        }
    }

    private static void getUserData() {
        try {
            System.out.print("Enter your users filename: ");
            userFilePath = scanner.nextLine();
            File file = new File(userFilePath);
            Scanner scanner = new Scanner(file);

            while (scanner.hasNextLine()) {
                //parse data one line at a time
                String data = scanner.nextLine().trim();
                parseUserData(data);
            }
            System.out.println("User data parsed successfully.");
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("ERROR FILE NOT FOUND\n");
            getUserData();
        }
    }


    public static void parseUserData(String data) {
        //split data on ;
        String[] dataArray = data.split(";");

        //special case handling friend list data: remove [] and split on commas
        String[] friendsList = dataArray[3].substring(1, dataArray[3].length() - 1).split(",");
        ArrayList<String> friends = new ArrayList<>(Arrays.asList(friendsList));

        //create new user with parsed data and add user to user list;
        User newUser = new User(dataArray[0], dataArray[1], dataArray[2], friends);
        users.add(newUser);
    }

    public static void parsePostData(String data) {
        //split data on ;
        String[] dataArray = data.split(";");


        //create new post with parsed data and add post to post list;
        Post newPost = new Post(dataArray[0], dataArray[1], dataArray[2]);
        posts.add(newPost);
    }

}
