# mcp_backend/app/domain/models/base.py

from sqlalchemy.orm import registry

# 1) Cria o registry (onde o SQLA vai guardar as mappings)
mapper_registry = registry()

# 2) Expõe a MetaData para o Alembic (e para quem precisar fazer Table(), etc)
metadata = mapper_registry.metadata

# 3) Cria o Base declarativo que você usa em todos os models
#    Aqui você poderá usar mapped_column(), mapped_as_dataclass(), etc.
Base = mapper_registry.generate_base()
