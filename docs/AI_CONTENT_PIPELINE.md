# AI Content Generation Pipeline

## Overview

The AI content pipeline transforms educational concepts into engaging 45-90 second video lessons with interactive quizzes, optimized for 12-15 year old students.

## Pipeline Architecture

### High-Level Flow
```
User Concept → Script Generation → Visual Assets → Voice Synthesis → Video Composition → QA Validation → Publishing
```

### LangGraph Workflow Definition
```python
from langraph import StateGraph, END
from typing import TypedDict, List

class ContentGenerationState(TypedDict):
    # Input
    concept: str
    age_group: str
    difficulty_level: int
    
    # Generated Content
    learning_objectives: List[str]
    script: str
    visual_storyboard: List[dict]
    voice_config: dict
    background_music: str
    quiz_questions: List[dict]
    
    # Processing Status
    current_step: str
    errors: List[str]
    qa_results: dict
    approval_status: str
    
    # Output
    video_url: str
    thumbnail_url: str
    metadata: dict

def create_content_pipeline():
    workflow = StateGraph(ContentGenerationState)
    
    # Content Generation Nodes
    workflow.add_node("objectives_generator", generate_learning_objectives)
    workflow.add_node("script_writer", generate_educational_script)
    workflow.add_node("visual_designer", create_visual_storyboard)
    workflow.add_node("voice_synthesizer", generate_voice_narration)
    workflow.add_node("music_composer", select_background_music)
    workflow.add_node("quiz_creator", generate_quiz_questions)
    workflow.add_node("video_compositor", compose_final_video)
    workflow.add_node("qa_validator", run_quality_assurance)
    workflow.add_node("publisher", publish_content)
    
    # Define workflow paths
    workflow.add_edge("objectives_generator", "script_writer")
    workflow.add_edge("script_writer", "visual_designer")
    workflow.add_edge("script_writer", "voice_synthesizer")
    workflow.add_edge("script_writer", "quiz_creator")
    workflow.add_edge(["visual_designer", "voice_synthesizer", "music_composer"], "video_compositor")
    workflow.add_edge("video_compositor", "qa_validator")
    workflow.add_edge("qa_validator", "publisher")
    
    # Error handling and retry logic
    workflow.add_conditional_edges(
        "qa_validator",
        should_retry_generation,
        {
            "retry": "script_writer",
            "approve": "publisher",
            "manual_review": END
        }
    )
    
    workflow.set_entry_point("objectives_generator")
    return workflow.compile()
```

## Content Generation Nodes

### 1. Learning Objectives Generator
```python
async def generate_learning_objectives(state: ContentGenerationState):
    """Generate clear, measurable learning objectives for the concept."""
    
    prompt = f"""
    Create 2-3 specific learning objectives for teaching {state['concept']} to {state['age_group']} year olds.
    
    Guidelines:
    - Use action verbs (explain, identify, demonstrate, calculate)
    - Be specific and measurable
    - Age-appropriate complexity
    - Achievable in 60-90 seconds
    
    Example format:
    - Students will be able to explain why ice floats on water
    - Students will identify the key factors that affect density
    
    Return as JSON array of objective strings.
    """
    
    response = await openai_client.chat.completions.create(
        model="gpt-4",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    objectives = json.loads(response.choices[0].message.content)
    return {"learning_objectives": objectives["objectives"]}
```

