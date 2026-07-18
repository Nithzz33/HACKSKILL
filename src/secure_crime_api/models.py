from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


Role = Literal["super_admin", "supervisor", "investigator", "analyst", "policymaker", "viewer"]
CaseStatus = Literal["open", "under_review", "closed"]
Sensitivity = Literal["standard", "restricted"]


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str = Field(min_length=12, max_length=256)
    full_name: str = Field(min_length=1, max_length=120)
    role: Role
    district: str = Field(min_length=1, max_length=80)
    is_active: bool = True


class UserPublic(BaseModel):
    id: str
    username: str
    full_name: str
    role: Role
    district: str
    is_active: bool = True


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=120)
    role: Role | None = None
    district: str | None = Field(default=None, min_length=1, max_length=80)
    is_active: bool | None = None


class PasswordResetRequest(BaseModel):
    password: str = Field(min_length=12, max_length=256)


class AuthenticatedUser(UserPublic):
    jti: str


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserPublic


class CaseCreate(BaseModel):
    fir_number: str = Field(min_length=1, max_length=40)
    year: int = Field(ge=1900, le=2200)
    district: str = Field(min_length=1, max_length=80)
    status: CaseStatus = "open"
    case_type: str | None = Field(default=None, max_length=120)
    modus_operandi: str | None = Field(default=None, max_length=240)
    incident_at: datetime | None = None
    complainant_name: str = Field(min_length=1, max_length=120)
    complainant_phone: str = Field(min_length=4, max_length=30)
    victim_name: str = Field(min_length=1, max_length=120)
    victim_age: int | None = Field(default=None, ge=0, le=120)
    victim_gender: str | None = Field(default=None, max_length=40)
    suspect_name: str = Field(min_length=1, max_length=120)
    suspect_age: int | None = Field(default=None, ge=0, le=120)
    suspect_gender: str | None = Field(default=None, max_length=40)
    summary: str = Field(min_length=1, max_length=4000)
    sensitivity: Sensitivity = "standard"
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    socio_economic_context: str | None = Field(default=None, max_length=240)
    urbanization_context: str | None = Field(default=None, max_length=240)
    migration_context: str | None = Field(default=None, max_length=240)
    education_context: str | None = Field(default=None, max_length=240)
    event_context: str | None = Field(default=None, max_length=240)
    source_system: str | None = Field(default=None, max_length=120)
    source_record_id: str | None = Field(default=None, max_length=120)


