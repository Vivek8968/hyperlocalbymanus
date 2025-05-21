import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, status
from typing import Dict, Any, Optional
from ..config.settings import get_settings

settings = get_settings()

# Initialize Firebase Admin SDK if credentials are provided
firebase_app = None
if settings.FIREBASE_CREDENTIALS:
    try:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
        firebase_app = firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

async def verify_firebase_token(id_token: str) -> Dict[str, Any]:
    """
    Verify Firebase ID token and return user data
    """
    if not firebase_app:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Firebase not initialized"
        )
    
    try:
        decoded_token = auth.verify_id_token(id_token, firebase_app)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Firebase token: {str(e)}"
        )

async def get_firebase_user(uid: str) -> Optional[Dict[str, Any]]:
    """
    Get Firebase user by UID
    """
    if not firebase_app:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Firebase not initialized"
        )
    
    try:
        user = auth.get_user(uid, firebase_app)
        return {
            "uid": user.uid,
            "email": user.email,
            "phone_number": user.phone_number,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
            "disabled": user.disabled,
        }
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting Firebase user: {str(e)}"
        )
