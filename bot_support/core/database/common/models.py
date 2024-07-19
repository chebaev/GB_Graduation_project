from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from core.database.utils.database import Base




class Support(Base):

    __tablename__ = 'support'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    questions: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)

    def __str__(self) -> str:
        return f"Support(id={self.id!r}, questions={self.questions}, answer={self.answer})"
    def __repr__(self) -> str:
        return str(self)



