import random
from typing import List, Optional

from enums import Turn, MovementOption, BulletType, MovementResult


def generate_random_bullet_list(blank_num: int, live_ammo_num: int) -> List[BulletType]:
    bullet_list = [BulletType.BLANK] * blank_num + [BulletType.LIVE_AMMO] * live_ammo_num
    random.shuffle(bullet_list)
    return bullet_list

def random_movement() -> MovementOption:
    return random.choice(list(MovementOption))


class GameStatus:
    def __init__(self,
                 turn: Turn = Turn.PLAYER,
                 live_ammo_num: int = 1,
                 blank_num: int = 2,
                 player_life: int = 2,
                 dealer_life: int = 2):
        self._turn: Turn = turn
        self._live_ammo_num: int = live_ammo_num
        self._blank_num: int = blank_num
        self._player_life: int = player_life
        self._dealer_life: int = dealer_life

    def is_player_turn(self):
        return self._turn == Turn.PLAYER

    def is_player_win(self) -> bool:
        return self._player_life > 0 and self._dealer_life == 0

    def is_player_lose(self) -> bool:
        return self._player_life == 0 and self._dealer_life > 0

    def get_blank_bullet_num(self):
        return self._blank_num

    def get_live_ammo_num(self):
        return self._live_ammo_num

    def is_valid_move(self, bullet: BulletType) -> bool:
        return self._live_ammo_num > 0 if bullet == BulletType.LIVE_AMMO else self._blank_num > 0

    @staticmethod
    def get_move_result(move: MovementOption, bullet: BulletType) -> MovementResult:
        if move == MovementOption.SHOT_SELF and bullet == BulletType.BLANK:
            return MovementResult.HAVE_GUTS
        elif move == MovementOption.SHOT_SELF and bullet == BulletType.LIVE_AMMO:
            return MovementResult.SUICIDE
        elif move == MovementOption.SHOT_OPPOSITE and bullet == BulletType.BLANK:
            return MovementResult.SPECTACLE
        else:
            return MovementResult.KILL

    def update(self, move: MovementOption, bullet: BulletType, need_print_info: bool = False) -> 'GameStatus':
        if need_print_info:
            if self.is_player_turn():
                print(f'It is player turn, player life: {self._player_life}, dealer life: {self._dealer_life}, '
                      f'blank num: {self._blank_num}, live ammo num: {self._live_ammo_num}')
                if move == MovementOption.SHOT_SELF:
                    if bullet == BulletType.LIVE_AMMO:
                        print("The player shoot himself with a live ammo.")
                    else:
                        print("The player shoot himself with a blank ammo.")
                else:
                    if bullet == BulletType.LIVE_AMMO:
                        print("The player shoot dealer with a live ammo.")
                    else:
                        print("The player shoot dealer with a blank ammo.")
            else:
                print(f'It is dealer turn, player life: {self._player_life}, dealer life: {self._dealer_life}, '
                      f'blank num: {self._blank_num}, live ammo num: {self._live_ammo_num}')
                if move == MovementOption.SHOT_SELF:
                    if bullet == BulletType.LIVE_AMMO:
                        print("The dealer shoot himself with a live ammo.")
                    else:
                        print("The dealer shoot himself with a blank ammo.")
                else:
                    if bullet == BulletType.LIVE_AMMO:
                        print("The dealer shoot player with a live ammo.")
                    else:
                        print("The dealer shoot player with a blank ammo.")


        move_result: MovementResult = self.get_move_result(move, bullet)

        turn = self._turn
        live_ammo_num = self._live_ammo_num
        blank_num = self._blank_num
        player_life = self._player_life
        dealer_life = self._dealer_life

        match move_result:
            case MovementResult.HAVE_GUTS:
                blank_num -= 1
            case MovementResult.SUICIDE:
                live_ammo_num -= 1
                if self.is_player_turn():
                    player_life -= 1
                else:
                    dealer_life -= 1
                turn = Turn.PLAYER if self._turn == Turn.DEALER else Turn.DEALER
            case MovementResult.SPECTACLE:
                blank_num -= 1
                turn = Turn.PLAYER if self._turn == Turn.DEALER else Turn.DEALER
            case MovementResult.KILL:
                live_ammo_num -= 1
                if self.is_player_turn():
                    dealer_life -= 1
                else:
                    player_life -= 1
                turn = Turn.PLAYER if self._turn == Turn.DEALER else Turn.DEALER
        if live_ammo_num == 0 and blank_num == 0:
            live_ammo_num = 3
            blank_num = 2
            turn = Turn.PLAYER

        next_status = GameStatus(turn, live_ammo_num, blank_num, player_life, dealer_life)
        if need_print_info:
            if next_status.is_player_win():
                print("Player WINS!")
            elif next_status.is_player_lose():
                print("Player LOSES!")
            else:
                if next_status.is_player_turn():
                    print(f'Next will be player turn, player life: {player_life}, dealer life: {dealer_life}, '
                          f'blank num: {blank_num}, live ammo num: {live_ammo_num}')
                else:
                    print(f'Next will be dealer turn, player life: {player_life}, dealer life: {dealer_life}, '
                          f'blank num: {blank_num}, live ammo num: {live_ammo_num}')
            print("===================================")

        return next_status