### 2. Educational Script Writer
```python
async def generate_educational_script(state: ContentGenerationState):
    """Generate engaging educational script optimized for video format."""
    
    objectives_text = "\n".join(state["learning_objectives"])
    
    prompt = f"""
    Write an educational script for {state['concept']} targeting {state['age_group']} year olds.
    
    Learning Objectives:
    {objectives_text}
    
    Script Requirements:
    - Duration: 60-90 seconds when narrated (approximately 150-225 words)
    - Hook: Start with an intriguing question or surprising fact
    - Structure: Introduction → Explanation → Real-world example → Conclusion
    - Language: Age-appropriate, conversational tone
    - Visual cues: Include [VISUAL: description] markers for animation opportunities
    - Engagement: Include moments for viewer interaction
    
    Format:
    Return the script with clear paragraphs and visual cue markers.
    """
    
    response = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    script = response.choices[0].message.content
    
    # Extract visual cues for storyboard generation
    visual_cues = extract_visual_cues(script)
    
    return {
        "script": script,
        "visual_cues": visual_cues
    }

def extract_visual_cues(script: str) -> List[dict]:
    """Extract [VISUAL: ...] markers from script for storyboard."""
    import re
    
    pattern = r'\[VISUAL: ([^\]]+)\]'
    matches = re.findall(pattern, script)
    
    visual_cues = []
    for i, description in enumerate(matches):
        visual_cues.append({
            "sequence": i + 1,
            "description": description,
            "timestamp": estimate_timestamp(script, i),
            "duration": 3.0  # Default 3 seconds per visual
        })
    
    return visual_cues
```

### 3. Visual Storyboard Creator
```python
async def create_visual_storyboard(state: ContentGenerationState):
    """Generate visual assets and storyboard for the video."""
    
    script = state["script"]
    visual_cues = state.get("visual_cues", [])
    
    storyboard = []
    
    for cue in visual_cues:
        # Generate image prompt for DALL-E
        image_prompt = await generate_image_prompt(cue["description"], state["age_group"])
        
        # Create image with DALL-E
        image_response = await openai_client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1792",  # Vertical format for mobile
            quality="standard",
            n=1
        )
        
        # Generate animation suggestions
        animation_type = suggest_animation_type(cue["description"])
        
        storyboard_item = {
            "sequence": cue["sequence"],
            "timestamp": cue["timestamp"],
            "duration": cue["duration"],
            "image_url": image_response.data[0].url,
            "animation_type": animation_type,
            "description": cue["description"]
        }
        
        storyboard.append(storyboard_item)
    
    return {"visual_storyboard": storyboard}

async def generate_image_prompt(description: str, age_group: str) -> str:
    """Convert visual description to DALL-E prompt."""
    
    prompt = f"""
    Convert this educational visual description into a DALL-E prompt:
    "{description}"
    
    Requirements:
    - Educational illustration style suitable for {age_group} year olds
    - Clean, colorful, engaging visuals
    - Vertical 9:16 aspect ratio orientation
    - High contrast for mobile viewing
    - Scientific accuracy
    
    Return only the DALL-E prompt.
    """
    
    response = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    
    return response.choices[0].message.content

def suggest_animation_type(description: str) -> str:
    """Suggest appropriate animation type based on visual description."""
    
    animation_map = {
        "molecule": "particle_animation",
        "flow": "motion_path",
        "cycle": "circular_animation", 
        "growth": "scale_animation",
        "comparison": "side_by_side",
        "process": "step_by_step",
        "structure": "build_animation"
    }
    
    for keyword, animation in animation_map.items():
        if keyword.lower() in description.lower():
            return animation
    
    return "fade_in_out"  # Default animation
```

