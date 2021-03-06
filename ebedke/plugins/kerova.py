from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
from ebedke.utils.utils import get_fb_post_attached_image, on_workdays, ocr_image, days_lower, pattern_slice, skip_empty_lines
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/kerovaetelbar/posts/"
FB_ID = "582373908553561"


@on_workdays
def get_menu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() >= today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and "heti menü" in post['message'].lower()
    image = get_fb_post_attached_image(FB_ID, menu_filter)
    if image:
        image = Image.open(BytesIO(image)).convert('L')
        f = BytesIO()
        image.save(f, format="png", optimize=True)
        menu = ocr_image(f).splitlines()
        if not menu:
            return []

        menu = pattern_slice(menu, [days_lower[today.weekday()]], days_lower + ['desszert', "890"], inclusive=False)
        menu = list(skip_empty_lines(menu))
    else:
        return []

    return menu


plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Kerova',
    id='kv',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=23),
    cards=[]
)
