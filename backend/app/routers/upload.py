from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import aiofiles
import os
from app.session_manager import session_manager
from app.models import TemplateBbox, ProcessConfig, ProcessResult
from modules.web_adapter import WebChatAvatarReplacer

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/{session_id}/upload/chat-image")
async def upload_chat_image(session_id: str, file: UploadFile = File(...)):
    """上传聊天记录截图"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    # 检查文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="请上传图片文件")

    try:
        # 保存文件
        temp_dir = session['temp_dir']
        file_path = os.path.join(temp_dir, f"chat_image_{file.filename}")

        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)

        # 更新会话信息
        session_manager.update_session(
            session_id,
            chat_image_path=file_path,
            status='chat_image_uploaded',
            message='聊天截图上传成功'
        )

        return {
            "message": "聊天截图上传成功",
            "filename": file.filename,
            "size": len(content)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.post("/{session_id}/upload/avatar")
async def upload_new_avatar(session_id: str, file: UploadFile = File(...)):
    """上传新头像图片"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    # 检查文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="请上传图片文件")

    try:
        # 保存文件
        temp_dir = session['temp_dir']
        file_path = os.path.join(temp_dir, f"avatar_{file.filename}")

        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)

        # 更新会话信息
        session_manager.update_session(
            session_id,
            avatar_path=file_path,
            status='avatar_uploaded',
            message='新头像上传成功'
        )

        return {
            "message": "新头像上传成功",
            "filename": file.filename,
            "size": len(content)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.post("/{session_id}/template/set")
async def set_template_and_detect(session_id: str, bbox: TemplateBbox):
    """设置头像模板区域并检测相似头像"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    if not all([session.get('chat_image_path'), session.get('avatar_path')]):
        raise HTTPException(status_code=400, detail="请先上传聊天截图和新头像")

    try:
        # 1. 保存模板区域信息
        template_bbox = (bbox.x, bbox.y, bbox.width, bbox.height)
        session_manager.update_session(
            session_id,
            template_bbox=template_bbox,
            status='template_set',
            message='模板区域设置成功'
        )

        # 2. 读取图片文件
        async with aiofiles.open(session['chat_image_path'], 'rb') as f:
            chat_image_bytes = await f.read()

        # 3. 创建处理器进行检测
        processor = WebChatAvatarReplacer(session_id)
        
        # 设置进度回调
        async def progress_callback(progress: int, message: str):
            session_manager.set_progress(session_id, progress, message)

        processor.set_progress_callback(progress_callback)

        # 4. 使用默认配置检测相似头像
        detected_avatars, preview_base64 = await processor.detect_similar_avatars(
            chat_image_bytes=chat_image_bytes,
            bbox=template_bbox,
            threshold=0.8,  # 默认阈值
            right_ratio=0.6  # 默认右侧筛选比例
        )

        # 5. 更新会话状态
        session_manager.update_session(
            session_id,
            detected_avatars=detected_avatars,
            status='avatars_detected',
            message=f'检测完成，找到 {len(detected_avatars)} 个相似头像'
        )

        return {
            "message": f"检测完成，找到 {len(detected_avatars)} 个相似头像",
            "detected_avatars": detected_avatars,
            "avatar_count": len(detected_avatars),
            "preview_image": preview_base64
        }

    except Exception as e:
        session_manager.update_session(
            session_id,
            status='error',
            message=f'检测失败: {str(e)}'
        )
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

@router.post("/{session_id}/process/start")
async def start_processing(session_id: str, config: ProcessConfig):
    """开始头像替换处理"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    # 检查必要文件
    if not all([session.get('chat_image_path'), session.get('avatar_path'), session.get('template_bbox')]):
        raise HTTPException(status_code=400, detail="请先上传图片并设置模板区域")

    try:
        # 读取图片文件
        async with aiofiles.open(session['chat_image_path'], 'rb') as f:
            chat_image_bytes = await f.read()

        async with aiofiles.open(session['avatar_path'], 'rb') as f:
            avatar_bytes = await f.read()

        # 创建处理器并设置进度回调
        processor = WebChatAvatarReplacer(session_id)

        async def progress_callback(progress: int, message: str):
            session_manager.set_progress(session_id, progress, message)

        processor.set_progress_callback(progress_callback)

        # 开始处理
        session_manager.update_session(session_id, status='processing')

        result_img, avatar_count = await processor.process_from_bytes(
            chat_image_bytes=chat_image_bytes,
            avatar_bytes=avatar_bytes,
            bbox=session['template_bbox'],
            threshold=config.threshold,
            right_ratio=config.right_ratio
        )

        # 保存结果
        result_path = os.path.join(session['temp_dir'], 'result.png')
        result_bytes = processor._cv2_to_bytes(result_img)

        async with aiofiles.open(result_path, 'wb') as f:
            await f.write(result_bytes)

        # 生成base64图片数据用于前端显示
        import base64
        result_base64 = base64.b64encode(result_bytes).decode('utf-8')

        # 更新会话状态
        session_manager.update_session(
            session_id,
            status='completed',
            result_path=result_path,
            result_base64=result_base64,
            progress=100,
            message=f'处理完成，替换了{avatar_count}个头像'
        )

        return ProcessResult(
            success=True,
            message=f'处理完成，替换了{avatar_count}个头像',
            avatar_count=avatar_count,
            result_url=f'/api/{session_id}/result/download',
            result_base64=result_base64
        )

    except Exception as e:
        session_manager.update_session(
            session_id,
            status='error',
            message=f'处理失败: {str(e)}'
        )
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@router.get("/{session_id}/result/download")
async def download_result(session_id: str):
    """下载处理结果"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    result_path = session.get('result_path')
    if not result_path or not os.path.exists(result_path):
        raise HTTPException(status_code=404, detail="结果文件不存在")

    return FileResponse(
        result_path,
        media_type='image/png',
        filename=f'avatar_replaced_{session_id}.png'
    )