### 4. Voice Synthesis
```python
async def generate_voice_narration(state: ContentGenerationState):
    """Generate natural voice narration using ElevenLabs."""
    
    script = state["script"]
    age_group = state["age_group"]
    
    # Select appropriate voice based on age group
    voice_config = select_voice_for_age_group(age_group)
    
    # Clean script for narration (remove visual cues)
    narration_text = clean_script_for_narration(script)
    
    # Generate voice with ElevenLabs
    audio_response = await elevenlabs_client.generate(
        text=narration_text,
        voice=voice_config["voice_id"],
        model="eleven_multilingual_v2",
        voice_settings={
            "stability": voice_config["stability"],
            "similarity_boost": voice_config["similarity_boost"],
            "style": voice_config["style"]
        }
    )
    
    # Upload audio to storage
    audio_url = await upload_audio_file(audio_response)
    
    return {
        "voice_config": voice_config,
        "narration_url": audio_url,
        "narration_duration": estimate_audio_duration(narration_text)
    }

def select_voice_for_age_group(age_group: str) -> dict:
    """Select appropriate voice characteristics for age group."""
    
    voice_configs = {
        "12-15": {
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel - clear, friendly
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "description": "Clear, engaging, slightly energetic"
        },
        "9-11": {
            "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Domi - warm, patient
            "stability": 0.7,
            "similarity_boost": 0.8,
            "style": 0.2,
            "description": "Warm, patient, encouraging"
        }
    }
    
    return voice_configs.get(age_group, voice_configs["12-15"])

def clean_script_for_narration(script: str) -> str:
    """Remove visual cues and format for natural speech."""
    import re
    
    # Remove [VISUAL: ...] markers
    cleaned = re.sub(r'\[VISUAL: [^\]]+\]', '', script)
    
    # Clean up extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Add natural pauses
    cleaned = cleaned.replace('.', '... ')
    cleaned = cleaned.replace('!', '! ')
    cleaned = cleaned.replace('?', '? ')
    
    return cleaned
```

### 5. Background Music Selection
```python
async def select_background_music(state: ContentGenerationState):
    """Select or generate appropriate background music."""
    
    concept = state["concept"]
    age_group = state["age_group"]
    
    # Analyze concept for mood
    mood_analysis = await analyze_content_mood(concept, state["script"])
    
    # Select from pre-approved music library or generate new
    if mood_analysis["use_existing"]:
        music_url = select_from_music_library(mood_analysis["mood"], age_group)
    else:
        music_url = await generate_custom_music(mood_analysis, age_group)
    
    return {
        "background_music": music_url,
        "music_mood": mood_analysis["mood"],
        "music_volume": 0.3  # Background level
    }

async def analyze_content_mood(concept: str, script: str) -> dict:
    """Analyze content to determine appropriate musical mood."""
    
    prompt = f"""
    Analyze the mood and energy level for this educational content:
    
    Concept: {concept}
    Script: {script}
    
    Determine:
    1. Overall mood (curious, exciting, calm, mysterious, energetic)
    2. Energy level (1-10)
    3. Whether to use existing library music or generate custom
    
    Return JSON with mood, energy_level, and use_existing fields.
    """
    
    response = await openai_client.chat.completions.create(
        model="gpt-4",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return json.loads(response.choices[0].message.content)
```

### 6. Quiz Question Generator
```python
async def generate_quiz_questions(state: ContentGenerationState):
    """Generate interactive quiz questions based on the script."""
    
    script = state["script"]
    objectives = state["learning_objectives"]
    
    prompt = f"""
    Create 3 binary (yes/no or true/false) quiz questions based on this educational content:
    
    Script: {script}
    Learning Objectives: {objectives}
    
    Requirements:
    - Test key concepts from the script
    - Appropriate for quick mobile interaction (3-5 second response time)
    - Clear, unambiguous correct answers
    - Avoid trick questions
    - Progressive difficulty (easy → medium → challenging)
    
    For each question include:
    - question_text: The question to display
    - correct_answer: true or false
    - explanation: Brief explanation of why the answer is correct
    - difficulty: easy, medium, or hard
    - concept_tested: Which learning objective this tests
    
    Return as JSON array.
    """
    
    response = await openai_client.chat.completions.create(
        model="gpt-4",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    
    quiz_data = json.loads(response.choices[0].message.content)
    
    # Add timing and presentation details
    questions = []
    for i, q in enumerate(quiz_data["questions"]):
        questions.append({
            **q,
            "sequence": i + 1,
            "time_limit": 5000,  # 5 seconds
            "show_after_video": True,
            "feedback_duration": 2000  # 2 seconds
        })
    
    return {"quiz_questions": questions}
```

