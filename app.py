import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "gachacore.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_includes=["*.j2"],
    )
