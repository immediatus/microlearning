# Technical Architecture

## System Overview

### High-Level Architecture
```
[Student Mobile App] ← API → [FastAPI Backend] ← AI → [Content Generation Pipeline]
       ↓                           ↓                         ↓
[Local Storage]              [PostgreSQL]              [AI Services]
[Video Cache]                [Redis Cache]             [Video Storage]
```

## Database Design

### Core Tables

#### Students Table
```sql
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    age_group VARCHAR(10) NOT NULL,
    learning_preferences JSONB,
    streak_count INTEGER DEFAULT 0,
    total_videos_watched INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active TIMESTAMP DEFAULT NOW()
);
```

#### Learning Videos Table
```sql
CREATE TABLE learning_videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    script_content TEXT NOT NULL,
    video_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    duration_seconds INTEGER NOT NULL,
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 10),
    age_groups INTEGER[] NOT NULL,
    quiz_questions JSONB NOT NULL,
    popularity_score FLOAT DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    completion_rate FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'draft'
);
```

#### Quiz Responses Table
```sql
CREATE TABLE quiz_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    video_id UUID REFERENCES learning_videos(id),
    question_index INTEGER NOT NULL,
    user_answer BOOLEAN NOT NULL,
    correct_answer BOOLEAN NOT NULL,
    response_time_ms INTEGER NOT NULL,
    is_correct BOOLEAN GENERATED ALWAYS AS (user_answer = correct_answer) STORED,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Content Projects Table (Creator)
```sql
CREATE TABLE content_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creator_id UUID REFERENCES creators(id),
    concept_prompt TEXT NOT NULL,
    age_group VARCHAR(20) NOT NULL,
    status VARCHAR(50) DEFAULT 'generating',
    ai_generated_script TEXT,
    visual_config JSONB,
    qa_results JSONB,
    approval_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    approved_at TIMESTAMP,
    published_video_id UUID REFERENCES learning_videos(id)
);
```

## API Design

### Student Endpoints

#### Get Personalized Feed
```python
@app.get("/api/student/feed/{user_id}")
async def get_learning_feed(
    user_id: str, 
    page: int = 0, 
    age_group: str = None
) -> List[VideoCard]:
    """
    Returns personalized video feed based on:
    - User's learning history
    - Age-appropriate content
    - Spaced repetition algorithm
    - Popularity and engagement scores
    """
```

#### Submit Quiz Response
```python
@app.post("/api/student/quiz-response")
async def submit_quiz_response(response: QuizResponse) -> QuizResult:
    """
    Processes quiz answer and returns:
    - Immediate feedback (correct/incorrect)
    - Next video recommendation
    - Updated learning analytics
    """
```

#### Get Learning Progress
```python
@app.get("/api/student/progress/{user_id}")
async def get_progress(user_id: str) -> LearningProgress:
    """
    Returns student progress including:
    - Topics mastered
    - Current streak
    - Achievements unlocked
    - Recommended next topics
    """
```

### Creator Endpoints

#### Generate Content
```python
@app.post("/api/creator/generate-content")
async def generate_content(request: ContentRequest) -> GenerationTask:
    """
    Starts AI content generation pipeline:
    - Script generation
    - Visual asset creation
    - Voice synthesis
    - Video compilation
    """
```

#### Review Generated Content
```python
@app.get("/api/creator/review/{project_id}")
async def get_content_review(project_id: str) -> ContentReview:
    """
    Returns generated content for review:
    - Script text
    - Video preview
    - Quality assurance results
    - Suggested improvements
    """
```

## AI Content Generation Pipeline

### LangGraph Workflow
```python
class ContentGenerationState(TypedDict):
    concept: str
    age_group: str
    script: str
    visual_assets: List[Asset]
    audio_tracks: List[AudioTrack]
    qa_results: QAResults
    approval_status: str

def create_content_workflow():
    workflow = StateGraph(ContentGenerationState)
    
    # Define processing nodes
    workflow.add_node("script_generator", generate_educational_script)
    workflow.add_node("visual_creator", create_visual_assets)
    workflow.add_node("voice_synthesizer", generate_voiceover)
    workflow.add_node("video_compositor", compile_final_video)
    workflow.add_node("qa_validator", run_quality_checks)
    workflow.add_node("human_reviewer", await_human_approval)
    
    # Define workflow edges
    workflow.add_edge("script_generator", "visual_creator")
    workflow.add_edge("script_generator", "voice_synthesizer")
    workflow.add_edge(["visual_creator", "voice_synthesizer"], "video_compositor")
    workflow.add_edge("video_compositor", "qa_validator")
    workflow.add_edge("qa_validator", "human_reviewer")
    
    return workflow.compile()
