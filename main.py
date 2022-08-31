from sys import exit as ex
import praw
from praw import Reddit


def get_subreddits_for_user(subreddit_num, reddit_instance: Reddit):
    user_subreddits = list(reddit_instance.user.subreddits(limit=subreddit_num))
    sorted_subreddits = sorted(user_subreddits, key=lambda x: x.display_name)
    print(f"PRINTING SUBREDDITS FOR USER : u/{reddit_instance.user.me().name}")
    count = 1
    for user_subreddit in sorted_subreddits:
        print(f"{count}. {user_subreddit.display_name}")
        count += 1


# Need to try some alternative approach of getting saved posts
def get_saved_posts_for_user(num_posts, reddit_instance: Reddit):
    user_saved_posts = reddit_instance.user.me().saved(limit=num_posts)
    print(f"Listing {num_posts} recently saved posts for user u/{reddit_instance.user.me().name}")
    for saved_item in user_saved_posts:
        if isinstance(saved_item, praw.reddit.Submission):
            saved_item_id = saved_item.id
            post = reddit_instance.submission(id=saved_item_id)
            print(f"Post =====> {post.title}")


# Need to refactor this method for more flexible user choice
def get_submissions_by_category(num_submissions, subreddit_name, reddit_instance: Reddit):
    subreddit = reddit_instance.subreddit(subreddit_name)
    hot_submission = subreddit.hot(limit=num_submissions)
    print(f"Hot topics in subreddit : r/{subreddit_name}")
    for submission in hot_submission:
        if not submission.stickied:
            print(
                f"Submission titled : {submission.title}, upvote count: {submission.ups}, "
                f"downvote count: {submission.downs}")


def transfer_subreddits(num_subreddits_to_transfer, source_reddit_instance: Reddit,
                        destination_reddit_instance: Reddit):
    source_user_name = source_reddit_instance.user.me().name
    dest_user_name = destination_reddit_instance.user.me().name
    source_subreddits_list = list(source_reddit_instance.user.subreddits(limit=num_subreddits_to_transfer))
    source_subreddits_size = len(source_subreddits_list)
    print(f"Starting to transfer {source_subreddits_size} subscriptions from user u/{source_user_name}")
    for sub in source_subreddits_list:
        subreddit_name = sub.display_name
        destination_reddit_instance.subreddit(subreddit_name).subscribe()

    print(f"Finished transferring {num_subreddits_to_transfer} subs")
    dest_subreddit_list = list(destination_reddit_instance.user.subreddits(limit=None))
    dest_subreddit_size = len(dest_subreddit_list)
    if dest_subreddit_size == source_subreddits_size:
        print(f"Successfully transferred {num_subreddits_to_transfer} subscriptions from user u/{source_user_name}"
              f"to user u/{dest_user_name}")
    else:
        print(f"Could not transfer subs from source to destination account. Error occurred!!!")


# Accessing the reddit API for source user account
reddit = praw.Reddit(client_id='nFLb6ib1HBt-kP15ZoBvcw',
                     client_secret='hAaL00n8XI-eeaPNhW2tcu95iyUO6g',
                     username='Swarnim_Bhardwaj',
                     password='shriganesh',
                     user_agent='prawtutorialv1')

# Accessing the reddit API for destination user account
reddit_destination = praw.Reddit(client_id='I28p7woybsPjQuYgmm86xA',
                                 client_secret='6lLMMp7TVfdgFvFPqWIGQh_Oq75xGg',
                                 username='Tony-Stark-DSA',
                                 password='shriganesh',
                                 user_agent='request by Tony')

user_choice = input("Hey user what operation do you want to perform\n"
                    "1.For Displaying Subreddits for user\n"
                    "2.View Submissions in a subreddit\n"
                    "3.View saved posts for a user\n"
                    "4.Transfer subreddits from one user account to another account\n")

print(f"Hello user you Entered {user_choice}")

if user_choice == "1":
    get_subreddits_for_user(5, reddit)
elif user_choice == "2":
    get_submissions_by_category(10, 'learnprogramming', reddit)
elif user_choice == "3":
    get_saved_posts_for_user(20, reddit)
elif user_choice == "4":
    transfer_subreddits(None, reddit, reddit_destination)
else:
    print("Requested function not available. Sorry")

print("Good Bye")
ex(0)
