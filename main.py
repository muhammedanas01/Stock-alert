import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = 'AC19718c410e6cbf5c242bb6d372'
auth_token = '76ffa73a25836c14cf96cd468b0'

stock_api = '8VLZVG8ARZ3VUOYT'
stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'TSLA',
    'outputsize': 'compact',
    'apikey': stock_api,
}
response = requests.get(STOCK_ENDPOINT, stock_parameters)
stock_data = response.json()

# # this holds the first two key-value of nested dictionary
close_values = list(stock_data['Time Series (Daily)'].items())[:2]

# this holds the close value from the dictionary according date (logic of date is positions)
close_value_of_yesterday = float(close_values[0][1]['4. close'])
close_value_of_day_before_yesterday = float(close_values[1][1]['4. close'])

percentage = ((close_value_of_yesterday - close_value_of_day_before_yesterday) / close_value_of_day_before_yesterday) * 100

if percentage >= 5:
    newsapi = 'b51d2eb51d92483099062566a73c83a7'
    news_parameters = {
        'q': 'tesla',
        'from': '2024-06-01',
        'sortBy': 'publishedAt',
        'language': 'en',
        'apikey': newsapi
    }

    news_response = requests.get(NEWS_ENDPOINT, news_parameters)
    news_data = news_response.json()

    articles = news_data['articles'][:4]

    # msg = [news['content'] for news in articles]
    msg = [news["content"] for news in articles]
    msg_title = [news['title'] for news in articles]
    info = [title + ":\n" + msg for title, msg in zip(msg_title, msg)]
    print(info[0])
    client = Client(account_sid, auth_token)
    for msg in info:
        message = client.messages.create(
            body=msg,
            from_='+15709903339',
            to='+917025662785'
        )

        print(message.status)


