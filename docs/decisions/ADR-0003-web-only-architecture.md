# ADR-0003: Web-Only Architecture (PWA) Decision

## Status
**Accepted** - 2025-08-15

## Context

The original plan included separate React Native mobile app and React web dashboard. However, modern web technologies have advanced significantly, and a well-designed Progressive Web App (PWA) can provide native-like experience without the complexity of maintaining separate codebases.

Key considerations:
- 98% of target users (12-15 year olds) access content via mobile browsers
- Modern PWA capabilities rival native apps for media consumption
- Reduced development complexity and maintenance overhead
- Faster iteration and deployment cycles
- No app store approval processes

## Decision

We will implement a **single Progressive Web App (PWA)** with responsive design:

### Primary Platform: React PWA
- **Student Interface**: Mobile-first responsive web app
- **Creator Dashboard**: Desktop-optimized web interface within same app
- **Progressive Web App**: Installable, offline-capable, push notifications
- **Video Player**: HTML5 with optimized mobile controls
- **Responsive Design**: Adaptive UI from mobile to desktop

### Technical Implementation
- **Framework**: React + TypeScript + Vite
- **Styling**: Tailwind CSS + CSS-in-JS for component-level styles
- **PWA Features**: Service worker, web app manifest, offline caching
- **Video Delivery**: HLS/DASH streaming with adaptive bitrate
- **State Management**: Zustand for simplicity and performance

## Rationale

### Advantages of Web-Only Approach

**Development Efficiency:**
- Single codebase for all platforms (mobile web, desktop web)
- Faster development cycles without app store submissions
- Shared components between student and creator interfaces
- Easier testing and debugging across devices

**User Experience:**
- Instant access via URL sharing (no installation required)
- Progressive enhancement (works on any device)
- Automatic updates without user intervention
- Deep linking to specific content

**Modern Web Capabilities:**
- Service Workers for offline functionality
- Web Push API for notifications
- Media Session API for background video controls
- Screen Wake Lock API for continuous viewing
- Fullscreen API for immersive video experience

**Cost and Maintenance:**
- Reduced development team requirements
- Single deployment pipeline
- Lower infrastructure costs
- Easier A/B testing and feature rollouts

### Web Technologies for Mobile-Native Experience

**Video Playback:**
- HTML5 video with custom controls
- HLS.js for adaptive streaming
- Intersection Observer for autoplay
- Picture-in-Picture API support

**Touch Interactions:**
- Pointer Events API for unified touch/mouse handling
- CSS touch-action for gesture optimization
- Haptic feedback via Vibration API
- Touch-friendly button sizes (44px minimum)

**Performance:**
- Vite for fast development and optimized builds
- Code splitting and lazy loading
- Image optimization with WebP/AVIF
- Critical CSS inlining

## Consequences

### Positive
- **Simplified Architecture**: Single codebase, single deployment
- **Faster Development**: No platform-specific code or testing
- **Better SEO**: Web-indexable educational content
- **Universal Access**: Works on any device with a browser
- **Real-time Updates**: Instant feature rollouts and bug fixes

### Negative
- **iOS Limitations**: Some PWA features limited on iOS Safari
- **Performance**: Slight performance difference vs native for intensive operations
- **App Store Presence**: No native app store discoverability
- **Platform Integration**: Limited deep OS integration capabilities

### Mitigation Strategies
- **Performance**: Optimize with modern web APIs and efficient bundling
- **iOS PWA**: Design around iOS limitations, provide installation prompts
- **Discovery**: Focus on web-based marketing and SEO optimization
- **Features**: Use progressive enhancement for advanced capabilities

## Implementation Plan

### Phase 1: Core Web App (Week 1-3)
- [ ] Set up React + TypeScript + Vite project
- [ ] Implement responsive design system with Tailwind CSS
- [ ] Create mobile-first video player component
- [ ] Build quiz interaction components
- [ ] Basic PWA setup (manifest, service worker)

### Phase 2: Student Experience (Week 4-6)
- [ ] Complete student learning interface
- [ ] Implement offline video caching
- [ ] Add progress tracking and achievements
- [ ] Web push notifications for engagement
- [ ] Performance optimization for mobile

