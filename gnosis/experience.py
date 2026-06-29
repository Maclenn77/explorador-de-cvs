"""Tool to calculate years of professional experience from CV profiles"""
import re
from datetime import date


class ExperienceCalculator:
    """Calculates years of experience from CV content stored in ChromaDB"""

    def __init__(self, chroma_db):
        self.chroma_db = chroma_db

    def run(self, query: str) -> str:
        if not self.chroma_db.api_key:
            return "No API key set. Please add your OpenAI API key in the sidebar."

        collection = self.chroma_db.get_collection("pdf-explainer")

        if not hasattr(collection, "query"):
            return "Could not access the collection. Please check your API key."

        if collection.count() == 0:
            return "No documents found. Please upload a CV first."

        results = collection.query(query_texts=[query], n_results=10)["documents"][0]
        text = " ".join(results)

        years = [int(y) for y in re.findall(r"\b(19[6-9]\d|20[0-2]\d)\b", text)]
        if not years:
            return "Could not find any year references in the CV to calculate experience."

        oldest_year = min(years)
        current_year = date.today().year
        experience = current_year - oldest_year

        return (
            f"Based on the CV content, the earliest year found is {oldest_year}. "
            f"As of {current_year}, this profile has approximately {experience} years of experience."
        )
