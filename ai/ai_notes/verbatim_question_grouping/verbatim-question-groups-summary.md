# ResAuto Verbatim Question Groups - Executive Summary

## Overview
This document provides a comprehensive analysis and design for implementing question grouping functionality in the ResAuto Verbatim module, allowing users to group multiple questions to share a common codebook/codelist.

## Current System Analysis

### Existing Architecture
The current Verbatim module follows a **one-question-one-codebook** model:

1. **Questions** (`verbatim_questions`): Individual survey questions with selection and status tracking
2. **Codes** (`verbatim_codes`): Individual codes belonging to specific questions
3. **Categories** (`verbatim_categories`): Groupings of codes within a question
4. **Response-Code Links** (`verbatim_response_code`): Assignments of codes to specific responses

### Current Workflow
```
Question Selection → Codebook Generation → Code Assignment → Completion
     ↓                      ↓                    ↓              ↓
is_selected=true    AI generates codes    AI assigns codes    is_assigned=true
```

### Key Constraints Identified
1. Questions with `is_assigned=true` cannot be modified
2. Questions with status ≠ `NOT_STARTED` cannot generate new codebooks
3. Each question maintains independent codebook isolation
4. No mechanism for shared codebooks across questions

## Proposed Solution

### Core Design Principles
1. **Backward Compatibility**: Existing individual question workflows remain unchanged
2. **Group Isolation**: Groups operate independently with shared codebooks
3. **Mutual Exclusivity**: Questions belong either to groups OR remain individual
4. **Constraint Enforcement**: Database-level validation prevents invalid states

### New Database Schema

#### Primary Tables
```sql
-- Question Groups
CREATE TABLE verbatim_question_groups (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    file_id INTEGER REFERENCES files(id),
    group_name VARCHAR(255) NOT NULL,  -- Contains question codes (e.g., "Q1_Q3_Q7")
    status verbatim_group_status_enum DEFAULT 'NOT_STARTED',
    is_assigned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL
);
```

#### Enhanced Existing Tables
```sql
-- Add group reference for direct relationship
ALTER TABLE verbatim_questions ADD COLUMN group_id INTEGER REFERENCES verbatim_question_groups(id);
ALTER TABLE verbatim_codes ADD COLUMN group_id INTEGER REFERENCES verbatim_question_groups(id);
ALTER TABLE verbatim_categories ADD COLUMN group_id INTEGER REFERENCES verbatim_question_groups(id);
```

**Key Design Benefits:**
- **Simplified Relationship**: Direct foreign key relationship eliminates junction table complexity
- **Single Source of Truth**: `group_name` contains the question codes, eliminating redundant `group_code` column
- **Efficient Queries**: Direct joins between questions and groups improve performance

### Business Logic Changes

#### Group Management Rules
1. **Creation Requirements**:
   - All questions must belong to same file
   - Questions cannot already be in groups
   - Questions cannot have existing assignments (`is_assigned=false`)
   - Questions must have compatible status (`NOT_STARTED` or `CODING_FAILED`)

2. **Group Naming**:
   - Group names contain question codes (e.g., "Q1_Q3_Q7") as the primary identifier
   - Auto-generated from question text patterns or fallback to question IDs

3. **Deletion Policy**:
   - Delete entire group including all codes, categories, and assignments
   - Reset member questions to individual state
   - Cannot delete partially processed groups

#### Codebook Generation Updates
```python
# Individual Questions (Existing)
POST /verbatim/question/{question_id}/generate-codebook
- Uses responses from single question
- Creates codes with question_id

# Question Groups (New)
POST /verbatim/groups/{group_id}/generate-codebook  
- Uses responses from ALL questions in group
- Creates codes with group_id
- Shares codebook across all group members
```

#### Code Assignment Updates
```python
# Individual Questions (Existing)
POST /verbatim/question/{question_id}/assign-codebook
- Assigns codes to single question's responses

# Question Groups (New)
POST /verbatim/groups/{group_id}/assign-codebook
- Assigns shared codes to ALL group questions' responses
- Uses same confidence scoring and assignment logic
```

### Data Integrity Constraints

