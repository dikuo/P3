def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def have_largest_fleet(state):
    return sum(p.num_ships for p in state.my_planets()) + sum(f.num_ships for f in state.my_fleets()) \
        > sum(p.num_ships for p in state.enemy_planets()) + sum(f.num_ships for f in state.enemy_fleets())

def is_invade(state):
    try:
        my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
        my_planet = next(my_planets)

        while my_planet:
            if any(f.destination_planet == my_planet.ID for f in state.enemy_fleets()):
                return True
            my_planet = next(my_planets)

    except StopIteration:
        return False

def enough_planets(state):
    sum = 0
    for p in state.my_planets():
        sum += 1
    return sum > 8

def finish_state(state):
    return len(state.enemy_planets()) <= 3


