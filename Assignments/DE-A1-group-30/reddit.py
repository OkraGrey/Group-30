import praw
import pandas as pd

def collect_reddit_data():
    reddit = praw.Reddit(
        client_id="nTXzjE09hSPfqsA36NhwRA",          
        client_secret="M_8BjsqEonxHdZ9gY5698UMoHBBe1A",  
        user_agent="DataPipeline" 
    )

    subreddit_name = "RemoteWork" 
    keywords = ["remote work", "work from home", "WFH", "hybrid work"]
    posts_data = []

    for keyword in keywords:
        print(f"Searching for posts containing: {keyword}")
        for submission in reddit.subreddit(subreddit_name).search(keyword, limit=100):  
            posts_data.append({
                "title": submission.title,
                "post_text": submission.selftext,
                "author": str(submission.author),
                "date": submission.created_utc,
                "upvotes": submission.score,
                "subreddit": submission.subreddit.display_name
            })

    df_reddit = pd.DataFrame(posts_data)
    df_reddit = df_reddit.dropna()
    df_reddit.to_csv("datasets/raw/reddit_posts.csv", index=False)
    print("Reddit data collected and saved")

def collect_public_data():
    public_path = "datasets/raw/public_data.csv"
    df_public = pd.read_csv(public_path)
    df_public = df_public.dropna()
    df_public.to_csv("datasets/raw/public_data_cleaned.csv", index=False)
    print("Public data collected and saved")

def summarize_reddit_data():
    df_reddit = pd.read_csv("datasets/raw/reddit_posts.csv")
    print("\nFirst 5 rows:")
    print(df_reddit.head())
    print("\nSummary statistics for numeric columns:")
    print(df_reddit.describe())
    print("\nCount of posts by keyword (title):")
    for keyword in ["remote work", "work from home", "WFH", "hybrid work"]:
        count = df_reddit[df_reddit["title"].str.contains(keyword, case=False, na=False)].shape[0]
        print(f"{keyword}: {count} posts")

def summarize_public_data():
    df_public = pd.read_csv("datasets/raw/public_data_cleaned.csv")
    print("\nFirst 5 rows:")
    print(df_public.head())
    print("\nSummary statistics for numeric columns:")
    print(df_public.describe())
    print("\nCount of unique values for categorical columns:")
    for column in df_public.select_dtypes(include=["object"]).columns:
        print(f"{column}: {df_public[column].nunique()} unique values")

if __name__ == "__main__":
    print("\nCollecting, cleaning and storing Reddit data")
    collect_reddit_data()
    summarize_reddit_data()
    print("\nCollecting, cleaning and storing public data")
    collect_public_data()
    summarize_public_data()

