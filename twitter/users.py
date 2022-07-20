import utils
from time import sleep
import random
import json
import pandas as pd


def get_user_information(users, driver=None, headless=True):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless)

    users_info = {}

    for i, user in enumerate(users):

        log_user_page(user, driver)

        if user is not None:

            try:
                following = driver.find_element_by_xpath(
                    '//a[contains(@href,"/following")]/span[1]/span[1]').text
                followers = driver.find_element_by_xpath(
                    '//a[contains(@href,"/followers")]/span[1]/span[1]').text
            except Exception as e:
                following=None
                followers=None
                continue

            try:
                element = driver.find_element_by_xpath('//div[contains(@data-testid,"UserProfileHeader_Items")]//a[1]')
                website = element.get_attribute("href")
            except Exception as e:
                # print(e)
                website = ""

            try:
                desc = driver.find_element_by_xpath('//div[contains(@data-testid,"UserDescription")]').text
            except Exception as e:
                # print(e)
                desc = ""
            a = 0
            try:
                join_date = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[3]').text
                birthday = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                location = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
            except Exception as e:
                # print(e)
                try:
                    join_date = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                    span1 = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                    if hasNumbers(span1):
                        birthday = span1
                        location = ""
                    else:
                        location = span1
                        birthday = ""
                except Exception as e:
                    # print(e)
                    try:
                        join_date = driver.find_element_by_xpath(
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                        birthday = ""
                        location = ""
                    except Exception as e:
                        # print(e)
                        join_date = ""
                        birthday = ""
                        location = ""
            # print("--------------- " + user + " information : ---------------")
            # print("Following : ", following)
            # print("Followers : ", followers)
            # print("Location : ", location)
            # print("Join date : ", join_date)
            # print("Birth date : ", birthday)
            # print("Description : ", desc)
            # print("Website : ", website)
            users_info[user] = [following, followers, join_date, birthday, location, website, desc]

            # if i == len(users) - 1:
            #     driver.close()
            #     return users_info
        else:
            print("You must specify the user")
            continue

    driver.close()
    print(f'Processed ',i,' out of ',len(users),' users')
    return users_info
      


def log_user_page(user, driver, headless=True):
    sleep(random.uniform(1, 2))
    driver.get('https://twitter.com/' + user)
    sleep(random.uniform(1, 2))


def get_users_followers(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    followers = utils.get_users_follow(users, headless, env, "followers", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = str(users[0]) + '_' + 'followers.json'
    else:
        file_path = file_path + str(users[0]) + '_' + 'followers.json'
    with open(file_path, 'w') as f:
        json.dump(followers, f)
        print(f"file with followers saved in {file_path}")
    return followers


def get_users_following(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    following = utils.get_users_follow(users, headless, env, "following", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = str(users[0]) + '_' + 'following.json'
    else:
        file_path = file_path + str(users[0]) + '_' + 'following.json'
    with open(file_path, 'w') as f:
        json.dump(following, f)
        print(f"file saved in {file_path}")
    return following


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def get_followers_info(group_name):
  followers = get_users_followers(users=[group_name], env="env", verbose=0, headless = True, wait=2)
  followers = followers[group_name]
  followers_info = get_user_information(followers, headless=True)
  
  followers_df = pd.DataFrame(followers_info, index = ["nb of following","nb of followers", "join date", 
                                             "birthdate", "location", "website", "description"]).T
  file_name=group_name+'_followers_info.csv'
  followers_df.to_csv(file_name, sep='\t')
  print(f"file with followers info saved in {file_name}")
  #return followers_df,followers_info

