import pandas as pd

import re


def extract_references_section(text):
    """
    Extracts the section of the text that follows the keywords "BIBLIOGRAFIA",
    "BIBLIOGRAPHY", or "REFERENCES".

    Parameters:
    - text: str, the input text containing the bibliographic references section.

    Returns:
    - A string containing the text after the specified keywords.
    """
    # Define the regular expression pattern for matching the keywords
    pattern = re.compile(r'\s*\b(BIBLIOGRAFIA|BIBLIOGRAPHY|REFERENCES)\b(.*)', re.DOTALL)

    # Search for the pattern in the text
    match = pattern.search(text)

    # If a match is found, return the group that captures the content after the keyword
    if match:
        return match.group(2).strip()
    else:
        return ""


def extract_bibliography(text):
    """
    Extracts bibliographic references from the given text.

    Parameters:
    - text: str, the input text containing bibliographic references.

    Returns:
    - A list of extracted references.
    """
    # Define the regular expression pattern for references
    # This pattern captures the format (number) Authors. Title. Journal. Year; volume(issue):pages.

    # Clean up the extracted references to remove any trailing or leading whitespace
    references = text.split("\n")

    return references







from pybliometrics.scopus import AbstractRetrieval,ScopusSearch
#s = ScopusSearch("TITLE(Suicide among the young population and the urgency of public health policies - response to Guimarães, Moreira and Costa)",)


import pybliometrics


pybliometrics.scopus.init()


df=pd.read_csv("dataset_articles.csv")

for text in df["articles"]:
    biblio_section=extract_references_section(text)

    extracted_references = extract_bibliography(biblio_section)
    if(extracted_references):
        print("extracted bio")
        for ref in extracted_references:
            print(ref)

    print("_________________________________________________")



