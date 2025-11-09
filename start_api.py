"""
Start the FastAPI server.
"""

import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable (for Railway/Render) or default to 8000
    port = int(os.getenv("PORT", 8000))
    # Disable reload in production
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    uvicorn.run(
        "empire_automation.api.main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        log_level="info"
    )

