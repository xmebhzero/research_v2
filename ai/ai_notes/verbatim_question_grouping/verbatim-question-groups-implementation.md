# ResAuto Verbatim Question Groups - Implementation Guide

## Database Migration Plan

### Migration 1: Create Base Tables and Enums
**File**: `migrations/versions/xxxx_create_verbatim_question_groups.py`

```python
"""Create verbatim question groups tables

Revision ID: xxxx_create_verbatim_question_groups
Revises: [latest_migration]
Create Date: 2025-09-18
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    # Create enum for group status
    op.execute("CREATE TYPE verbatim_group_status_enum AS ENUM ('NOT_STARTED', 'GENERATING_CODEBOOK', 'CODEBOOK_GENERATED', 'CODING', 'COMPLETED', 'FAILED')")
    
    # Create verbatim_question_groups table
    op.create_table(
        'verbatim_question_groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('file_id', sa.Integer(), nullable=False),
        sa.Column('group_name', sa.String(255), nullable=False),
        sa.Column('status', sa.Enum(name='verbatim_group_status_enum'), nullable=False, server_default='NOT_STARTED'),
        sa.Column('is_assigned', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['file_id'], ['files.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('file_id', 'group_name', 'deleted_at', name='uq_verbatim_question_groups_file_name_deleted')
    )
    
    # Add indexes
    op.create_index(op.f('ix_verbatim_question_groups_id'), 'verbatim_question_groups', ['id'], unique=False)
    op.create_index(op.f('ix_verbatim_question_groups_project_id'), 'verbatim_question_groups', ['project_id'], unique=False)
    op.create_index(op.f('ix_verbatim_question_groups_file_id'), 'verbatim_question_groups', ['file_id'], unique=False)
    op.create_index(op.f('ix_verbatim_question_groups_status'), 'verbatim_question_groups', ['status'], unique=False)

def downgrade() -> None:
    # Drop table
    op.drop_table('verbatim_question_groups')
    
    # Drop enum
    op.execute("DROP TYPE verbatim_group_status_enum")
```

### Migration 2: Add Foreign Key Columns
**File**: `migrations/versions/xxxx_add_group_foreign_keys.py`

```python
"""Add group_id foreign keys to existing tables

Revision ID: xxxx_add_group_foreign_keys  
Revises: xxxx_create_verbatim_question_groups
Create Date: 2025-09-18
"""

from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Add group_id to verbatim_questions
    op.add_column('verbatim_questions', sa.Column('group_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_verbatim_questions_group_id'), 'verbatim_questions', ['group_id'], unique=False)
    op.create_foreign_key('fk_verbatim_questions_group_id', 'verbatim_questions', 'verbatim_question_groups', ['group_id'], ['id'], ondelete='SET NULL')
    
    # Add group_id to verbatim_codes
    op.add_column('verbatim_codes', sa.Column('group_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_verbatim_codes_group_id'), 'verbatim_codes', ['group_id'], unique=False)
    op.create_foreign_key('fk_verbatim_codes_group_id', 'verbatim_codes', 'verbatim_question_groups', ['group_id'], ['id'], ondelete='CASCADE')
    
    # Add group_id to verbatim_categories
    op.add_column('verbatim_categories', sa.Column('group_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_verbatim_categories_group_id'), 'verbatim_categories', ['group_id'], unique=False)
    op.create_foreign_key('fk_verbatim_categories_group_id', 'verbatim_categories', 'verbatim_question_groups', ['group_id'], ['id'], ondelete='CASCADE')

def downgrade() -> None:
    # Remove foreign keys and columns in reverse order
    op.drop_constraint('fk_verbatim_categories_group_id', 'verbatim_categories', type_='foreignkey')
    op.drop_index(op.f('ix_verbatim_categories_group_id'), table_name='verbatim_categories')
    op.drop_column('verbatim_categories', 'group_id')
    
    op.drop_constraint('fk_verbatim_codes_group_id', 'verbatim_codes', type_='foreignkey')
    op.drop_index(op.f('ix_verbatim_codes_group_id'), table_name='verbatim_codes')
    op.drop_column('verbatim_codes', 'group_id')
    
    op.drop_constraint('fk_verbatim_questions_group_id', 'verbatim_questions', type_='foreignkey')
    op.drop_index(op.f('ix_verbatim_questions_group_id'), table_name='verbatim_questions')
    op.drop_column('verbatim_questions', 'group_id')
```

