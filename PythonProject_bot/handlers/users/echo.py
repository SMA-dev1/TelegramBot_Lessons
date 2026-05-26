from html import escape
from aiogram import F, Router, types
from pathlip import Path
from uuid import uuid4
from loader import bot

router = Router()
DOWNLOADS_DIR = Path('downloads')

def format_size(size: int | None) -> str:
    if not size:
        return "Noma'lum"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    file_size = float(size)
    for unit in units:
        if file_size < 1024:
            return f"{file_size:.2f} {unit}"
        file_size /= 1024
    return f"{file_size:.2f} TB"

def safe_filename(file_name: str | None, default_extension: str) -> str:
    name = file_name or f"{uuid4().hex}{default_extension}"
    return ".".join(char for char in name if char.isalnum() or char in [" ", ".", "_", "-"]).strip()

async def save_file(file_id: str, folder: str, file_name: str | None = None, default_extension: str = "") -> Path:
    directory = DOWNLOADS_DIR / folder
    directory.mkdir(parents=True, exist_ok=True)

    path = directory / safe_filename(file_name, default_extension)
    if path.exists():
        path = directory / f"{path.stem}_{uuid4().hex[:8]}{path.suffix}"

    await bot.download(file_id, destination=path)
    return path


def file_info_text(title: str, saved_path: Path, **data) -> str:
    lines = [f"<b>{escape(title)}</b>"]
    for key, value in data.items():
        lines.append(f"<b>{escape(key)}:</b> {escape(str(value))}")
    lines.append(f"<b>Saqlangan joyi:</b> {escape(str(saved_path))}")
    return "\n".join(lines)


@router.message(F.text)
async def text_handler(message: types.Message):
    await message.answer(f"Matn qabul qilindi:\n{message.text}")

@router.message(F.text)
async def text_handler(message: types.Message):
    await message.answer(f"Matn qabul qilindi:\n{message.text}")


@router.message(F.photo)
async def photo_handler(message: types.Message):
    photo = message.photo[-1]
    saved_path = await save_file(photo.file_id, folder="photos", default_extension=".jpg")

    await message.answer(file_info_text(
        title="Foto qabul qilindi.",
        saved_path=saved_path,
        Hajmi=format_size(photo.file_size),
        Kengligi=photo.width,
        Balandligi=photo.height,
        File_ID=photo.file_id,
    ))

@router.message(F.video)
async def video_handler(message: types.Message):
    video = message.video
    saved_path = await save_file(video.file_id, folder="videos", file_name=video.file_name, default_extension=".mp4")

    await message.answer(file_info_text(
        title="Video qabul qilindi.",
        saved_path=saved_path,
        Nomi=video.file_name or "Noma'lum",
        Hajmi=format_size(video.file_size),
        Turi=video.mime_type or "Noma'lum",
        Davomiyligi=f"{video.duration} soniya",
        Olchami=f"{video.width}x{video.height}",
        File_ID=video.file_id,
    ))

@router.message(F.sticker)
async def sticker_handler(message: types.Message):
    sticker = message.sticker
    extension = ".webm" if sticker.is_video else ".tgs" if sticker.is_animated else ".webp"
    saved_path = await save_file(sticker.file_id, folder="stickers", default_extension=extension)

    await message.answer(file_info_text(
        title="Stiker qabul qilindi.",
        saved_path=saved_path,
        Emoji=sticker.emoji or "Noma'lum",
        Hajmi=format_size(sticker.file_size),
        Turi="Video stiker" if sticker.is_video else "Animatsion stiker" if sticker.is_animated else "Oddiy stiker",
        Toplam=sticker.set_name or "Noma'lum",
        Olchami=f"{sticker.width}x{sticker.height}",
        File_ID=sticker.file_id,
    ))

@router.message(F.animation)
async def animation_handler(message: types.Message):
    animation = message.animation
    saved_path = await save_file(animation.file_id, folder="animations", file_name=animation.file_name, default_extension=".gif")

    await message.answer(file_info_text(
        title="GIF/animatsiya qabul qilindi.",
        saved_path=saved_path,
        Nomi=animation.file_name or "Noma'lum",
        Hajmi=format_size(animation.file_size),
        Turi=animation.mime_type or "Noma'lum",
        Davomiyligi=f"{animation.duration} soniya",
        Olchami=f"{animation.width}x{animation.height}",
        File_ID=animation.file_id,
    ))

@router.message(F.document)
async def document_handler(message: types.Message):
    document = message.document
    saved_path = await save_file(document.file_id, folder="documents", file_name=document.file_name)

    await message.answer(file_info_text(
        title="Fayl qabul qilindi.",
        saved_path=saved_path,
        Nomi=document.file_name or "Noma'lum",
        Hajmi=format_size(document.file_size),
        Turi=document.mime_type or "Noma'lum",
        File_ID=document.file_id,
    ))

@router.message(F.audio)
async def audio_handler(message: types.Message):
    audio = message.audio
    saved_path = await save_file(audio.file_id, folder="audios", file_name=audio.file_name, default_extension=".mp3")

    await message.answer(file_info_text(
        title="Audio qabul qilindi.",
        saved_path=saved_path,
        Nomi=audio.file_name or "Noma'lum",
        Hajmi=format_size(audio.file_size),
        Turi=audio.mime_type or "Noma'lum",
        Ijrochi=audio.performer or "Noma'lum",
        Sarlavha=audio.title or "Noma'lum",
        Davomiyligi=f"{audio.duration} soniya",
        File_ID=audio.file_id,
    ))

@router.message(F.voice)
async def voice_handler(message: types.Message):
    voice = message.voice
    saved_path = await save_file(voice.file_id, folder="voices", default_extension=".ogg")

    await message.answer(file_info_text(
        title="Ovozli xabar qabul qilindi.",
        saved_path=saved_path,
        Hajmi=format_size(voice.file_size),
        Turi=voice.mime_type or "Noma'lum",
        Davomiyligi=f"{voice.duration} soniya",
        File_ID=voice.file_id,
    ))

@router.message(F.video_note)
async def video_note_handler(message: types.Message):
    video_note = message.video_note
    saved_path = await save_file(video_note.file_id, folder="video_notes", default_extension=".mp4")

    await message.answer(file_info_text(
        title="Video xabar qabul qilindi.",
        saved_path=saved_path,
        Hajmi=format_size(video_note.file_size),
        Davomiyligi=f"{video_note.duration} soniya",
        Olchami=f"{video_note.length}x{video_note.length}",
        File_ID=video_note.file_id,
    ))


@router.message()
async def other_handler(message: types.Message):
    await message.answer("Xabar qabul qilindi.")