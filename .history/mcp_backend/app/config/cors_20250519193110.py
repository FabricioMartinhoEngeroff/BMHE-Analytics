from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ❗️ Ajuste para origens específicas em produção
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
