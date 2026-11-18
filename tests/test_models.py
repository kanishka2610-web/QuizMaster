from app import db
from app.models import Attempt, Question, Quiz


def test_question_to_dict_excludes_correct_option(app):
    with app.app_context():
        quiz = Quiz(title="Math Quiz")
        db.session.add(quiz)
        db.session.commit()

        question = Question(
            quiz_id=quiz.id,
            text="What is 2 + 2?",
            option_a="1",
            option_b="2",
            option_c="3",
            option_d="4",
            correct_option="D",
        )
        db.session.add(question)
        db.session.commit()

        data = question.to_dict()

        # Acceptance criterion: Question.to_dict does not include correct_option
        assert "correct_option" not in data
        assert data["id"] == question.id
        assert data["text"] == "What is 2 + 2?"
        assert data["option_a"] == "1"
        assert data["option_b"] == "2"
        assert data["option_c"] == "3"
        assert data["option_d"] == "4"
        assert set(data.keys()) == {
            "id",
            "text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
        }


def test_quiz_to_dict(app):
    with app.app_context():
        quiz = Quiz(
            title="Python Basics",
            description="Test your Python knowledge",
            category="Programming",
            difficulty="easy",
        )
        db.session.add(quiz)
        db.session.commit()

        # Acceptance criterion: Quiz.to_dict, including question_count
        data = quiz.to_dict()
        assert data["id"] == quiz.id
        assert data["title"] == "Python Basics"
        assert data["description"] == "Test your Python knowledge"
        assert data["category"] == "Programming"
        assert data["difficulty"] == "easy"
        assert data["question_count"] == 0
        assert data["created_at"] == quiz.created_at.isoformat()
        assert set(data.keys()) == {
            "id",
            "title",
            "description",
            "category",
            "difficulty",
            "question_count",
            "created_at",
        }

        # Add questions to verify question_count updates dynamically
        q1 = Question(
            quiz_id=quiz.id,
            text="Which keyword defines a function?",
            option_a="def",
            option_b="func",
            option_c="function",
            option_d="define",
            correct_option="A",
        )
        q2 = Question(
            quiz_id=quiz.id,
            text="What does len() return?",
            option_a="Length",
            option_b="Type",
            option_c="Index",
            option_d="Value",
            correct_option="A",
        )
        db.session.add_all([q1, q2])
        db.session.commit()

        updated_data = quiz.to_dict()
        assert updated_data["question_count"] == 2


def test_quiz_to_dict_defaults(app):
    with app.app_context():
        quiz = Quiz(title="Minimal Quiz")
        db.session.add(quiz)
        db.session.commit()

        data = quiz.to_dict()
        assert data["title"] == "Minimal Quiz"
        assert data["description"] == ""
        assert data["category"] == "General"
        assert data["difficulty"] == "easy"
        assert data["question_count"] == 0


def test_attempt_to_dict(app):
    with app.app_context():
        quiz = Quiz(title="Science Quiz")
        db.session.add(quiz)
        db.session.commit()

        attempt = Attempt(
            quiz_id=quiz.id,
            player_name="Asha",
            score=3,
            total_questions=5,
            time_taken_seconds=45,
        )
        db.session.add(attempt)
        db.session.commit()

        # Acceptance criterion: Attempt.to_dict
        data = attempt.to_dict()
        assert data["id"] == attempt.id
        assert data["quiz_id"] == quiz.id
        assert data["quiz_title"] == "Science Quiz"
        assert data["player_name"] == "Asha"
        assert data["score"] == 3
        assert data["total_questions"] == 5
        assert data["time_taken_seconds"] == 45
        assert data["created_at"] == attempt.created_at.isoformat()
        assert set(data.keys()) == {
            "id",
            "quiz_id",
            "quiz_title",
            "player_name",
            "score",
            "total_questions",
            "time_taken_seconds",
            "created_at",
        }