### Phase 3: Creator Dashboard (Week 7-9)
- [ ] Creator interface within same app
- [ ] AI content generation integration
- [ ] Content management and approval workflows
- [ ] Analytics and performance dashboards
- [ ] Advanced PWA features

### Phase 4: Advanced Features (Week 10-12)
- [ ] Advanced offline capabilities
- [ ] Social sharing and collaboration
- [ ] Advanced analytics and personalization
- [ ] Performance optimization at scale
- [ ] Cross-browser compatibility testing

## Technical Requirements

### Mobile Web Performance Targets
- **First Contentful Paint**: <1.5 seconds on 3G
- **Video Load Time**: <2 seconds on 4G networks
- **Quiz Response Time**: <100ms for touch interactions
- **Lighthouse Score**: >90 for Performance, Accessibility, Best Practices
- **Core Web Vitals**: All metrics in "Good" range

### PWA Requirements
- **Installability**: Web App Manifest with proper icons
- **Offline Support**: Service Worker with video caching
- **Push Notifications**: Web Push API for engagement
- **Responsive Design**: Mobile-first, desktop-enhanced
- **Security**: HTTPS required for PWA features

### Browser Support
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Progressive Enhancement**: Basic functionality on older browsers
- **Polyfills**: Minimal polyfills for critical features only
- **Testing**: Automated testing across browser matrix

## Success Metrics

### User Experience Metrics
- **Mobile Usability Score**: >95 (Google PageSpeed Insights)
- **Session Duration**: >8 minutes average per learning session
- **Completion Rate**: >85% video completion rate
- **PWA Install Rate**: >20% of returning users
- **Bounce Rate**: <15% for educational content

### Performance Metrics
- **Load Time**: <2 seconds for first video on mobile
- **Video Streaming**: <1 second start time on 90% of devices
- **Offline Usage**: 40%+ of learning sessions support offline mode
- **Cross-Browser Consistency**: <5% difference in core metrics

### Development Efficiency Metrics
- **Development Velocity**: 2-week sprint cycles maintained
- **Bug Resolution**: <24 hours for critical user-affecting issues
- **Deployment Frequency**: Daily deployments without issues
- **Code Reuse**: >80% shared code between mobile and desktop views

## Superseded Decisions

This decision supersedes:
- **ADR-0002**: Mobile-First Architecture Strategy (React Native approach)
- The React Native mobile app is no longer needed
- Mobile development resources can focus on web optimization

## Migration Plan

### From React Native to Web Components
- [ ] Convert React Native components to web-compatible React components
- [ ] Migrate styling from React Native to CSS-in-JS/Tailwind
- [ ] Replace native APIs with web APIs (Camera, Storage, Notifications)
- [ ] Update navigation from React Navigation to React Router
- [ ] Convert Expo-specific features to web equivalents

### Component Mapping
- **Video Player**: React Native Video → HTML5 Video + HLS.js
- **Touch Interactions**: Gesture Handler → Pointer Events
- **Storage**: AsyncStorage → IndexedDB/LocalStorage
- **Navigation**: React Navigation → React Router
- **Notifications**: Expo Notifications → Web Push API

## Review Schedule

This architecture decision will be reviewed:
- **Monthly**: Performance metrics and user feedback analysis
- **Quarterly**: PWA feature adoption and mobile web trends
- **Annually**: Comparison with native app alternatives

Key review triggers:
- Significant improvements in PWA capabilities
- Major browser API additions affecting mobile experience
- User feedback indicating need for native features
- Performance issues that can't be resolved with web technologies

## Related Documents

- [UI/UX Specifications](../UI_UX_SPECIFICATIONS.md) - Updated for web-only approach
- [Technical Architecture](../TECHNICAL_ARCHITECTURE.md) - Simplified web architecture
- [Development Principles](../DEVELOPMENT_PRINCIPLES.md) - Web-first development principles

---

**Decision made by:** Technical Architecture Team  
**Stakeholders consulted:** Product, UX, Engineering, Business  
**Implementation owner:** Frontend Team  
**Review date:** 2025-11-15