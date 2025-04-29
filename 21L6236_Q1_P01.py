import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import timedelta
from statistics import mode
import matplotlib.pyplot as plt

# Fetching the website
driver = webdriver.Chrome()
urlPath = 'https://www.youtube.com/@UnfoldDataScience'
driver.get(urlPath)
time.sleep(2)

# Fetching the Videos from Video tab
videos_tab = driver.find_element(By.XPATH, value='//*[@id="tabsContent"]/tp-yt-paper-tab[2]')
videos_tab.send_keys(Keys.ENTER)
time.sleep(2)

# Fetching the oldest Videos from the oldest tab
oldest_videos = driver.find_element(By.XPATH, '//*[@id="chips"]/yt-chip-cloud-chip-renderer[3]')
oldest_videos.send_keys(Keys.ENTER)
time.sleep(5)

scroll_pause_time = 1
scrolls = 14
for _ in range(scrolls):
    # Scroll down to the bottom of the page
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(scroll_pause_time)

# retrieving links of all videos
video_links = driver.find_elements(By.XPATH, '//*[@id="thumbnail"]')
videos_arr = []
for i in range(len(video_links)):
    videos_arr.append(video_links[i].get_attribute('href'))
# removing duplicates among the links
videos_arr = list(set(filter(None, videos_arr)))

title = []
views = []
likes = []
upload_date = []
no_of_comments = []

for video in videos_arr:
    driver.get(video)
    time.sleep(2)
    info = driver.find_element(By.XPATH, '//*[@id="expand"]')
    info.send_keys(Keys.ENTER)
    time.sleep(2)
    # retrieving and appending titles to list
    title.append(driver.find_element(By.XPATH, '//*[@id="title"]/h1').text)

    # retrieving and appending views to list
    views.append(driver.find_element(By.XPATH, '//*[@id="info"]/span[1]').text.split()[0])

    # retrieving and appending likes to list,Also removing K from likes and multiplying the rest with 1000
    like_videos = driver.find_element(By.XPATH, '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span').text
    if 'K' in like_videos:
        like_videos = int(float(like_videos.split('K')[0]) * 1000)
    likes.append(like_videos)

    # retrieving and appending date to list
    upload_date.append(driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text)

    # retrieving and appending comments count to list
    no_of_comments.append(driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text)

driver.quit()

# Converting Scraped data to csv file

df = pd.DataFrame(
    {'title': title, 'views': views, 'likes': likes, 'Upload Date': upload_date, 'Number of Comments': no_of_comments})
df.to_csv('prim_channel.csv', index=False)


# Task1
def average_views():

    df['Upload Date'] = pd.to_datetime(df['Upload Date'], format='%b %d, %Y')
    today = pd.to_datetime('today')
    thirty_days_ago = today - timedelta(days=30)

    filtered_df = df[df['Upload Date'] >= thirty_days_ago]

    views_col = filtered_df['views'].str.replace(',', '', regex=True).astype(int)

    total_views = views_col.sum()
    num_videos = len(filtered_df)

    average_views_per_video = total_views / num_videos

    print("Total Views:", total_views)
    print("Number of Videos:", num_videos)
    print("Average Views per Video:", average_views_per_video)


# Task2
def likes_to_views_ratio():
    views_col = df['views'].str.replace(',', '', regex=True).astype(int)
    likes_col = df['likes'].astype(int)
    highest_ratio = 0
    for element in range(0, len(views_col)):
        new_ratio = likes_col[element] / views_col[element]
        if new_ratio > highest_ratio:
            highest_ratio = new_ratio
    print(highest_ratio)


# Task 3
def correlation_btw():
    likes_col = df['likes'].astype(int)
    comments = df['Number of Comments'].astype(int)
    correlation = likes_col.corr(comments)
    print(correlation)


# Task 4
def common_weekday():
    df['Upload Date'] = pd.to_datetime(df['Upload Date'], format='%b %d, %Y')
    weekdays = []
    for i in range(0, len(df['Upload Date'])):
        if df['Upload Date'][i].weekday() == 0:
            weekdays.append('Monday')
        elif df['Upload Date'][i].weekday() == 1:
            weekdays.append('Tuesday')
        elif df['Upload Date'][i].weekday() == 2:
            weekdays.append('Wednesday')
        elif df['Upload Date'][i].weekday() == 3:
            weekdays.append('Thursday')
        elif df['Upload Date'][i].weekday() == 4:
            weekdays.append('Friday')
        elif df['Upload Date'][i].weekday() == 5:
            weekdays.append('Saturday')
        else:
            weekdays.append('Sunday')
    print(weekdays)
    print(mode(weekdays))


# Task 5
def outlier_detection():
    views_col = df['views'].str.replace(',', '', regex=True).astype(int)
    plt.boxplot(views_col)
    plt.show()


print("\nTask1 Output:\n")
average_views()
print("\n\nTask2 Output:\n")
likes_to_views_ratio()
print("\n\nTask3 Output:\n")
correlation_btw()
print("\n\nTask4 Output:\n")
common_weekday()
print("\n\nTask5 Output:\n")
outlier_detection()