### 7. Video Composition
```python
async def compose_final_video(state: ContentGenerationState):
    """Compose final video from all generated assets."""
    
    composition_config = {
        "format": "mp4",
        "resolution": "1080x1920",  # 9:16 aspect ratio
        "fps": 30,
        "duration": estimate_total_duration(state),
        "audio_tracks": [
            {
                "type": "narration",
                "url": state["narration_url"],
                "volume": 1.0,
                "start_time": 0
            },
            {
                "type": "background_music", 
                "url": state["background_music"],
                "volume": 0.3,
                "start_time": 0,
                "fade_in": 1.0,
                "fade_out": 2.0
            }
        ],
        "visual_timeline": create_visual_timeline(state),
        "text_overlays": generate_text_overlays(state),
        "transitions": "smooth_fade"
    }
    
    # Start video rendering job
    render_job_id = await start_video_render(composition_config)
    
    # Wait for completion (or handle async)
    video_url = await wait_for_render_completion(render_job_id)
    
    # Generate thumbnail
    thumbnail_url = await generate_video_thumbnail(video_url)
    
    return {
        "video_url": video_url,
        "thumbnail_url": thumbnail_url,
        "composition_config": composition_config
    }

def create_visual_timeline(state: ContentGenerationState) -> List[dict]:
    """Create timeline of visual elements for video composition."""
    
    timeline = []
    current_time = 0
    
    for item in state["visual_storyboard"]:
        timeline_item = {
            "start_time": current_time,
            "duration": item["duration"],
            "asset_url": item["image_url"],
            "animation": item["animation_type"],
            "layer": "background"
        }
        timeline.append(timeline_item)
        current_time += item["duration"]
    
    return timeline
```

## Quality Assurance Pipeline

### Automated QA Checks
```python
async def run_quality_assurance(state: ContentGenerationState):
    """Run comprehensive quality checks on generated content."""
    
    qa_results = {}
    
    # Educational Standards Check
    qa_results["curriculum_alignment"] = await check_curriculum_alignment(
        state["concept"], 
        state["script"], 
        state["age_group"]
    )
    
    # Age Appropriateness Check
    qa_results["age_appropriateness"] = await check_age_appropriateness(
        state["script"],
        state["visual_storyboard"], 
        state["age_group"]
    )
    
    # Factual Accuracy Check
    qa_results["factual_accuracy"] = await verify_factual_accuracy(
        state["concept"],
        state["script"]
    )
    
    # Engagement Prediction
    qa_results["engagement_score"] = await predict_engagement(
        state["script"],
        state["quiz_questions"],
        state["visual_storyboard"]
    )
    
    # Technical Quality Check
    qa_results["technical_quality"] = await check_technical_quality(
        state["video_url"],
        state["narration_url"]
    )
    
    # Accessibility Check
    qa_results["accessibility"] = await check_accessibility(
        state["video_url"],
        state["script"]
    )
    
    # Overall pass/fail determination
    overall_pass = all([
        qa_results["curriculum_alignment"]["score"] >= 0.8,
        qa_results["age_appropriateness"]["appropriate"],
        qa_results["factual_accuracy"]["score"] >= 0.9,
        qa_results["engagement_score"] >= 0.7,
        qa_results["technical_quality"]["pass"],
        qa_results["accessibility"]["compliant"]
    ])
    
    return {
        "qa_results": qa_results,
        "overall_pass": overall_pass,
        "approval_status": "approved" if overall_pass else "needs_review"
    }

async def check_curriculum_alignment(concept: str, script: str, age_group: str) -> dict:
    """Check alignment with educational standards."""
    
    # Load curriculum standards for age group
    standards = await load_curriculum_standards(age_group)
    
    prompt = f"""
    Evaluate how well this educational content aligns with curriculum standards:
    
    Concept: {concept}
    Script: {script}
    Age Group: {age_group}
    Relevant Standards: {standards}
    
    Analyze:
    1. Curriculum alignment score (0-1)
    2. Which standards are addressed
    3. Missing curriculum elements
    4. Suggestions for better alignment
    
    Return JSON with score, standards_addressed, missing_elements, suggestions.
    """
    
    response = await openai_client.chat.completions.create(
        model="gpt-4",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    return json.loads(response.choices[0].message.content)
```