class CaseRecord(CaseCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class CaseSearchResult(BaseModel):
    case: CaseRecord
    score: int


class CaseSearchResponse(BaseModel):
    query: str
    normalized_terms: list[str]
    result_count: int
    elapsed_ms: float
    results: list[CaseSearchResult]


class CaseImportRequest(BaseModel):
    source_system: str = Field(min_length=1, max_length=120)
    records: list[CaseCreate] = Field(min_length=1, max_length=5000)


class ImportResponse(BaseModel):
    imported: int
    source_system: str
    indexed: bool


class FileUploadRecord(BaseModel):
    id: str
    uploaded_at: datetime
    uploaded_by: str | None
    original_filename: str
    content_type: str | None
    extension: str
    sha256: str
    size_bytes: int
    case_id: str | None
    upload_type: str
    parsed_case_count: int
    skipped_case_count: int
    status: str
    notes: str
    extracted_preview: str | None = None
    extracted_summary: str | None = None
    extracted_summary_kn: str | None = None
    extraction_status: str | None = None
    extracted_char_count: int = 0
    extracted_metadata: dict[str, Any] = Field(default_factory=dict)
    fir_reconstruction_xml: str | None = None
    fir_reconstruction_status: str | None = None
    preview_supported: bool = False
    linked_fir_number: str | None = None
    linked_district: str | None = None


class CaseStatusUpdate(BaseModel):
    status: CaseStatus


class CaseNoteCreate(BaseModel):
    body: str = Field(min_length=1, max_length=4000)


class CaseNote(BaseModel):
    id: str
    case_id: str
    author_user_id: str
    body: str
    created_at: datetime


class AuditLog(BaseModel):
    id: int
    created_at: datetime
    actor_user_id: str | None
    actor_username: str | None
    actor_role: str | None
    action: str
    resource_type: str
    resource_id: str | None
    status: str
    request_id: str | None
    entry_hash: str


class RateLimitAlert(BaseModel):
    id: int
    created_at: datetime
    actor_user_id: str | None
    actor_username: str | None
    actor_role: str | None
    client_ip: str | None
    method: str
    path: str
    limit_per_minute: int
    window_seconds: int
    request_count: int
    request_id: str | None
    acknowledged_at: datetime | None
    acknowledged_by: str | None


class HealthResponse(BaseModel):
    status: str
    service: str


class TrendBucket(BaseModel):
    key: str
    count: int


class TrendSummary(BaseModel):
    total_cases: int
    open_cases: int
    restricted_cases: int
    by_district: list[TrendBucket]
    by_status: list[TrendBucket]
    by_sensitivity: list[TrendBucket]
    by_case_type: list[TrendBucket]
    by_modus_operandi: list[TrendBucket]
    by_month: list[TrendBucket]
    generated_at: datetime


class NetworkNode(BaseModel):
    id: str
    label: str
    type: str
    case_count: int
    districts: list[str]
    metadata: dict[str, Any] = Field(default_factory=dict)


class NetworkLink(BaseModel):
    source: str
    target: str
    relationship: str
    weight: int
    case_ids: list[str]
    metadata: dict[str, Any] = Field(default_factory=dict)


class NetworkGraph(BaseModel):
    nodes: list[NetworkNode]
    links: list[NetworkLink]
    generated_at: datetime
    focus: dict[str, Any] = Field(default_factory=dict)


class IntelligenceQuery(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    language: Literal["en", "kn"] = "en"
    include_sources: bool = True


class IntelligenceSource(BaseModel):
    case_id: str
    fir_number: str
    district: str
    status: CaseStatus
    sensitivity: Sensitivity
    excerpt: str


class QueryAnalysis(BaseModel):
    original_query: str
    normalized_query: str
    interpreted_terms: list[str]
    interpreted_filters: dict[str, Any] = Field(default_factory=dict)
    evidence_mode: str
    data_scope: str = "crime_data_only"


class IntelligenceResponse(BaseModel):
    intent: str
    answer: str
    visible_case_count: int
    sources: list[IntelligenceSource]
    safeguards: list[str]
    query_analysis: QueryAnalysis | None = None
    selected_module: str | None = None
    selected_api: str | None = None
    confidence: str | None = None
    reasoning: list[str] = Field(default_factory=list)
    suggested_followups: list[str] = Field(default_factory=list)
    orchestration_trace: list[str] = Field(default_factory=list)
    extracted_entities: dict[str, Any] = Field(default_factory=dict)
    conversation_memory: dict[str, Any] = Field(default_factory=dict)
    presentation: dict[str, Any] = Field(default_factory=dict)


class SimilarCase(BaseModel):
    case_id: str
    fir_number: str
    district: str
    status: CaseStatus
    reason: str


class DecisionSupportResponse(BaseModel):
    case: CaseRecord
    summary: str
    evidence: list[str]
    investigation_timeline: list[str]
    similar_cases: list[SimilarCase]
    recommended_next_steps: list[str]
    investigative_leads: list[str]
    safeguards: list[str]


class PatternCluster(BaseModel):
    key: str
    district: str | None = None
    case_type: str | None = None
    modus_operandi: str | None = None
    count: int
    fir_numbers: list[str]
    confidence: float
    explanation: str


class PatternAnalyticsResponse(BaseModel):
    total_cases: int
    by_case_type: list[TrendBucket]
    by_modus_operandi: list[TrendBucket]
    by_month: list[TrendBucket]
    event_trends: list[TrendBucket]
    clusters: list[PatternCluster]
    data_quality: list[str]
    safeguards: list[str]


class ModuleStatus(BaseModel):
    id: str
    name: str
    status: str
    endpoint: str
    security: str


class TranslationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    source_language: Literal["en", "kn"] = "en"
    target_language: Literal["en", "kn"] = "kn"


class TranslationResponse(BaseModel):
    source_language: str
    target_language: str
    translated_text: str
    confidence: float
    provider: str
    notes: list[str]


class ConversationCreate(BaseModel):
    title: str = Field(default="Investigation chat", min_length=1, max_length=120)


class ConversationMessageRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    language: Literal["en", "kn"] = "en"


class ConversationMessage(BaseModel):
    id: str
    conversation_id: str
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConversationRecord(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationExchange(BaseModel):
    conversation: ConversationRecord
    user_message: ConversationMessage
    assistant_message: ConversationMessage
    intelligence: IntelligenceResponse


class SociologicalInsights(BaseModel):
    total_cases: int
    district_workload: list[TrendBucket]
    sensitivity_mix: list[TrendBucket]
    status_mix: list[TrendBucket]
    demographic_mix: dict[str, list[TrendBucket]]
    social_indicators: list[TrendBucket]
    correlations: list[str]
    observations: list[str]
    safeguards: list[str]


class SuspectProfileResponse(BaseModel):
    suspect_name: str
    named_in_case_count: int
    districts: list[str]
    statuses: list[TrendBucket]
    cases: list[IntelligenceSource]
    risk_score: int
    risk_level: Literal["none", "low", "medium", "high"]
    risk_factors: list[str]
    behavioral_indicators: list[str]
    profile: str
    safeguards: list[str]


class FinancialFinding(BaseModel):
    finding_type: str
    severity: Literal["low", "medium", "high"]
    description: str
    related_transaction_ids: list[str]


class FinancialAnalysisResponse(BaseModel):
    transaction_count: int
    total_amount: float
    findings: list[FinancialFinding]
    account_links: list[dict[str, str | float | int]]
    safeguards: list[str]


class HotspotForecast(BaseModel):
    district: str
    current_cases: int
    projected_7_day_cases: int
    confidence: float
    drivers: list[str]


class ForecastResponse(BaseModel):
    generated_at: datetime
    hotspots: list[HotspotForecast]
    early_warnings: list[str]
    safeguards: list[str]


class ExplanationResponse(BaseModel):
    subject_type: str
    subject_id: str
    explanation: str
    factors: list[str]
    evidence: list[str]
    reasoning_path: list[str]
    correlations: list[str]
    audit: dict[str, str | None]
    safeguards: list[str]


class FinancialTransactionCreate(BaseModel):
    occurred_at: datetime
    source_account: str = Field(min_length=1, max_length=120)
    target_account: str = Field(min_length=1, max_length=120)
    source_account_holder: str | None = Field(default=None, max_length=120)
    target_account_holder: str | None = Field(default=None, max_length=120)
    source_bank_name: str | None = Field(default=None, max_length=120)
    source_ifsc_code: str | None = Field(default=None, max_length=32)
    source_branch: str | None = Field(default=None, max_length=120)
    source_bank_manager_phone: str | None = Field(default=None, max_length=30)
    target_bank_name: str | None = Field(default=None, max_length=120)
    target_ifsc_code: str | None = Field(default=None, max_length=32)
    target_branch: str | None = Field(default=None, max_length=120)
    target_bank_manager_phone: str | None = Field(default=None, max_length=30)
    amount: float = Field(ge=0)
    currency: str = Field(default="INR", min_length=3, max_length=8)
    district: str = Field(min_length=1, max_length=80)
    case_id: str | None = Field(default=None, max_length=80)
    description: str = Field(min_length=1, max_length=1000)


class FinancialTransactionImportRequest(BaseModel):
    source_system: str = Field(min_length=1, max_length=120)
    records: list[FinancialTransactionCreate] = Field(min_length=1, max_length=5000)


class CrimeDataImportRequest(BaseModel):
    path: str = Field(min_length=1, max_length=1000)
    source_system: str = Field(default="local-crime-csv", min_length=1, max_length=120)
    limit: int | None = Field(default=None, ge=1, le=5_000_000)
    reset_source: bool = False


class CrimeDataImportResponse(BaseModel):
    imported: int
    skipped: int
    source_system: str
    path: str


class CrimeDataStatusResponse(BaseModel):
    imported_count: int
    geocoded_count: int
    first_incident_at: datetime | None
    latest_incident_at: datetime | None
    source_systems: list[TrendBucket]
    by_district: list[TrendBucket]
    by_crime_type: list[TrendBucket]


class CrimeHeatmapPoint(BaseModel):
    latitude: float
    longitude: float
    weight: float
    incident_count: int
    district: str
    top_crime_type: str
    dominant_time_bucket: str
    risk_level: Literal["low", "medium", "high"]


class CrimeTrendAlert(BaseModel):
    district: str
    crime_type: str
    recent_count: int
    baseline_expected: float
    spike_ratio: float
    severity: Literal["low", "medium", "high"]
    explanation: str


class CrimeRiskArea(BaseModel):
    district: str
    crime_type: str
    score: int
    risk_level: Literal["low", "medium", "high"]
    recent_count: int
    baseline_count: int
    night_share: float
    weapon_share: float
    drivers: list[str]


class CrimeAnomalySignal(BaseModel):
    district: str
    crime_type: str
    recent_count: int
    expected_count: float
    z_score: float
    explanation: str


class AdvancedCrimeAnalyticsResponse(BaseModel):
    generated_at: datetime
    imported_count: int
    geocoded_count: int
    heatmap_points: list[CrimeHeatmapPoint]
    spatiotemporal_clusters: list[CrimeHeatmapPoint]
    emerging_trend_alerts: list[CrimeTrendAlert]
    risk_areas: list[CrimeRiskArea]
    anomalies: list[CrimeAnomalySignal]
    network: NetworkGraph
    data_quality: list[str]
    safeguards: list[str]


class PenalCodeRecord(BaseModel):
    id: str
    code_type: str = Field(description="E.g., BNS, IPC, CRPC")
    section: str = Field(description="Section number, e.g., 115(2)")
    description: str = Field(description="Description of the penal code section")
    punishment: str | None = None


class CrimeLogCreate(BaseModel):
    crime_type: str = Field(min_length=1, max_length=120)
    accused_name: str = Field(min_length=1, max_length=120)
    accused_aadhaar: str | None = Field(default=None, max_length=12)
    accused_age: int | None = Field(default=None, ge=0, le=120)
    accused_gender: str | None = Field(default=None, max_length=40)
    witness_a1: str | None = Field(default=None, max_length=120)
    witness_a2: str | None = Field(default=None, max_length=120)
    witness_a3: str | None = Field(default=None, max_length=120)
    witness_a4: str | None = Field(default=None, max_length=120)
    witness_a5: str | None = Field(default=None, max_length=120)
    prosecutor_name: str | None = Field(default=None, max_length=120)
    defense_lawyer_name: str | None = Field(default=None, max_length=120)
    bail_type: str | None = Field(default=None, max_length=120)
    bail_surety_name: str | None = Field(default=None, max_length=120)
    charge_sheet_sections: list[str] = Field(default_factory=list)


class CrimeLogRecord(CrimeLogCreate):
    id: str
    logged_by: str
    created_at: datetime
