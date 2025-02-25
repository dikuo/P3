import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    enemy_planets = sorted([p for p in state.enemy_planets() if not any(f.destination_planet == p.ID for f in state.my_fleets())], key=lambda p: p.num_ships)

    my_planets_iter = iter(my_planets)
    target_planets_iter = iter(enemy_planets)

    for my_planet in my_planets:
        target_planet = next(target_planets_iter, None)
        if not target_planet:
            break

        while my_planet:
            required_ships = target_planet.num_ships + \
                              state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 2

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                target_planet = next(target_planets_iter, None)
                if not target_planet:
                    return

            my_planet = next(my_planets_iter, None)
            if not my_planet:
                return


def spread_to_weakest_neutral_planet(state):
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    neutral_planets = sorted([p for p in state.neutral_planets() if not any(f.destination_planet == p.ID for f in state.my_fleets())], key=lambda p: p.num_ships)

    my_planets_iter = iter(my_planets)
    target_planets_iter = iter(neutral_planets)

    for my_planet in my_planets:
        target_planet = next(target_planets_iter, None)
        if not target_planet:
            break

        while my_planet:
            required_ships = target_planet.num_ships + 2

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                target_planet = next(target_planets_iter, None)
                if not target_planet:
                    return

            my_planet = next(my_planets_iter, None)
            if not my_planet:
                return


def strong_attack(state):
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
    enemy_planets = sorted([p for p in state.enemy_planets() if not any(f.destination_planet == p.ID for f in state.my_fleets())], key=lambda p: p.num_ships)

    my_planets_iter = iter(my_planets)
    target_planets_iter = iter(enemy_planets)

    for my_planet in my_planets:
        target_planet = next(target_planets_iter, None)
        if not target_planet:
            break

        while my_planet:
            required_ships = target_planet.num_ships + state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 5

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                target_planet = next(target_planets_iter, None)
                if not target_planet:
                    return

            my_planet = next(my_planets_iter, None)
            if not my_planet:
                return


def support_planet(state):
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships)
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)

    my_planets_iter = iter(my_planets)

    for my_planet in my_planets:
        if any(f.destination_planet == my_planet.ID for f in state.enemy_fleets()) and not any(f.destination_planet == my_planet.ID for f in state.my_fleets()):
            for f in state.enemy_fleets():
                if f.destination_planet == my_planet.ID:
                    if (my_planet.num_ships + f.turns_remaining * my_planet.growth_rate + strongest_planet.num_ships / 15 + 5) >= (f.num_ships + (state.distance(strongest_planet.ID, my_planet.ID) - f.turns_remaining) * my_planet.growth_rate):
                        issue_order(state, strongest_planet.ID, my_planet.ID, strongest_planet.num_ships / 15 + 1)

        my_planet = next(my_planets_iter, None)
        if not my_planet:
            return


def multi_attacks(state):
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
    enemy_planets = sorted([p for p in state.enemy_planets() if not any(f.destination_planet == p.ID for f in state.my_fleets())], key=lambda p: p.num_ships)

    my_planets_iter = iter(my_planets)
    target_planets_iter = iter(enemy_planets)

    target_planet = next(target_planets_iter, None)
    size = 7

    while target_planet:
        group = []
        i = 0
        my_ships = 0

        while i < size - 1:
            planet = next(my_planets_iter, None)
            if not planet:
                return
            group.append(planet)
            my_ships += planet.num_ships / (size - 2) + 2
            i += 1

        distance = 0
        furthest_planet = None
        for planet in group:
            temp = state.distance(planet.ID, target_planet.ID)

            if temp > distance:
                furthest_planet = planet
                distance = temp

        required_ships = target_planet.num_ships + state.distance(furthest_planet.ID, target_planet.ID) * target_planet.growth_rate + 2

        if my_ships > required_ships:
            for planet in group:
                issue_order(state, planet.ID, target_planet.ID, planet.num_ships / (size - 3) + 2)

        target_planet = next(target_planets_iter, None)


def multi_spread(state):
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
    neutral_planets = sorted([p for p in state.neutral_planets() if not any(f.destination_planet == p.ID for f in state.my_fleets())], key=lambda p: p.num_ships)

    my_planets_iter = iter(my_planets)
    target_planets_iter = iter(neutral_planets)

    neutral_planet = next(target_planets_iter, None)
    size = 10

    while neutral_planet:
        group = []
        i = 0
        my_ships = 0

        while i < size - 1:
            planet = next(my_planets_iter, None)
            if not planet:
                return
            group.append(planet)
            my_ships += planet.num_ships / (size - 2) + 2
            i += 1

        required_ships = neutral_planet.num_ships

        if my_ships > required_ships:
            for planet in group:
                issue_order(state, planet.ID, neutral_planet.ID, planet.num_ships / size + 2)

        neutral_planet = next(target_planets_iter, None)


def swarm(state):
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
    enemy_planets = sorted([p for p in state.enemy_planets() if not any(f.destination_planet == p.ID for f in state.my_fleets())], key=lambda p: p.num_ships)

    if len(state.enemy_planets()) > 3:
        return

    my_planets_iter = iter(my_planets)
    target_planets_iter = iter(enemy_planets)

    target_planet = next(target_planets_iter, None)

    while target_planet:
        group = []
        i = 0

        while i < 10:
            planet = next(my_planets_iter, None)
            if not planet:
                return
            group.append(planet)
            i += 1

        for planet in group:
            issue_order(state, planet.ID, target_planet.ID, planet.num_ships / 2)

        target_planet = next(target_planets_iter, None)
