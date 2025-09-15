#!/usr/bin/env python3
"""
Setup configuration for AI Educational Assistant
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-educational-assistant",
    version="1.0.0",
    author="Capstone Project Team",
    author_email="student@university.edu",
    description="A Generative AI Personalized Educational Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/ai-educational-assistant",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-tutor=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ai_educational_assistant": [
            "data/*.json",
            "templates/*.html",
            "static/css/*.css",
            "static/js/*.js",
        ],
    },
    keywords="ai education machine-learning personalized-learning tutoring",
    project_urls={
        "Bug Reports": "https://github.com/username/ai-educational-assistant/issues",
        "Source": "https://github.com/username/ai-educational-assistant",
        "Documentation": "https://ai-educational-assistant.readthedocs.io/",
    },
)