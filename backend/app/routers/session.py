from fastapi import APIRouter, HTTPException
from app.session_manager import session_manager
from app.models import SessionCreateResponse, SessionStatus

router = APIRouter(prefix="/api", tags=["session"])

@router.post("/session/create", response_model=SessionCreateResponse)
async def create_session():
    """创建新的处理会话"""
    try:
        session_id = session_manager.create_session()
        return SessionCreateResponse(
            session_id=session_id,
            message="会话创建成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建会话失败: {str(e)}")

@router.get("/session/{session_id}/status", response_model=SessionStatus)
async def get_session_status(session_id: str):
    """获取会话状态"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    return SessionStatus(
        session_id=session_id,
        status=session.get('status', 'unknown'),
        progress=session.get('progress', 0),
        message=session.get('message', ''),
        created_at=session['created_at'].isoformat(),
        updated_at=session['updated_at'].isoformat(),
        result_base64=session.get('result_base64')
    )

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    session_manager.delete_session(session_id)
    return {"message": "会话删除成功"}