import pygame
import os
import json
import time
from typing import Literal
from loguru import logger
from handler import Server
import random

WHITE, BLUE, BLACK = (255, 255, 255), (70, 130, 180), (0, 0, 0)
GREEN, RED, YELLOW, ORANGE = (34, 139, 34), (220, 20, 60), (255, 215, 0), (255, 165, 0)

FAST_RESPONSE_TIME = 10
SLOW_RESPONSE_TIME = 20
INACTIVE_TIME = 60

ENCOURAGEMENT_MESSAGES = {
    "CF": ["Outstanding work!", "You're on fire!", "Brilliant thinking!", "That was impressive!", "You nailed it!"],
    "CS": ["You're getting the hang of it!",
           "Keep going, you're making progress.",
           "You're doing great, keep it up.",
           "That was a tough one, but you got it!",
           "Nice effort, let's keep pushing forward."],
    "WF": ["No worries, let's try again.",
        "You're close, think it through.",
        "Good effort, let's take another shot at it.",
        "Mistakes help us learn, let's keep going!",
        "Almost there, let's give it another go."],
    "WS": ["I see where you're going with that.",
        "It's okay, take your time to figure it out.",
        "That was a tricky one, but you'll get the next.",
        "You're learning, and that's what matters.",
        "Let's break it down step by step."],
    "IN": ["You can do this!",
    "Take your time, no rush",
    "Almost there!",
    "You got this!"]
}

def create_data_folder(name):
    os.makedirs(name, exist_ok=True)

