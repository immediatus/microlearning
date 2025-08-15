# UI/UX Specifications

## Design Philosophy

### Student-First Approach
- **Mobile-native experience** optimized for 12-15 year olds
- **Zero learning curve** - intuitive TikTok/Instagram-style interface
- **Instant gratification** with quick feedback loops
- **Gamified progression** to maintain engagement

### Visual Design Principles
- **Clean, modern aesthetic** (Spotify/Discord inspiration)
- **High contrast** for outdoor mobile usage
- **Minimal cognitive load** with focused interactions
- **Consistent visual language** across all components

## Student Mobile App

### App Structure
```
┌─ Discovery Feed (Primary)
├─ Learning Progress
├─ Profile & Achievements  
├─ Settings
└─ Offline Content
```

### Discovery Feed (Main Screen)

#### Layout Specifications
```jsx
// Full-screen video cards
const FeedLayout = {
  viewport: "100vh x 100vw",
  video_aspect: "9:16", // TikTok format
  snap_behavior: "vertical_paging",
  preload_count: 3, // Next 3 videos
  transition: "smooth_snap"
}
```

#### Interactive Elements
```jsx
// Video overlay components
<VideoOverlay>
  <TopBar>
    <TopicBadge text="Physics" color="#4ECDC4" />
    <ProgressIndicator current={3} total={5} />
  </TopBar>
  
  <BottomBar>
    <SwipeUpIndicator text="Quiz next!" />
    <VideoProgress duration={75} current={45} />
  </BottomBar>
  
  <SideActions>
    <HeartButton count={1247} />
    <ShareButton />
    <BookmarkButton />
    <ProfileAvatar src="creator_avatar.jpg" />
  </SideActions>
</VideoOverlay>
```

### Quiz Interface

#### Binary Choice Design
```jsx
// Touch zone specifications
const QuizZones = {
  left_zone: {
    area: "0-50% width, 30-90% height",
    color: "#FF6B6B", // Red for NO/False
    icon: "x-circle",
    feedback: "shake_animation"
  },
  right_zone: {
    area: "50-100% width, 30-90% height", 
    color: "#4ECDC4", // Teal for YES/True
    icon: "check-circle",
    feedback: "pulse_animation"
  }
}
```

#### Question Display
```jsx
<QuestionCard>
  <TimerBar 
    duration={5000}
    color="linear-gradient(90deg, #FF6B6B, #4ECDC4)"
    warning_threshold={1000} // Last second warning
  />
  
  <QuestionText 
    fontSize="clamp(18px, 5vw, 24px)"
    fontWeight="600"
    textAlign="center"
    maxLines={3}
  >
    "Does ice float because it's less dense than water?"
  </QuestionText>
  
  <InstructionText>
    Tap left for NO • Tap right for YES
  </InstructionText>
</QuestionCard>
```

#### Feedback Animations
```jsx
const FeedbackStates = {
  correct: {
    animation: "confetti_burst",
    color: "#4ECDC4",
    haptic: "success",
    sound: "ding",
    duration: 1500
  },
  incorrect: {
    animation: "gentle_shake",
    color: "#FF6B6B", 
    haptic: "error",
    sound: "buzz",
    duration: 1000
  },
  timeout: {
    animation: "fade_out",
    color: "#FFA726",
    haptic: "warning",
    duration: 800
  }
}
```

### Navigation & Progress

#### Bottom Tab Bar
```jsx
<TabBar position="bottom" style="floating">
  <Tab icon="home" label="Learn" active />
  <Tab icon="chart" label="Progress" />
  <Tab icon="user" label="Profile" />
</TabBar>
```

