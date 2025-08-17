import pytest
import uuid
from decimal import Decimal
from datetime import datetime

from sqlalchemy.future import select

from app.models.creator import Creator
from app.models.student import Student, StudentSession, StudentPreference
from app.models.content import ContentProject, LearningVideo, ContentStatus
from app.models.quiz import Quiz, QuizResponse
from app.models.billing import CreatorBudget, AIServiceCost, ApprovalRequest, ApprovalStatus
from app.models.analytics import AnalyticsEvent

@pytest.mark.asyncio
async def test_create_creator(db_session):
    """Test creating a Creator and verifying it's stored correctly."""
    creator = Creator(
        username="test_creator",
        email="creator@test.com",
        hashed_password="hashed_password_example"
    )
    db_session.add(creator)
    await db_session.commit()
    await db_session.refresh(creator)

    assert creator.id is not None
    assert creator.username == "test_creator"

    retrieved_creator = await db_session.get(Creator, creator.id)
    assert retrieved_creator is not None
    assert retrieved_creator.email == "creator@test.com"

@pytest.mark.asyncio
async def test_create_student_and_related_models(db_session):
    """Test creating a Student and their related preference and session models."""
    student = Student(
        username="test_student",
        age_group="12-15",
    )
    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    assert student.id is not None
    assert student.username == "test_student"

    preference = StudentPreference(student_id=student.id, dark_mode=True)
    session = StudentSession(student_id=student.id)

    db_session.add_all([preference, session])
    await db_session.commit()

    retrieved_student = await db_session.get(Student, student.id)
    # Note: relationships are not automatically refreshed, so we can't directly check them
    # without a fresh query. We will test relationships explicitly.

    retrieved_pref = await db_session.execute(select(StudentPreference).filter_by(student_id=student.id))
    assert retrieved_pref.scalar_one().dark_mode is True

@pytest.mark.asyncio
async def test_full_content_creation_flow(db_session):
    """Test the full relationship chain from creator to quiz response."""
    # 1. Create Creator and Student
    creator = Creator(username="flow_creator", email="flow@test.com", hashed_password="pw")
    student = Student(username="flow_student", age_group="12-15")
    db_session.add_all([creator, student])
    await db_session.commit()

    # 2. Create Content Project
    project = ContentProject(
        creator_id=creator.id,
        concept_prompt="Testing relationships",
        age_group="12-15",
        subject_area="Software Engineering"
    )
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)

    assert project.creator_id == creator.id

    # 3. Create Learning Video from the project
    video = LearningVideo(
        creator_id=creator.id,
        content_project_id=project.id,
        title="Test Video",
        topic="SQLAlchemy",
        concept="A video about testing SQLAlchemy relationships.",
        script_content="...",
        learning_objectives=["Objective 1"],
        video_url="http://example.com/video.mp4",
        duration_seconds=90,
        difficulty_level=5,
        age_groups=["12-15"],
        subject_area="Software Engineering",
        quiz_questions=[{"q": "Is this a test?", "a": "Yes"}],
        status=ContentStatus.PUBLISHED
    )
    db_session.add(video)
    await db_session.commit()
    await db_session.refresh(video)

    assert video.content_project_id == project.id
    assert video.creator_id == creator.id

    # 4. Create a Quiz for the video
    quiz = Quiz(
        video_id=video.id,
        question="Does this relationship work?",
        options={"a": "Yes", "b": "No"},
        correct_answer="a",
        order=1
    )
    db_session.add(quiz)
    await db_session.commit()
    await db_session.refresh(quiz)

    assert quiz.video_id == video.id

    # 5. Student responds to the quiz
    response = QuizResponse(
        student_id=student.id,
        quiz_id=quiz.id,
        video_id=video.id,
        submitted_answer="a",
        is_correct=True
    )
    db_session.add(response)
    await db_session.commit()
    await db_session.refresh(response)

    assert response.student_id == student.id
    assert response.quiz_id == quiz.id

    # 6. Test relationships by querying
    await db_session.refresh(creator)
    await db_session.refresh(student)
    await db_session.refresh(video)

    # Query and check relationships
    test_creator = await db_session.get(Creator, creator.id)
    assert len(test_creator.content_projects) == 1
    assert test_creator.content_projects[0].concept_prompt == "Testing relationships"

    test_video = await db_session.get(LearningVideo, video.id)
    assert test_video.content_project.id == project.id
    assert len(test_video.quizzes) == 1

    test_student = await db_session.get(Student, student.id)
    assert len(test_student.quiz_responses) == 1
    assert test_student.quiz_responses[0].is_correct is True

@pytest.mark.asyncio
async def test_billing_and_analytics_relationships(db_session):
    """Test relationships for billing and analytics models."""
    creator = Creator(username="billing_creator", email="billing@test.com", hashed_password="pw")
    db_session.add(creator)
    await db_session.commit()

    budget = CreatorBudget(
        creator_id=creator.id,
        daily_limit=Decimal("100.00"),
        monthly_limit=Decimal("1000.00"),
        daily_reset_at=datetime.utcnow(),
        weekly_reset_at=datetime.utcnow(),
        monthly_reset_at=datetime.utcnow()
    )
    db_session.add(budget)
    await db_session.commit()

    cost_entry = AIServiceCost(
        creator_id=creator.id,
        service_type="openai_gpt",
        operation_type="text_generation",
        estimated_cost=Decimal("0.50"),
        cost_tier="low",
        request_parameters={"prompt": "hello"},
        content_type="script"
    )
    db_session.add(cost_entry)
    await db_session.commit()

    approval = ApprovalRequest(
        cost_entry_id=cost_entry.id,
        creator_id=creator.id,
        operation_description="Generate script",
        estimated_cost=Decimal("0.50"),
        cost_tier="low",
        status=ApprovalStatus.APPROVED,
        expires_at=datetime.utcnow()
    )
    db_session.add(approval)
    await db_session.commit()

    analytics_event = AnalyticsEvent(
        event_type="creator_login",
        creator_id=creator.id,
        payload={"ip_address": "127.0.0.1"}
    )
    db_session.add(analytics_event)
    await db_session.commit()

    # Test relationships
    await db_session.refresh(creator)
    assert creator.budget.daily_limit == Decimal("100.00")
    assert len(creator.ai_service_costs) == 1
    assert len(creator.approval_requests) == 1
    assert len(creator.analytics_events) == 1

    await db_session.refresh(cost_entry)
    assert cost_entry.creator.username == "billing_creator"
    assert cost_entry.approval_request.status == ApprovalStatus.APPROVED
