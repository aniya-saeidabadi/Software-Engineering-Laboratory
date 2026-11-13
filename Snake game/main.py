# کتابخانه random برای انتخاب تصادفی میوه و محل ظاهر شدن آن استفاده می‌شود.
import random
# کتابخانه sys برای بستن کامل برنامه پس از خروج از بازی به کار می‌رود.
import sys
# کتابخانه pygame ابزارهای ساخت پنجره، رسم اجزا و دریافت ورودی بازیکن را فراهم می‌کند.
import pygame

# راه‌اندازی اولیه بخش‌های مختلف کتابخانه Pygame
pygame.init()

# تعیین اندازه پنجره بازی بر حسب پیکسل
WIDTH, HEIGHT = 900, 600
# هر خانه از صفحه بازی ۳۰ پیکسل در نظر گرفته شده است.
CELL_SIZE = 30
# محاسبه تعداد خانه‌های افقی و عمودی صفحه با تقسیم اندازه پنجره بر اندازه هر خانه
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
# تعداد دفعات به‌روزرسانی بازی در هر ثانیه؛ این مقدار سرعت حرکت مار را مشخص می‌کند.
FPS = 9

# تعریف رنگ‌های مورد استفاده در بازی با قالب RGB
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
RED = (235, 55, 55)
BUTTON_COLOR = (45, 135, 75)
BUTTON_HOVER = (65, 165, 95)

# ساخت پنجره اصلی بازی و تنظیم عنوان آن
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
# ساعت داخلی Pygame برای کنترل سرعت اجرای حلقه بازی
clock = pygame.time.Clock()

# تعریف فونت‌های جداگانه برای امتیاز، پیام پایان بازی، دکمه‌ها و ایموجی‌ها
# فونت Segoe UI Emoji در ویندوز برای نمایش بهتر شکلک‌ها استفاده می‌شود.
score_font = pygame.font.SysFont("Arial", 25, bold=True)
message_font = pygame.font.SysFont("Arial", 54, bold=True)
button_font = pygame.font.SysFont("Arial", 25, bold=True)
emoji_font = pygame.font.SysFont("Segoe UI Emoji", 27)

# فهرست میوه‌ها؛ هر عضو شامل ایموجی میوه و امتیاز مربوط به آن است.
# هنگام خوردن هر میوه، امتیاز آن به امتیاز کل بازیکن اضافه می‌شود.
FRUITS = [
    ("🍏", 2),   # سیب سبز: ۲ امتیاز
    ("🍎", 4),   # سیب قرمز: ۴ امتیاز
    ("🍉", 10),  # هندوانه: ۱۰ امتیاز
    ("🍓", 15),  # توت‌فرنگی: ۱۵ امتیاز
    ("🍌", 20),  # موز: ۲۰ امتیاز
    ("🍊", 25),  # پرتقال: ۲۵ امتیاز
    ("🫐", 50),  # بلوبری: ۵۰ امتیاز
]

# تعیین موقعیت و اندازه دکمه شروع در مرکز صفحه
START_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 27, 200, 54)


def draw_button(text, rect):
    """دکمه را رسم می‌کند و در صورت قرار گرفتن نشانگر ماوس روی آن، رنگش را تغییر می‌دهد."""
    # بررسی می‌کنیم نشانگر ماوس روی محدوده دکمه قرار دارد یا خیر.
    color = BUTTON_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    # رسم مستطیل دکمه با گوشه‌های گرد
    pygame.draw.rect(screen, color, rect, border_radius=10)
    # تبدیل نوشته دکمه به تصویر قابل نمایش و قرار دادن آن در مرکز دکمه
    label = button_font.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))


def random_empty_position(snake):
    """یک خانه خالی از صفحه انتخاب می‌کند تا میوه در آن ظاهر شود."""
    # تمام خانه‌های صفحه را بررسی می‌کنیم و خانه‌هایی را که بدن مار در آن‌ها نیست، نگه می‌داریم.
    empty_cells = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in snake
    ]
    # اگر خانه خالی وجود داشته باشد، یکی را به صورت تصادفی برمی‌گردانیم.
    # اگر صفحه کاملاً پر شده باشد، مقدار None برگردانده می‌شود.
    return random.choice(empty_cells) if empty_cells else None


