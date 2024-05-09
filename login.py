import json
import os
from instaloader import Instaloader, Post, Profile, InstaloaderContext
from instaloader.exceptions import ConnectionException, LoginRequiredException

# Set up Instaloader
L = Instaloader(save_metadata=False, download_video_thumbnails=False)
context = InstaloaderContext(L)

# Prompt for Instagram credentials
USERNAME = "charliebobaboss"
PASSWORD = "Bobalover"

try:
    # Login to Instagram
    L.login(USERNAME, PASSWORD)
except LoginRequiredException as e:
    print(f"Login failed: {e}")
    exit()

# Set the apparent location to a country where you can access the desired Instagram account
context._session._shared_data['country_code'] = 'US'  # Change 'US' to any country code where access is allowed

PROFILE = input("Instagram Account: ")  # Replace this with the Instagram username of the profile you want to download data from
profile = Profile.from_username(context, PROFILE)  # Get the profile data

post_data = []

def download_post_with_filename(post: Post, target: str) -> str:
    """Download a post and return its generated filename with the correct extension."""
    filename = L.format_filename(post, target=target)
    try:
        L.download_post(post, target)
    except ConnectionException as e:
        print(f"Error downloading post {post.shortcode}: {e}")
        return None
    if post.is_video:
        filename += ".mp4"
    else:
        filename += ".jpg"
    return filename

# Create directory if it doesn't exist
directory = PROFILE
if not os.path.exists(directory):
    os.makedirs(directory)

# Download all the posts and save them in a folder named after the profile
for post in profile.get_posts():
    filename = download_post_with_filename(post, PROFILE)
    if filename is None:
        continue  # Skip this post if there was an error downloading it
    local_file_path = os.path.join(PROFILE, filename)  # Construct the local file path
    post_data.append({
        'local_file': local_file_path,  # Save the local file path instead of the post's URL
        'caption': post.caption,
    })

# Save the local file path and caption of each post in index.json
with open(os.path.join(PROFILE, "index.json"), 'w') as f:
    json.dump(post_data, f, indent=4)

# Delete all the '.txt' files in the profile's folder
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        os.remove(os.path.join(directory, filename))

print("\n\n\n", len(post_data))
