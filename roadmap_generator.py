roadmap = {
    "FastAPI": "Learn FastAPI basics and create a simple API.",
    "Docker": "Learn Docker fundamentals and containerize a Python project.",
    "Machine Learning": "Learn supervised learning and basic ML algorithms.",
    "Deep Learning": "Learn neural networks and deep learning fundamentals.",
    "SQL": "Practice SQL queries, joins, grouping and subqueries.",
    "Power BI": "Learn data visualization and dashboard creation.",
    "NLP": "Learn text preprocessing, TF-IDF and basic NLP techniques.",
    "Transformers": "Learn transformer architecture and its applications.",
    "Git": "Learn Git commands, branching and version control.",
    "GitHub": "Learn repositories, commits, branches and pull requests.",
    "AWS": "Learn basic cloud concepts and deployment.",
    "OpenCV": "Learn image processing and computer vision basics.",
    "CNN": "Learn convolutional neural networks and image classification.",
    "YOLO": "Learn object detection using YOLO.",
    "PyTorch": "Learn tensors, neural networks and model training using PyTorch.",
    "Hugging Face": "Learn how to use pretrained NLP models from Hugging Face.",
    "LLM": "Learn the basics of large language models and their applications.",
    "RAG": "Learn retrieval augmented generation and vector search."
}


def generate_roadmap(missing_skills):
    result = []

    for skill in missing_skills:

        if skill in roadmap:
            result.append(
                (skill, roadmap[skill])
            )

        else:
            result.append(
                (
                    skill,
                    f"Learn the fundamentals of {skill}."
                )
            )

    return result