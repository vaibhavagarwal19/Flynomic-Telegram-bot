from .api_client import post

def search_hotels(user_id, checkin, checkout, lat, lng, place, rooms=1, adults=1, children=0, radius=200):
    payload = {
        "stay": {
            "checkIn": checkin,
            "checkOut": checkout
        },
        "occupancies": [
            {
                "rooms": rooms,
                "adults": adults,
                "children": children,
                "paxes": []
            }
        ],
        "geolocation": {
            "latitude": lat,
            "longitude": lng,
            "radius": radius,
            "unit": "km",
            "place": place
        },
        "userId": user_id,
        "pageNo": 1,
        "limitVal": 50
    }

    return post("hotels/search", payload)
