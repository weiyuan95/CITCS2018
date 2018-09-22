import requests
import sys
from pprint import pprint


def get_evaluation():
    """
    This function takes in the name of a challenge as a command line argument, and prints its evaluation

    example use case:
    python eval.py CalculateSquare

    :return: None
    """
    team_name = "5Cube"
    challenge_name = sys.argv[1]
    payload = {"team": team_name, "challenge": challenge_name}
    root_url = "http://cis2018-coordinator-sg.herokuapp.com"

    r = requests.post(root_url + "/api/evaluate", json=payload)

    run_id = r.json()["runId"]

    r = requests.get(root_url + "/api/evaluation-run/" + run_id)

    print()
    pprint(r.json())


if __name__ == "__main__":
    get_evaluation()