#### Progress Screen
```jsx
<ProgressDashboard>
  <StatsCards>
    <StatCard 
      title="Streak" 
      value="7 days" 
      icon="fire"
      color="#FF6B6B"
    />
    <StatCard 
      title="Videos" 
      value="23 completed" 
      icon="play"
      color="#4ECDC4"
    />
    <StatCard 
      title="Topics" 
      value="5 mastered" 
      icon="brain"
      color="#FFA726"
    />
  </StatsCards>
  
  <LearningPath>
    <PathNode status="completed" topic="Photosynthesis" />
    <PathNode status="current" topic="Gravity" />
    <PathNode status="locked" topic="DNA Structure" />
  </LearningPath>
  
  <Achievements>
    <Badge title="Quick Learner" earned />
    <Badge title="Science Explorer" earned />
    <Badge title="Quiz Master" locked />
  </Achievements>
</ProgressDashboard>
```

## Creator Web Interface

### Dashboard Layout
```jsx
<CreatorDashboard>
  <Sidebar>
    <Logo />
    <Navigation>
      <NavItem icon="plus" text="Create Content" active />
      <NavItem icon="list" text="My Content" />
      <NavItem icon="chart" text="Analytics" />
      <NavItem icon="settings" text="Settings" />
    </Navigation>
  </Sidebar>
  
  <MainContent>
    <Header>
      <Title>Create Learning Content</Title>
      <UserMenu />
    </Header>
    
    <ContentCreationPanel />
  </MainContent>
</CreatorDashboard>
```

### Content Creation Interface

#### AI Prompt Input
```jsx
<PromptInput>
  <Label>What would you like to teach?</Label>
  <TextArea 
    placeholder="Example: Explain photosynthesis for 13-year-olds focusing on why plants need sunlight"
    maxLength={500}
    rows={4}
  />
  
  <OptionsRow>
    <AgeSelector 
      options={["5-8", "9-11", "12-15", "16-18"]}
      selected="12-15"
    />
    <DifficultySlider 
      min={1} 
      max={10} 
      value={5}
      label="Complexity Level"
    />
  </OptionsRow>
  
  <GenerateButton 
    size="large"
    loading={isGenerating}
  >
    Generate Content
  </GenerateButton>
</PromptInput>
```

#### Review Interface
```jsx
<ReviewPanel>
  <ContentPreview>
    <ScriptTab>
      <ScriptEditor 
        content={generatedScript}
        readOnly={false}
        suggestions={aiSuggestions}
      />
    </ScriptTab>
    
    <VideoTab>
      <VideoPlayer 
        src={previewVideoUrl}
        controls={true}
        quality="preview"
      />
    </VideoTab>
    
    <QuizTab>
      <QuizPreview questions={generatedQuestions} />
    </QuizTab>
  </ContentPreview>
  
  <ActionPanel>
    <QualityChecks>
      <CheckItem status="pass" text="Age Appropriate" />
      <CheckItem status="pass" text="Factually Accurate" />
      <CheckItem status="warning" text="Needs Audio Description" />
      <CheckItem status="pass" text="Engagement Score: 8.5/10" />
    </QualityChecks>
    
    <ActionButtons>
      <Button variant="secondary">
        🔄 Regenerate
      </Button>
      <Button variant="primary">
        ✅ Approve & Publish
      </Button>
    </ActionButtons>
  </ActionPanel>
</ReviewPanel>
```

## Color Palette & Typography

### Color System
```css
:root {
  /* Primary Colors */
  --primary-blue: #2E86AB;
  --primary-teal: #4ECDC4;
  --primary-orange: #FFA726;
  --primary-red: #FF6B6B;
  
  /* Neutral Colors */
  --background-light: #FAFAFA;
  --background-dark: #1A1A1A;
  --text-primary: #2D2D2D;
  --text-secondary: #757575;
  --text-inverse: #FFFFFF;
  
  /* Semantic Colors */
  --success: #4CAF50;
  --warning: #FFC107;
  --error: #F44336;
  --info: #2196F3;
  
  /* Gradients */
  --gradient-quiz: linear-gradient(135deg, #FF6B6B, #4ECDC4);
  --gradient-progress: linear-gradient(90deg, #2E86AB, #4ECDC4);
}
```

