import random
from typing import List, Optional
from enums import MovementOption, BulletType
from functools import lru_cache

def generate_random_bullet_list(blank_num: int, live_ammo_num: int) -> List[BulletType]:
    bullet_list = [BulletType.BLANK] * blank_num + [BulletType.LIVE_AMMO] * live_ammo_num
    random.shuffle(bullet_list)
    return bullet_list

def random_movement() -> MovementOption:
    return random.choice(list(MovementOption))

@lru_cache(None)
def solve(play_live, dealer_live, blank_ammo_num, live_ammo_num, is_player_turn: bool) -> tuple[float, MovementOption]:

    if play_live == 0:
        return 0.0, MovementOption.NONE
    if dealer_live == 0:
        return 1.0, MovementOption.NONE

    total = blank_ammo_num + live_ammo_num
    if total == 0:
        return solve(play_live, dealer_live, 2, 3, True)

    p_empty = blank_ammo_num / total
    p_live = live_ammo_num / total

    def eval_self():
        if blank_ammo_num > 0:
            v_empty = solve(play_live, dealer_live, blank_ammo_num - 1, live_ammo_num, is_player_turn)[0]
        else:
            v_empty = 0.0
        if live_ammo_num > 0:
            v_live = solve(play_live - 1, dealer_live, blank_ammo_num, live_ammo_num - 1,
                           False if is_player_turn else True)[0]
        else:
            v_live = 0.0
        return p_empty * v_empty + p_live * v_live

    def eval_opp():
        if blank_ammo_num > 0:
            v_empty = solve(play_live, dealer_live, blank_ammo_num - 1, live_ammo_num,
                            False if is_player_turn else True)[0]
        else:
            v_empty = 0.0
        if live_ammo_num > 0:
            v_live = solve(play_live, dealer_live - 1, blank_ammo_num, live_ammo_num - 1,
                           False if is_player_turn else True)[0]
        else:
            v_live = 0.0
        return p_empty * v_empty + p_live * v_live

    if is_player_turn:
        v_self = eval_self()
        v_opp = eval_opp()
        if v_self >= v_opp:
            return v_self, MovementOption.SHOT_SELF
        else:
            return v_opp, MovementOption.SHOT_OPPOSITE
    else:
        v_self = eval_self()
        v_opp = eval_opp()
        if v_self <= v_opp:
            return v_self, MovementOption.SHOT_SELF
        else:
            return v_opp, MovementOption.SHOT_OPPOSITE


