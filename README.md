# arXiv Article Explorer

This Streamlit application fetches the latest machine learning papers from arXiv and presents them in a user-friendly interface. Users can translate titles and abstracts into Turkish, mark papers as favorites, and quickly access any GitHub repositories that are mentioned.

Access the hosted demo at https://arxiv-ai.streamlit.app/

## Features

- **Fresh Papers**: Retrieves up-to-date publications from the "Computer Science > Machine Learning" category on arXiv.
- **Translation Support**: Translate paper titles and abstracts into Turkish on demand.
- **Reaction System**: Let users like papers and persist their likes in the current session.
- **GitHub Discovery**: Surface GitHub links when they are referenced in the paper summary.
- **Navigation Menu**: Switch between Home, Machine Learning, Transformers, and Favorites views.

## Setup

1. **Install Python**
   - Python 3.10 or newer is required to run the project.
   - Download the latest version from the [official Python website](https://www.python.org/downloads/).

2. **Download the Project Files**
   - Clone or download the repository:
     ```bash
     git clone https://github.com/username/project-repo.git
     cd project-repo
     ```

3. **Install Dependencies**
   - Install the dependencies listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

## Running the App

1. **Start the Streamlit App**
   - Launch the application from the project directory:
     ```bash
     streamlit run app.py
     ```

2. **View in the Browser**
   - Streamlit opens a browser tab automatically. If it does not, copy the URL shown in the terminal (for example, `http://localhost:8501`).

## Contributing

If you would like to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push the branch (`git push origin feature-name`).
5. Open a Pull Request on GitHub.
