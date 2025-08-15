# Jules Agent Autonomous Development Plan

## Overview
This document provides comprehensive task breakdown and autonomous instructions for Jules agent (jules.google.com) to maximize independent development velocity on the MicroLearning platform.

## Project Context Summary
- **Target**: Educational platform for 12-15 year olds with TikTok-style 45-90 second learning videos
- **Architecture**: Progressive Web App (PWA) with React + TypeScript + Vite
- **UI Framework**: Tailwind CSS with age-adaptive design system
- **Core Interaction**: Binary choice quizzes (yes/no) with immediate feedback
- **Video Format**: 9:16 aspect ratio (portrait) optimized for mobile consumption

## Jules Primary Development Areas

### 1. Web UI Component System (Phase 1)
**Autonomous Tasks:**
- Complete missing UI components from existing design system
- Build mobile-first responsive layouts
- Implement touch-optimized interactions
- Create age-adaptive component variants

### 2. Video Learning Engine (Phase 2) 
**Autonomous Tasks:**
- HTML5 video player with custom controls
- HLS.js integration for adaptive streaming
- Quiz timing and interaction system
- Progress tracking and session management
- PWA features (offline, installation)

### 3. Student Interface (Phase 4)
**Autonomous Tasks:**
- TikTok-style feed navigation
- Swipe gestures and touch interactions
- Achievement and progress visualization
- Social sharing capabilities

## Detailed Task Instructions

### Task Group 1: Complete UI Component Library

#### Task 1.1: Missing Component Implementation
```
AUTONOMOUS INSTRUCTION:
1. Analyze existing components in web-app/src/components/ui/
2. Identify gaps based on mobile/src/components/ React Native versions
3. Create web equivalents for missing components:
   - Input fields with age-adaptive sizing
   - Modal/Dialog components
   - Loading states and animations
   - Navigation components
   - Form validation components

SUCCESS CRITERIA:
- All components match age-adaptive design patterns from Button.tsx
- Components use Tailwind CSS with proper responsive classes
- TypeScript interfaces follow existing patterns
- Components include proper accessibility attributes
- Mobile-first responsive design (min 44px touch targets)

REFERENCE FILES:
- web-app/src/components/ui/Button.tsx (pattern to follow)
- web-app/src/components/ui/VideoPlayer.tsx (pattern to follow)
- mobile/src/components/ui/ (components to convert)
```

#### Task 1.2: Design System Utilities
```
AUTONOMOUS INSTRUCTION:
1. Create /web-app/src/lib/design-system.ts with:
   - Age-group constants and types
   - Color palette utilities
   - Spacing scale utilities
   - Typography scale utilities
   - Touch target size helpers

2. Create /web-app/src/components/ui/Layout.tsx with:
   - Container components with max-widths
   - Grid system for responsive layouts
   - Safe area handling for mobile
   - Flexbox utility components

SUCCESS CRITERIA:
- Design system matches existing age-adaptive patterns
- All utilities are TypeScript-typed
- Components use design system instead of hardcoded values
- Responsive breakpoints match mobile-first approach

REFERENCE FILES:
- web-app/src/components/ui/Button.tsx (ageGroup variants)
- mobile/src/components/ui/DesignSystem.ts (patterns to convert)
```

### Task Group 2: Video Learning Engine

#### Task 2.1: Enhanced Video Player
```
AUTONOMOUS INSTRUCTION:
1. Enhance existing VideoPlayer.tsx with:
   - HLS.js integration for adaptive streaming
   - Gesture controls (swipe up/down for volume, double-tap for seek)
   - Picture-in-picture support
   - Background play handling
   - Video quality selector

2. Create VideoFeed.tsx component:
   - Infinite scroll video feed
   - Preload next video for smooth experience
   - Intersection Observer for autoplay
   - Swipe navigation between videos

SUCCESS CRITERIA:
- Smooth video transitions with <1s load time
- Adaptive bitrate streaming works on 3G/4G/5G
- Touch gestures feel native and responsive
- Memory management prevents crashes on long sessions
- Works offline with cached videos

REFERENCE FILES:
- web-app/src/components/ui/VideoPlayer.tsx (base to enhance)
- web-app/package.json (HLS.js already included)
```

