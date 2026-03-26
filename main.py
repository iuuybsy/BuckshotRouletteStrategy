from enums import MovementOption, BulletType
from stage_one_strategy import GameStatus
from stage_one_strategy import generate_random_bullet_list, random_movement


status = GameStatus()

first_chamber = generate_random_bullet_list(2, 1)
second_chamber = generate_random_bullet_list(2, 3)
full_chamber = first_chamber + second_chamber

ind = 0

while not (status.is_player_win() or status.is_player_lose()):
    status = status.update(random_movement(), full_chamber[ind], True)
    ind += 1