```

### AI Service Integration
```python
class AIServiceManager:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.elevenlabs_client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        self.video_generator = VideoGenerationAPI()
    
    async def generate_script(self, concept: str, age_group: str) -> str:
        prompt = f"""
        Create an educational script about {concept} for {age_group} year olds.
        
        Requirements:
        - Duration: 45-90 seconds when narrated
        - Engaging hook in first 5 seconds
        - Clear learning objective
        - Age-appropriate language
        - Include 2-3 interactive moments for quizzes
        
        Format: Return only the script text, no additional formatting.
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    async def generate_quiz_questions(self, script: str) -> List[QuizQuestion]:
        prompt = f"""
        Based on this educational script, create 3 binary (yes/no) quiz questions:
        
        Script: {script}
        
        Requirements:
        - Questions test key concepts from the script
        - Appropriate for quick mobile interaction
        - Clear, unambiguous answers
        - Engaging but not tricky
        
        Return as JSON array with question text and correct answer.
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.choices[0].message.content)
```

## Performance Optimizations

### Video Delivery
```python
class VideoOptimization:
    # CDN Configuration
    cdn_config = {
        "primary": "Cloudflare Stream",
        "fallback": "AWS CloudFront",
        "adaptive_bitrate": True,
        "formats": ["1080p", "720p", "480p"],
        "preload_strategy": "next_3_videos"
    }
    
    # Caching Strategy
    cache_config = {
        "video_metadata": "Redis - 1 hour TTL",
        "user_feed": "Redis - 5 minutes TTL", 
        "video_files": "Local device - 50MB limit",
        "offline_mode": "Download up to 20 videos"
    }
```

### Database Optimization
```sql
-- Indexes for performance
CREATE INDEX idx_students_age_group ON students(age_group);
CREATE INDEX idx_videos_topic_age ON learning_videos(topic, age_groups);
CREATE INDEX idx_quiz_responses_student_time ON quiz_responses(student_id, created_at);
CREATE INDEX idx_videos_popularity ON learning_videos(popularity_score DESC);

-- Partitioning for scale
CREATE TABLE quiz_responses_2025 PARTITION OF quiz_responses 
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

## Security & Privacy

### Data Protection
- **Student Privacy**: No PII collection beyond username
- **Content Security**: All AI-generated content passes safety filters
- **API Security**: JWT tokens with short expiration
- **Data Encryption**: AES-256 for sensitive data at rest

### Content Moderation
```python
class ContentModerator:
    def __init__(self):
        self.safety_filters = [
            "inappropriate_content",
            "factual_accuracy", 
            "age_appropriateness",
            "educational_value"
        ]
    
    async def validate_content(self, content: dict) -> ModerationResult:
        results = {}
        for filter_name in self.safety_filters:
            filter_func = getattr(self, f"check_{filter_name}")
            results[filter_name] = await filter_func(content)
        
        return ModerationResult(
            passed=all(results.values()),
            details=results
        )
```

## Monitoring & Analytics

### Key Metrics
- **Performance**: API response times, video load times
- **Engagement**: Session duration, completion rates, quiz accuracy
- **Content**: Video popularity, creator efficiency
- **System Health**: Error rates, resource utilization

### Analytics Pipeline
```python
class AnalyticsTracker:
    def track_video_view(self, user_id: str, video_id: str, duration: int):
        event = {
            "event_type": "video_view",
            "user_id": user_id,
            "video_id": video_id,
            "duration_seconds": duration,
            "timestamp": datetime.utcnow()
        }
        self.amplitude_client.track(event)
    
    def track_quiz_response(self, user_id: str, response: QuizResponse):
        event = {
            "event_type": "quiz_response",
            "user_id": user_id,
            "video_id": response.video_id,
            "correct": response.is_correct,
            "response_time_ms": response.response_time,
            "timestamp": datetime.utcnow()
        }
        self.amplitude_client.track(event)
```

## Deployment Architecture

### Production Environment
```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    image: microlearning/api:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/microlearning
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=microlearning
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
  
  celery:
    image: microlearning/api:latest
    command: celery -A app.celery worker --loglevel=info
    depends_on:
      - redis
      - db
```

### Kubernetes Scaling
```yaml
# k8s-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: microlearning-api
spec:
  replicas: 5
  selector:
    matchLabels:
      app: microlearning-api
  template:
    spec:
      containers:
      - name: api
        image: microlearning/api:latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```