import math

import numpy as np
import uvicorn
from collections import defaultdict
from fastapi import FastAPI, HTTPException
import random

app = FastAPI()

click_offer = defaultdict(set)
recommendation_click = defaultdict(int)
offer_reward = defaultdict(float)
count_conversions = defaultdict(int)
COUNT = 0


# def upper_confidence_bound(offer_id):
#     avg_revenue_per_click = offer_reward.get(offer_id, 0) / len(click_offer.get(offer_id, 0))
#     delta_i = math.sqrt(1.5 * (math.log(count_conversions.get(offer_id, 0)) / len(click_offer.get(offer_id, 0))))
#     upper_bound = avg_revenue_per_click + delta_i


def increment():
    global COUNT
    COUNT = COUNT + 1


@app.on_event("startup")
def startup_event():
    click_offer.clear()
    offer_reward.clear()
    recommendation_click.clear()
    count_conversions.clear()


@app.get("/sample/")
def sample(click_id: int, offer_ids: str) -> dict:
    """Sample random offer"""
    # Parse offer IDs
    increment()
    offers_ids = [int(offer) for offer in offer_ids.split(",")]
    if not offers_ids:
        raise HTTPException(status_code=400, detail="Offer IDs must be specified")
    max_upper_bound = 0
    offer_id = int(offers_ids[0])
    if np.random.random() < 0.1:
        # Sample random offer ID
        offer_id = int(random.choice(offers_ids))
    else:
        for item in offers_ids:
            if item in offer_reward:
                avg_revenue_per_click = offer_reward.get(item, 0) / len(click_offer.get(item, 0))
                delta_i = math.sqrt(
                    1.5 * (math.log(count_conversions.get(item, 0)) / len(click_offer.get(item, 0))))
                upper_bound = avg_revenue_per_click + delta_i
            else:
                upper_bound = 1e500
            if upper_bound > max_upper_bound:
                max_upper_bound = upper_bound
                offer_id = item
    click_offer[offer_id].add(click_id)
    recommendation_click[click_id] = offer_id

    # Prepare response
    response = {
        "click_id": click_id,
        "offer_id": offer_id,
    }

    return response


@app.put("/feedback/")
def feedback(click_id: int, reward: float) -> dict:
    """Get feedback for particular click"""
    # Response body consists of click ID
    # and accepted click status (True/False)
    offer_id = recommendation_click.get(click_id, 0)
    if reward:
        count_conversions[offer_id] += 1
        offer_reward[offer_id] += reward

    response = {
        "click_id": click_id,
        "offer_id": offer_id,
        "is_conversion": bool(reward),
        "reward": reward
    }
    return response


@app.get("/offer_ids/{offer_id}/stats/")
def stats(offer_id: int) -> dict:
    """Return offer's statistics"""
    try:
        clicks = len(click_offer.get(offer_id, 0))
        conversions = count_conversions.get(offer_id, 0)
        reward = offer_reward.get(offer_id, 0)
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
    except:
        response = {
            "offer_id": offer_id,
            "clicks": 0,
            "conversions": 0,
            "reward": 0.0,
            "cr": 0.0,
            "rpc": 0.0,
        }
    return response


def main() -> None:
    """Run application"""
    uvicorn.run("main:app", host="localhost")


if __name__ == "__main__":
    main()