#### Task 2.2: Quiz Interaction System
```
AUTONOMOUS INSTRUCTION:
1. Convert React Native BinaryChoice to web component:
   - Use web-app/src/components/ui/Button.tsx BinaryChoiceButton
   - Implement timing system with visual countdown
   - Add haptic feedback via Vibration API
   - Create smooth animations with CSS transitions

2. Create QuizSession.tsx component:
   - Manage series of binary choice questions
   - Track response times and accuracy
   - Provide immediate feedback with animations
   - Auto-advance to next question after delay

SUCCESS CRITERIA:
- Quiz interactions feel instant (<100ms response)
- Visual feedback matches native app experience
- Timing system is accurate and fair
- Progress tracking persists across sessions
- Works with keyboard navigation for accessibility

REFERENCE FILES:
- mobile/src/components/quiz/BinaryChoice.tsx (logic to convert)
- web-app/src/components/ui/Button.tsx (BinaryChoiceButton to use)
```

#### Task 2.3: PWA Implementation
```
AUTONOMOUS INSTRUCTION:
1. Enhance existing PWA setup:
   - Complete service worker for video caching
   - Implement background sync for progress
   - Add push notification support
   - Create installation prompts

2. Create offline experience:
   - Cache management for videos
   - Offline quiz completion
   - Progress sync when online
   - Offline indicator UI

SUCCESS CRITERIA:
- Videos play smoothly offline
- Installation prompt appears at right moment
- Push notifications work for engagement
- Offline experience doesn't feel broken
- App launches in <2s when installed

REFERENCE FILES:
- web-app/vite.config.ts (PWA plugin already configured)
- docs/decisions/ADR-0003-web-only-architecture.md (PWA requirements)
```

### Task Group 3: Student Learning Interface

#### Task 3.1: Feed-Style Navigation
```
AUTONOMOUS INSTRUCTION:
1. Create LearningFeed.tsx component:
   - Vertical scrolling video feed
   - Smooth video-to-video transitions
   - Topic filtering and recommendations
   - Pull-to-refresh functionality

2. Implement navigation patterns:
   - Swipe gestures for video navigation
   - Topic-based filtering
   - Search functionality
   - Recently viewed history

SUCCESS CRITERIA:
- Feed scrolling feels smooth at 60fps
- Video autoplay works reliably
- Topic navigation is intuitive
- Search returns relevant results quickly
- History tracking works offline

REFERENCE FILES:
- web-app/src/components/ui/VideoPlayer.tsx (base component)
- web-app/src/components/ui/Button.tsx (navigation buttons)
```

#### Task 3.2: Progress & Achievements
```
AUTONOMOUS INSTRUCTION:
1. Create ProgressDashboard.tsx:
   - Weekly learning streaks
   - Topic completion percentages
   - Daily learning goals
   - Achievement badges

2. Implement gamification:
   - Points system for correct answers
   - Streak bonuses for consistency
   - Topic mastery indicators
   - Social comparison features

SUCCESS CRITERIA:
- Progress updates feel immediate and rewarding
- Achievements motivate continued learning
- Dashboard loads quickly with smooth animations
- Data persists across devices when logged in

REFERENCE FILES:
- app/models/user_progress.py (backend progress tracking)
- docs/MICROLEARNING_BEST_PRACTICES.md (gamification principles)
```

## Jules Autonomy Guidelines

### Quality Standards
- **Code Quality**: Follow existing TypeScript patterns, use proper types
- **Performance**: Target <2s load times, 60fps animations
- **Accessibility**: WCAG 2.1 AA compliance, keyboard navigation
- **Mobile-First**: Touch targets >44px, responsive design
- **Testing**: Write unit tests for complex logic, integration tests for user flows

