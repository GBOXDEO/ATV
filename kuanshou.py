import requests

def get_kuaishou_orders(access_token, shop_id):
    url = f"https://open.kuaishou.com/openapi/v1/shop/{shop_id}/order/list"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "page": 1,
        "page_size": 50
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    access_token = "K_ZWRjMjYyOWMtNDI2NS01NDJkLWEyNTYtOGIyYjU4MmNmODJl"
    shop_id = "2140226322"
    orders = get_kuaishou_orders(access_token, shop_id)
    if orders:
        for order in orders["data"]["orders"]:
            print(order)
    else:
        print("No orders found.")
