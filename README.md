# 🩺 MedLink: Clinical Case Retrieval and Ranking Dashboard

MedLink is a web application designed to support clinical decision-making by retrieving and ranking relevant clinical case reports based on physician-provided medical reports. Built with Plotly's Dash in Python, this app utilizes advanced NLP models to help healthcare professionals find similar cases, aiding in complex diagnostic scenarios.

[Visit MedLink here](http://medlink.inesctec.pt)

![image2](https://github.com/LIAAD/MedLink/raw/main/medlink-medreport.png)




## 📑 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Methodology](#methodology)
- [Installation](#installation)
- [Usage](#usage)
- [File/Directory Explanations](#file/directory-explanations)
- [Support](#support)
- [Acknowledgments](#acknowledgments)

## 📖 Overview

In healthcare, physician-patient interactions are often documented as free-text medical reports, which may be challenging to reference in complex diagnostic cases. MedLink addresses this by retrieving and ranking relevant clinical case reports from health conferences and journals, offering valuable insights based on similar past cases. This tool utilizes advanced NLP techniques, specifically two BERT models, to:
1. Retrieve similar cases (using a bi-encoder) and,
2. Re-rank the retrieved cases based on relevance (using a cross-encoder).

MedLink’s effectiveness was evaluated by a physician, achieving a ranking model performance of NDCG@10 of 0.747.

## ⭐ Features 

- **Medical Report Search**: Input a medical report to retrieve similar published case reports.
- **Ranking and Scoring**: Case reports are ranked based on relevance using a cross-encoder model.
- **Clinical Entity Visualization**: Key entities (e.g., symptoms, diagnoses) highlighted using Named Entity Recognition (NER).
- **Textual Explanations**: Provides context and explanations to facilitate comparison of case reports.

## ⚙️ Methodology



![image](https://github.com/LIAAD/MedLink/blob/main/MedLink-architecture.png)

1. **Bi-Encoder Retrieval**: The retrieval process begins with the bi-encoder model, which independently encodes a set of medical case reports and the input medical report.

2. **Top-10 Candidates**: Based on the similarity scores of the bi-encoder, the top-10 most similar case reports are retrieved.

3. **Re-Ranking with Cross-Encoder**: The cross-encoder model takes the medical report and each of the top-10 retrieved case reports as input. It computes a ranking score for each pair, which reflects the relevance of each case report in relation to the medical report.


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

### Run the Dash app:

```bash
python app.py
```


### 📂 File/Directory Explanations

MedLink repository is divided into 3 different folders, each containing the essential components to replicate and extend the proposed application.

- **`spmi_dataset/`**: Contains the necessary scripts for extracting and cleaning the dataset used for this project extracted from ![SPMI Case Reports](https://casereports.spmi.pt/index.php/cr), as well as the dataset itself. It also contains the sample dataset used for evaluation.
- **`IR/`**: Contains the scripts required to reproduce the retrieval and re-ranker models.
- **`dash_app/`**: Contains the MedLink application and necessary files to run it.
  - **`pages/`**: Contains the different files for the application pages.
  - **`assets/`**: Contains the CSS and images for the application.
- **`requirements.txt`**: Lists all dependencies needed to run the project. Install these with `pip install -r requirements.txt`.
- **`README.md`**: Documentation file (this file), providing an overview, installation instructions, and usage guidelines.


## 💬 Support
For questions, please contact the authors.


##  🤝 Acknowledgments

This work is co-financed by Component 5 - Capitalization and Business Innovation, integrated in the Resilience Dimension of the Recovery and Resilience Plan within the scope of the Recovery and Resilience Mechanism (MRR) of the European Union (EU), framed in the Next Generation EU, for the period 2021 - 2026, within project HfPT, with reference 41.
The authors also would like to acknowledge project StorySense, with reference 2022.09312.PTDC (DOI 10.54499/2022.09312.PTDC) and the Advanced
Computing Project CPCA-IAC/AV/594794/2023(https://doi.org/10.54499/CPCAIAC/ AV/594794/2023). The authors also thank Dr Luís Monteiro Dias for his contribution in elaborating the queries (medical reports) and the Sociedade Portuguesa de Medicina Interna (SPMI) for allowing access to the case reports used in this paper.
Luís Filipe Cunha thanks the Fundação para a Ciência e Tecnologia (FCT), Portugal, for the Ph.D. Grant (2024.04202.BD).

