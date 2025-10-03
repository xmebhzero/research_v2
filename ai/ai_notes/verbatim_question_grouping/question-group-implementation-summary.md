# Question Group Implementation Summary

## Overview
This implementation adds the ability to group verbatim questions together to share common codebooks. The feature includes a new REST endpoint, service layer, and repository for managing question groups.

## Components Created

### 1. Repository Layer
**File**: `src/modules/verbatim/repositories/verbatim_question_group_postgres_repository.py`
- `VerbatimQuestionGroupPostgresRepository`
- Methods:
  - `create_question_group()`: Creates a new question group
  - `get_by_id()`: Retrieves a question group by ID
  - `update_questions_group_id()`: Assigns questions to a group

### 2. Service Layer  
**File**: `src/modules/verbatim/services/verbatim_question_group_service.py`
- `VerbatimQuestionGroupService`
- Methods:
  - `create_question_group()`: Main business logic for creating groups
  - `_validate_file_and_project_access()`: Validates user permissions
  - `_get_and_validate_questions()`: Validates question requirements
  - `_generate_group_name()`: Creates group name from question codes

### 3. Schema Layer
**File**: `src/modules/verbatim/schemas/verbatim_question_group_schema.py`
- `CreateQuestionGroupRequest`: API request schema
- `CreateQuestionGroupParams`: Internal service parameters

### 4. Controller Layer
**File**: `src/modules/verbatim/controllers/verbatim_controller.py`
- New endpoint: `POST /verbatim/file/{file_id}/question-group`

### 5. Repository Enhancement
**File**: `src/modules/verbatim/repositories/verbatim_question_postgres_repository.py`
- Added `get_questions_by_ids()` method for batch question retrieval

## API Specification

### Endpoint
```
POST /verbatim/file/{file_id}/question-group
```

### Request Body
```json
{
  "question_ids": [2, 3]
}
```

### Response
```json
{
  "result": {
    "id": 1
  }
}
```

## Validation Rules

1. **Question Count**: Maximum 10 questions per group
2. **Question Status**: All questions must have `NOT_STARTED` status
3. **Question Group**: Questions must not already belong to another group
4. **File Association**: All questions must belong to the specified file
5. **User Authorization**: User must own the project containing the file

## Database Schema

The implementation leverages existing database schema:
- `verbatim_question_groups` table (already exists)
- `question_group_id` foreign key in `verbatim_questions` (already exists)
- `question_group_id` foreign key in `verbatim_codes` (already exists)
- `question_group_id` foreign key in `verbatim_categories` (already exists)

## Transaction Management

The service uses database transactions (`start_autocommit_transaction`) to ensure:
1. Question group creation
2. Question assignment to group
3. Rollback on any validation failure

## Group Naming Convention

Group names are automatically generated from question codes:
- Extracts question codes like "Q1", "Q2" from question text
- Falls back to sequence numbering if codes not found
- Format: "Q1, Q2, Q3"

## Integration Points

The implementation integrates with existing services:
- `FilePostgresRepository`: File validation
- `ProjectPostgresRepository`: Project authorization
- `VerbatimQuestionPostgresRepository`: Question validation and updates

## Benefits

1. **Performance**: Maintains direct foreign key relationships for efficient queries
2. **Compatibility**: Zero impact on existing individual question workflows  
3. **Validation**: Comprehensive input validation and authorization checks
4. **Transaction Safety**: Uses database transactions for data consistency
5. **Extensibility**: Clean architecture supports future grouping features

## Usage Flow

1. User selects questions from a file
2. POST request to `/verbatim/file/{file_id}/question-group` with question IDs
3. System validates questions and user permissions
4. Creates question group with auto-generated name
5. Assigns questions to the group
6. Returns group ID for future operations

This implementation provides a solid foundation for question grouping while maintaining the existing system's performance and reliability.