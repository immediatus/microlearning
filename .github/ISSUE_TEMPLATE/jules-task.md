---
name: Jules Agent Task
about: Task template for Jules AI agent development
title: '[JULES] '
labels: ['jules', 'enhancement']
assignees: ''
---

## Task Description
<!-- Clear description of what needs to be implemented -->

## Acceptance Criteria
- [ ] Specific, testable requirement 1
- [ ] Specific, testable requirement 2
- [ ] Code coverage >80% for new functionality
- [ ] Documentation updated (API docs, inline comments)
- [ ] Performance requirements met
- [ ] Security review passed

## Technical Context
<!-- Relevant technical information for implementation -->

**Related Files:**
- `app/models/...` 
- `app/api/routes/...`
- `docs/...`

**Dependencies:**
- [ ] Database models
- [ ] API endpoints
- [ ] External services

**Integration Points:**
- Database: <!-- tables/models involved -->
- APIs: <!-- endpoints affected -->
- AI Services: <!-- if applicable, with cost estimate -->
- Frontend: <!-- components affected -->

## AI Service Usage (if applicable)
**Estimated Costs:**
- Service: <!-- e.g., OpenAI GPT-4 -->
- Estimated usage: <!-- e.g., 1000 tokens per operation -->
- Estimated cost: <!-- e.g., $0.06 per operation -->
- Expected volume: <!-- e.g., 100 operations/day -->

**Cost Tracking Required:**
- [ ] Implement cost tracking for this feature
- [ ] Add budget approval workflow
- [ ] Include caching to minimize costs

## Performance Requirements
- [ ] Response time: < <!-- specify time -->
- [ ] Memory usage: < <!-- specify limit -->
- [ ] Database queries: < <!-- specify limit -->
- [ ] Mobile optimization: <!-- specific requirements -->

## Security Considerations
- [ ] Input validation implemented
- [ ] Authentication/authorization checked
- [ ] No sensitive data exposure
- [ ] SQL injection prevention

## Documentation Requirements
- [ ] API documentation updated
- [ ] Inline code comments added
- [ ] Architecture decisions documented (ADR if significant)
- [ ] README/setup instructions updated

## Testing Requirements
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests for API endpoints
- [ ] Performance tests if applicable
- [ ] Security tests for user data

## Definition of Done
- [ ] Code implemented and tested
- [ ] All acceptance criteria met
- [ ] Documentation complete
- [ ] Code review approved
- [ ] Performance benchmarks met
- [ ] Security scan clean
- [ ] Deployed to staging environment

## Additional Context
<!-- Any other relevant information, screenshots, examples, etc. -->

---

**Jules Agent Instructions:**
1. Read all project documentation in `/docs` before starting
2. Follow coding standards in `docs/DEVELOPMENT_PRINCIPLES.md`
3. Use existing patterns from similar implemented features
4. Request cost approval for any AI service usage >$1
5. Create detailed PR with cost impact analysis
6. Include comprehensive tests and documentation