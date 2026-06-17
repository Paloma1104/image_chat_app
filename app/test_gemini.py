from app.services.gemini_service import (
    generate_image_caption
)

print(
    generate_image_caption(
        "uploads/play.jpg"
    )
)