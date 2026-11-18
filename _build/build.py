# -*- coding: utf-8 -*-
"""Генерує сторінки портфоліо: головну, /ig/ (без Carbonis) і сторінки кейсів.
Запуск з кореня репозиторію:  python3 _build/build.py
Папка _build не публікується на GitHub Pages (Jekyll пропускає папки з «_»)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = '5'  # збільшуйте при зміні css/js, щоб браузери не брали старі файли
SITE = 'https://max-vorozhko.github.io/'
HERO = open(os.path.join(ROOT, '_build/hero.html'), encoding='utf-8').read()
HOW = open(os.path.join(ROOT, '_build/how.html'), encoding='utf-8').read()

LINKS = {
    'arcade': 'https://max-vorozhko.github.io/rankova-arcade/',
    'hub': 'https://max-vorozhko.github.io/rankova_usefull/',
    'titan': 'https://max-vorozhko.github.io/Titan-Club-Rivne/',
    'baby': 'https://max-vorozhko.github.io/My-baby/',
    'carb': 'https://max-vorozhko.github.io/Carbonis/',
    'carb_calc': 'https://max-vorozhko.github.io/Carbonis/calculator/',
    'carb_game': 'https://max-vorozhko.github.io/Carbonis/game/',
}

def ext(href, text, cls='btn'):
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener">{text}</a>'

# ---------------------------------------------------------------- cases
CASES = [
 dict(slug='rankova', icon='rankova', name='RANKOVA<br>МУЗИЧНІ ІГРИ', plain='Rankova Музичні Ігри', v='v1',
      niche='Музична студія · освіта', meta='Rankova Studio · Рівне', carbonis=False,
      title='Теорію музики не любить ніхто. Тому вона стала грою',
      teaser='Сім мініігор і хаб для учнів музичної студії: тренування слуху й ритму між уроками та запис на пробний урок просто з гри.',
      keys='11 ігор · рейтинг · iOS і Android',
      play=[(LINKS['arcade'], 'Грати')]),
 dict(slug='carbonis', icon='carbonis', name='CARBONIS BBQ', plain='Carbonis BBQ', v='v2',
      niche='Виробництво · застосунок бренду', meta='Carbonis charcoal group', badge='оновлено', carbonis=True,
      title='Скільки вугілля брати на шашлик? Тепер є кому порахувати',
      teaser='Застосунок бренду деревного вугілля: BBQ-калькулятор, покроковий гід приготування, каталог грилів і гра на 9 рівнів.',
      keys='4 розділи · UA / EN · працює без інтернету',
      play=[(LINKS['carb'], 'Відкрити')]),
 dict(slug='titan', icon='titan', name='TITAN RUN', plain='Titan Club Rivne', v='v3',
      niche='Спорт · комʼюніті', meta='Titan Club Rivne', carbonis=False,
      title='Клуб бігає по неділях. А що між неділями?',
      teaser='Гра, клубний застосунок з особистими кабінетами, адмінка й промо для бігового клубу, співзасновником якого я є.',
      keys='5 режимів · 40+ у рейтингу · iOS і Android',
      play=[(LINKS['titan'], 'Бігти')]),
 dict(slug='my-baby', icon='mybaby', name='MY BABY', plain='My Baby', v='v4',
      niche='Батьківство · застосунок', meta='Власний продукт', badge='не гра, але теж затягує', carbonis=False,
      title='О 3-й ночі ніхто не памʼятає, коли дитина востаннє їла',
      teaser='Мій власний застосунок для сну, годування, прикорму й шкіри малюка. Зроблений за кілька вечорів, бо готові не підійшли.',
      keys='4 розділи · дані лише на телефоні · офлайн',
      play=[(LINKS['baby'], 'Відкрити')]),
]
BY = {c['slug']: c for c in CASES}

# ---------------------------------------------------------------- building blocks
def head(p, title, desc, url, robots=False):
    return f'''<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#fff4d6">
{'<meta name="robots" content="noindex">' if robots else ''}
<link rel="icon" href="{p}favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="{p}favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="{p}favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{p}icon-192.png">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}css/site.css?v={V}">
</head>'''

def nav(p, case=False):
    if case:
        items = (f'<li><a href="#contact">Контакти</a></li>'
                 f'<li><a class="back" href="{p}#cases" data-home data-ig-href="{p}ig/#cases">← Усі кейси</a></li>')
        logo = f'<a href="{p}" class="logo" data-home data-ig-href="{p}ig/">MAX <i>VOROZHKO</i></a>'
    else:
        items = '<li><a href="#cases">Кейси</a></li><li><a href="#how">Як працюю</a></li><li><a href="#contact">Контакти</a></li>'
        logo = '<a href="#" class="logo">MAX <i>VOROZHKO</i></a>'
    return f'''<nav>
  <div class="bar">
    {logo}
    <ul>
      {items}
    </ul>
  </div>
</nav>'''

CONTACT = '''<section id="contact">
  <div class="wrap">
    <div class="contact">
      <h2>{h}</h2>
      <p>{t}</p>
      <div class="cta">
        <a class="btn y" href="https://www.linkedin.com/in/max-vorozhko/" target="_blank" rel="noopener">Написати в LinkedIn</a>
        <a class="btn" href="https://www.instagram.com/max_vorozhko/" target="_blank" rel="noopener">Instagram @max_vorozhko</a>
      </div>
    </div>
  </div>
</section>'''

FOOT = '''<footer>
  <div class="wrap">© <span id="y">2026</span> Max Vorozhko · Рівне <span>· Game over? Ні, натисніть «Грати» ще раз.</span></div>
</footer>
<dialog class="lb" aria-label="Перегляд слайда"><div class="lb-in"><img alt=""><button class="x" type="button" aria-label="Закрити">✕</button><button class="pv" type="button" aria-label="Попередній">←</button><button class="nx" type="button" aria-label="Наступний">→</button><div class="cap"></div></div></dialog>
<script>document.getElementById('y').textContent = new Date().getFullYear();</script>
<script src="{p}js/site.js?v={V}"></script>
</body>
</html>
'''

def facts(items):
    return '<div class="facts">' + ''.join(f'<div class="fact"><b>{a}</b><span>{b}</span></div>' for a, b in items) + '</div>'

def gallery(p, folder, n, alts, tall=False, size=(1080, 1350)):
    figs = []
    for i in range(1, n + 1):
        src = f'{p}media/{folder}-{i}.jpg' if isinstance(folder, str) else f'{p}media/{folder[i-1]}.jpg'
        figs.append(f'<figure><img src="{src}" alt="{alts[i-1]}" width="{size[0]}" height="{size[1]}" loading="lazy" decoding="async"></figure>')
    return (f'<div class="gallery"><div class="track{" tall" if tall else ""}">' + ''.join(figs) +
            f'</div><div class="g-nav"><button class="g-prev" type="button" aria-label="Назад">←</button>'
            f'<button class="g-next" type="button" aria-label="Далі">→</button><span class="count">{n} слайдів · натисніть, щоб збільшити</span></div></div>')

def section(h, inner, sub=''):
    return f'<section class="cs"><div class="wrap"><h2>{h}</h2>{f"<p class=sub>{sub}</p>" if sub else ""}{inner}</div></section>'

def others(p, slug, include_carbonis):
    out = []
    for c in CASES:
        if c['slug'] == slug or (c['carbonis'] and not include_carbonis):
            continue
        out.append(f'<a href="{p}cases/{c["slug"]}/"><img src="{p}icons/{c["icon"]}.png" alt="" width="52" height="52"><span>{c["plain"]}<small>{c["niche"]}</small></span></a>')
    return section('Інші кейси', '<div class="others">' + ''.join(out) + '</div>')

def case_hero(p, c, h1, lead, buttons, extra=''):
    badge = f' <span class="badge">{c["badge"]}</span>' if c.get('badge') else ''
    return f'''<header class="c-hero">
  <div class="wrap">
    <div class="top">
      <img class="app" src="{p}icons/{c["icon"]}.png" alt="Іконка {c["plain"]}" width="96" height="96">
      <div class="kicker">{c["meta"]}{badge}<br><span class="niche">{c["niche"]}</span></div>
    </div>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="cta">{buttons}</div>
    {extra}
  </div>
</header>'''

# ---------------------------------------------------------------- case bodies
def page_rankova(p):
    c = BY['rankova']
    story_alts = ['Слайд 1: Теорію музики не любить ніхто. Навіть ті, хто сам прийшов на уроки',
                  'Слайд 2: Rankova Arcade працює як застосунок на телефоні, iOS і Android',
                  'Слайд 3: Викладачі кажуть: на уроці всі хочуть грати, а теорія йде туго',
                  'Слайд 4: Тому я зробив Rankova Arcade: 7 мініігор, по одній на інструмент',
                  'Слайд 5: Рівні від Новачка до Легенди Soul Place',
                  'Слайд 6: Просто з гри: рейтинг сцени, виклик другу, запис на пробний урок 30 хв',
                  'Слайд 7: Головний критик — Яна. Дизайн і тексти ще зміняться: це прототип',
                  'Слайд 8: Що я зрозумів: гра без метрик — це гіпотеза',
                  'Слайд 9: Скільки часу зайняло? Кілька вечорів']
    promo_alts = ['Слайд 1: Грай у музику — 7 мініігор на слух, ритм і пальці',
                  'Слайд 2: Як це працює: обери інструмент, набирай бали, лізь у рейтинг',
                  'Слайд 3: 7 інструментів, від вокалу до етноспіву',
                  'Слайд 4: Слух — вокал, фортепіано, гітара',
                  'Слайд 5: Ритм — барабани і кахон',
                  'Слайд 6: Пальці й коріння — сопілка і етноспів',
                  'Слайд 7: Від Новачка до Легенди: рахунок — сума рекордів у семи іграх',
                  'Слайд 8: Як встановити на телефон, iPhone і Android',
                  'Слайд 9: Набрав бали? Час на справжній інструмент — пробний урок 30 хв']
    body = case_hero(p, c,
        'Теорію музики не любить ніхто. Тому я зробив з неї гру',
        'Сім мініігор, у яких учні тренують слух, ритм і пальці між уроками, а нові люди знайомляться зі студією і записуються на пробний урок. Працює в браузері й ставиться на телефон як застосунок.',
        ext(LINKS['arcade'], 'Грати в музичні ігри →', 'btn y') + ext(LINKS['hub'], 'Хаб ігор для учнів'),
        facts([('7', 'мініігор, по одній на інструмент'), ('5', 'рівнів гравця, до Легенди Soul Place'),
               ('кілька вечорів', 'на перший прототип'), ('iOS і Android', 'ставиться з браузера')]))
    body += section('Звідки ідея', '''<div class="panel"><div class="prose">
<p>Rankova Studio починалась як невелика студія Яни: вона заснувала бренд, і філософія студії — її. Тепер студію розвивають четверо партнерів: новий простір на 10 кабінетів, викладачі вокалу, фортепіано, гітари, укулеле, сопілки, кахону й етноспіву, заняття для дорослих і дітей.</p>
<p>Викладачі кажуть одне й те саме: на уроці всі хочуть грати, а теорія йде туго. Тож я спробував упакувати теорію в гру, яку хочеться відкрити між уроками, і поставити в кінці кнопку «Записатися».</p>
</div></div>''')
    body += section('Як я розповів про це в Instagram', gallery(p, 'rankova/story', 9, story_alts))
    body += section('Що всередині', '''<div class="sets">
  <div class="set s-arcade">
    <div class="set-head"><span class="set-title">Проєкт 1 · Rankova Музичні Ігри</span><span class="count">7 мініігор</span></div>
    <p>Ігри на слух, ритм і пальці зі спільним рейтингом: найкращі результати з усіх ігор складаються в рівень гравця.</p>
    <div class="chips"><span>Вокал · Чистий слух</span><span>Фортепіано · Мелодійна памʼять</span><span>Барабани · Грув-машина</span><span>Гітара · Акорд-квест</span><span>Кахон · Кахон-патерн</span><span>Сопілка · Пальці сопілки</span><span>Етноспів · Етно-код</span></div>
  </div>
  <div class="set s-hub">
    <div class="set-head"><span class="set-title">Проєкт 2 · Хаб ігор для учнів</span><span class="count">4 гри</span></div>
    <p>Окремий сайт для тренування між уроками: ритм, ноти й сольфеджіо в ігровій формі.</p>
    <div class="chips"><span>Драм Тренажер з таблицею лідерів</span><span>Повтори ритм</span><span>Нотна пригода, 16 рівнів</span><span>Квіз «Який інструмент твій?»</span></div>
  </div>
</div>
<div class="feat" style="margin-top:18px">
  <div><h4>Рейтинг сцени</h4><p>Рахунок — сума рекордів у семи іграх. Рівні: Новачок, Аматор, Сесійний музикант, Хедлайнер, Легенда Soul Place.</p></div>
  <div><h4>Виклик другу</h4><p>Результатом можна поділитися й кинути виклик: побий мій рекорд.</p></div>
  <div><h4>Запис на пробний урок</h4><p>30 хвилин з викладачем, онлайн або офлайн. Кнопка запису є прямо в грі.</p></div>
  <div><h4>Фото для Instagram</h4><p>Стилі «Студія», «Урок», «Плівка», «Квартирник» для поста чи сторіз. Фото обробляється на телефоні й нікуди не завантажується.</p></div>
</div>''')
    body += section('Промо для учнів студії', gallery(p, 'rankova/promo', 9, promo_alts))
    body += section('Чесно про результат', '''<div class="panel sun"><div class="prose">
<p>Це прототип: дизайн і тексти ще зміняться, а головний критик — Яна.</p>
<p>У рейтингу вже понад 10 гравців, але поки це переважно свої: адміни, викладачі й частина учнів. Скільки записів на урок дала гра, поки не видно, бо посилання на запис ходить і в інших місцях.</p>
<p><b>Гра без метрик — це гіпотеза.</b> Наступний крок — окрема мітка на кнопці запису з гри, щоб рахувати ліди саме з неї.</p>
</div></div>''')
    return body

def page_titan(p):
    c = BY['titan']
    alts = ['Слайд 1: Клуб бігає по неділях. А що між неділями?',
            'Слайд 2: Я співзасновник Titan Club Rivne. Після навчання з AI вирішив перевірити, чи можна зробити клуб цифровим без розробників',
            'Слайд 3: Перша версія — гра, де бігун у кольорах клубу збирає монети. Близько 30 гравців за перші дні',
            'Слайд 4: Далі — застосунок для iOS та Android: рівні, типи гри, турнірні таблиці, вхід через Google',
            'Слайд 5: Особистий кабінет і подарунки за 5, 15, 25, 35, 45 пробіжок',
            'Слайд 6: Тематичні ігри під події: підготовка до Житомирської вертикалі',
            'Слайд 7: Що я зрозумів: сама гра надовго не тримає, бігуни не геймери',
            'Слайд 8: Гра тепер магніт для нових, а для своїх — кабінет зі статистикою й подарунками',
            'Слайд 9: Це плацдарм на 2027 рік']
    banner = f'''<div class="banner"><video autoplay muted loop playsinline preload="metadata" poster="{p}media/titan/logo-3d.jpg" aria-label="3D-логотип Titan Club Rivne"><source src="{p}media/titan/logo-3d.mp4" type="video/mp4"></video></div>'''
    body = case_hero(p, c,
        'Клуб бігає по неділях. А що між неділями?',
        'Я співзасновник Titan Club Rivne. Після навчання з AI у Smart People Business School вирішив перевірити, чи можна зробити клуб цифровим без розробників. Вийшли гра, клубний застосунок, адмінка й промо.',
        ext(LINKS['titan'], 'Бігти →', 'btn y'),
        banner + facts([('≈30', 'гравців за перші дні'), ('40+', 'людей у рейтингу'),
                        ('5', 'режимів гри'), ('кілька тижнів', 'вечорами, без команди')]))
    body += section('Як це росло', '''<ol class="steps-line">
<li><div><b>Гра на сторінці</b>Бігун у кольорах клубу біжить вулицями Рівного й збирає монети.</div></li>
<li><div><b>Застосунок для iOS та Android</b>Рівні, кілька типів гри, турнірні таблиці, вхід через Google.</div></li>
<li><div><b>Особисті кабінети</b>Пробіжки за тиждень, місяць і рік, місце в рейтингу й прогрес до подарунків за 5, 15, 25, 35 і 45 неділь: футболка, худі, рюкзак. Справжні імена бачать лише учасники клубу.</div></li>
<li><div><b>Тематичні ігри під події</b>Зараз — трейл для підготовки до «Житомирської вертикалі».</div></li>
</ol>''')
    body += section('Карусель для Instagram', gallery(p, 'titan/story', 9, alts))
    body += section('Промо-ролики', f'''<div class="videos">
<figure><video controls playsinline preload="none" poster="{p}media/titan/promo-3d.jpg"><source src="{p}media/titan/promo-3d.mp4" type="video/mp4"></video><figcaption>3D-ролик Titan Run<span>29 с · для сторіз і Reels</span></figcaption></figure>
<figure><video controls playsinline preload="none" poster="{p}media/titan/promo-ui.jpg"><source src="{p}media/titan/promo-ui.mp4" type="video/mp4"></video><figcaption>Ролик про режими<span>15 с · без звуку</span></figcaption></figure>
</div>''', 'Плюс 3D-логотип клубу на початку сторінки.')
    body += section('Що всередині', '''<div class="sets">
  <div class="set s-game">
    <div class="set-head"><span class="set-title">1 · Гра і застосунок бігунів</span><span class="count">5 режимів</span></div>
    <p>Раннер, який виріс у клубний застосунок: рейтинги, профіль бігуна з ачівками й гардеробом, прокачка персонажа тренуваннями, статистика недільних пробіжок і шлях до нагород.</p>
    <div class="chips"><span>Біг</span><span>Неділя, 5 або 10 км</span><span>Трейл, 7 / 13 / 26 км</span><span>Малюнок дня</span><span>Клуб</span><span>Рейтинг</span><span>Профіль</span></div>
  </div>
  <div class="set s-promo">
    <div class="set-head"><span class="set-title">2 · Фото з пробіжки</span><span class="count">нове</span></div>
    <p>Завантажуєш фото, і застосунок оформлює пост або сторіз у стилі клубу: час, темп, дистанція й контур маршруту. Хвилина замість кількох застосунків і монтажу.</p>
  </div>
  <div class="set s-admin">
    <div class="set-head"><span class="set-title">3 · Адмінка клубу</span><span class="count">закритий доступ</span></div>
    <p>Окремий застосунок для організаторів із входом через Google і ролями. Те, що раніше жило в таблицях і месенджерах, тепер в одному місці.</p>
    <div class="chips"><span>Відвідуваність неділь</span><span>Атлети</span><span>Входи учасників</span><span>Промокоди</span><span>Пробіг за рік</span><span>Експорт у Google-таблицю</span></div>
  </div>
</div>''')
    body += section('Що я зрозумів', '''<div class="panel pink"><div class="prose">
<p>Сама гра надовго не тримає: бігуни не геймери. У лідерборді понад 40 людей, але щотижня стабільно грає один справжній геймер, і він завжди перший.</p>
<p>Тому гра тепер магніт для нових, а для своїх — кабінет зі статистикою й подарунками. Це плацдарм на 2027 рік: у клубу великі плани з розвитку й діджиталізації.</p>
</div></div>''')
    return body

def page_baby(p):
    c = BY['my-baby']
    alts = ['Слайд 1: О 3-й ночі ніхто не памʼятає, коли дитина востаннє їла. Тому я зробив собі додаток',
            'Слайд 2: У голові з малюком — ціла таблиця: сон, годування, прикорм, шкіра',
            'Слайд 3: Тому я зробив My Baby за кілька вечорів у Claude Code',
            'Слайд 4: Сон — таймер і прогноз типового дня',
            'Слайд 5: Їжа — годування, прикорм і трекер алергенів',
            'Слайд 6: Шкіра — графік поруч із новими продуктами',
            'Слайд 7: Дані — тільки на телефоні. Головний критик дизайну — Яна',
            'Слайд 8: Далі — спільний доступ для мами, тата й бабусь']
    body = case_hero(p, c,
        'О 3-й ночі ніхто не памʼятає, коли дитина востаннє їла',
        'Тому я зробив собі застосунок. Сон, годування, прикорм і шкіра малюка 6–12 місяців в одному місці, записи в 1–2 дотики.',
        ext(LINKS['baby'], 'Відкрити My Baby →', 'btn y'),
        facts([('кілька вечорів', 'у Claude Code'), ('4', 'розділи: сон, годування, прикорм, шкіра'),
               ('0', 'даних на сервері: усе на телефоні'), ('офлайн', 'працює без інтернету')]))
    body += section('Чому свій', '''<div class="panel"><div class="prose">
<p>Нам з Яною треба було стежити за годуванням і введенням прикорму. Готові застосунки під наші потреби не підійшли, тож я зробив власний.</p>
<p>Перші спроби дизайну вдалися не всі: я шукав баланс між функціональністю й мінімалізмом. Головний критик дизайну — Яна, і правки ще будуть.</p>
</div></div>''')
    body += section('Карусель для Instagram', gallery(p, 'mybaby/story', 8, alts))
    body += section('Що всередині', '''<div class="feat">
  <div><h4>Сон</h4><p>Таймер в один дотик і прогноз типового дня: коли прокинеться і коли нічний сон, за вашими власними записами.</p></div>
  <div><h4>Їжа</h4><p>Груди або пляшечка, прикорм і трекер алергенів: що вже давали і що ще ні.</p></div>
  <div><h4>Шкіра</h4><p>Графік стану шкіри поруч із новими продуктами. Це лише збіги в записах, не причини: висновки робить лікар.</p></div>
  <div><h4>Статистика й нічна тема</h4><p>Тижневі цифри без порад і спокійний темний режим для нічних записів.</p></div>
</div>
<p class="note">My Baby — щоденник спостережень. Він не дає медичних порад і не замінює лікаря.</p>''')
    body += section('Що далі', '''<div class="panel mint"><div class="prose">
<p>Вхід через Google і спільний доступ: мама, тато, а за потреби й бабусі бачать записи одне одного.</p>
</div></div>''')
    return body

def page_carbonis(p):
    c = BY['carbonis']
    shots = ['carbonis/home', 'carbonis/calc', 'carbonis/guide', 'carbonis/kamado', 'carbonis/game']
    alts = ['Головний екран Carbonis BBQ', 'BBQ-калькулятор: скільки вугілля і мішків взяти', 'Гід приготування з анімованою схемою гриля',
            'Каталог грилів Kamado Bono', 'Гра «Пригоди Вуглинки»']
    body = case_hero(p, c,
        'Скільки вугілля брати на шашлик? Тепер є кому порахувати',
        'Застосунок бренду деревного вугілля: калькулятор, покроковий гід приготування, каталог грилів і гра. Українською й англійською, ставиться на телефон і працює без інтернету.',
        ext(LINKS['carb'], 'Відкрити Carbonis BBQ →', 'btn y') + ext(LINKS['carb_calc'], 'Порахувати вугілля') + ext(LINKS['carb_game'], 'Грати'),
        facts([('4', 'розділи в одному застосунку'), ('7', 'страв у калькуляторі'), ('9', 'рівнів гри'), ('UA / EN', 'дві мови')]))
    body += section('Як це виглядає', '<div class="gallery"><div class="track tall">' + ''.join(
        f'<figure><img src="{p}media/{s}.jpg" alt="{a}" width="600" height="1299" loading="lazy" decoding="async"><figcaption>{a}</figcaption></figure>' for s, a in zip(shots, alts)) +
        '</div><div class="g-nav"><button class="g-prev" type="button" aria-label="Назад">←</button><button class="g-next" type="button" aria-label="Далі">→</button><span class="count">5 екранів · натисніть, щоб збільшити</span></div></div>')
    body += section('Що всередині', '''<div class="sets">
  <div class="set s-calc">
    <div class="set-head"><span class="set-title">1 · BBQ-калькулятор</span><span class="count">7 страв</span></div>
    <p>Обираєте страву, кількість гостей і мангал чи гриль, а калькулятор рахує вугілля в кілограмах і мішках Carbonis. Розрахунком можна поділитися, а кнопка «Де купити» веде до покупки.</p>
    <div class="chips"><span>Мангал або камадо</span><span>Кілограми й мішки</span><span>Жар і час готування</span><span>Чек-лист «Що взяти»</span></div>
  </div>
  <div class="set s-hub">
    <div class="set-head"><span class="set-title">2 · Гід приготування</span><span class="count">крок за кроком</span></div>
    <p>Інструкції для камадо й мангала з анімованою схемою гриля, положенням заслінок і таймерами.</p>
  </div>
  <div class="set s-game">
    <div class="set-head"><span class="set-title">3 · Грилі Kamado Bono</span><span class="count">каталог</span></div>
    <p>Моделі й характеристики грилів поруч із вугіллям, яке для них підходить.</p>
  </div>
  <div class="set s-vug">
    <div class="set-head"><span class="set-title">4 · Гра «Пригоди Вуглинки»</span><span class="count">9 рівнів</span></div>
    <p>Вуглинка проходить шлях продукту: стрибає в мішок на лінії фасування, складає палети у фуру за реальною схемою й розпалює гриль. Зірки за точність і онлайн-рейтинг.</p>
    <div class="chips"><span>Мішок</span><span>Фура</span><span>Гриль</span></div>
  </div>
</div>''')
    return body

PAGES = {'rankova': page_rankova, 'titan': page_titan, 'my-baby': page_baby, 'carbonis': page_carbonis}

# ---------------------------------------------------------------- home
def card(c, href_suffix=''):
    badge = f' <span class="badge">{c["badge"]}</span>' if c.get('badge') else ''
    url = f'cases/{c["slug"]}/{href_suffix}'
    plays = ''.join(ext(h, t) for h, t in c['play'])
    return f'''      <article class="case">
        <a class="visual {c["v"]}" href="{url}" aria-label="Кейс {c["plain"]}">
          <img class="app" src="icons/{c["icon"]}.png" alt="" width="124" height="124">
          <div class="name">{c["name"]}</div>
          <div class="niche">{c["niche"]}</div>
        </a>
        <div class="body">
          <div class="meta">{c["meta"]}{badge}</div>
          <h3><a href="{url}">{c["title"]}</a></h3>
          <p class="teaser">{c["teaser"]}</p>
          <p class="keys">{c["keys"]}</p>
          <div class="links"><a class="btn y" href="{url}">Читати кейс →</a>{plays}</div>
        </div>
      </article>'''

def home(ig):
    cases = [c for c in CASES if not (ig and c['carbonis'])]
    n = len(cases)
    word = {3: 'Три', 4: 'Чотири'}[n]
    niches = 'Музика, біг і батьківство' if ig else 'Музика, вугілля, біг і батьківство'
    p = '../' if ig else ''
    hero = HERO
    if ig:
        hero = re.sub(r'\s*<img class="float f2" src="icons/carbonis.png"[^>]*>', '', hero)
    hero = re.sub(r'(src|href)="(?!https?:|#)([^"]+)"', lambda m: f'{m.group(1)}="{p}{m.group(2)}"', hero)
    cards = '\n\n'.join(card(c, '?from=ig' if ig else '') for c in cases)
    cards = cards.replace('href="cases/', f'href="{p}cases/').replace('src="icons/', f'src="{p}icons/')
    desc = ('Роблю брендовані ігри й застосунки для бізнесу: навчання, маркетинг, комʼюніті. Кейси: '
            + ', '.join(c['plain'] for c in cases) + '.')
    extra_css = '<style>.f3{top:206px!important}.f4{top:356px!important;right:8%!important}</style>' if ig else ''
    html = head(p, 'Max Vorozhko — ігри й застосунки для бізнесу', desc, SITE + ('ig/' if ig else '')) + extra_css
    html += f'\n<body data-ig="{1 if ig else 0}">\n\n' + nav(p) + '\n\n' + hero + '\n\n'
    html += f'''<section id="cases">
  <div class="wrap">
    <h2>{word} ніші. <mark>Один</mark> підхід</h2>
    <p class="sub">{niches}: різні світи, але зручний продукт у телефоні скрізь працює як канал із людьми. Натисніть на кейс, щоб прочитати історію й подивитися матеріали.</p>

    <div class="cases">

{cards}

    </div>
  </div>
</section>

''' + HOW + '\n' + CONTACT.format(h='Зробимо гру для вашого бізнесу?', t='Напишіть коротко про свою нішу та задачу. Запропоную формат і наступні кроки. Обіцяю не питати «а чи не можна просто банер».') + '\n\n' + FOOT.format(p=p, V=V)
    return html

def case_page(slug):
    c = BY[slug]; p = '../../'
    html = head(p, f'{c["plain"]} — кейс · Max Vorozhko', c['teaser'], f'{SITE}cases/{slug}/')
    html += '\n<body class="case-page">\n\n' + nav(p, case=True) + '\n\n' + PAGES[slug](p) + '\n'
    html += others(p, slug, include_carbonis=c['carbonis'])
    html += '\n' + CONTACT.format(h='Хочете щось схоже для свого бізнесу?', t='Напишіть коротко про нішу та задачу. Запропоную формат і наступні кроки.')
    html += '\n\n' + FOOT.format(p=p, V=V)
    return html

def write(rel, html):
    path = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(html)

write('index.html', home(False))
write('ig/index.html', home(True))
for s in PAGES:
    write(f'cases/{s}/index.html', case_page(s))

# safety check: nothing reachable from the Instagram side mentions Carbonis
bad = re.compile(r'(?i)carbonis|вугіл|вуглин|charcoal|мангал|шашлик|bbq|камадо|kamado')
for rel in ['ig/index.html', 'cases/rankova/index.html', 'cases/titan/index.html', 'cases/my-baby/index.html']:
    hits = bad.findall(open(os.path.join(ROOT, rel), encoding='utf-8').read())
    assert not hits, (rel, hits)
print('built OK')
