from pydantic import BaseModel
from enum import IntEnum


class AnswerCondition(IntEnum):
    FAST_CORRECT = 0
    SLOW_CORRECT = 1
    FAST_INCORRECT = 2
    SLOW_INCORRECT = 3
    HINT_CORRECT = 4


STREAK_MESSAGES: tuple[str, ...] = (
    "You're on fire today!",
    "Correct again! You're unstoppable!",
    "Right again! You're in the zone!",
)

ENCOURAGEMENT_MESSAGES: tuple[str, ...] = (
    "You can do this!",
    "Take your time, no rush",
    "Almost there!",
    "You got this!",
    "Believe in yourself. You are smarter than you think!",
    "Stay confident and don’t overthink",
    "Stay calm and focused!",
)

COMPLIMENT_MESSAGES: dict[int, tuple[str, ...]] = {
    # Fast and correct
    AnswerCondition.FAST_CORRECT: (
        "Outstanding work!",
        "You're on fire!",
        "Brilliant thinking!",
        "That was impressive!",
        "You nailed it!",
    ),
    # Slow and correct
    AnswerCondition.SLOW_CORRECT: (
        "Keep going, you're making progress.",
        "You're doing great, keep it up.",
        "That was a tough one, but you got it!",
    ),
    # Fast and incorrect
    AnswerCondition.FAST_INCORRECT: (
        "No worries, let's try again.",
        "Good effort, let's take another shot at it.",
        "Mistakes help us learn, let's keep going!",
        "Almost there, let's give it another go.",
    ),
    # Slow and incorrect
    AnswerCondition.SLOW_INCORRECT: (
        "That was a tricky one, but you'll get the next.",
        "You're learning, and that's what matters.",
    ),
}


class Question(BaseModel):
    encouragements_human: tuple[str, ...]
    compliments_human: dict[int, str]
    hints: tuple[str, ...]
    answer: str | None = None


Question1 = Question(
    encouragements_human=(
        "You’re doing great. Sometimes these puzzles just need a shift in perspective. Try checking how the numbers are changing step by step.",
        "Don’t give up! You’re close!.",
    ),
    compliments_human={
        AnswerCondition.FAST_CORRECT: "Whoa! That was super fast—high five!",
        AnswerCondition.SLOW_CORRECT: "Great work! You really spotted that pattern.",
        AnswerCondition.FAST_INCORRECT: "That was fast! Even though it’s not quite right, you’re clearly engaged. Let’s give it another go.",
        AnswerCondition.SLOW_INCORRECT: "That one was tough, but you didn’t quit—that matters.",
        AnswerCondition.HINT_CORRECT: "You used that hint like a pro! Nice teamwork.",
    },
    hints=(
        "Look at the difference between each pair of numbers going down the ladder. What do you notice?",
        "Seems like the difference is increasing each time. Is there a pattern in how much is subtracted?",
        "If you just subtracted 4 to get to 15, what happens if you subtract 5 next?",
    ),
    answer="The answer is 10. The pattern is subtracting 4, then 5, then 6, and so on.",
)

Question2 = Question(
    encouragements_human=(
        "Take your time, but remember — there’s a pattern when you change the size of all sides in a cube. You’ve got this!",
        "You’re doing great! Let’s break it down: if one side doubles, what happens to the whole volume? Don’t give up!",
    ),
    compliments_human={
        AnswerCondition.FAST_CORRECT: "Excellent work — you didn’t just rush, you understood it!",
        AnswerCondition.SLOW_CORRECT: "Great perseverance! You cracked it with careful reasoning.",
        AnswerCondition.FAST_INCORRECT: "Speed shows confidence! Let’s slow down next time and think it through.",
        AnswerCondition.SLOW_INCORRECT: "I can tell you really thought about it. Don’t worry — every try builds understanding.",
        AnswerCondition.HINT_CORRECT: "Nice job applying the clues — we got there together!",
    },
    hints=(
        "To find the volume of a cube, just imagine taking the length of one side and multiplying it by itself, and then doing that one more time.",
        "The cube’s volume is 27, so think: what number, when you multiply it by itself three times, gives you 27? That number is the length of one side.",
        "Now, if we double that side length, we’re making the cube much bigger in every direction. When that happens, the volume doesn’t just double — it grows way more. Try thinking how much bigger it gets when every side is twice as long.",
    ),
    answer="The answer is 216. When you double the side length of a cube, the volume increases by a factor of 2^3 = 8. So, 27 * 8 = 216.",
)

