# 🩺 MedLink: Clinical Case Retrieval and Ranking Dashboard

MedLink is a web application designed to support clinical decision-making by retrieving and ranking relevant clinical case reports based on physician-provided medical reports. Built with Plotly's Dash in Python, this app utilizes advanced NLP models to help healthcare professionals find similar cases, aiding in complex diagnostic scenarios.

[Visit MedLink here](http://medlink.inesctec.pt)

## 📑 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [License](#license)

## 📖 Overview

In healthcare, physician-patient interactions are often documented as free-text medical reports, which may be challenging to reference in complex diagnostic cases. MedLink addresses this by retrieving and ranking relevant clinical case reports from health conferences and journals, offering valuable insights based on similar past cases. This tool utilizes advanced NLP techniques, specifically two BERT models, to:
1. Retrieve similar cases (using a bi-encoder) and,
2. Re-rank the retrieved cases based on relevance (using a cross-encoder).

MedLink’s effectiveness was evaluated by a physician, achieving a ranking model performance of NDCG@10 of 0.747.

## ⚙️ Features

- **Medical Report Search**: Input a medical report to retrieve similar published case reports.
- **Ranking and Scoring**: Case reports are ranked based on relevance using a cross-encoder model.
- **Clinical Entity Visualization**: Key entities (e.g., symptoms, diagnoses) highlighted using Named Entity Recognition (NER).
- **Textual Explanations**: Provides context and explanations to facilitate comparison of case reports.

## 🛠️ Installation

**Note:** The models are available on HuggingFace and the dataset for the Dash app is available in this repository. Therefore, it is not necessary to run the data extraction and model training scripts to run the MedLink application.

### Prerequisites
- **Python 3.7+**
- **Virtual Environment Tool**: You can use Python’s built-in `venv` module or a tool like `virtualenv`.

### Setup

1. **Clone the repository** and navigate to the project directory:

    ```bash
    git clone https://github.com/LIAAD/MedLink.git
    cd medlink
    ```

2. **Create a virtual environment** in the project directory:

    ```bash
    python3 -m venv venv
    ```

3. **Activate the virtual environment**:

    - **On Windows**:

      ```bash
      venv\ Scripts\ activate
      ```

    - **On macOS and Linux**:

      ```bash
      source venv/bin/activate
      ```

4. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

### Run the data extraction scripts

### Run the model training scripts

### Run the Dash app:

```bash
python app.py
```


### 📂 File/Directory Explanations

MedLink repository is divided into 3 different folders, each containing the essential components to replicate and extend the proposed application.

- **`data/`**: Contains the necessary scripts for extracting and cleaning the dataset used for this project, as well as the dataset itself. It also contains the sample dataset used for evaluation.
- **`models/`**: Contains the scripts required to reproduce the retrieval and re-ranker models.
- **`dash_app/`**: Contains the MedLink application and necessary files to run it.
  - **`pages/`**: Contains the different files for the application pages.
  - **`assets/`**: Contains the CSS and images for the application.
- **`requirements.txt`**: Lists all dependencies needed to run the project. Install these with `pip install -r requirements.txt`.
- **`README.md`**: Documentation file (this file), providing an overview, installation instructions, and usage guidelines.
- **`LICENSE`**: Specifies the license for the project, detailing permissions and restrictions.



## 💬 Support
For questions, please contact the authors.


## ✍️ Authors and acknowledgments

This work is financed by National Funds through the Fundação para a Ciência e a Tecnologia, within the project StorySense (DOI \url{10.54499/2022.09312.PTDC}) and the Recovery and Resilience Plan within project HfPT, with reference 41.

## 📄 License
For open source projects, say how it is licensed.

## 📊 Project Status