### Typography Scale
```css
/* Mobile Typography */
.text-hero { font-size: clamp(28px, 8vw, 36px); font-weight: 700; }
.text-h1 { font-size: clamp(24px, 6vw, 28px); font-weight: 600; }
.text-h2 { font-size: clamp(20px, 5vw, 24px); font-weight: 600; }
.text-body { font-size: clamp(16px, 4vw, 18px); font-weight: 400; }
.text-small { font-size: clamp(14px, 3.5vw, 16px); font-weight: 400; }
.text-caption { font-size: clamp(12px, 3vw, 14px); font-weight: 400; }

/* Web Typography */
.web-h1 { font-size: 32px; font-weight: 700; }
.web-h2 { font-size: 24px; font-weight: 600; }
.web-h3 { font-size: 20px; font-weight: 600; }
.web-body { font-size: 16px; font-weight: 400; }
.web-small { font-size: 14px; font-weight: 400; }
```

## Responsive Design

### Mobile Breakpoints
```css
/* Phone Sizes */
@media (max-width: 390px) { /* iPhone 14 Pro and smaller */ }
@media (min-width: 391px) and (max-width: 430px) { /* iPhone 14 Pro Max */ }
@media (min-width: 431px) and (max-width: 768px) { /* Small tablets */ }

/* Tablet Sizes */
@media (min-width: 769px) and (max-width: 1024px) { /* iPad */ }
@media (min-width: 1025px) { /* Desktop */ }
```

### Touch Target Sizes
```css
/* Minimum touch targets for accessibility */
.touch-target {
  min-height: 44px;
  min-width: 44px;
  padding: 12px;
}

/* Age-specific adjustments */
.age-5-8 .touch-target { min-height: 60px; min-width: 60px; }
.age-9-11 .touch-target { min-height: 50px; min-width: 50px; }
.age-12-15 .touch-target { min-height: 44px; min-width: 44px; }
```

## Animation & Micro-interactions

### Core Animations
```css
/* Smooth transitions */
.transition-standard { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.transition-quick { transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1); }
.transition-slow { transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); }

/* Bouncy animations for engagement */
@keyframes bounceIn {
  0% { transform: scale(0.3); opacity: 0; }
  50% { transform: scale(1.05); opacity: 0.8; }
  70% { transform: scale(0.9); opacity: 0.9; }
  100% { transform: scale(1); opacity: 1; }
}

/* Loading states */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

### Gesture Interactions
```javascript
// React Native gesture handling
const QuizGestures = {
  tap: {
    maxDuration: 200,
    feedback: "haptic",
    visual: "scale_down"
  },
  swipe: {
    velocity_threshold: 500,
    distance_threshold: 100,
    feedback: "haptic_selection"
  }
}
```

## Accessibility Standards

### WCAG 2.1 AA Compliance
- **Color Contrast**: Minimum 4.5:1 for normal text
- **Touch Targets**: Minimum 44x44px
- **Font Scaling**: Support for 200% zoom
- **Screen Reader**: Full VoiceOver/TalkBack support
- **Captions**: Auto-generated for all videos

### Implementation
```jsx
// Accessibility props example
<TouchableOpacity 
  accessibilityRole="button"
  accessibilityLabel="Answer yes to the quiz question"
  accessibilityHint="Double tap to select yes as your answer"
  accessibilityState={{ selected: false }}
>
  <Text>YES</Text>
</TouchableOpacity>
```

## Performance Guidelines

### Core Web Vitals
- **LCP**: < 2.5 seconds (video load time)
- **FID**: < 100ms (touch response)
- **CLS**: < 0.1 (layout stability)

### Mobile Performance
- **App Launch**: < 3 seconds to first video
- **Video Transition**: < 500ms between videos
- **Quiz Response**: < 100ms feedback
- **Memory Usage**: < 150MB peak usage
- **Battery Impact**: Optimized video decoding

---

*Last updated: 2025-08-15*