class StageOneStrategy:
    def __init__(self):
        self._is_player_turn: bool = True
        self._player_live: int = 2
        self._dealer_live: int = 2
        self._blank_ammo_num: int = 2
        self._live_ammo_num: int = 1

    def check_chamber(self):
        if self._blank_ammo_num + self._live_ammo_num > 0:
            return
        print("Reload chamber.")
        self._is_player_turn = True
        self._blank_ammo_num = 2
        self._live_ammo_num = 3

    def change_side(self):
        self._is_player_turn = not self._is_player_turn

    def sumerize(self):
        if self._player_live == 0:
            print("Player lost, bad luck.")
        elif self._dealer_live == 0:
            print("Player won, well done.")
        else:
            print(f"For now, the player has {self._player_live} live and the dealer has {self._dealer_live} live.")
            print(f"There are {self._blank_ammo_num} blank bullets and {self._live_ammo_num} live bullets in the chamber.")
            if self._is_player_turn:
                print("Next will be player's turn.")
            else:
                print("Next will be dealer's turn.")
        print("========================================")

    def progress_game(self,
                      move: MovementOption = MovementOption.SHOT_OPPOSITE,
                      bullet: BulletType = BulletType.LIVE_AMMO):
        if self._player_live == 0 or self._dealer_live == 0:
            print("Game over, start a new one.")
            return
        if self._is_player_turn:
            print("It's player's turn, and the player just ", end = "")
            if move == MovementOption.SHOT_SELF and bullet == BulletType.LIVE_AMMO:
                print("shoot himself with a live ammo. It's suicide!")
                self._player_live -= 1
                self._live_ammo_num -= 1
                self.change_side()
            elif move == MovementOption.SHOT_SELF and bullet == BulletType.BLANK:
                print("shoot himself with a blank bullet. Hard ass.")
                self._blank_ammo_num -= 1
            elif move == MovementOption.SHOT_OPPOSITE and bullet == BulletType.LIVE_AMMO:
                print("shoot the dealer with a live ammo. Good kill.")
                self._dealer_live -= 1
                self._live_ammo_num -= 1
                self.change_side()
            elif move == MovementOption.SHOT_OPPOSITE and bullet == BulletType.BLANK:
                print("shoot the dealer with a blank bullet. Joker.")
                self._blank_ammo_num -= 1
                self.change_side()
        else:
            print("It's dealer's turn, and the dealer just ", end="")
            if move == MovementOption.SHOT_SELF and bullet == BulletType.LIVE_AMMO:
                print("shoot himself with a live ammo. HA HA!")
                self._dealer_live -= 1
                self._live_ammo_num -= 1
                self.change_side()
            elif move == MovementOption.SHOT_SELF and bullet == BulletType.BLANK:
                print("shoot himself with a blank bullet. Hard ass.")
                self._blank_ammo_num -= 1
            elif move == MovementOption.SHOT_OPPOSITE and bullet == BulletType.LIVE_AMMO:
                print("shoot the player with a live ammo. Painful.")
                self._player_live -= 1
                self._live_ammo_num -= 1
                self.change_side()
            elif move == MovementOption.SHOT_OPPOSITE and bullet == BulletType.BLANK:
                print("shoot the player with a blank bullet. Nice try.")
                self._blank_ammo_num -= 1
                self.change_side()
        self.check_chamber()
        self.sumerize()

    @staticmethod
    def _get_yes_no_input(prompt: str, max_attempts: int = 3) -> Optional[str]:
        attempts = 0
        while attempts < max_attempts:
            user_input = input(prompt).strip().lower()
            if user_input in ('y', 'n', 'q'):
                return None if user_input == 'q' else user_input
            attempts += 1
            if attempts < max_attempts:
                print("Right input, please. y/n, q for quit     ")
        print("Fuck you!")
        return None

    def interface(self) -> None:
        self.sumerize()
        while True:
            if self._player_live == 0 or self._dealer_live == 0:
                break

            if self._is_player_turn:
                winning_rate, move = solve(
                    self._player_live,
                    self._dealer_live,
                    self._blank_ammo_num,
                    self._live_ammo_num,
                    True)
                if move == MovementOption.SHOT_SELF:
                    print(f"Be brave and shoot yourself! The winning rate is {winning_rate}.")
                elif move == MovementOption.SHOT_OPPOSITE:
                    print(f"Be hard and shot him! The winning rate is {winning_rate}.")
                else:
                    print(f"Just drink some tea and fix the bug.")

            prompt = ("Tell me what happened, did you shoot yourself? y/n, q for quit     "
                      if self._is_player_turn
                      else "Tell me what happened, did dealer shoot himself? y/n, q for quit     ")
            shoot_text = self._get_yes_no_input(prompt)
            if shoot_text is None:
                return

            if self._blank_ammo_num == 0 and self._live_ammo_num != 0:
                bullet_text = "n"
                print("It must be a live bullet i see.")
            elif self._blank_ammo_num != 0 and self._live_ammo_num == 0:
                bullet_text = "y"
                print("It must be a blank bullet i see.")
            elif self._blank_ammo_num == 0 and self._live_ammo_num == 0:
                print("Drink some tea and fix the bug.")
                return
            else:
                bullet_text = self._get_yes_no_input(
                    "Tell me about the bullet, was it a blank bullet? y/n, q for quit     ")
                if bullet_text is None:
                    return

            print("---------------------------------------")

            move = MovementOption.SHOT_SELF if shoot_text == "y" else MovementOption.SHOT_OPPOSITE
            bullet = BulletType.BLANK if bullet_text == "y" else BulletType.LIVE_AMMO

            self.progress_game(move, bullet)
