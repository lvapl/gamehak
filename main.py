from entities import GameWorld
from api import send_get_request, send_post_request, send_put_request

if __name__ == "__main__":

    reg = send_put_request("play/zombidef/participate")

    if reg == None:
        print("Не удалось зарегистрироваться")

    params = {'userId': 1}
    api_response = send_get_request("play/zombidef/units", params)
    game = GameWorld.FromJson(api_response)

    print(game)