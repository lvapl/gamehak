import math
import requests
import time
import uuid
import random

# Сервер и токен
server_url = 'https://games.datsteam.dev/'
game_name = 'zombidef'
token = '668f9d09cb8ce668f9d09cb8d2'
headers = {
    'X-Auth-Token': token,
    'Content-Type': 'application/json'
}

def register_player():
    url = f"{server_url}/play/{game_name}/participate"
    while True:
        response = requests.put(url, headers=headers)
        if response.status_code == 200:
            print("Успешно зарегистрирован на раунд.")
            return True
        else:
            print(f"Ошибка при регистрации: {response.json()}")
            times_for_next_try = 30
            time.sleep(times_for_next_try)

def get_world_state():
    url = f"{server_url}/play/{game_name}/world"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при получении состояния мира: {response.json()}")
        return None

def get_units_state():
    url = f"{server_url}/play/{game_name}/units"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при получении состояния юнитов: {response.json()}")
        return None

def send_command(build_commands, attack_commands, move_command=None):
    url = f"{server_url}/play/{game_name}/command"
    command = {
        "build": build_commands,
        "attack": attack_commands
    }
    if move_command:
        command["moveBase"] = move_command

    response = requests.post(url, headers=headers, json=command)
    if response.status_code == 200:
        print("Команды отправлены успешно.")
    else:
        print(f"Ошибка при отправке команд: {response.json()}")

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def is_free_to_build(nx, ny, base, zombies, enemy_blocks, zpots):
    for b in base:
        if nx == b['x'] and ny == b['y']:
            return False
    for z in zombies:
        if nx == z['x'] and ny == z['y']:
            return False
    for e in enemy_blocks:
        if nx == e['x'] and ny == e['y']:
            return False
        if calculate_distance(nx, ny, e['x'], e['y']) <= 1:
            return False
        if e['x'] + 1 == nx and e['y'] - 1 == ny:
            return False
        if e['x'] + 1 == nx and e['y'] + 1 == ny:
            return False
        if e['x'] - 1 == nx and e['y'] - 1 == ny:
            return False
        if e['x'] - 1 == nx and e['y'] + 1 == ny:
            return False
    for zp in zpots:
        if calculate_distance(nx, ny, zp['x'], zp['y']) <= 1:
            return False
    return True

def get_zomby_attacked_by_block(block, zombies):
    attack_range = 8 if block.get('isHead') else 5
    target_zombies = []
    for z in zombies:
        if (z['health'] <= 0):
            continue
        distance = calculate_distance(block['x'], block['y'], z['x'], z['y'])
        if distance <= attack_range:
            z['distance'] = distance
            target_zombies.append(z)
    target_zombies = sorted(target_zombies, key=lambda x: x['distance'])
    if not target_zombies:
        return None
    return target_zombies[0]

def get_central_element(elements):
    x_values = [elem["x"] for elem in elements]
    y_values = [elem["y"] for elem in elements]
    
    avg_x = sum(x_values) / len(elements)
    avg_y = sum(y_values) / len(elements)
    
    smallest_distance = float('inf')
    central_element = None
    
    for elem in elements:
        distance = abs(elem["x"] - avg_x) + abs(elem["y"] - avg_y)
        if distance < smallest_distance:
            smallest_distance = distance
            central_element = elem
            
    return central_element

def start_game():
    register_player()
    while True:
        units_state = get_units_state()
        if not units_state:
            time.sleep(1)
            continue
        if not units_state.get('base'):
            print(f'Конец игры: {units_state}')
            time.sleep(1)
            break

        zpots = get_world_state().get('zpots', []) or []
        base = units_state.get('base', []) or []
        zombies = units_state.get('zombies', []) or []
        enemy_blocks = units_state.get('enemyBlocks', []) or []
        player_gold = units_state.get('player', {}).get('gold', 0)
        turn_ends_in_ms = units_state.get('turnEndsInMs', 1000)

        build_commands = []
        attack_commands = []
        move_command = None

        # Зомби
        for block in base:
            attacked = block.get('attacked', False)
            if attacked:
                continue
            zomby = get_zomby_attacked_by_block(block, zombies)
            if not zomby:
                continue
            attack_commands.append({
                "blockId": block['id'],
                "target": {"x": zomby['x'], "y": zomby['y']}
            })
            attack = 40 if block.get('isHead') else 10
            zomby['health'] = zomby['health'] - attack
            block['attacked'] = True

        # Вражеские игроки
        for z in enemy_blocks:
            is_head_enemy = z.get("isHead")
            z['hp'] = 300 if is_head_enemy else 100
            for block in base:
                if z['hp'] <= 0:
                    break
                is_head_our = block.get('isHead')
                attack_range = 8 if is_head_our else 5
                attacked = block.get('attacked', False)
                if attacked:
                    continue
                if calculate_distance(block['x'], block['y'], z['x'], z['y']) <= attack_range:
                    attack_commands.append({
                        "blockId": block['id'],
                        "target": {"x": z['x'], "y": z['y']}
                    })
                    attack = 40 if is_head_our else 10
                    z['hp'] = z['hp'] - attack
                    block['attacked'] = True

        # Строительство базы
        if player_gold > 0:
            for block in base:
                neighboring_positions = [(block['x'] + dx, block['y'] + dy)
                                         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
                random.shuffle(neighboring_positions)
                for nx, ny in neighboring_positions:
                    if is_free_to_build(nx, ny, base, zombies, enemy_blocks, zpots):
                        build_commands.append({"x": nx, "y": ny})
                        player_gold -= 1
                        if player_gold <= 0:
                            break
                if player_gold <= 0:
                    break
        
        # Перенос главной базы в центр
        move_command = get_central_element(base)

        print()
        print(f'Золота осталось: {player_gold}')
        print(f'Ход: {units_state.get('turn')}')
        print(f'Размер базы: {len(base)}')
        print(f'Вражеские блоки: {len(enemy_blocks)}')
        print(f'Зомби: {len(zombies)}')
        print()

        send_command(build_commands, attack_commands, move_command)
        time.sleep(turn_ends_in_ms / 1000)

def bot_main():
    while True:
        start_game()

if __name__ == "__main__":
    bot_main()