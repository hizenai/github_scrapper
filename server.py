from bs4 import BeautifulSoup
import requests
from flask import *
import json
from flask_cors import CORS
import re
from math import log2

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
    score = log2(followers/100+1)/5 + log2(following/100+1)/8 + log2(repositories/100+1) + log2(projects/100+1) + log2(packages/100+1) + log2(stars/100+1)/5 + log2(contributions/100+1)/2 + log2(interactions/100+1)
    print("score",score)
    score = 2*(100/(1+2.71828**(-score)) - 50)
    score = round(score, 0)

    res = {
        "username": username,
        "followers": followers,
        "following": following,
        "repositories": repositories,
        "projects": projects,
        "packages": packages,
        "stars": stars,
        "contributions": contributions,
        "interactions": interactions,
        "score": score
    }

    return res


if __name__ == "__main__":
    app.run()
