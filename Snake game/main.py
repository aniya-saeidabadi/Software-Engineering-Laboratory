import random
import sys
import pygame

# تنظیمات اصلی بازی
pygame.init()

WIDTH, HEIGHT = 900, 600
CELL_SIZE = 30
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 9

BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
RED = (235, 55, 55)
BUTTON_COLOR = (45, 135, 75)
BUTTON_HOVER = (65, 165, 95)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# برای نمایش ایموجی‌ها، در ویندوز از فونت Segoe UI Emoji استفاده می‌شود.
score_font = pygame.font.SysFont("Arial", 25, bold=True)
message_font = pygame.font.SysFont("Arial", 54, bold=True)
button_font = pygame.font.SysFont("Arial", 25, bold=True)
emoji_font = pygame.font.SysFont("Segoe UI Emoji", 27)

FRUITS = [
    ("🍏", 2),   # سیب سبز
    ("🍎", 4),   # سیب قرمز
    ("🍉", 10),  # هندوانه
    ("🍓", 15),  # توت فرنگی
    ("🍌", 20),  # موز
    ("🍊", 25),  # پرتقال
    ("🫐", 50),  # بلوبری
]

START_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 27, 200, 54)


def draw_button(text, rect):
    """دکمه را با توجه به محل نشانگر ماوس رسم می‌کند."""
    color = BUTTON_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = button_font.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))


def random_empty_position(snake):
    """یک خانه خالی برای ظاهر شدن میوه انتخاب می‌کند."""
    empty_cells = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in snake
    ]
    return random.choice(empty_cells) if empty_cells else None


def new_game():
    """وضعیت اولیه بازی را می‌سازد."""
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
             (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
             (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    fruit_position = random_empty_position(snake)
    fruit = random.choice(FRUITS)
    return snake, direction, fruit_position, fruit, 0


def draw_game(snake, fruit_position, fruit, score):
    """مار، میوه و امتیاز را نمایش می‌دهد."""
    screen.fill(BLACK)

    score_surface = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (15, 12))

    if fruit_position is not None:
        fruit_surface = emoji_font.render(fruit[0], True, WHITE)
        fruit_rect = fruit_surface.get_rect(
            center=(fruit_position[0] * CELL_SIZE + CELL_SIZE // 2,
                    fruit_position[1] * CELL_SIZE + CELL_SIZE // 2)
        )
        screen.blit(fruit_surface, fruit_rect)

    for segment in snake:
        snake_surface = emoji_font.render("🟩", True, WHITE)
        snake_rect = snake_surface.get_rect(
            center=(segment[0] * CELL_SIZE + CELL_SIZE // 2,
                    segment[1] * CELL_SIZE + CELL_SIZE // 2)
        )
        screen.blit(snake_surface, snake_rect)

    pygame.display.flip()


def show_start_screen():
    screen.fill(BLACK)
    draw_button("START", START_BUTTON)
    pygame.display.flip()


def show_game_over():
    screen.fill(BLACK)
    title = message_font.render("GAME OVER", True, RED)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 65)))

    again_button = pygame.Rect(WIDTH // 2 - 115, HEIGHT // 2 + 5, 230, 54)
    draw_button("START AGAIN", again_button)
    pygame.display.flip()
    return again_button


def main():
    state = "start"
    snake, direction, fruit_position, fruit, score = new_game()
    next_direction = direction
    game_over_button = None

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state in ("start", "game_over"):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked_rect = START_BUTTON if state == "start" else game_over_button
                    if clicked_rect and clicked_rect.collidepoint(event.pos):
                        snake, direction, fruit_position, fruit, score = new_game()
                        next_direction = direction
                        state = "playing"

            elif state == "playing" and event.type == pygame.KEYDOWN:
                # حرکت معکوس مستقیم مجاز نیست.
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    next_direction = (1, 0)

        if state == "start":
            show_start_screen()

        elif state == "playing":
            direction = next_direction
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # برخورد با دیواره یا بدن مار باعث پایان بازی می‌شود.
            hit_wall = (
                new_head[0] < 0 or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
            )

            eating = new_head == fruit_position
            body_to_check = snake if eating else snake[:-1]
            hit_self = new_head in body_to_check

            if hit_wall or hit_self:
                state = "game_over"
                game_over_button = show_game_over()
                continue

            snake.insert(0, new_head)

            if eating:
                score += fruit[1]
                fruit_position = random_empty_position(snake)
                if fruit_position is not None:
                    fruit = random.choice(FRUITS)
                else:
                    # اگر تمام خانه‌ها پر شوند، بازی با امتیاز فعلی پایان می‌یابد.
                    state = "game_over"
                    game_over_button = show_game_over()
            else:
                snake.pop()

            draw_game(snake, fruit_position, fruit, score)

        elif state == "game_over":
            # صفحه پایان بازی تا انتخاب شروع مجدد ثابت می‌ماند.
            if game_over_button is None:
                game_over_button = show_game_over()


if __name__ == "__main__":
    main()
