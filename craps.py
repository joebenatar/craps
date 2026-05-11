import random


def rolar_dados():
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    return d1, d2, d1 + d2


def mostrar_dados(d1, d2, soma):
    print(f"Dados: [{d1}] [{d2}] = {soma}")


def pedir_apostas(banca):
    print(f"\n Banca: ${banca}")
    print("Digite suas apostas: Pass e Don't Pass.")
    print("(separar por espaço ou vírgula. 0 pra não apostar)")

    while True:
        entrada = input("Apostas: ").strip()

        entrada = entrada.replace(",", " ").replace(";", " ")
        
        partes = entrada.split()
        
        while "" in partes:
            partes.remove("")

        if len(partes) != 2:
            print("  Digite exatamente 2 valores.")
            continue

        try:
            pass_bet = int(partes[0])
            dont_bet = int(partes[1])
        except ValueError:
            print("  Os dois valores precisam ser números inteiros.")
            continue

        if pass_bet < 0 or dont_bet < 0:
            print("  Valores não podem ser negativos.")
            continue

        if pass_bet + dont_bet > banca:
            print(f"  Soma das apostas (${pass_bet + dont_bet}) maior que a banca (${banca}).")
            continue

        if pass_bet == 0 and dont_bet == 0:
            print("  Você precisa apostar em pelo menos um lado.")
            continue

        return pass_bet, dont_bet


def odds_payout(point, valor):

    if point in (4, 10):
        return valor * 2
    if point in (5, 9):
        return int(valor * 1.5)
    if point in (6, 8):
        return int(valor * 6 / 5)
    return 0


def oferecer_odds(banca, aposta_principal):
    
    if banca <= 0:
        return 0
    print(f"\n Quer fazer uma Odds bet? (paga odds justas, sem vantagem da casa)")
    max_odds = min(banca, aposta_principal * 3)
    while True:
        entrada = input(f"Valor da odds (0 para pular, máx ${max_odds}): ").strip()
        try:
            valor = int(entrada)
            if 0 <= valor <= max_odds:
                return valor
            print("Valor fora do permitido.")
        except ValueError:
            print("Digite um número inteiro.")


def resolver_come_out(soma, pass_bet, dont_bet):
    ret_pass, ret_dont = 0, 0
    terminou_pass, terminou_dont = False, False

    if pass_bet > 0:
        if soma in (7, 11):
            print("Natural! Pass Line ganha.")
            ret_pass = pass_bet * 2
            terminou_pass = True
        elif soma in (2, 3, 12):
            print("Craps! Pass Line perde.")
            terminou_pass = True

    if dont_bet > 0:
        if soma in (2, 3):
            print("Don't Pass ganha!")
            ret_dont = dont_bet * 2
            terminou_dont = True
        elif soma == 12:
            print("Empate (push) no 12 na Don't Pass. Aposta devolvida.")
            ret_dont = dont_bet
            terminou_dont = True
        elif soma in (7, 11):
            print("Don't Pass perde.")
            terminou_dont = True

    encerrou = (pass_bet == 0 or terminou_pass) and (dont_bet == 0 or terminou_dont)
    return ret_pass, ret_dont, encerrou


def jogar_rodada(banca):
    pass_bet, dont_bet = pedir_apostas(banca)
    banca -= pass_bet + dont_bet

    input("Pressione Enter para rolar os dados...")
    d1, d2, soma = rolar_dados()
    mostrar_dados(d1, d2, soma)

    ret_pass, ret_dont, encerrou = resolver_come_out(soma, pass_bet, dont_bet)
    if encerrou:
        return banca + ret_pass + ret_dont

    point = soma
    print(f"\n Point estabelecido: {point}")

    odds = 0
    if pass_bet > 0:
        odds = oferecer_odds(banca, pass_bet)
        banca -= odds

    # Continua rolando até sair o point ou um 7
    while True:
        input("Pressione Enter para rolar os dados...")
        d1, d2, soma = rolar_dados()
        mostrar_dados(d1, d2, soma)

        if soma == point:
            ganho = 0
            if pass_bet > 0:
                print(f" Saiu o point ({point})! Pass Line ganha.")
                ganho += pass_bet * 2
                if odds:
                    ganho += odds + odds_payout(point, odds)
            if dont_bet > 0:
                print(f"Saiu o point ({point}). Don't Pass perde.")
            return banca + ganho

        if soma == 7:
            ganho = 0
            if pass_bet > 0:
                print(" Seven out! Pass Line perde.")
            if dont_bet > 0:
                print(" Seven out! Don't Pass ganha.")
                ganho += dont_bet * 2
            return banca + ganho

        print(f"  ...continua. Procurando {point} (ou 7).")


def main():
    banca = int(input("Quanto você quer entrar no casino? "))
    print(f"\nVocê começa com ${banca}.")

    while banca > 0:
        banca = jogar_rodada(banca)
        print(f"\n Banca atual: ${banca}")

        if banca <= 0:
            print("\n Você quebrou! Fim de jogo.")
            break

        if input("\nJogar de novo? (s/n): ").strip().lower() != "s":
            break

    print(f"\nVocê terminou com ${banca}. Até a próxima!")


if __name__ == "__main__":
    main()