### Migration 3: Add Data Validation Constraints
**File**: `migrations/versions/xxxx_add_group_validation_constraints.py`

```python
"""Add validation constraints for question groups

Revision ID: xxxx_add_group_validation_constraints
Revises: xxxx_add_group_foreign_keys
Create Date: 2025-09-18
"""

from alembic import op

def upgrade() -> None:
    # Ensure codes belong to either question OR group, not both
    op.execute("""
        ALTER TABLE verbatim_codes 
        ADD CONSTRAINT check_verbatim_codes_single_parent 
        CHECK (
            (question_id IS NOT NULL AND group_id IS NULL) OR 
            (question_id IS NULL AND group_id IS NOT NULL)
        )
    """)
    
    # Ensure categories belong to either question OR group, not both
    op.execute("""
        ALTER TABLE verbatim_categories 
        ADD CONSTRAINT check_verbatim_categories_single_parent 
        CHECK (
            (question_id IS NOT NULL AND group_id IS NULL) OR 
            (question_id IS NULL AND group_id IS NOT NULL)
        )
    """)
    
    # Ensure grouped questions don't have individual assignments
    op.execute("""
        ALTER TABLE verbatim_questions 
        ADD CONSTRAINT check_verbatim_questions_group_assignment 
        CHECK (
            (group_id IS NULL) OR 
            (group_id IS NOT NULL AND is_assigned = FALSE)
        )
    """)

def downgrade() -> None:
    op.execute("ALTER TABLE verbatim_questions DROP CONSTRAINT check_verbatim_questions_group_assignment")
    op.execute("ALTER TABLE verbatim_categories DROP CONSTRAINT check_verbatim_categories_single_parent")
    op.execute("ALTER TABLE verbatim_codes DROP CONSTRAINT check_verbatim_codes_single_parent")
```

## Model Definitions

### New SQLAlchemy Models
**File**: `src/core/postgres_model.py` (additions)

```python
### New SQLAlchemy Models
**File**: `src/core/postgres_model.py` (additions)

```python
class VerbatimGroupStatusEnum(Enum):
    NOT_STARTED = "NOT_STARTED"
    GENERATING_CODEBOOK = "GENERATING_CODEBOOK"
    CODEBOOK_GENERATED = "CODEBOOK_GENERATED"
    CODING = "CODING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class VerbatimQuestionGroup(TimeStampedTable, Base):
    __tablename__ = "verbatim_question_groups"
    
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"), nullable=False, index=True)
    group_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[VerbatimGroupStatusEnum] = mapped_column(
        Enum(VerbatimGroupStatusEnum), 
        nullable=False, 
        default=VerbatimGroupStatusEnum.NOT_STARTED.value,
        server_default=text("'NOT_STARTED'")
    )
    is_assigned: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"), default=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    
    # Relationships
    questions: Mapped[list["VerbatimQuestion"]] = relationship("VerbatimQuestion", back_populates="group")
    codes: Mapped[list["VerbatimCode"]] = relationship("VerbatimCode", back_populates="group")
    categories: Mapped[list["VerbatimCategory"]] = relationship("VerbatimCategory", back_populates="group")
    
    __table_args__ = (
        UniqueConstraint(
            "file_id", "group_name", "deleted_at",
            name="uq_verbatim_question_groups_file_name_deleted"
        ),
        Index("ix_verbatim_question_groups_status", "status"),
    )

