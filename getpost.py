import json
import os
from instaloader import Instaloader, Post, Profile
from instaloader.exceptions import ConnectionException

L = Instaloader(save_metadata=False, download_video_thumbnails=False)  # Disable metadata and video thumbnails download

PROFILE = input("Instagram Account: ")  # Replace this with the Instagram username of the profile you want to download data from
profile = Profile.from_username(L.context, PROFILE)  # Get the profile data

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
with open(str(PROFILE + "/index.json"), 'w') as f:
    json.dump(post_data, f, indent=4)

# Delete all the '.txt' files in the profile's folder
directory = PROFILE
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        os.remove(os.path.join(directory, filename))

print("\n\n\n", len(post_data))