class StageOneStrategy:
    def __init__(self):
        self._status = GameStatus()
        self._move_list: list[MovementOption] = [MovementOption.SHOT_SELF, MovementOption.SHOT_OPPOSITE]
        self._bullet_list: list[BulletType] = [BulletType.BLANK, BulletType.LIVE_AMMO]
        self._num: int = 0
        self.interface()

    def progress_game(self,
                      move: MovementOption = MovementOption.SHOT_OPPOSITE,
                      bullet: BulletType = BulletType.LIVE_AMMO):
        if self._num > 0:
            self._status = self._status.update(move, bullet)
        self._num += 1
        print(
            f"There gotta be {self._status.get_blank_bullet_num()} blanks and {self._status.get_live_ammo_num()} lives remaining.")
        if self._status.is_player_turn():
            shoot_self_win_rate = self.search_strategy(MovementOption.SHOT_SELF)
            shoot_opposite_win_rate = self.search_strategy(MovementOption.SHOT_OPPOSITE)
            print(f"shoot self: {shoot_self_win_rate}, shoot other: {shoot_opposite_win_rate}")
            if shoot_self_win_rate > shoot_opposite_win_rate:
                print("BE BRAVE! SHOOT YOURSELF!!!")
            else:
                print("SHOOT HIM NOW!!!")

    def interface(self):
        self.progress_game()
        while True:
            if self._status.is_player_turn():
                shoot_text = input("Tell me what happened, did you shoot yourself? y/n, q for quit")
            else:
                shoot_text = input("Tell me what happened, did dealer shoot himself? y/n, q for quit")
            wrong_input_count: int = 0
            while shoot_text != 'q' and shoot_text != 'y' and shoot_text != 'n':
                if wrong_input_count == 3:
                    print("Fuck you!")
                    return
                shoot_text = input("Right input, please. y/n, q for quit")
                wrong_input_count += 1

            if shoot_text == 'q':
                return

            bullet_text = input("Tell me about the bullet, was it a blank bullet? y/n, q for quit")
            wrong_input_count = 0
            while bullet_text != 'q' and bullet_text != 'y' and bullet_text != 'n':
                if wrong_input_count == 3:
                    print("Fuck you!")
                    return
                bullet_text = input("Right input, please. y/n, q for quit")
                wrong_input_count += 1

            move = MovementOption.SHOT_SELF if shoot_text == 'y' else MovementOption.SHOT_OPPOSITE
            bullet = BulletType.BLANK if bullet_text == 'y' else BulletType.LIVE_AMMO

            if self._status.is_player_turn():
                self.progress_game(move, bullet)


    def search_strategy(self, move: MovementOption) -> float:
        stack: list[GameStatus] = []

        # print(self._status.get_blank_bullet_num())
        # print(self._status.get_live_ammo_num())

        for i in range(self._status.get_blank_bullet_num()):
            stack.append(self._status.update(move, BulletType.BLANK))
        for i in range(self._status.get_live_ammo_num()):
            stack.append(self._status.update(move, BulletType.LIVE_AMMO))

        good_ending_num: int = 0
        bad_ending_num: int = 0

        # status: GameStatus = stack.pop()
        # status.print_info()
        # if status.is_player_win():
        #     good_ending_num += 1
        #     # continue
        # elif status.is_player_lose():
        #     bad_ending_num += 1
        #     # continue
        # for i in range(len(self._move_list)):
        #     for j in range(len(self._bullet_list)):
        #         next_status: GameStatus = self._status.update(self._move_list[i], self._bullet_list[j])
        #         stack.append(next_status)

        while len(stack) > 0:
            status: GameStatus = stack.pop()
            # status.print_info()
            if status.is_player_win():
                good_ending_num += 1
                continue
            elif status.is_player_lose():
                bad_ending_num += 1
                continue
            for i in range(len(self._move_list)):
                for j in range(len(self._bullet_list)):
                    next_status: GameStatus = status.update(self._move_list[i], self._bullet_list[j])
                    if next_status.is_valid():
                        stack.append(next_status)
        if bad_ending_num == 0 and good_ending_num == 0:
            return 1.0
        return good_ending_num / (bad_ending_num + good_ending_num)