def new_game():
    """تمام متغیرهای لازم را برای شروع یک بازی تازه مقداردهی اولیه می‌کند."""
    # مار در ابتدای بازی سه خانه طول دارد و در مرکز صفحه قرار می‌گیرد.
    # عضو اول فهرست، سر مار است و بقیه اعضا به ترتیب بدن آن هستند.
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
             (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
             (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
    # جهت اولیه حرکت مار به سمت راست است؛ هر زوج عدد نشان‌دهنده تغییر x و y است.
    direction = (1, 0)
    # انتخاب محل خالی تصادفی برای اولین میوه و انتخاب تصادفی نوع میوه
    fruit_position = random_empty_position(snake)
    fruit = random.choice(FRUITS)
    # برگرداندن وضعیت اولیه مار، جهت حرکت، میوه و امتیاز صفر
    return snake, direction, fruit_position, fruit, 0


def draw_game(snake, fruit_position, fruit, score):
    """صفحه بازی را پاک‌سازی و امتیاز، میوه و تمام قسمت‌های مار را دوباره رسم می‌کند."""
    # پاک کردن تصویر قبلی صفحه برای جلوگیری از باقی ماندن شکل‌های حرکت قبلی
    screen.fill(BLACK)

    # نمایش امتیاز فعلی در قسمت بالای صفحه
    score_surface = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (15, 12))

    # اگر محل میوه معتبر باشد، ایموجی آن را در مرکز خانه مربوطه رسم می‌کنیم.
    if fruit_position is not None:
        fruit_surface = emoji_font.render(fruit[0], True, WHITE)
        fruit_rect = fruit_surface.get_rect(
            center=(fruit_position[0] * CELL_SIZE + CELL_SIZE // 2,
                    fruit_position[1] * CELL_SIZE + CELL_SIZE // 2)
        )
        screen.blit(fruit_surface, fruit_rect)

    # با پیمایش فهرست snake، تمام خانه‌های تشکیل‌دهنده بدن مار رسم می‌شوند.
    for segment in snake:
        snake_surface = emoji_font.render("🟩", True, WHITE)
        snake_rect = snake_surface.get_rect(
            center=(segment[0] * CELL_SIZE + CELL_SIZE // 2,
                    segment[1] * CELL_SIZE + CELL_SIZE // 2)
        )
        screen.blit(snake_surface, snake_rect)

    # نمایش تغییرات رسم‌شده در پنجره بازی
    pygame.display.flip()


def show_start_screen():
    """صفحه آغازین را با پس‌زمینه سیاه و دکمه START نمایش می‌دهد."""
    screen.fill(BLACK)
    draw_button("START", START_BUTTON)
    pygame.display.flip()


def show_game_over():
    """صفحه پایان بازی را نمایش می‌دهد و محدوده دکمه شروع دوباره را برمی‌گرداند."""
    # پاک کردن صفحه و نمایش پیام GAME OVER با رنگ قرمز
    screen.fill(BLACK)
    title = message_font.render("GAME OVER", True, RED)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 65)))

    # ساخت دکمه START AGAIN و قرار دادن آن در مرکز، پایین پیام پایان بازی
    again_button = pygame.Rect(WIDTH // 2 - 115, HEIGHT // 2 + 5, 230, 54)
    draw_button("START AGAIN", again_button)
    pygame.display.flip()
    # برگرداندن محدوده دکمه برای تشخیص کلیک بازیکن
    return again_button


def main():
    """تابع اصلی برنامه؛ رویدادها، وضعیت بازی، حرکت مار و برخوردها را مدیریت می‌کند."""
    # بازی سه وضعیت دارد: start برای صفحه آغاز، playing برای بازی و game_over برای پایان.
    state = "start"
    # ساخت وضعیت اولیه بازی و ذخیره متغیرهای مورد نیاز
    snake, direction, fruit_position, fruit, score = new_game()
    # next_direction جهت انتخاب‌شده توسط بازیکن را نگه می‌دارد تا در نوبت حرکت اعمال شود.
    next_direction = direction
    # این متغیر تا زمان نمایش صفحه پایان بازی، محدوده دکمه شروع دوباره را نگه می‌دارد.
    game_over_button = None

    # حلقه اصلی بازی تا زمانی که بازیکن پنجره را نبندد، اجرا می‌شود.
    while True:
        # محدود کردن سرعت حلقه به مقدار FPS
        clock.tick(FPS)

        # دریافت و بررسی رویدادهایی مانند بستن پنجره، کلیک ماوس و فشردن کلیدها
        for event in pygame.event.get():
            # اگر کاربر علامت بستن پنجره را انتخاب کند، برنامه به طور کامل بسته می‌شود.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # در صفحه شروع یا پایان، کلیک ماوس برای شروع بازی یا شروع مجدد بررسی می‌شود.
            if state in ("start", "game_over"):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # با توجه به وضعیت فعلی، محدوده دکمه مناسب انتخاب می‌شود.
                    clicked_rect = START_BUTTON if state == "start" else game_over_button
                    # اگر کلیک داخل محدوده دکمه باشد، همه چیز از ابتدا تنظیم می‌شود.
                    if clicked_rect and clicked_rect.collidepoint(event.pos):
                        snake, direction, fruit_position, fruit, score = new_game()
                        next_direction = direction
                        state = "playing"

            # هنگام بازی، کلیدهای جهت‌دار یا W، A، S و D جهت حرکت مار را تغییر می‌دهند.
            elif state == "playing" and event.type == pygame.KEYDOWN:
                # حرکت مستقیم به سمت مخالف جهت فعلی ممنوع است تا مار به خودش برنگردد.
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    next_direction = (1, 0)

        # در وضعیت start فقط صفحه آغازین نمایش داده می‌شود و حرکت مار هنوز شروع نشده است.
        if state == "start":
            show_start_screen()

        # در وضعیت playing منطق اصلی حرکت و امتیازدهی اجرا می‌شود.
        elif state == "playing":
            # جهت انتخاب‌شده اعمال می‌شود؛ اگر کلید تازه‌ای فشرده نشود، جهت قبلی حفظ خواهد شد.
            direction = next_direction
            # مختصات فعلی سر مار از اولین عضو فهرست snake خوانده می‌شود.
            head_x, head_y = snake[0]
            # محاسبه مختصات خانه بعدی سر مار با افزودن جهت حرکت به مختصات فعلی
            new_head = (head_x + direction[0], head_y + direction[1])

            # بررسی برخورد با دیواره‌ها؛ خروج مختصات سر از محدوده جدول به معنی برخورد است.
            hit_wall = (
                new_head[0] < 0 or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
            )

            # بررسی می‌کنیم آیا خانه بعدی سر مار همان محل میوه است یا خیر.
            eating = new_head == fruit_position
            # اگر مار میوه نخورد، خانه انتهایی دم در همین حرکت حذف می‌شود؛
            # بنابراین برخورد با خانه فعلی دم در این حالت برخورد واقعی محسوب نمی‌شود.
            # اما هنگام خوردن میوه، دم حذف نمی‌شود و کل بدن باید برای برخورد بررسی شود.
            body_to_check = snake if eating else snake[:-1]
            # بررسی برخورد سر جدید با بخش‌های بدن مار
            hit_self = new_head in body_to_check

            # اگر مار به دیواره یا بدن خودش برخورد کرده باشد، بازی پایان می‌یابد.
            if hit_wall or hit_self:
                state = "game_over"
                game_over_button = show_game_over()
                # ادامه این دور از حلقه متوقف می‌شود تا حرکت دیگری انجام نشود.
                continue

            # سر جدید به ابتدای فهرست اضافه می‌شود؛ این کار حرکت مار را ایجاد می‌کند.
            snake.insert(0, new_head)

            # اگر سر مار به میوه رسیده باشد، امتیاز میوه به امتیاز کل اضافه می‌شود.
            if eating:
                score += fruit[1]
                # پس از خوردن میوه، محل خالی تصادفی دیگری برای میوه بعدی انتخاب می‌شود.
                fruit_position = random_empty_position(snake)
                if fruit_position is not None:
                    # نوع میوه بعدی نیز به صورت تصادفی انتخاب می‌شود.
                    fruit = random.choice(FRUITS)
                else:
                    # اگر هیچ خانه خالی باقی نمانده باشد، بازی با امتیاز فعلی پایان می‌یابد.
                    state = "game_over"
                    game_over_button = show_game_over()
            else:
                # اگر میوه‌ای خورده نشده باشد، آخرین خانه دم حذف می‌شود تا طول مار ثابت بماند.
                snake.pop()

            # رسم وضعیت جدید بازی پس از انجام حرکت و محاسبه امتیاز
            draw_game(snake, fruit_position, fruit, score)

        # در وضعیت game_over صفحه پایان بازی باقی می‌ماند تا بازیکن شروع مجدد را انتخاب کند.
        elif state == "game_over":
            if game_over_button is None:
                game_over_button = show_game_over()


# این شرط باعث می‌شود تابع main فقط هنگام اجرای مستقیم همین فایل اجرا شود.
# اگر فایل در برنامه دیگری import شود، بازی به طور خودکار شروع نخواهد شد.
if __name__ == "__main__":
    main()
