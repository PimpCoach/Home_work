import random

proverbs = [
    "Ум хорошо, а два лучше.",
    "Ум — горячая штука.",
    "Ум всё голова.",
    "Умом Россию не понять.",
    "Ум бережет, а глупость губит.",
    "Ум в голову приходит.",
    "Ум от ума не горит.",
    "Умом нагружен, а волосы развеваются.",
    "Умом обдумал, а ногами пошел.",
    "Ум — сокровище, не пропадет без него и копье на ветру.",
    "Ум — грех, а бес — мера.",
    "Ум есть богатство.",
    "Ум роднит народы.",
    "Ум краток, да забот — бездна.",
    "Ум не камень, взял и положил.",
    "Ум не велит, а наставляет.",
    "Ум с мерой, а глупость без меры.",
    "Ум — сокол, глаз его — телескоп.",
    "Ум — не конская морда, не разобьешь.",
    "Ум — семь пядей во лбу.",
    "Ум — не барсук, в нору не залезет.",
    "Ум в голове, а не на ветру.",
    "Ум греет душу, а глупость терпение.",
    "Ум служит человеку, а глупость — хозяином.",
    "Ум мил, да безумству хозяин.",
    "Ум в труде, да наслаждение в праздности.",
    "Ум глаза исправляет.",
    "Ум человека не обманешь.",
    "Ум на подобии огня — без сна не останешься.",
    "Ум к уму приходит.",
    "Ум с пользой тратит время.",
    "Ум желание творит.",
    "Ум общего дела дело.",
    "Ум — друг, а воля — враг.",
    "Ум — бесценное сокровище.",
    "Ум тонок, да разум невелик.",
    "Ум — враг бедности.",
    "Ум — теремок, да не на прокол.",
    "Ум силен, да не камень.",
    "Ум рассудит, что сердце не посоветует.",
    "Ум — подкова, а топор — ось.",
    "Ум легче камня, да весомей золота.",
    "Ум не вешать на гроздья.",
    "Ум — не мешок, на плечи не вешай.",
    "Ум — лучшая победа.",
    "Ум — в суде велик, а в деле своем мал.",
    "Ум голове краса.",
    "Ум — сокровище, а глупость — нищета.",
    "Ум человека — огонь, а глаза — масло.",
    "Ум — путь, а дорога — конец.",
    "Ум стоит денег.",
    "Ум от смеха бьет в ладоши.",
    "Ум — коза, к барскому плечу привыкает.",
    "Ум — лезвие, а лень — ржавчина.",
    "Ум на вершине — мир в руках.",
]

variants = [
    'кот',
    'шеф',
    'мозг',
    'лес',
    'фолк',
    'код',
    'рот',
    'мёд',
    'лук',
    'лес',
    'год',
    'час',
    'друг',
    'муж',
    'айфон',
    'стол',
    'нос',
    'сыр',
    'хлеб',
    'мир',
    'свет',
    'рок',
    'дед',
    'дом',
    'сон',
    'глаз',
]

proverbs_list = []
count = 1
VARIANTS_LEN = len(variants) 

user_proverb_num = int(input(f"Введите число пословиц от 1 до {len(variants)}: "))

while count <= min(user_proverb_num, VARIANTS_LEN): # Если len(variants) в константу не прописать, то выдает максимально 13 пословиц, т.к. удаляются в цикле варианты, которые уже использовались. Доходит до 13-го варианта и цикл завершается)

    proverb_choice = random.choice(proverbs)
    proverbs.remove(proverb_choice)
    
    variants_choice = random.choice(variants)
    variants.remove(variants_choice)
    print(variants)

    proverbs_list.append(proverb_choice.replace("Ум", variants_choice).capitalize())
    
    count += 1

print('\n'.join(proverbs_list))

# print('\n'.join([random.choice(proverbs).replace("Ум", random.choice(variants)).capitalize() for _ in range(min(int(input(f"Введите число пословиц от 1 до {len(variants)}: ")), len(variants)))]))  ###(Хотел сам однострочник написать, но не мог понять как условие с for прописать и запросил помощь CODY)