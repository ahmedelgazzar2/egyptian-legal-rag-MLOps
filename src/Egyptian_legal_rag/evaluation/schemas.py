from dataclasses import dataclass


@dataclass(frozen=True)
class RAGResult:
    question: str
    answer: str
    contexts: list[str]
    ground_truth: str


@dataclass(frozen=True)
class RAGConfig:
    chunk_size: str
    overlap: int
    embedding_model: str
    top_k: int = 4

    def validate(self) -> None:
        if self.top_k <= 0:
            raise ValueError("top_k must be positive")
