from bs4 import BeautifulSoup
import requests
from flask import *
import json
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


def text_to_int(text):
    digitPattern = re.compile(r'\d+')
    matches = digitPattern.findall(text)
    digits = ''.join(matches)
    return int(digits)

@app.route("/", methods=["GET"])  # creating an endpoint for GET request
def home_page():
    data_set = {"Page": "Home", "Message": "Successfully loaded the HomePage"}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route("/user/", methods=["GET"])
def request_data():
    username = str(request.args.get("user"))

    base_url = "https://github.com/"

    final_url = base_url + username

    final_repo_url = final_url + "?tab=repositories&q=&type=&language=&sort=stargazers"

    html_text = requests.get(final_url).text

    soup = BeautifulSoup(html_text, "lxml")

    username = soup.find(
        "span", class_="p-nickname vcard-username d-block"
    ).text.strip()

    follow = soup.find_all(
        "span", class_="text-bold color-fg-default"
    )

    # # try:
    # commitPercentage = soup.find(
    #     "text", class_="activity-overview-percentage js-highlight-percent-left"
    # )

    
    # commitPercentage = text_to_int(commitPercentage.text)

        # issuePercentage = soup.find(
        #     "text", class_="activity-overview-percentage js-highlight-percent-right"
        # ).text.strip()

        # issuePercentage = text_to_int(issuePercentage)

        # prPercentage = soup.find(
        #     "text",class_="activity-overview-percentage js-highlight-percent-bottom"
        # ).text.strip()

        # prPercentage = text_to_int(prPercentage)
    # except:
    #     commitPercentage = 0
    #     issuePercentage = 0
    #     prPercentage = 0
    #     print("Error in getting commitPercentage, issuePercentage, prPercentage")
    


    followers = text_to_int(follow[0].text)
    following = text_to_int(follow[1].text)
    print("username:", username)
    print("followers:", followers)
    print("following:", following)


    counter = soup.find_all(
        "span", class_="Counter"
    )


    repositories = text_to_int(counter[0].text.strip())
    projects = text_to_int(counter[1].text.strip())
    packages = text_to_int(counter[2].text.strip())
    stars = text_to_int(counter[3].text.strip())

    print("repositories:", repositories)
    print("projects:", projects)
    print("packages:", packages)
    print("stars:", stars)



    contributions = soup.find(
        "h2", class_="f4 text-normal mb-2"
    ).text.strip().split(" ")

    if contributions[0] == "":
        contributions = text_to_int(contributions[1])
    else:
        contributions = text_to_int(contributions[0])
    

    print("contributions: ", contributions)    

    html_repo_text = requests.get(final_repo_url).text

    repo_soup = BeautifulSoup(html_repo_text, "lxml")

    interactions_stars_forks = repo_soup.find_all(
        "a", class_="Link--muted mr-3"
    )
    # print("interactions_stars_forks:", interactions_stars_forks)
    interactions = 0;


    for i in interactions_stars_forks:
        interactions += text_to_int(i.text.strip())
    
    print("Interactions:",interactions)

    # print(interactions_stars_forks)

    res = {
        "username": username,
        "followers": followers,
        "following": following,
        "repositories": repositories,
        "projects": projects,
        "packages": packages,
        "stars": stars,
        "contributions": contributions,
        "interactions": interactions
    }

    return res

    candidate_name = soup.find(
        "div",
        class_="text-label-1 dark:text-dark-label-1 break-all text-base font-semibold",
    ).text

    candidate_rank = soup.find(
        "span", class_="ttext-label-1 dark:text-dark-label-1 font-medium"
    ).text

    contest_attended = soup.find_all(
        "div", class_="text-label-1 dark:text-dark-label-1 font-medium leading-[22px]"
    )[1].text

    contest_rating = soup.find(
        "div", class_="text-label-1 dark:text-dark-label-1 flex items-center text-2xl"
    ).text

    contest_global_ranking = soup.find(
        "div", class_="text-label-1 dark:text-dark-label-1 font-medium leading-[22px]"
    ).text

    total_problem_solved = soup.find(
        "div", class_="text-[24px] font-medium text-label-1 dark:text-dark-label-1"
    ).text

    problems_solved = soup.find_all(
        "span",
        class_="mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1",
    )

    total_submissions = soup.find(
        "span", class_="mr-[5px] text-base font-medium lc-md:text-xl"
    ).text

    language_used = soup.find_all(
        "span",
        class_="inline-flex items-center px-2 whitespace-nowrap text-xs leading-6 rounded-full text-label-3 dark:text-dark-label-3 bg-fill-3 dark:bg-dark-fill-3 notranslate",
    )

    total_active_days = soup.find_all(
        "span", class_="font-medium text-label-2 dark:text-dark-label-2"
    )[3].text

    max_streak = soup.find_all(
        "span", class_="font-medium text-label-2 dark:text-dark-label-2"
    )[4].text

    solved_problem = soup.find_all(
        "span", class_="text-label-1 dark:text-dark-label-1 font-medium line-clamp-1"
    )

    topics_covered = soup.find_all(
        "span",
        class_="inline-flex items-center px-2 whitespace-nowrap text-xs leading-6 rounded-full bg-fill-3 dark:bg-dark-fill-3 cursor-pointer transition-all hover:bg-fill-2 dark:hover:bg-dark-fill-2 text-label-2 dark:text-dark-label-2",
    )

    badges_earned = soup.find_all(
        "img", class_="h-full w-full cursor-pointer object-contain"
    )

    most_recent_badge = soup.find(
        "div", class_="text-label-1 dark:text-dark-label-1 text-base"
    ).text

    last_solved = soup.find(
        "span",
        class_="text-label-3 dark:text-dark-label-3 hidden whitespace-nowrap lc-md:inline",
    ).text

    language_used_list = []
    ind = 0
    for language in language_used:
        language_used_list.insert(ind, language.text)
        ind = ind + 1

    solved_problem_list = []
    ind = 0
    for problem in solved_problem:
        solved_problem_list.insert(ind, problem.text)
        ind = ind + 1

    topics_covered_list = []
    ind = 0
    for topic in topics_covered:
        topics_covered_list.insert(ind, topic.text)
        ind = ind + 1

    badges_earned_list = []
    ind = 0
    for badge in badges_earned:
        badges_earned_list.insert(ind, badge["alt"])
        ind = ind + 1

    solved_problem_json = json.dumps(solved_problem_list)
    topics_covered_json = json.dumps(topics_covered_list)
    badges_earned_json = json.dumps(badges_earned_list)
    language_used_json = json.dumps(language_used_list)

    data_set = {
        "LeetCodeUsername": username,
        "CandidateName": candidate_name,
        "CandidateRank": candidate_rank,
        "ContestAttended": contest_attended,
        "ContestRating": contest_rating,
        "ContestGlobalRanking": contest_global_ranking,
        "TotalProblemsSolved": total_problem_solved,
        "EasyProblem": problems_solved[0].text,
        "MediumProblem": problems_solved[1].text,
        "HardProblem": problems_solved[2].text,
        "TotalSubmissions": total_submissions,
        "TotalActiveDays": total_active_days,
        "MaxStreak": max_streak,
        "MostRecentlyEarnedBadge": most_recent_badge,
        "Last15SolvedProblems": solved_problem_json,
        "TopicsCovered": topics_covered_json,
        "BadgesEarned": badges_earned_json,
        "LanguageUsed": language_used_json,
        "LastSolved": last_solved,
    }

    json_dump = json.dumps(data_set)
    return json_dump


if __name__ == "__main__":
    app.run()
