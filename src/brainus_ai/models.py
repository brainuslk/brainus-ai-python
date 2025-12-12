"""Data models for the Brainus AI SDK."""

from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator


class Citation(BaseModel):
    """A citation from a source document."""

    document_id: str = Field(..., description="Unique document identifier")
    document_name: str = Field(..., description="Name of the source document")
    pages: list[int] = Field(default_factory=list, description="Page numbers referenced")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    chunk_text: Optional[str] = Field(None, description="Relevant text chunk")

    @field_validator("pages", mode="before")
    @classmethod
    def validate_pages(cls, v: Any) -> Any:
        if v is None:
            return []
        return v

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata(cls, v: Any) -> Any:
        if v is None:
            return {}
        return v


class QueryFilters(BaseModel):
    """Metadata filters for query."""

    subject: Optional[str] = Field(None, description="Subject filter (e.g., ICT, Science)")
    grade: Optional[str] = Field(None, description="Grade level filter (e.g., 10, 11, 12)")
    year: Optional[str] = Field(None, description="Year filter (e.g., 2023, 2024)")
    category: Optional[str] = Field(None, description="Category filter (Past Paper, Textbook, etc.)")
    language: Optional[str] = Field(None, description="Language filter (English, Sinhala, Tamil)")


class QueryRequest(BaseModel):
    """Request model for querying the AI."""

    query: str = Field(..., min_length=1, max_length=1000, description="The query text")
    store_id: Optional[str] = Field(None, description="Store ID (optional - uses default if not provided)")
    filters: Optional[QueryFilters] = Field(None, description="Optional metadata filters")
    model: Optional[str] = Field(None, description="Gemini model to use (must be in your plan's allowed_models)")


class QueryResponse(BaseModel):
    """Response model from a query."""

    answer: str = Field(..., description="The generated answer")
    citations: list[Citation] = Field(default_factory=list, description="Source citations")
    has_citations: bool = Field(..., description="Whether citations are available")


class PlanInfo(BaseModel):
    """Plan information included in usage stats."""

    name: str = Field(..., description="Plan name")
    rate_limit_per_minute: int = Field(..., description="Rate limit per minute")
    rate_limit_per_day: int = Field(..., description="Rate limit per day")
    monthly_quota: Optional[int] = Field(None, description="Monthly quota")


class UsageStats(BaseModel):
    """API usage statistics."""

    total_requests: int = Field(..., description="Total requests this period")
    total_tokens: Optional[int] = Field(None, description="Total tokens used")
    total_cost_usd: Optional[float] = Field(None, description="Total cost in USD")
    by_endpoint: dict[str, int] = Field(
        default_factory=dict, description="Request count per endpoint"
    )
    quota_remaining: Optional[int] = Field(None, description="Remaining quota")
    quota_percentage: Optional[float] = Field(None, description="Percentage of quota used")
    plan: Optional[PlanInfo] = Field(None, description="Plan information")
    period_start: Optional[str] = Field(None, description="Period start date")
    period_end: Optional[str] = Field(None, description="Period end date")


class Plan(BaseModel):
    """API subscription plan."""

    id: str
    name: str
    description: Optional[str] = None
    rate_limit_per_minute: int
    rate_limit_per_day: int
    monthly_quota: Optional[int] = None
    price_lkr: Optional[float] = Field(None, description="Price in LKR (null = free)")
    allowed_models: list[str] = Field(default_factory=list, description="Allowed models for this plan")
    features: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True



