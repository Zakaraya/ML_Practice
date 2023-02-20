import numpy as np
import uvicorn
from collections import defaultdict
from fastapi import FastAPI

app = FastAPI()

click_offer = defaultdict(int)
offer_reward = defaultdict(float)
count_conversions = defaultdict(int)
count_click_offer = defaultdict(int)


@app.on_event("startup")
def startup_event():
    click_offer.clear()
    offer_reward.clear()
    count_conversions.clear()
    count_click_offer.clear()


@app.get("/sample/")
def sample(click_id: int, offer_ids: str) -> dict:
    """Sample random offer"""
    # Parse offer IDs
    offers_ids = [int(offer) for offer in offer_ids.split(",")]

    # Sample random offer ID
    offer_id = int(np.random.choice(offers_ids))
    sampler = "random"

    try:
        # Get the offer with the highest RPC
        rpc_max = max([offer_reward[item] / count_click_offer[item] for item in click_offer])
        offer_id = max(click_offer,
                       key=lambda x: offer_reward[x] / count_click_offer[x] if count_click_offer[x] > 0 else -1)
        sampler = "greedy"
    except:
        pass

    count_click_offer[offer_id] += 1
    count_conversions[offer_id] += 1

    # Prepare response
    response = {
        "click_id": click_id,
        "offer_id": offer_id,
        "sampler": sampler,
    }

    return response


# @app.get("/sample/")
# def sample(click_id: int, offer_ids: str) -> dict:
#     """Sample random offer"""
#     # Parse offer IDs
#     offers_ids = [int(offer) for offer in offer_ids.split(",")]
#     rpc_max = 0
#
#     if len(click_offer) < 100:
#         # Sample random offer ID
#         offer_id = int(np.random.choice(offers_ids))
#         sampler = "random"
#     else:
#         for item in click_offer:
#             if rpc_max < offer_reward[item] / count_click_offer[item]:
#                 rpc_max = offer_reward[item] / count_click_offer[item]
#                 offer_id = item
#         sampler = "greedy"
#
#     count_click_offer[offer_id] += 1
#     count_conversions[offer_id] += 1
#     # Prepare response
#     response = {
#         "click_id": click_id,
#         "offer_id": offer_id,
#         "sampler": sampler,
#     }
#
#     return response


# def get_key(arr, value):
#     for k, v in arr.items():
#         if v == value:
#             return k


@app.put("/feedback/")
def feedback(click_id: int, reward: float) -> dict:
    """Get feedback for particular click"""
    # Response body consists of click ID
    # and accepted click status (True/False)
    # offer_id = click_offer[click_id]
    offer_id = click_offer[click_id]
    if reward:
        offer_reward[offer_id] += reward
        count_conversions[offer_id] += 1
    # offer_id = get_key(click_offer, click_id)
    # is_conversion = True if reward != 0 else False
    # offer_reward[offer_id] += reward
    # count_click_offer[offer_id] += 1
    # count_conversions[offer_id] += 1

    response = {
        "click_id": click_id,
        "offer_id": offer_id,
        "is_conversion": bool(reward),
        "reward": offer_reward[offer_id]
    }
    return response


@app.get("/offer_ids/{offer_id}/stats/")
def stats(offer_id: int) -> dict:
    """Return offer's statistics"""
    try:
        clicks = count_click_offer[offer_id]
        conversions = count_conversions[offer_id]
        reward = offer_reward[offer_id]
        cr = float(conversions) / clicks
        rpc = reward / clicks
        response = {
            "offer_id": offer_id,
            "clicks": clicks,
            "conversions": conversions,
            "reward": reward,
            "cr": cr,
            "rpc": rpc,
        }
    except KeyError:
        response = {}
    return response


def main() -> None:
    """Run application"""
    uvicorn.run("main:app", host="localhost")


if __name__ == "__main__":
    main()