Question3 = Question(
    encouragements_human=(
        "Nice progress! Look closely — each row follows a rule. Focus on one row at a time.",
        "Almost there! Think about what the shapes have in common across each row and column. Keep your eyes sharp!",
    ),
    compliments_human={
        AnswerCondition.FAST_CORRECT: "That was fast and right on target! — impressive!",
        AnswerCondition.SLOW_CORRECT: "Thoughtful work leads to solid results. Nicely done!",
        AnswerCondition.FAST_INCORRECT: "Quick thinking is a great sign — now we just need to match it with careful checking.",
        AnswerCondition.SLOW_INCORRECT: "Even without the right answer, your persistence is impressive. Let’s learn from it and keep moving!",
        AnswerCondition.HINT_CORRECT: "You listened, adjusted, and got it right. That’s real problem-solving.",
    },
    hints=(
        "Each row seems to follow a pattern where shapes either change or stay the same in a certain way. Start by describing out loud what’s happening from left to right in the first row.",
        "In the second row, focus on the number and placement of dots. Notice how they relate to the shape around them.",
        "The last row might combine what happens in the top two rows. So ask yourself: how are the shapes and inner lines connected? Which option fits the same style?",
    ),
    answer="The answer is E. In each row, the right figure combines the rotated version of middle figure with the left figure. So, the final figure combines the circle and the vertical line — which matches option E",
)

Question4 = Question(
    encouragements_human=(
        "This one’s about finding a pattern. Try listing or visualizing who shakes hands with who!",
        "Almost there! Try not to count duplicates. Each handshake only happens once.",
    ),
    compliments_human={
        AnswerCondition.FAST_CORRECT: "That was fast and right on target! — impressive!",
        AnswerCondition.SLOW_CORRECT: "Thoughtful work leads to solid results. Nicely done!",
        AnswerCondition.FAST_INCORRECT: "Quick thinking is a great sign — now we just need to match it with careful checking.",
        AnswerCondition.SLOW_INCORRECT: "Even without the right answer, your persistence is impressive. Let’s learn from it and keep moving!",
        AnswerCondition.HINT_CORRECT: "You listened, adjusted, and got it right. That’s real problem-solving.",
    },
    hints=(
        "Start by imagining four people. The first person shakes hands with three others. That’s three handshakes so far.",
        "Now, the second person doesn’t shake hands with the first again—only with the remaining two.",
        "Keep going like that: each person shakes hands only with those they haven’t already. That keeps you from counting the same one twice.",
    ),
    answer="The answer is 6. The first person shakes hands with 3 others, the second with 2, and the last one with 1. So, 3 + 2 + 1 = 6.",
)

Question5 = Question(
    encouragements_human=(
        "Take your time, you’re doing great! Think carefully about patterns between numbers and words.",
        "You’ve already solved four questions — don’t give up now! Focus on breaking it into parts.",
    ),
    compliments_human={
        AnswerCondition.FAST_CORRECT: "Impressive speed and accuracy — you should feel proud of how fast you reasoned that out!",
        AnswerCondition.SLOW_CORRECT: "Well done! Careful thinking always pays off, and you showed great focus here.",
        AnswerCondition.FAST_INCORRECT: "Quick thinking is valuable — just combine it with a double-check and you’ll master this.",
        AnswerCondition.SLOW_INCORRECT: "It’s okay to miss sometimes — what counts is how carefully you worked through it.",
        AnswerCondition.HINT_CORRECT: "Fantastic! You worked hard, used the hints well, and got to the correct answer — that’s real learning.",
    },
    hints=(
        "Look at how the numbers 16, 5, 1, 3, 5 might map to letters using A=1, B=2, C=3. Does that spell something close to “peace”?",
        "Try applying the same number-to-letter pattern to 12, 15, 22, 5. What word could that create?",
        "If the direct mapping doesn’t form a clear word, think about synonyms or related words to “peace” — maybe “calm,” “quiet,” or “love.” See which fits.",
    ),
    answer="The answer is LOVE. The numbers 12, 15, 22, and 5 correspond to the letters L, O, V, and E respectively. The first set of numbers (16, 5, 1, 3, 5) spells PEACE.",
)

MESSAGES: tuple[Question, ...] = (
    Question1,
    Question2,
    Question3,
    Question4,
    Question5,
)
