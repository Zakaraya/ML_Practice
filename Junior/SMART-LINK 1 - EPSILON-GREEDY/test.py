import numpy as np
import uvicorn
from collections import defaultdict
from fastapi import FastAPI

app = FastAPI()

click_offer = defaultdict(set)
recommendation_click = defaultdict(int)
offer_reward = defaultdict(float)
count_conversions = defaultdict(int)


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
    offers_ids = [int(offer) for offer in offer_ids.split(",")]
    rpc_max = 0
    offer_id = sorted(offer_ids)[0]
    if len(click_offer) < 100:
        # Sample random offer ID
        offer_id = int(np.random.choice(offers_ids))
        sampler = "random"
    else:
        for item in click_offer:
            if item in offer_reward:
                if rpc_max < offer_reward[item] / len(click_offer.get(item, set())):
                    rpc_max = offer_reward[item] / len(click_offer.get(item, set()))
                    offer_id = item
        sampler = "greedy"

    recommendation_click[click_id] = offer_id

    # Prepare response
    response = {
        "click_id": click_id,
        "offer_id": offer_id,
        "sampler": sampler,
    }

    return response


@app.put("/feedback/")
def feedback(click_id: int, reward: float) -> dict:
    """Get feedback for particular click"""
    # Response body consists of click ID
    # and accepted click status (True/False)
    offer_id = recommendation_click.get(click_id, 0)
    if reward:
        offer_reward[offer_id] += reward
        count_conversions[offer_id] += 1
    click_offer[offer_id].add(click_id)

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
        response = {}
    return response


def main() -> None:
    """Run application"""
    uvicorn.run("main:app", host="localhost")


if __name__ == "__main__":
    main()
