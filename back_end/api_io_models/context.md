# api_io_models/

| File | Purpose |
|---|---|
| `input_models.py` | Pydantic request body models: `SignupInput` (email + password, min 8 chars), `LoginInput` (email + password), `UpdateProfileInput` (optional first/last name and phone). |
| `output_models.py` | Pydantic response models: `MessageOut` (generic message), `UserProfileOut` (profile fields), `UserMeOut` (full user info including profile), `HelloOut` (hello message). |
| `context.md` | This file. |