## Error Handling & Retry Logic

### Retry Strategies
```python
def should_retry_generation(state: ContentGenerationState) -> str:
    """Determine if content generation should be retried."""
    
    qa_results = state.get("qa_results", {})
    
    # Critical failures that require regeneration
    if qa_results.get("factual_accuracy", {}).get("score", 1.0) < 0.7:
        return "retry"
    
    if not qa_results.get("age_appropriateness", {}).get("appropriate", True):
        return "retry"
    
    # Minor issues that can be manually reviewed
    if qa_results.get("engagement_score", 1.0) < 0.5:
        return "manual_review"
    
    # Content passes QA
    return "approve"

class ContentGenerationError(Exception):
    """Custom exception for content generation failures."""
    pass

async def handle_generation_error(error: Exception, state: ContentGenerationState) -> dict:
    """Handle errors in content generation pipeline."""
    
    error_info = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "failed_step": state.get("current_step", "unknown"),
        "retry_count": state.get("retry_count", 0) + 1
    }
    
    # Log error for monitoring
    logger.error(f"Content generation failed: {error_info}")
    
    # Determine retry strategy
    if error_info["retry_count"] < 3:
        # Retry with modified parameters
        return {
            "errors": state.get("errors", []) + [error_info],
            "retry_count": error_info["retry_count"],
            "status": "retrying"
        }
    else:
        # Escalate to manual review
        return {
            "errors": state.get("errors", []) + [error_info],
            "status": "failed",
            "requires_manual_intervention": True
        }
```

## Performance Optimization

### Parallel Processing
```python
async def optimize_content_generation(state: ContentGenerationState):
    """Optimize generation pipeline with parallel processing."""
    
    # Run independent tasks in parallel
    script_task = asyncio.create_task(generate_educational_script(state))
    objectives_task = asyncio.create_task(generate_learning_objectives(state))
    
    # Wait for dependencies
    script_result, objectives_result = await asyncio.gather(
        script_task, 
        objectives_task
    )
    
    # Update state with results
    state.update(script_result)
    state.update(objectives_result)
    
    # Run next parallel batch
    visual_task = asyncio.create_task(create_visual_storyboard(state))
    voice_task = asyncio.create_task(generate_voice_narration(state))
    quiz_task = asyncio.create_task(generate_quiz_questions(state))
    music_task = asyncio.create_task(select_background_music(state))
    
    # Wait for all to complete
    results = await asyncio.gather(
        visual_task,
        voice_task, 
        quiz_task,
        music_task,
        return_exceptions=True
    )
    
    # Process results and handle any exceptions
    for result in results:
        if isinstance(result, Exception):
            await handle_generation_error(result, state)
        else:
            state.update(result)
    
    return state
```

### Caching Strategy
```python
class ContentGenerationCache:
    """Cache frequently used content generation results."""
    
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379)
        self.cache_ttl = 3600  # 1 hour
    
    async def get_cached_script(self, concept: str, age_group: str) -> str:
        """Get cached script if available."""
        cache_key = f"script:{hash(concept)}:{age_group}"
        cached_script = await self.redis_client.get(cache_key)
        
        if cached_script:
            return json.loads(cached_script)
        return None
    
    async def cache_script(self, concept: str, age_group: str, script: str):
        """Cache generated script."""
        cache_key = f"script:{hash(concept)}:{age_group}"
        await self.redis_client.setex(
            cache_key, 
            self.cache_ttl, 
            json.dumps(script)
        )
    
    async def get_cached_visual(self, description: str) -> str:
        """Get cached visual asset if available."""
        cache_key = f"visual:{hash(description)}"
        return await self.redis_client.get(cache_key)
```

---

*Last updated: 2025-08-15*