class QuizGame:
    def __init__(self, mode: Literal["robot", "human"]):
        pygame.init()
        self.data_directory = os.path.join("data", mode)
        create_data_folder(self.data_directory)
        self.server = Server(mode)
        self.server.start()

        self.FONT = pygame.font.SysFont("Arial", 28)
        self.SMALL_FONT = pygame.font.SysFont("Arial", 22)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((800, 600))
        self.WIDTH, self.HEIGHT = self.screen.get_size()
        pygame.display.set_caption("Robot Interaction Quiz")

        self.questions = [
            {
                "question": 1,
                "options": ["4", "8", "10", "12","14"],
                "correct": "10",
                "image": "questions/ME1.png"
            },
            {
                "question": 2,
                "options": ["18", "21", "25", "29","32"],
                "correct": "25",
                "image": "questions/ME2.png"
            },
            {
                "question": 3,
                "options": [".79999", ".83333", ".88888", ".91111",".93333"],
                "correct": ".88888",
                "image": "questions/MM1.png"
            },
            {
                "question": 4,
                "options": ["54", "81", "162", "216","729"],
                "correct": "216",
                "image": "questions/MM2.png"
            },
            {
                "question": 5,
                "options": ["3/5", "5/8", "6/11", "8/14","10/18"],
                "correct": "5/8",
                "image": "questions/MH1_5_8.png"
            },
            {
                "question": 6,
                "options": ["A", "B", "C", "D","E","F"],
                "correct": "E",
                "image": "questions/PE1_E.png"
            },
            {
                "question": 7,
                "options": ["A", "B", "C", "D","E","F"],
                "correct": "C",
                "image": "questions/PE2_C.png"
            },
            {
                "question": 8,
                "options": ["A", "B", "C", "D","E","F"],
                "correct": "E",
                "image": "questions/PM1_E.png"
            },
            {
                "question": 9,
                "options": ["A", "B", "C", "D","E","F"],
                "correct": "E",
                "image": "questions/PM2_E.png"
            },
            {
                "question": 10,
                "options": ["A", "B", "C", "D","E","F"],
                "correct": "D",
                "image": "questions/PH1_D.png"
            },
            {
                "question": 11,
                "options": ["4", "5", "6", "7","8"],
                "correct": "E",
                "image": "questions/R1_6.png"
            },
            {
                "question": 12,
                "options": ["Monday", "Tuesday", "Thursday", "Friday","Saturday", "Sunday"],
                "correct": "Friday",
                "image": "questions/R2_Friday.png"
            },
            {
                "question": 13,
                "options": ["A", "B", "C", "D","E","F"],
                "correct": "D",
                "image": "questions/R3_D.png"
            },
            {
                "question": 14,
                "options": ["Lead", "Love", "Loop", "Auras","Abode"],
                "correct": "Love",
                "image": "questions/R4_Love.png"
            },
            {
                "question": 15,
                "options": ["Binding", "Copy", "Page", "Cover","Bookmark"],
                "correct": "Page",
                "image": "questions/R5_Page.png"
            },
            ]

        # Track results
        self.results = []
        self.total_quiz_time = 15 * 60  # 15 minutes
        self.quiz_start_time = time.time()

    def draw_text(self, text, pos, font, color=BLACK):
        lines = text.split('\n')
        y_offset = 0
        for line in lines:
            rendered = font.render(line, True, color)
            self.screen.blit(rendered, (pos[0], pos[1] + y_offset))
            y_offset += rendered.get_height() + 5

    def draw_options(self, offset, options, selected):
        button_width, button_height = 300, 35
        spacing = 10

        y_start = offset + spacing * 2
        x_center = (self.WIDTH - button_width) // 2

        rects = []
        mouse_pos = pygame.mouse.get_pos()

        for idx, val in enumerate(options):
            rect = pygame.Rect(
                x_center,
                y_start + idx * (button_height + spacing),
                button_width,
                button_height)

            is_hovered = rect.collidepoint(mouse_pos)

            if selected == idx:
                color = GREEN
            elif is_hovered:
                color = (255, 165, 0)
            else:
                color = BLUE

            pygame.draw.rect(self.screen, color, rect)
            self.draw_text(val, (rect.x + 10, rect.y + 5), self.SMALL_FONT, WHITE)
            rects.append(rect)
        return rects

    def draw_exit_button(self):
        button_width, button_height = 120, 40
        exit_button = pygame.Rect(
            (self.WIDTH*0.9 - button_width),
            self.HEIGHT*0.9,
            button_width,
            button_height)
        color = RED
        mouse_pos = pygame.mouse.get_pos()
        if exit_button.collidepoint(mouse_pos):
            color = (255, 165, 0)

        pygame.draw.rect(self.screen, color, exit_button, border_radius=2)

        text_surface = self.FONT.render("Exit", True, WHITE)
        text_rect = text_surface.get_rect(center=exit_button.center)
        self.screen.blit(text_surface, text_rect)

        return exit_button

    def draw_timer(self, quiz_start_time, total_quiz_time):
        remaining_time = total_quiz_time - (time.time() - quiz_start_time)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_text = f"Time Left: {minutes:02}:{seconds:02}"
        text_surface = self.SMALL_FONT.render(timer_text, True, RED)
        self.screen.blit(text_surface, text_surface.get_rect(topright=(self.WIDTH - 40, 30)))

    def render_question(self, q, selected):
        self.screen.fill(WHITE)
        offset = 0

        if "image" in q:
            try:
                img = pygame.image.load(q["image"])
                img_rect = img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 120))
                self.screen.blit(img, img_rect)
                offset = img_rect.y + img_rect.height
            except:
                self.draw_text("[Image not found]", (300, 100), self.SMALL_FONT, RED)

        return self.draw_options(offset, q["options"], selected)

    def encouragement_popup(self, sentences: list[str]):
        popup = pygame.Surface((500, 150))
        popup.fill(YELLOW)
        pygame.draw.rect(popup, BLACK, popup.get_rect(), 2)

        # Draw text ON THE POPUP, not on the main screen
        y_offset = 30
        for sentence in sentences:
            text_surface = self.FONT.render(sentence, True, BLACK)
            popup.blit(text_surface, (30, y_offset))
            y_offset += text_surface.get_height() + 10
            self.server.send(sentence)

        # Now blit the full popup to the main screen
        popup_rect = popup.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(popup, popup_rect)

        pygame.display.flip()
        pygame.time.delay(2000)  # show for 2 seconds

    def quiz_loop(self):
        total_quiz_time = 15 * 60  # 15 minutes in seconds
        quiz_start_time = time.time()
        logger.info("Quiz initilising")

        for idx, q in enumerate(self.questions):
            selected = None
            start_time = time.time()
            encouragement_shown = False
            encouragement_level = 0
            answered = False

            while not answered:
                rects = self.render_question(q, selected)
                self.draw_timer(quiz_start_time, total_quiz_time)

                # Global remaining time display
                remaining_time = total_quiz_time - (time.time() - quiz_start_time)
                if remaining_time <= 0:
                    self.show_results()
                    return

                # Per-question timer
                elapsed = time.time() - start_time
                waiting_key = None

                if elapsed >= FAST_RESPONSE_TIME and encouragement_level == 0:
                    waiting_key = "CF"
                    encouragement_level += 1
                elif elapsed >= SLOW_RESPONSE_TIME and encouragement_level == 1:
                    waiting_key = "WF"
                    encouragement_level += 1
                elif elapsed >= INACTIVE_TIME and encouragement_level == 2:
                    waiting_key = "IN"
                    encouragement_level += 1
                if waiting_key is not None and encouragement_level <= 3:
                    self.encouragement_popup(random.choices(ENCOURAGEMENT_MESSAGES[waiting_key]))
                    waiting_key = None

                exit_button = self.draw_exit_button()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if exit_button.collidepoint(event.pos):
                            self.show_results()
                            return

                        for i, rect in enumerate(rects):
                            if rect.collidepoint(pos):
                                selected = i
                                answer_time = time.time() - start_time
                                correct = q["options"][selected] == q["correct"]
                                self.results.append({
                                    "question": q["question"],
                                    "selected": q["options"][selected],
                                    "correct": q["correct"],
                                    "is_correct": correct,
                                    "time_taken": round(answer_time, 2)
                                })
                                answered = True
                                key = None
                                if answer_time <= FAST_RESPONSE_TIME:
                                    key = "CF" if correct else "CS"
                                elif answer_time <= SLOW_RESPONSE_TIME:
                                    key = "WF" if correct else "WS"
                                if key is not None:
                                    self.encouragement_popup(random.choices(ENCOURAGEMENT_MESSAGES[key]))

                pygame.display.flip()

        self.show_results()

    def show_results(self):
        self.save_results()
        self.screen.fill(WHITE)
        quiz_done = self.FONT.render("Quiz Complete!", True, GREEN)
        self.screen.blit(quiz_done, quiz_done.get_rect(center=(self.WIDTH // 2, 100)))

        correct_count = sum(1 for r in self.results if r["is_correct"])
        total_time = sum(r["time_taken"] for r in self.results)
        self.draw_text(f"Correct Answers: {correct_count} / {len(self.questions)}", (250, 200), self.FONT)
        self.draw_text(f"Total Time: {round(total_time, 2)}s", (250, 250), self.FONT)

        running = True

        while running:
            exit_button = self.draw_exit_button()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):  # Check if Exit button was clicked
                        running = False
            pygame.display.flip()
        self.quit()

    def save_results(self):
        folder_path = self.data_directory
        number_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        file_path = os.path.join(folder_path, f"result_{number_files+1}.json")
        with open(file_path, 'w') as json_file:
            json.dump(self.results, json_file, indent=4)

    def quit(self):
        self.server.stop()
        pygame.quit()