#### Database-Level Validation
```sql
-- Codes belong to either question OR group, never both
ALTER TABLE verbatim_codes ADD CONSTRAINT check_single_parent 
CHECK ((question_id IS NOT NULL AND group_id IS NULL) OR 
       (question_id IS NULL AND group_id IS NOT NULL));

-- Categories belong to either question OR group, never both  
ALTER TABLE verbatim_categories ADD CONSTRAINT check_single_parent
CHECK ((question_id IS NOT NULL AND group_id IS NULL) OR 
       (question_id IS NULL AND group_id IS NOT NULL));

-- Grouped questions cannot be individually assigned
ALTER TABLE verbatim_questions ADD CONSTRAINT check_group_assignment
CHECK ((group_id IS NULL) OR (group_id IS NOT NULL AND is_assigned = FALSE));
```

#### Application-Level Validation
1. **Question Selection**: Prevent selection of grouped questions individually
2. **Group Operations**: Validate user permissions and group state
3. **Status Consistency**: Ensure group status reflects all member questions

## API Design

### New Endpoints
```python
# Group Management
POST   /verbatim/groups/file/{file_id}           # Create group
GET    /verbatim/groups/file/{file_id}           # List groups  
PUT    /verbatim/groups/{group_id}               # Update group
DELETE /verbatim/groups/{group_id}               # Delete group

# Group Operations  
POST   /verbatim/groups/{group_id}/generate-codebook
POST   /verbatim/groups/{group_id}/assign-codebook
GET    /verbatim/groups/{group_id}/codes
GET    /verbatim/groups/{group_id}/status
```

### Enhanced Existing Endpoints
```python
# Updated to detect and handle grouped questions
GET    /verbatim/question/{question_id}/codes    # Show group codes if grouped
POST   /verbatim/question/{question_id}/generate-codebook  # Error if grouped
```

## Migration Strategy

### Phase 1: Infrastructure Setup
1. **Database Migrations** (2 migrations):
   - Create new table and enum
   - Add foreign key columns to existing tables
   - Add validation constraints

2. **Model Updates**:
   - Add new SQLAlchemy models
   - Update existing models with group relationships
   - Add enum definitions

### Phase 2: Service Layer Implementation
1. **New Service**: `VerbatimQuestionGroupService`
   - Group creation and validation
   - Group codebook generation
   - Group deletion and cleanup

2. **Updated Services**:
   - `VerbatimQuestionService`: Handle grouped question detection
   - `VerbatimCodeService`: Support group-based code retrieval
   - Worker services: Group-aware codebook generation

### Phase 3: API Layer Implementation
1. **New Controller**: `VerbatimGroupController`
2. **Updated Controllers**: Enhanced error handling for grouped questions
3. **Schema Updates**: Request/response models for group operations

### Phase 4: Testing & Rollout
1. **Unit Tests**: Group creation, validation, operations
2. **Integration Tests**: End-to-end workflows, error scenarios
3. **Performance Tests**: Large groups, concurrent operations
4. **User Acceptance Testing**: UI/UX validation

## Business Impact

### Benefits
1. **Improved Efficiency**: Shared codebooks reduce duplication
2. **Better Analysis**: Consistent coding across related questions
3. **User Experience**: Simplified workflow for question sets
4. **Data Quality**: Unified coding approach for similar questions

### Constraints & Limitations
1. **All-or-Nothing**: Must delete entire group if errors occur
2. **Group Lock-in**: Questions cannot be individually modified once grouped
3. **Complexity**: Additional layer of management for users
4. **Migration**: Existing individual questions remain separate

## Risk Mitigation

### Technical Risks
1. **Data Consistency**: Comprehensive validation constraints prevent invalid states
2. **Performance**: Efficient indexing and query optimization for group operations
3. **Backward Compatibility**: Existing workflows remain unchanged

### User Experience Risks  
1. **Learning Curve**: Provide clear documentation and training
2. **Error Recovery**: Implement comprehensive error messages and recovery options
3. **Feature Discovery**: Intuitive UI design for group management

## Success Metrics

### Technical Metrics
1. **Database Performance**: Query response times <100ms for group operations
2. **Data Integrity**: Zero constraint violations in production
3. **Backward Compatibility**: 100% existing functionality preserved

### Business Metrics
1. **User Adoption**: % of new projects using question groups
2. **Efficiency Gains**: Reduced time for codebook creation/assignment
3. **Data Quality**: Consistency scores for grouped vs individual questions

## Conclusion

The proposed question grouping feature provides a robust, scalable solution that:

1. **Maintains System Integrity**: Strong constraints prevent invalid data states
2. **Preserves Existing Functionality**: Zero impact on current workflows
3. **Enables New Capabilities**: Shared codebooks for related questions
4. **Supports Future Growth**: Extensible design for additional group features

The implementation follows ResAuto's established patterns and maintains the high standards of data quality and system reliability that users expect.