class LastAttack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @staticmethod
    def FromJson(data):
        return LastAttack(
            x=data.get('x'),
            y=data.get('y')
        )

class Base:
    def __init__(self, attack, health, id, isHead, lastAttack, range, x, y):
        self.attack = attack
        self.health = health
        self.id = id
        self.isHead = isHead
        self.lastAttack = lastAttack
        self.range = range
        self.x = x
        self.y = y
    
    @staticmethod
    def FromJson(data):
        game_data = data.get('lastAttack')
        lastAttack = LastAttack.FromJson(game_data) if game_data else None
        return Base(
            attack=data.get('attack'),
            health=data.get('health'),
            id=data.get('id'),
            isHead=data.get('isHead'),
            lastAttack=lastAttack,
            range=data.get('range'),
            x=data.get('x'),
            y=data.get('y')
        )

class EnemyBlock:
    def __init__(self, attack, health, isHead, lastAttack, name, x, y):
        self.attack = attack
        self.health = health
        self.isHead = isHead
        self.lastAttack = lastAttack
        self.name = name
        self.x = x
        self.y = y
    
    @staticmethod
    def FromJson(data):
        game_data = data.get('lastAttack')
        lastAttack = LastAttack.FromJson(game_data) if game_data else None
        return Base(
            attack=data.get('attack'),
            health=data.get('health'),
            isHead=data.get('isHead'),
            lastAttack=lastAttack,
            name=data.get('name'),
            x=data.get('x'),
            y=data.get('y')
        )

class Player:
    def __init__(self, enemyBlockKills, gameEndedAt, gold, name, points, zombieKills):
        self.enemyBlockKills = enemyBlockKills
        self.gameEndedAt = gameEndedAt
        self.gold = gold
        self.name = name
        self.points = points
        self.zombieKills = zombieKills
    
    @staticmethod
    def FromJson(data):
        return Base(
            enemyBlockKills=data.get('enemyBlockKills'),
            gameEndedAt=data.get('gameEndedAt'),
            gold=data.get('gold'),
            name=data.get('name'),
            points=data.get('points'),
            zombieKills=data.get('zombieKills')
        )

class Zombie:
    def __init__(self, attack, direction, health, id, speed, type, waitTurns, x, y):
        self.attack = attack
        self.direction = direction
        self.health = health
        self.id = id
        self.speed = speed
        self.type = type
        self.waitTurns = waitTurns
        self.x = x
        self.y = y
    
    @staticmethod
    def FromJson(data):
        return Base(
            attack=data.get('attack'),
            direction=data.get('direction'),
            health=data.get('health'),
            id=data.get('id'),
            speed=data.get('speed'),
            type=data.get('type'),
            waitTurns=data.get('waitTurns'),
            x=data.get('x'),
            y=data.get('y')
        )

class GameWorld:
    def __init__(self, player, realmName, turn, turnEndsInMs, base=None, enemyBlocks=None, zombies=None):
        self.base = base or []
        self.enemyBlocks = enemyBlocks or []
        self.zombies = zombies or []
        self.player = player
        self.realmName = realmName
        self.turn = turn
        self.turnEndsInMs = turnEndsInMs
    
    @staticmethod
    def FromJson(data):
        base = [Base.FromJson(game_data) for game_data in data.get('base', [])]
        enemyBlocks = [Base.FromJson(game_data) for game_data in data.get('enemyBlocks', [])]
        zombies = [Base.FromJson(game_data) for game_data in data.get('zombies', [])]
        return GameWorld(
            base=base,
            enemyBlocks=enemyBlocks,
            zombies=zombies,
            player=data.get('player'),
            realmName=data.get('speed'),
            turn=data.get('turn'),
            turnEndsInMs=data.get('turnEndsInMs')
        )

