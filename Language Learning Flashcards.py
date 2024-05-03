import json
import random
from datetime import datetime

class FlashcardManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.flashcards = {}
        self.load_flashcards()

    def load_flashcards(self):
        try:
            with open(self.file_path, 'r') as file:
                self.flashcards = json.load(file)
        except FileNotFoundError:
            self.flashcards = {}

    def save_flashcards(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.flashcards, file, indent=4)

    def get_flashcard_categories(self):
        return list(self.flashcards.keys())

    def get_flashcards_by_category(self, category):
        return self.flashcards.get(category, [])

    def add_flashcard(self, category, question, answer):
        if category not in self.flashcards:
            self.flashcards[category] = []
        self.flashcards[category].append({"question": question, "answer": answer})
        self.save_flashcards()

    def remove_flashcard(self, category, index):
        if category in self.flashcards and 0 <= index < len(self.flashcards[category]):
            del self.flashcards[category][index]
            self.save_flashcards()

class SpacedRepetition:
    def __init__(self, flashcard_manager):
        self.flashcard_manager = flashcard_manager
        self.review_log = []

    def schedule_reviews(self, category):
        flashcards = self.flashcard_manager.get_flashcards_by_category(category)
        for flashcard in flashcards:
            self.review_log.append({"flashcard": flashcard, "review_date": datetime.now()})

    def get_next_flashcard(self):
        if self.review_log:
            next_flashcard = min(self.review_log, key=lambda x: x["review_date"])
            self.review_log.remove(next_flashcard)
            return next_flashcard["flashcard"]
        return None

    def update_review_status(self, flashcard, success):
        for entry in self.review_log:
            if entry["flashcard"] == flashcard:
                if success:
                    entry["review_date"] = datetime.now() + timedelta(days=1)
                else:
                    entry["review_date"] = datetime.now() + timedelta(days=3)
                break

flashcard_manager = FlashcardManager("flashcards.json")
spaced_repetition = SpacedRepetition(flashcard_manager)

# Example usage:
flashcard_manager.add_flashcard("Vocabulary", "Dog", "Perro")
flashcard_manager.add_flashcard("Vocabulary", "Cat", "Gato")
flashcard_manager.add_flashcard("Phrases", "Hello", "Hola")
flashcard_manager.add_flashcard("Phrases", "Goodbye", "Adiós")

spaced_repetition.schedule_reviews("Vocabulary")
next_flashcard = spaced_repetition.get_next_flashcard()
if next_flashcard:
    print("Next flashcard to review:")
    print("Question:", next_flashcard["question"])
    user_input = input("Enter answer: ")
    if user_input.strip().lower() == next_flashcard["answer"].lower():
        print("Correct! Review scheduled for tomorrow.")
        spaced_repetition.update_review_status(next_flashcard, success=True)
    else:
        print("Incorrect. Review scheduled for three days later.")
        spaced_repetition.update_review_status(next_flashcard, success=False)
else:
    print("No flashcards to review at the moment.")
