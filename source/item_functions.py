from source.game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    colors = args[1]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health.', colors.get('yellow'))})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', colors.get('green'))})

    return results


def cast_lightning(*args, **kwargs):
    caster = args[0]
    colors = args[1]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entitiy in entities:
        if entitiy.fighter and entitiy != caster and game_map.fov[entitiy.x, entitiy.y]:
            distance = caster.distance_to(entitiy)

            if distance < closest_distance:
                target = entitiy
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target,
                        'message': Message(
                            'A lightning bolt strikes the {0} with a loud thunder! The damage is {1}.'.format(
                                target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.',
                                                                              colors.get('red'))})

    return results
