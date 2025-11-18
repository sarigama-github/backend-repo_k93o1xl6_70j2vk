"""
Database Schemas for Sampurna – Waste Management Platform

Each Pydantic model maps to a MongoDB collection (lowercased class name).
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class ServiceRequest(BaseModel):
    full_name: str = Field(..., description="Pemohon layanan")
    email: EmailStr = Field(..., description="Email pemohon")
    phone: str = Field(..., description="Nomor telepon")
    address: str = Field(..., description="Alamat lengkap lokasi pickup")
    city: str = Field(..., description="Kota/Kabupaten")
    waste_type: str = Field(..., description="Jenis sampah: organik, anorganik, B3, campuran")
    quantity_kg: Optional[float] = Field(None, ge=0, description="Perkiraan berat (kg)")
    notes: Optional[str] = Field(None, description="Catatan tambahan")
    status: str = Field("submitted", description="submitted, scheduled, collected, cancelled")

class Facility(BaseModel):
    name: str
    type: str = Field(..., description="TPST, TPS3R, Bank Sampah, Material Recovery Facility")
    address: str
    city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_phone: Optional[str] = None
    opening_hours: Optional[str] = None

class Article(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    cover_image: Optional[str] = None
    tags: List[str] = []
    author: Optional[str] = None

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class Feedback(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    name: Optional[str] = None