# Updated existing models to include group relationships
class VerbatimQuestion(TimeStampedTable, Base):
    # ... existing fields ...
    group_id: Mapped[int] = mapped_column(ForeignKey("verbatim_question_groups.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Updated relationships
    group: Mapped["VerbatimQuestionGroup"] = relationship("VerbatimQuestionGroup", back_populates="questions")

class VerbatimCode(TimeStampedTable, Base):
    # ... existing fields ...
    group_id: Mapped[int] = mapped_column(ForeignKey("verbatim_question_groups.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Updated relationships
    group: Mapped["VerbatimQuestionGroup"] = relationship("VerbatimQuestionGroup", back_populates="codes")

class VerbatimCategory(TimeStampedTable, Base):
    # ... existing fields ...
    group_id: Mapped[int] = mapped_column(ForeignKey("verbatim_question_groups.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Updated relationships
    group: Mapped["VerbatimQuestionGroup"] = relationship("VerbatimQuestionGroup", back_populates="categories")
```

class VerbatimQuestionGroupMember(TimeStampedTable, Base):
    __tablename__ = "verbatim_question_group_members"
    
    group_id: Mapped[int] = mapped_column(ForeignKey("verbatim_question_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("verbatim_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relationships
    group: Mapped["VerbatimQuestionGroup"] = relationship("VerbatimQuestionGroup")
    question: Mapped["VerbatimQuestion"] = relationship("VerbatimQuestion")
    
    __table_args__ = (
        UniqueConstraint("question_id", name="uq_verbatim_question_group_members_question_id"),
    )

# Updated existing models to include group relationships
class VerbatimQuestion(TimeStampedTable, Base):
    # ... existing fields ...
    group_id: Mapped[int] = mapped_column(ForeignKey("verbatim_question_groups.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Updated relationships
    group: Mapped["VerbatimQuestionGroup"] = relationship("VerbatimQuestionGroup", back_populates="questions")

class VerbatimCode(TimeStampedTable, Base):
    # ... existing fields ...
    group_id: Mapped[int] = mapped_column(ForeignKey("verbatim_question_groups.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Updated relationships
    group: Mapped["VerbatimQuestionGroup"] = relationship("VerbatimQuestionGroup", back_populates="codes")

class VerbatimCategory(TimeStampedTable, Base):
    # ... existing fields ...
    group_id: Mapped[int] = mapped_column(ForeignKey("verbatim_question_groups.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Updated relationships
    group: Mapped["VerbatimQuestionGroup"] = relationship("VerbatimQuestionGroup", back_populates="categories")
```

## Business Logic Implementation

### Service Layer Changes

#### New Service: VerbatimQuestionGroupService
**File**: `src/modules/verbatim/services/verbatim_question_group_service.py`

```python
@container.register
@trace_class_methods
class VerbatimQuestionGroupService:
    def __init__(
        self,
        verbatim_question_group_postgres_repository: VerbatimQuestionGroupPostgresRepository,
        verbatim_question_postgres_repository: VerbatimQuestionPostgresRepository,
        verbatim_code_service: VerbatimCodeService,
        file_postgres_repository: FilePostgresRepository,
        project_postgres_repository: ProjectPostgresRepository,
    ):
        self._group_repo = verbatim_question_group_postgres_repository
        self._question_repo = verbatim_question_postgres_repository
        self._code_service = verbatim_code_service
        self._file_repo = file_postgres_repository
        self._project_repo = project_postgres_repository
    
    async def create_question_group(
        self, 
        user_id: int, 
        file_id: int, 
        question_ids: list[int], 
        group_name: str
    ) -> VerbatimQuestionGroup:
        """Create a new question group with validation."""
        
        # Validate file access
        file_detail = await self._file_repo.get_file_by_id(file_id=file_id)
        if not file_detail or file_detail.user_id != user_id:
            raise UnauthorizedError("File not found or unauthorized")
        
        # Validate questions
        await self._validate_questions_for_grouping(question_ids, file_id)
        
        # Generate group name from question codes
        group_name = await self._generate_group_name(question_ids)
        
        async with start_autocommit_transaction() as db_trx:
            # Create group
            group = await self._group_repo.create(
                CreateVerbatimQuestionGroupParams(
                    project_id=file_detail.project_id,
                    file_id=file_id,
                    group_name=group_name,
                ),
                session=db_trx
            )
            
            # Update questions with group_id (establishes membership)
            await self._question_repo.update_questions_group_id(
                question_ids=question_ids,
                group_id=group.id,
                session=db_trx
            )
        
        return group
    
    async def _validate_questions_for_grouping(self, question_ids: list[int], file_id: int) -> None:
        """Validate that questions can be grouped together."""
        
        # Check all questions exist and belong to the file
        questions = await self._question_repo.get_questions_by_ids(question_ids)
        if len(questions) != len(question_ids):
            raise BadRequestError("One or more questions not found")
        
        for question in questions:
            if question.file_id != file_id:
                raise BadRequestError("All questions must belong to the same file")
            
            if question.group_id is not None:
                raise BadRequestError(f"Question {question.id} is already in a group")
            
            if question.is_assigned:
                raise BadRequestError(f"Question {question.id} already has assigned codes")
            
            if question.status not in [VerbatimQuestionStatusEnum.NOT_STARTED, VerbatimQuestionStatusEnum.CODING_FAILED]:
                raise BadRequestError(f"Question {question.id} has incompatible status: {question.status}")
    
    async def _generate_group_name(self, question_ids: list[int]) -> str:
        """Generate group name based on question identifiers."""
        questions = await self._question_repo.get_questions_by_ids(question_ids)
        
        # Extract question codes from question text (e.g., "Q1.", "A2.", etc.)
        question_codes = []
        for question in sorted(questions, key=lambda q: q.id):
            # Use regex to extract question code from question text
            import re
            match = re.match(r'^([A-Za-z]+\d+[A-Za-z]*\.?)', question.question.strip())
            if match:
                code = match.group(1).rstrip('.')
                question_codes.append(code)
            else:
                # Fallback to question ID if no pattern found
                question_codes.append(f"Q{question.id}")
        
        return "_".join(question_codes)
    
    async def generate_group_codebook(self, user_id: int, group_id: int) -> GenerateCodebookResponse:
        """Generate codebook for all questions in a group."""
        
        group = await self._group_repo.get_by_id(group_id)
        if not group:
            raise NotFoundError("Question group not found")
        
        # Validate user access
        project = await self._project_repo.get_by_id(group.project_id)
        if not project or project.user_id != user_id:
            raise UnauthorizedError("Unauthorized access to group")
        
        if group.status not in [VerbatimGroupStatusEnum.NOT_STARTED, VerbatimGroupStatusEnum.FAILED]:
            raise BadRequestError("Group is not in a valid state for codebook generation")
        
        # Update group status
        await self._group_repo.update_status(group_id, VerbatimGroupStatusEnum.GENERATING_CODEBOOK)
        
        # Trigger background task for codebook generation
        # This will combine responses from all questions in the group
        self._celery_task_dispatcher.send_generate_group_codebook_task(
            group_id=group_id,
            user_id=user_id
        )
        
        return GenerateCodebookResponse(
            question_id=None,  # For groups, this is None
            group_id=group_id,
            status=VerbatimGroupStatusEnum.GENERATING_CODEBOOK
        )
    
    async def delete_group(self, user_id: int, group_id: int) -> None:
        """Delete a question group and reset questions to individual state."""
        
        group = await self._group_repo.get_by_id(group_id)
        if not group:
            raise NotFoundError("Question group not found")
        
        # Validate user access
        project = await self._project_repo.get_by_id(group.project_id)
        if not project or project.user_id != user_id:
            raise UnauthorizedError("Unauthorized access to group")
        
        async with start_autocommit_transaction() as db_trx:
            # Reset questions to individual state (remove group_id)
            questions = await self._question_repo.get_questions_by_group_id(group_id)
            question_ids = [q.id for q in questions]
            
            await self._question_repo.update_questions_group_id(
                question_ids=question_ids,
                group_id=None,
                session=db_trx
            )
            
            # Soft delete the group (this will cascade delete codes/categories via DB constraints)
            await self._group_repo.soft_delete(group_id, session=db_trx)
```

### Updated VerbatimQuestionService

```python
# In existing VerbatimQuestionService, update methods to handle groups

async def generate_codebook_by_question(self, user_id: int, question_id: int) -> GenerateCodebookResponse:
    """Generate codebook - updated to handle grouped questions."""
    
    question = await self._verbatim_question_postgres_repo.get_by_id(question_id)
    if not question:
        raise NotFoundError("Question not found")
    
    # Check if question is in a group
    if question.group_id is not None:
        raise BadRequestError(
            "This question is part of a group. Generate codebook for the entire group instead."
        )
    
    # Continue with existing individual question logic
    # ... rest of existing implementation
```

## API Endpoints

### New Controllers
**File**: `src/modules/verbatim/controllers/verbatim_group_controller.py`

```python
verbatim_group_router = APIRouter(prefix="/verbatim/groups", tags=["Verbatim Groups"])

@verbatim_group_router.post(
    path="/file/{file_id}",
    summary="Create question group",
    description="Create a group of questions that will share a common codebook",
    status_code=status.HTTP_201_CREATED,
    response_model=BaseResponse[VerbatimQuestionGroupResponse],
)
@container.autowire
async def create_question_group(
    request: Request,
    file_id: Annotated[int, Path(ge=0, description="ID of the file")],
    body: CreateQuestionGroupRequest,
    verbatim_group_service: Annotated[VerbatimQuestionGroupService, Inject()],
) -> ORJSONResponse:
    user: UserState = request.state.user
    result = await verbatim_group_service.create_question_group(
        user_id=user.id,
        file_id=file_id,
        question_ids=body.question_ids,
        group_name=body.group_name
    )
    
    return ORJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=BaseResponse[VerbatimQuestionGroupResponse](result=result).model_dump(),
    )

@verbatim_group_router.post(
    path="/{group_id}/generate-codebook",
    summary="Generate codebook for question group",
    description="Generate a shared codebook for all questions in the group",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse[GenerateCodebookResponse],
)
@container.autowire
async def generate_group_codebook(
    request: Request,
    group_id: Annotated[int, Path(ge=0, description="ID of the group")],
    verbatim_group_service: Annotated[VerbatimQuestionGroupService, Inject()],
) -> ORJSONResponse:
    user: UserState = request.state.user
    result = await verbatim_group_service.generate_group_codebook(
        user_id=user.id,
        group_id=group_id
    )
    
    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content=BaseResponse[GenerateCodebookResponse](result=result).model_dump(),
    )

@verbatim_group_router.delete(
    path="/{group_id}",
    summary="Delete question group",
    description="Delete a question group and reset questions to individual state",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse[BasicSuccessResponse],
)
@container.autowire
async def delete_question_group(
    request: Request,
    group_id: Annotated[int, Path(ge=0, description="ID of the group")],
    verbatim_group_service: Annotated[VerbatimQuestionGroupService, Inject()],
) -> ORJSONResponse:
    user: UserState = request.state.user
    await verbatim_group_service.delete_group(user_id=user.id, group_id=group_id)
    
    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content=BaseResponse[BasicSuccessResponse](result={"success": True}).model_dump(),
    )
```

## Testing Strategy

### Unit Tests
1. **Group Creation**: Test validation rules and group code generation
2. **Codebook Generation**: Test shared codebook creation from multiple questions
3. **Group Deletion**: Test cleanup and question state reset
4. **Constraint Validation**: Test database constraints and business rules

### Integration Tests
1. **End-to-end Workflow**: Create group → Generate codebook → Assign codes
2. **Error Scenarios**: Invalid group operations, constraint violations
3. **Backward Compatibility**: Ensure existing individual question workflows work

### Performance Tests
1. **Large Groups**: Test with groups containing many questions
2. **Concurrent Operations**: Test multiple users creating groups simultaneously
3. **Database Performance**: Test query performance with group-related joins

## Rollout Plan

### Phase 1: Infrastructure (Week 1-2)
1. Deploy database migrations
2. Add new models and repositories
3. Update existing services for compatibility

### Phase 2: Core Logic (Week 3-4)
1. Implement group management services
2. Update codebook generation for groups
3. Add API endpoints

### Phase 3: UI Integration (Week 5-6)
1. Frontend components for group management
2. Updated question selection interface
3. Group status tracking

### Phase 4: Testing & Optimization (Week 7-8)
1. Comprehensive testing
2. Performance optimization
3. Documentation and training

### Phase 5: Production Rollout (Week 9-10)
1. Gradual feature rollout
2. User training and support
3. Monitoring and bug fixes