### Decision-Making Framework
**HIGH AUTONOMY - Make decisions directly:**
- Component API design following existing patterns
- CSS styling and animations
- TypeScript interface definitions
- File organization within established structure
- Performance optimizations

**MEDIUM AUTONOMY - Document decisions:**
- New dependencies or libraries
- Architectural pattern changes
- Database schema modifications
- API endpoint designs
- State management patterns

**LOW AUTONOMY - Seek approval:**
- Major feature scope changes
- Security-related implementations
- Third-party service integrations
- Breaking changes to existing APIs
- Cost-impacting decisions (AI services, hosting)

### Documentation Requirements
**Always Document:**
- New components with JSDoc comments
- Complex business logic with inline comments
- API changes in relevant markdown files
- Performance optimizations and rationale
- Known limitations or technical debt

**Update These Files:**
- README.md for new setup requirements
- TECHNICAL_ARCHITECTURE.md for architectural changes
- Component documentation for new UI elements
- API documentation for backend changes

### Testing Requirements
**Required Tests:**
- Unit tests for utility functions
- Integration tests for quiz logic
- Component tests for user interactions
- E2E tests for critical user journeys
- Performance tests for video loading

**Test Files Location:**
- Unit: `web-app/src/__tests__/`
- Integration: `web-app/src/components/__tests__/`
- E2E: `web-app/e2e/`

### Git Workflow
**Branch Naming:**
- `feature/jules-component-name` for new components
- `fix/jules-issue-description` for bug fixes
- `enhancement/jules-performance-optimization` for improvements

**Commit Messages:**
```
feat(jules): add enhanced video player with HLS support

- Integrated HLS.js for adaptive streaming
- Added gesture controls for volume and seeking
- Implemented picture-in-picture support
- Added video quality selector

Closes #123
```

**Pull Request Requirements:**
- Clear description of changes made
- Screenshots/videos for UI changes
- Performance impact analysis
- Breaking change documentation
- Link to related issues

### Communication Protocol
**Status Updates:**
- Daily: Brief progress summary in commit messages
- Weekly: Detailed progress report in GitHub discussions
- Blockers: Immediate notification with context

**Questions Format:**
```
BLOCKER: [Component/Feature] - [Brief Description]

Context: What I'm trying to achieve
Problem: Specific technical issue
Attempted: What I've tried so far
Need: Specific guidance or decision required
Impact: How this affects timeline/other work
```

## Success Metrics for Jules

### Development Velocity
- **Target**: Complete 2-3 components per day
- **Quality**: <10% rework rate on code reviews
- **Integration**: All components work together without conflicts

### Code Quality
- **TypeScript**: 100% type coverage, no any types
- **Testing**: >80% code coverage on new code
- **Performance**: All Lighthouse scores >90

### User Experience
- **Load Times**: <2s for first contentful paint
- **Interactions**: <100ms response time for user actions
- **Mobile**: Perfect mobile usability score

### Autonomy Success
- **Decision Making**: >80% of technical decisions made independently
- **Problem Solving**: <20% of issues require human intervention
- **Documentation**: All changes self-documented

## Getting Started Checklist for Jules

- [ ] Read all reference files in web-app/src/components/ui/
- [ ] Review existing package.json dependencies
- [ ] Understand the age-adaptive design system pattern
- [ ] Set up development environment with `npm run dev`
- [ ] Create first branch: `feature/jules-ui-components`
- [ ] Start with Task 1.1: Missing Component Implementation
- [ ] Document progress in commit messages
- [ ] Test components in different age group variants
- [ ] Ensure mobile-first responsive behavior
- [ ] Run linting and type checking before commits

This plan provides maximum autonomy while ensuring quality and consistency. Jules can work independently on clearly defined tasks while following established patterns and quality standards.