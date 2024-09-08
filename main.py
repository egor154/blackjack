import os
import random

# Устанавливаем переменную окружения для терминала
os.environ['TERM'] = 'xterm'

# Функция для создания колоды карт
def create_deck(num_decks):
    single_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
    return single_deck * num_decks

# Функция для раздачи двух начальных карт
def deal(deck):
    random.shuffle(deck)
    hand = [deck.pop() for _ in range(2)]
    return [convert_card(card) for card in hand]

# Функция для конвертации числовых значений карт в строковые
def convert_card(card):
    card_map = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    return card_map.get(card, card)

# Функция для подсчета очков по картам на руке
def total(hand):
    points = 0
    ace_count = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            points += 10
        elif card == 'A':
            ace_count += 1
            points += 11
        else:
            points += card
    while points > 21 and ace_count:
        points -= 10
        ace_count -= 1
    return points

# Функция для добавления новой карты
def hit(deck, hand):
    card = deck.pop()
    hand.append(convert_card(card))
    return hand

# Функция для вывода результатов
def print_results(dealer_hand, player_hand):
    print("\n*** РЕЗУЛЬТАТЫ РАУНДА ***\n")
    print(f"У раздающего на руке: {dealer_hand}, в сумме: {total(dealer_hand)}")
    print(f"У вас на руке: {player_hand}, в сумме: {total(player_hand)}")

# Функция для проверки начальной раздачи на 21
def blackjack(dealer_hand, player_hand):
    global wins, losses
    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Поздравляю! У вас блек-джек, вы выиграли!\n")
        wins += 1
        play_again()
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Простите, вы проиграли. У раздающего блек-джек.\n")
        losses += 1
        play_again()
    elif total(dealer_hand) == total(player_hand):
        print_results(dealer_hand, player_hand)
        print("У вас и у раздающего блек-джек. В этом раунде победителя нет.\n")
        play_again()

# Функция для подсчета очков
def score(dealer_hand, player_hand):
    global wins, losses
    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Поздравляю! У вас 21, вы выиграли!\n")
        wins += 1
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Простите, вы проиграли. У раздающего 21.\n")
        losses += 1
    elif total(player_hand) < total(dealer_hand):
        print_results(dealer_hand, player_hand)
        print("У раздающего больше очков, чем у вас. Вы проиграли.\n")
        losses += 1
    elif total(player_hand) > total(dealer_hand):
        print_results(dealer_hand, player_hand)
        print("Поздравляю, у вас больше очков, чем у раздающего. Вы выиграли!\n")
        wins += 1
    elif total(player_hand) == total(dealer_hand):
        print_results(dealer_hand, player_hand)
        print("Раздающий набрал столько же, сколько и вы. В этом раунде победителя нет.\n")

# Функция для запуска нового раунда игры
def play_again():
    again = input("Хотите сыграть снова? (Да/Нет) : ").lower()
    if again == "да":
        game()
    else:
        print("Казино всегда выигрывает!")
        exit()

# Основная функция игры
def game():
    global wins, losses

    print("\n    Новая игра!\n")
    print("-" * 30 + "\n")
    print(f"    Победы: {wins}   Поражения: {losses}\n")
    print("-" * 30 + "\n")

    dealer_hand = deal(deck)
    player_hand = deal(deck)

    print("Раздающий показывает " + str(dealer_hand[0]))
    print(f"У вас на руке: {player_hand}, в сумме количество очков равно {total(player_hand)}")
    blackjack(dealer_hand, player_hand)

    while True:
        choice = input("Вы хотите [д]обрать карту, [о]становиться или [в]ыйти из игры? ").lower()
        if choice == 'д':
            hit(deck, player_hand)
            print(f"Ваша рука: {player_hand}")
            print("Сумма ваших очков: " + str(total(player_hand)))
            if total(player_hand) > 21:
                print('У вас перебор')
                losses += 1
                play_again()
        elif choice == 'о':
            while total(dealer_hand) < 17:
                hit(deck, dealer_hand)
                print('Раздающий взял новую карту. У него на руках: ', dealer_hand)
                if total(dealer_hand) > 21:
                    print('У раздающего перебор, вы выиграли!')
                    wins += 1
                    play_again()
            else:
                score(dealer_hand, player_hand)
                play_again()
        elif choice == "в":
            print("Казино всегда выигрывает!")
            exit()
        else:
            print("Неверный ввод. Пожалуйста, введите 'д', 'о' или 'в'.")

# Начальные значения счетчиков побед и поражений
wins = 0
losses = 0

# Создание колоды карт
decks = int(input("Введите количество колод: "))
deck = create_deck(decks)

# Запуск основной функции игры
game()
