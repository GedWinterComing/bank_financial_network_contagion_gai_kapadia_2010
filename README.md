# 🏦 Financial Contagion in Interbank Networks

## Project Overview
This repository contains a Python-based implementation and extension of the systemic risk and financial contagion model originally proposed by Gai and Kapadia (2010): *"Contagion in financial networks"*. 

While initial exploratory analysis was conducted using NetLogo (based on Blake LeBaron's framework https://people.brandeis.edu/~blebaron/classes/agentfin/GaiKapadia.html), the simulation engine was fully redeveloped from scratch in Python. This transition was necessary to overcome the limitations of the original NetLogo environment, correct existing architectural flaws, and achieve greater flexibility in modeling complex network topologies.

## Model Features & Implementation
* **Custom Network Topologies:** The simulation goes beyond standard random graphs, exploring contagion dynamics on **Scale-Free (Power-Law)** networks. 
* **Directed Graph Dynamics:** Specific implementations to isolate and test the effects of varying *in-degree* (lending/exposure) and *out-degree* (borrowing) distributions on systemic fragility.
* **Interactive Simulations:** Included interactive Python scripts to visualize and dynamically test the propagation of financial shocks across the interbank market.
* **Systemic Risk Analysis:** Demonstrates the "robust-yet-fragile" nature of highly interconnected financial systems.

## Theoretical Framework & Academic Report
Included in this repository is the original project report (`Relazione_Gai_Kapadia_contagio_banche.pdf`). This document provides a comprehensive theoretical summary of the mathematical tools used to model network contagion, specifically focusing on the analytical application of **Generating Functions** and **Giant Component** theory to assess the systemic vulnerability of financial systems.

## Tech Stack
* **Language:** Python, NetLogo.
* **Methodology:** Complex Network Analysis, Systemic Risk Modeling, Graph Theory, Generating Functions.
