import pygame
import os
import json
import time
from typing import Literal, Any
from loguru import logger
from handler import Server
from enum import IntEnum
import random
from mappings import (
    MESSAGES,
    ENCOURAGEMENT_MESSAGES,
    COMPLIMENT_MESSAGES,
    STREAK_MESSAGES,
    AnswerCondition,
)

WHITE, BLUE, BLACK = (255, 255, 255), (70, 130, 180), (0, 0, 0)
GREEN, RED, YELLOW, ORANGE = (34, 139, 34), (220, 20, 60), (255, 215, 0), (255, 165, 0)


class MessageType(IntEnum):
    HINT = 0
    ENCOURAGEMENT = 1
    COMPLIMENT = 2
    TIMEOUT = 3
    STREAK = 4


def create_data_folder(name):
    os.makedirs(name, exist_ok=True)


def get_participant_id():
    try:
        with open("participants.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0


def increment_participant_id():
    current_id = get_participant_id() + 1
    with open("participants.txt", "w") as file:
        file.write(str(current_id))
    return current_id


class QuizGame:
    ENCOURAGEMENT_TIME = 20
    ENCOURAGEMENT_STEP = 25
    HINT_TIME = 60
    HINT_STEP = 20
    TIME_OUT = 120

    FAST_RESPONSE_TIME = 50

    def __init__(self, mode: Literal["robot", "human"]):
        pygame.init()
        self.mode = mode
        self.current_question: int = 0
        self.encouragement_popup_time: int = self.ENCOURAGEMENT_TIME
        self.encouragement_level: int = 0
        self.hint_popup_time: int = self.HINT_TIME
        self.hint_level: int = 0

        self.data_directory = os.path.join("data", mode)
        create_data_folder(self.data_directory)

        self.server = Server(mode)
        self.server.start()

        self.FONT = pygame.font.SysFont("Arial", 28)
        self.SMALL_FONT = pygame.font.SysFont("Arial", 22)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((800, 750))
        self.WIDTH, self.HEIGHT = self.screen.get_size()
        pygame.display.set_caption("Robot Interaction Quiz")

        self.questions: list[dict[str, Any]] = self.load_questions()
        self.images = self.load_images()

        # Track results
        self.results: list[dict[str, Any]] = []
        self.total_quiz_time = 10 * 60  # 10 minutes
        self.quiz_start_time = time.time()
        self.streak = 0

    def load_questions(self):
        return [
            {
                "question": 1,
                "options": ["4", "8", "10", "12", "14"],
                "correct": "10",
                "image": "questions/ME1.png",
            },
            {
                "question": 2,
                "options": ["54", "81", "162", "216", "729"],
                "correct": "216",
                "image": "questions/MM2.png",
            },
            {
                "question": 3,
                "options": ["A", "B", "C", "D", "E", "F"],
                "correct": "E",
                "image": "questions/PE1_E.png",
            },
            {
                "question": 4,
                "options": ["4", "5", "6", "7", "8"],
                "correct": "6",
                "image": "questions/R1_6.png",
            },
            {
                "question": 5,
                "options": ["Lead", "Love", "Loop", "Auras", "Abode"],
                "correct": "Love",
                "image": "questions/R4_Love.png",
            },
        ]

    def load_images(self):
        images = {}
        for q in self.questions:
            path = q["image"]
            try:
                images[path] = pygame.image.load(path).convert_alpha()
            except pygame.error:
                logger.warning(f"Failed to load {path}")
        return images

    def draw_text(self, text, pos, font, color=BLACK):
        for idx, line in enumerate(text.split("\n")):
            rendered = font.render(line, True, color)
            self.screen.blit(
                rendered, (pos[0], pos[1] + idx * (rendered.get_height() + 5))
            )

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
                button_height,
            )

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
            (self.WIDTH * 0.9 - button_width),
            self.HEIGHT * 0.9,
            button_width,
            button_height,
        )
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
        self.screen.blit(
            text_surface, text_surface.get_rect(topright=(self.WIDTH - 40, 30))
        )

    def render_question(self, q, selected):
        self.screen.fill(WHITE)
        offset = 0
        if q["image"] in self.images:
            img = self.images[q["image"]]

            try:
                img_rect = img.get_rect(
                    center=(self.WIDTH // 2, self.HEIGHT // 2 - 120)
                )
                self.screen.blit(img, img_rect)
                offset = img_rect.y + img_rect.height
            except:
                self.draw_text("[Image not found]", (300, 100), self.SMALL_FONT, RED)

        return self.draw_options(offset, q["options"], selected)

    def encouragement_popup(self, sentence: str, message_type: int):
        self.server.send(f"{self.current_question}:{message_type}:{sentence}")

    def reset_question(self):
        self.encouragement_popup_time = self.ENCOURAGEMENT_TIME
        self.encouragement_level = 0
        self.hint_popup_time = self.HINT_TIME
        self.hint_level = 0

    def show_results(self):
        self.save_results()
        self.screen.fill(WHITE)
        quiz_done = self.FONT.render("Quiz Complete!", True, GREEN)
        self.screen.blit(quiz_done, quiz_done.get_rect(center=(self.WIDTH // 2, 100)))

        correct_count = sum(1 for r in self.results if r["is_correct"])
        total_time = sum(r["time_taken"] for r in self.results)
        self.draw_text(
            f"Correct Answers: {correct_count} / {len(self.questions)}",
            (250, 200),
            self.FONT,
        )
        self.draw_text(f"Total Time: {round(total_time, 2)}s", (250, 250), self.FONT)
        self.wait_for_exit()
        self.quit()

    def wait_for_exit(self):
        running = True
        while running:
            exit_button = self.draw_exit_button()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and exit_button.collidepoint(event.pos)
                ):
                    running = False
            pygame.display.flip()

    def save_results(self):
        folder_path = self.data_directory
        number_files = len(
            [
                f
                for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f))
            ]
        )
        file_path = os.path.join(
            folder_path, f"id_{get_participant_id()}_{number_files+1}.json"
        )
        with open(file_path, "w") as json_file:
            json.dump(self.results, json_file, indent=4)

    def quit(self):
        self.server.stop()
        pygame.quit()

    def handle_question(self, q):
        selected = None
        start_time = time.time()
        answered = False
        self.current_question = q["question"]
        self.reset_question()

        while not answered:
            rects = self.render_question(q, selected)
            remaining_time = self.total_quiz_time - (time.time() - self.quiz_start_time)
            self.draw_timer(self.quiz_start_time, self.total_quiz_time)
            elapsed = time.time() - start_time

            if remaining_time <= 0:
                self.show_results()
                return

            if self.check_time_for_encouragement(elapsed):
                continue
            if self.check_time_for_hint(elapsed):
                continue
            if self.check_time_for_timeout(elapsed):
                self.record_answer(q, None, False, time.time() - start_time)
                answered = True
                self.reset_question()
                time.sleep(6)
                self.quiz_start_time += 6
                continue

            answered, selected = self.handle_user_input(rects, q, start_time)

            pygame.display.flip()

    def check_time_for_encouragement(self, elapsed):
        if elapsed >= self.encouragement_popup_time and elapsed < self.HINT_TIME:
            message = (
                random.choice(ENCOURAGEMENT_MESSAGES)
                if self.mode == "robot"
                else f"{self.current_question}{MessageType.ENCOURAGEMENT}{self.encouragement_level}"
            )
            self.encouragement_popup(message, MessageType.ENCOURAGEMENT)
            self.encouragement_popup_time += self.ENCOURAGEMENT_STEP
            self.encouragement_level += 1
            return True
        return False

    def check_time_for_hint(self, elapsed):
        if self.hint_level >= len(MESSAGES[self.current_question - 1].hints):
            return False
        if elapsed >= self.hint_popup_time:
            message = (
                MESSAGES[self.current_question - 1].hints[self.hint_level]
                if self.mode == "robot"
                else f"{self.current_question}{MessageType.HINT}{self.hint_level}"
            )
            self.encouragement_popup(message, MessageType.HINT)
            self.hint_popup_time += self.HINT_STEP
            self.hint_level += 1
            return True
        return False

    def check_time_for_timeout(self, elapsed):
        if elapsed >= self.TIME_OUT:
            message = (
                MESSAGES[self.current_question - 1].answer
                if self.mode == "robot"
                else f"{self.current_question}{MessageType.TIMEOUT}0"
            )
            self.encouragement_popup(message, MessageType.TIMEOUT)
            return True
        return False

    def handle_user_input(self, rects, q, start_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if any(rect.collidepoint(pos) for rect in rects):
                    idx = [rect.collidepoint(pos) for rect in rects].index(True)
                    answer_time = time.time() - start_time
                    correct = q["options"][idx] == q["correct"]
                    self.record_answer(q, q["options"][idx], correct, answer_time)
                    self.send_feedback_message(correct, answer_time)
                    return True, idx
        return False, None

    def record_answer(self, q, selected, is_correct, time_taken):
        self.results.append(
            {
                "question": q["question"],
                "selected": selected,
                "correct": q["correct"],
                "is_correct": is_correct,
                "time_taken": round(time_taken, 2),
            }
        )
        self.streak = self.streak + 1 if is_correct else 0

    def send_feedback_message(self, correct, answer_time):
        if self.streak >= 3:
            if self.mode == "robot":
                message = STREAK_MESSAGES[self.streak - 3]
            else:
                message = f"0{MessageType.STREAK}{self.streak - 3}"
        else:
            condition = self.determine_condition(correct, answer_time)
            message = (
                random.choice((COMPLIMENT_MESSAGES[condition]))
                if self.mode == "robot"
                else f"{self.current_question}{MessageType.COMPLIMENT}{condition}"
            )
        self.encouragement_popup(message, MessageType.COMPLIMENT)

    def determine_condition(self, correct, answer_time):
        if answer_time <= self.FAST_RESPONSE_TIME:
            return (
                AnswerCondition.FAST_CORRECT
                if correct
                else AnswerCondition.FAST_INCORRECT
            )
        elif answer_time <= self.HINT_TIME:
            return (
                AnswerCondition.SLOW_CORRECT
                if correct
                else AnswerCondition.SLOW_INCORRECT
            )
        else:
            return (
                AnswerCondition.HINT_CORRECT
                if correct and self.mode == "human"
                else AnswerCondition.SLOW_INCORRECT
            )

    def quiz_loop(self):
        logger.info("Quiz starting")
        for q in self.questions:
            self.handle_question(q)
        self.current_question = 6
        self.encouragement_popup("Well done!", MessageType.COMPLIMENT)
        self.show_results()

    @staticmethod
    def landing_page():
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # screen = pygame.display.set_mode((800, 750))
        WIDTH, HEIGHT = screen.get_size()
        FONT = pygame.font.SysFont("Arial", 48)
        SMALL_FONT = pygame.font.SysFont("Arial", 28)
        clock = pygame.time.Clock()

        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
        running = True
        participant_id = get_participant_id()

        while running:
            screen.fill(WHITE)

            title = FONT.render("Welcome to the Experiments", True, BLACK)
            title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            screen.blit(title, title_rect)

            pid_text = SMALL_FONT.render(
                f"Participant ID: {participant_id}", True, BLUE
            )
            pid_rect = pid_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 60))
            screen.blit(pid_text, pid_rect)

            pygame.draw.rect(screen, GREEN, start_button)
            start_text = SMALL_FONT.render("Start", True, WHITE)
            start_rect = start_text.get_rect(center=start_button.center)
            screen.blit(start_text, start_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        new_id = increment_participant_id()
                        return new_id

            pygame.display.flip()
            clock.tick(60)
