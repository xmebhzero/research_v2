# ResAuto Verbatim Question Groups - Database Schema Design

## Overview
This document outlines the database schema design for the new question grouping feature in the ResAuto Verbatim module.

## New Tables

### 1. `verbatim_question_groups`
**Purpose**: Central table to manage groups of questions that share a common codebook.

```sql
CREATE TABLE verbatim_question_groups (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id),
    file_id INTEGER NOT NULL REFERENCES files(id),
    group_name VARCHAR(255) NOT NULL, -- Contains question codes (e.g., "Q1_Q3_Q7")
    status verbatim_group_status_enum NOT NULL DEFAULT 'NOT_STARTED',
    is_assigned BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL,
    
    INDEX idx_verbatim_question_groups_project_id (project_id),
    INDEX idx_verbatim_question_groups_file_id (file_id),
    INDEX idx_verbatim_question_groups_status (status),
    UNIQUE KEY unique_group_name_per_file (file_id, group_name, deleted_at)
);
```

**Key Fields:**
- `group_name`: Contains the question codes forming the group (e.g., "Q1_Q3_Q7")
- `status`: Tracks the group's processing status
- `is_assigned`: Whether codebook has been assigned to responses

**Note**: No separate junction table is needed since the relationship is established via `group_id` in the `verbatim_questions` table.

## Modified Tables

### 2. Updates to `verbatim_questions`
**New Fields:**
```sql
ALTER TABLE verbatim_questions 
ADD COLUMN group_id INTEGER NULL REFERENCES verbatim_question_groups(id) ON DELETE SET NULL,
ADD INDEX idx_verbatim_questions_group_id (group_id),
ADD UNIQUE KEY unique_question_group_membership (id, group_id); -- Ensures clean group membership
```

**Purpose**: Direct reference to the group. This establishes the one-to-many relationship where a group can have many questions, but each question belongs to at most one group.

### 3. Updates to `verbatim_codes`
**New Fields:**
```sql
ALTER TABLE verbatim_codes 
ADD COLUMN group_id INTEGER NULL REFERENCES verbatim_question_groups(id) ON DELETE CASCADE,
ADD INDEX idx_verbatim_codes_group_id (group_id);
```

**Purpose**: Links codes to groups instead of individual questions when grouped.

### 4. Updates to `verbatim_categories`
**New Fields:**
```sql
ALTER TABLE verbatim_categories 
ADD COLUMN group_id INTEGER NULL REFERENCES verbatim_question_groups(id) ON DELETE CASCADE,
ADD INDEX idx_verbatim_categories_group_id (group_id);
```

**Purpose**: Links categories to groups for shared categorization.

## New Enums

### `verbatim_group_status_enum`
```sql
CREATE TYPE verbatim_group_status_enum AS ENUM (
    'NOT_STARTED',
    'GENERATING_CODEBOOK', 
    'CODEBOOK_GENERATED',
    'CODING',
    'COMPLETED',
    'FAILED'
);
```

**Status Flow:**
1. `NOT_STARTED`: Group created, ready for codebook generation
2. `GENERATING_CODEBOOK`: AI is generating the shared codebook
3. `CODEBOOK_GENERATED`: Codebook ready for review/assignment
4. `CODING`: Assigning codes to responses across all group questions
5. `COMPLETED`: All questions in group have assigned codes
6. `FAILED`: Process failed, can retry

## Business Logic Changes

### Question Selection Rules
1. **Individual Questions**: Continue to work as before if not in a group
2. **Grouped Questions**: 
   - Cannot be selected individually once in a group
   - Group selection applies to all member questions
   - Must delete entire group to modify membership

### Codebook Generation Rules
1. **Individual Questions**: Generate codebook for single question (existing logic)
2. **Grouped Questions**: 
   - Generate shared codebook using responses from ALL questions in group
   - Store codes with `group_id` instead of `question_id`
   - Use combined responses for better AI training

### Code Assignment Rules
1. **Individual Questions**: Assign codes to responses of single question
2. **Grouped Questions**:
   - Assign shared codebook codes to responses across ALL questions in group
   - Use same confidence scoring and assignment logic
   - Track assignments per question via existing `verbatim_response_code` table

## Data Consistency Rules

### Constraints & Validations
1. **Group Membership**: A question can only be in one group (enforced by `group_id` foreign key)
2. **Group Status**: Questions in a group must have compatible statuses
3. **Codebook Isolation**: Codes belong either to a question OR a group, never both
4. **Assignment State**: If any question in group is assigned, entire group is assigned

### Validation Logic
```sql
-- Ensure codes belong to either question OR group, not both
CONSTRAINT check_verbatim_codes_single_parent 
CHECK (
    (question_id IS NOT NULL AND group_id IS NULL) OR 
    (question_id IS NULL AND group_id IS NOT NULL)
);

-- Ensure categories belong to either question OR group, not both
CONSTRAINT check_verbatim_categories_single_parent
CHECK (
    (question_id IS NOT NULL AND group_id IS NULL) OR 
    (question_id IS NULL AND group_id IS NOT NULL)
);

-- Ensure questions in group aren't individually assigned
CONSTRAINT check_verbatim_questions_group_assignment
CHECK (
    (group_id IS NULL) OR 
    (group_id IS NOT NULL AND is_assigned = FALSE)
);
```

## Migration Strategy

### Phase 1: Schema Creation
1. Create new table (`verbatim_question_groups`)
2. Add new enum (`verbatim_group_status_enum`)
3. Add new columns to existing tables (`group_id` foreign keys)

### Phase 2: Data Migration
1. All existing questions remain individual (group_id = NULL)
2. Update application code to handle both individual and grouped questions
3. Add validation constraints

### Phase 3: Feature Rollout
1. Deploy new UI for group management
2. Enable group creation functionality
3. Test codebook generation and assignment for groups

## API Changes Required

### New Endpoints
```python
# Group Management
POST /verbatim/file/{file_id}/question-groups
GET /verbatim/file/{file_id}/question-groups  
PUT /verbatim/group/{group_id}
DELETE /verbatim/group/{group_id}

# Group Operations
POST /verbatim/group/{group_id}/generate-codebook
POST /verbatim/group/{group_id}/assign-codebook
GET /verbatim/group/{group_id}/codes
```

### Modified Endpoints
```python
# Enhanced to support both individual and group contexts
GET /verbatim/question/{question_id}/codes  # Show group codes if question is grouped
POST /verbatim/question/{question_id}/generate-codebook  # Error if question is grouped
```

## Performance Considerations

### Indexing Strategy
- Group lookups: `idx_verbatim_questions_group_id`
- Group status queries: `idx_verbatim_question_groups_status`
- Code retrieval: `idx_verbatim_codes_group_id`

### Query Optimization
- Use denormalized `group_id` in questions table for faster joins
- Implement efficient group membership checks
- Cache group metadata for frequent operations

## Backward Compatibility

### Existing Functionality
- All existing individual question workflows remain unchanged
- Existing codebooks and assignments are preserved
- No changes to response data structure

### Migration Safety
- Default `group_id` is NULL (individual questions)
- Existing code continues to work for non-grouped questions
- Gradual migration allows testing before full adoption