from fastapi import FastAPI
import settings
import urls

# Properties
app = FastAPI(**settings.API_METADATA)

# CORS (Cross-Origin Resource Sharing)
app.add_middleware(**settings.MIDDLEWARE)

# Include every router in app package
[app.include_router(path) for path in urls.URL_PATTERNS]


@app.on_event("startup")
def startup():
    print("""
    Go to: http://localhost:8000/
    """)
