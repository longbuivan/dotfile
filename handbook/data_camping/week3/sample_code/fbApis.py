import requests
import requests

def get_facebook_ads_data(access_token):
    url = "https://graph.facebook.com/v12.0/me/adaccounts"
    params = {
        "access_token": access_token,
        "fields": "name,insights{reach,impressions,clicks}"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        # Retrieve all fields from insights
        insights_data = data['data']
        for account in insights_data:
                insights_url = f"https://graph.facebook.com/v12.0/{account['id']}/insights"
            insights_params = {
                "access_token": access_token
            }
            insights_response = requests.get(insights_url, params=insights_params)
            insights_data = insights_response.json()
            account['insights'] = insights_data['data']

        return data
    else:
        raise Exception(f"Failed to retrieve Facebook Ads data. Error: {data['error']['message']}")
    


def get_facebook_ads_omni_purchases_data(access_token):
    url = "https://graph.facebook.com/v12.0/me/adaccounts"
    params = {
        "access_token": access_token,
        "fields": "name,insights{omni_purchase}"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        # Retrieve all fields from insights
        insights_data = data['data']
        for account in insights_data:
            insights_url = f"https://graph.facebook.com/v12.0/{account['id']}/insights"
            insights_params = {
                "access_token": access_token
            }
            insights_response = requests.get(insights_url, params=insights_params)
            insights_data = insights_response.json()
            account['insights'] = insights_data['data']

        return data
    else:
        raise Exception(f"Failed to retrieve Facebook Ads data. Error: {data['error']['message']}")