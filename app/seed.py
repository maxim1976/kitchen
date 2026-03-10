import click
from flask import current_app
from app import db
from app.models import MenuItem


MENU_ITEMS = [
    # ── Appetizers ────────────────────────────────────────────────────────────
    dict(category='appetizers', name='Scallion Pancake',      name_zh='蔥油餅',   price=60,
         desc='Crispy pan-fried flatbread with fragrant scallion layers.',
         desc_zh='外酥內軟，層層蔥香，現煎上桌。'),
    dict(category='appetizers', name='Popcorn Chicken',       name_zh='鹽酥雞',   price=80,
         desc='Crispy seasoned chicken bites with basil and chilli.',
         desc_zh='酥脆多汁，九層塔爆香，台式夜市風味。'),
    dict(category='appetizers', name='Cold Tofu',             name_zh='涼拌豆腐', price=55,
         desc='Silken tofu with soy, sesame oil, and spring onion.',
         desc_zh='嫩豆腐佐醬油、麻油與蔥花，清爽開胃。'),
    dict(category='appetizers', name='Edamame',               name_zh='毛豆',     price=45,
         desc='Salted steamed edamame pods.',
         desc_zh='鹽水煮毛豆，簡單美味。'),

    # ── Mains ────────────────────────────────────────────────────────────────
    dict(category='mains', name='Three-Cup Chicken',          name_zh='三杯雞',   price=180,
         desc='Braised chicken with sesame oil, soy sauce, rice wine, and basil.',
         desc_zh='以麻油、醬油、米酒燜煮，九層塔提香，下飯必點。'),
    dict(category='mains', name='Braised Pork Rice',          name_zh='滷肉飯',   price=80,
         desc='Slow-braised minced pork belly over steamed white rice.',
         desc_zh='五花肉慢滷，油蔥酥增香，台灣家常魂。'),
    dict(category='mains', name='Salt & Pepper Pork Chop',    name_zh='椒鹽排骨', price=160,
         desc='Crispy fried pork ribs with a seasoned salt and white pepper crust.',
         desc_zh='外皮酥脆，椒鹽香氣濃郁，肉汁鮮嫩。'),
    dict(category='mains', name='Stir-Fried Water Spinach',   name_zh='炒空心菜', price=80,
         desc='Water spinach wok-tossed with garlic and fermented tofu.',
         desc_zh='大火快炒，蒜香豆腐乳，翠綠爽脆。'),
    dict(category='mains', name='Oyster Vermicelli',          name_zh='蚵仔麵線', price=90,
         desc='Thick vermicelli in savory broth with plump oysters and sweet potato starch.',
         desc_zh='鮮蚵配紅糟麵線，稠滑湯底，街頭經典小吃。'),
    dict(category='mains', name='Scallion Beef Stir-Fry',     name_zh='蔥爆牛肉', price=200,
         desc='Tender beef slices wok-tossed with green onions at high heat.',
         desc_zh='嫩滑牛肉與蔥段大火爆炒，鑊氣十足。'),
    dict(category='mains', name='Basil Clams',                name_zh='九層塔蛤蜊', price=150,
         desc='Fresh clams stir-fried with garlic, chilli, and Thai basil.',
         desc_zh='鮮蛤蜊爆炒九層塔，蒜辣提鮮，湯汁鮮甜。'),

    # ── Soups ────────────────────────────────────────────────────────────────
    dict(category='soups', name='Miso Soup',                  name_zh='味噌湯',   price=40,
         desc='Light miso broth with silken tofu and wakame.',
         desc_zh='嫩豆腐與海帶芽，清淡養胃。'),
    dict(category='soups', name='Tomato Egg Drop Soup',       name_zh='番茄蛋花湯', price=55,
         desc='Tangy tomato broth swirled with silky egg ribbons.',
         desc_zh='酸甜番茄湯底，蛋花絲滑，家常暖心湯。'),
    dict(category='soups', name='Pork Rib Soup',              name_zh='排骨湯',   price=90,
         desc='Slow-simmered pork ribs with ginger and radish.',
         desc_zh='豬肋排與白蘿蔔慢燉，湯清味鮮。'),
    dict(category='soups', name='Winter Melon Soup',          name_zh='冬瓜湯',   price=55,
         desc='Light broth with tender winter melon and clams.',
         desc_zh='冬瓜蛤蜊清湯，清甜爽口，消暑解膩。'),

    # ── Drinks ───────────────────────────────────────────────────────────────
    dict(category='drinks', name='Oolong Tea',                name_zh='烏龍茶',   price=35,
         desc='Chilled Taiwanese high-mountain oolong, lightly floral.',
         desc_zh='台灣高山烏龍，花香淡雅，冷熱均有。'),
    dict(category='drinks', name='Barley Water',              name_zh='薏仁水',   price=40,
         desc='Unsweetened pearl barley water, cooling and light.',
         desc_zh='無糖薏仁水，清熱消暑，台灣傳統飲品。'),
    dict(category='drinks', name='Soy Milk',                  name_zh='豆漿',     price=35,
         desc='Warm or cold fresh soy milk, lightly sweetened.',
         desc_zh='現磨豆漿，微甜順口，冷熱可選。'),
    dict(category='drinks', name='Fresh Lemon Juice',         name_zh='現榨檸檬汁', price=60,
         desc='Freshly squeezed lemon with a touch of honey.',
         desc_zh='現榨檸檬加蜂蜜，酸甜清爽。'),
    dict(category='drinks', name='Taiwan Beer',               name_zh='台灣啤酒', price=70,
         desc='The classic Taiwanese lager. Cold and crisp.',
         desc_zh='台灣金牌啤酒，清爽順口，配餐首選。'),
]


def register_seed_command(app):
    @app.cli.command('seed')
    @click.option('--force', is_flag=True, help='Re-seed even if items already exist.')
    def seed(force):
        """Seed the database with starter menu items."""
        existing = MenuItem.query.count()
        if existing and not force:
            click.echo(f'Skipped: {existing} items already in DB. Use --force to re-seed.')
            return

        if force:
            MenuItem.query.delete()
            db.session.commit()
            click.echo('Cleared existing menu items.')

        items = [MenuItem(**d) for d in MENU_ITEMS]
        db.session.add_all(items)
        db.session.commit()
        click.echo(f'Seeded {len(items)} menu items.')
