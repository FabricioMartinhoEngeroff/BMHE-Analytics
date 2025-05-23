# app/domain/models/base.py

from sqlalchemy.orm import registry

# Cria o registry principal para uso com mapped_as_dataclass
registry = registry()
