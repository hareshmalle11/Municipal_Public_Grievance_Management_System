from pydantic import BaseModel, Field

class ComplaintPredictRequest(BaseModel):
    complaint_text: str = Field(..., min_length=3)

class ComplaintPrediction(BaseModel):
    category: str
    priority: str
    category_confidence: float
    priority_confidence: float

class ComplaintCreateRequest(BaseModel):
    complaint_text: str = Field(..., min_length=3)
    locality: str = Field(..., min_length=2)
    address: str = Field(..., min_length=2)
    landmark: str | None = None
    user_id: int
    image_url: str | None = None

class ComplaintCreateResponse(BaseModel):
    message: str
    grievance: dict
    prediction: ComplaintPrediction

class ComplaintStatusUpdate(BaseModel):
    status: str = Field(..., min_length=2)
    officer_id: int | None = None
    remarks: str | None = None

class ComplaintReopenRequest(BaseModel):
    reason: str = Field(..., min_length=1)

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: str = Field(..., min_length=5)
    phone_number: str | None = None
    password: str = Field(..., min_length=6)

class UserLoginRequest(BaseModel):
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    phone_number: str | None = None
    created_at: str | None = None

class AuthResponse(BaseModel):
    message: str
    user: UserResponse

# Officer-related validation schemas
class OfficerRegisterRequest(BaseModel):
    officer_name: str = Field(..., min_length=2)
    username: str = Field(..., min_length=2)
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)
    locality: str = Field(..., min_length=2)
    is_active: bool | None = True

class OfficerLoginRequest(BaseModel):
    username: str
    password: str = Field(..., min_length=6)

class OfficerResponse(BaseModel):
    officer_id: int
    officer_name: str
    username: str
    email: str
    locality: str
    is_active: bool
    created_at: str | None = None

class OfficerUpdateRequest(BaseModel):
    username: str | None = None
    password: str | None = None
    locality: str | None = None

class OfficerAuthResponse(BaseModel):
    message: str
    officer: OfficerResponse

class FeedbackCreateRequest(BaseModel):
    grievance_id: int
    user_id: int
    rating: int = Field(..., ge=1, le=5)
    feedback_text: str | None = None
    image_url: str | None = None

class FeedbackResponse(BaseModel):
    feedback_id: int | None = None
    grievance_id: int
    user_id: int
    rating: int
    feedback_text: str | None = None
    image_url: str | None = None
    submitted_at: str | None = None
