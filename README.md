# 📊 CRR Option Pricing Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**A comprehensive platform for Cox-Ross-Rubinstein option pricing, demonstrating convergence to Black-Scholes and delta-hedging strategies.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Theory](#-mathematical-theory) • [Screenshots](#-screenshots)

</div>

---

## 🎯 Project Overview

This platform is developed as part of the **ESILV Industrial Innovation Project (Pi²)**, focusing on quantitative finance and derivative pricing. The project demonstrates the foundational concepts of option pricing through the binomial CRR model and its convergence to the continuous Black-Scholes framework.

### Objectives

1. **Implement a CRR pricing platform** with interactive graphical interface
2. **Demonstrate convergence** of CRR to Black-Scholes as N → ∞
3. **Visualize delta-hedging strategies** with Monte Carlo simulation
4. **Discuss model limitations** compared to Heston, SABR, and jump-diffusion models

---

## ✨ Features

### 📊 Dashboard
- Real-time option pricing comparison (CRR vs Black-Scholes)
- Complete Greeks calculation (Δ, Γ, ν, Θ, ρ)
- Model parameters visualization
- Price convergence preview

### 🌳 CRR Model Visualization
- Interactive binomial tree display
- Node-by-node stock prices and option values
- Delta hedging ratios at each node
- No-arbitrage condition verification

### 📈 Convergence Analysis
- Dynamic convergence plots (price and delta)
- Error analysis with configurable step range
- Theoretical vs empirical convergence rate comparison
- O(1/N) convergence demonstration

### 🛡️ Hedging Simulation
- Monte Carlo simulation of delta-hedging strategy
- Configurable rebalancing frequency (daily/weekly/monthly)
- P&L distribution analysis
- VaR calculations (95% and 99%)
- Hedging error decomposition

### 📚 Theory Section
- Complete mathematical derivations
- LaTeX-rendered formulas
- CRR and Black-Scholes comparison
- Model limitations and extensions (Heston, SABR)

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/AlexisAHG/Quant-Option-Portfolio.git
cd Quant-Option-Portfolio

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.28.0 | Web interface |
| numpy | ≥1.24.0 | Numerical computing |
| pandas | ≥2.0.0 | Data manipulation |
| scipy | ≥1.11.0 | Statistical functions |
| plotly | ≥5.18.0 | Interactive visualizations |

---

## 💻 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Configuration

Use the sidebar to configure:
- **Spot Price (S₀)**: Current underlying price
- **Strike Price (K)**: Option strike
- **Time to Maturity (T)**: In years
- **Risk-Free Rate (r)**: Annual rate
- **Volatility (σ)**: Annual volatility
- **Option Type**: Call or Put
- **CRR Steps (N)**: Number of binomial steps

---

## 📐 Mathematical Theory

### CRR Model

The Cox-Ross-Rubinstein model discretizes asset price evolution:

$$S_{t+\Delta t} = \begin{cases} S_t \cdot u & \text{with probability } p \\ S_t \cdot d & \text{with probability } 1-p \end{cases}$$

With parameters:

$$u = e^{\sigma\sqrt{\Delta t}}, \quad d = \frac{1}{u}, \quad p = \frac{e^{r\Delta t} - d}{u - d}$$

### Delta Hedging

The replicating portfolio at each node:

$$\phi_t = \frac{C_{t+1}^u - C_{t+1}^d}{S_t(u-d)}$$

### Convergence

As N → ∞, the CRR model converges to Black-Scholes:

$$\lim_{N \to \infty} C_{CRR}^N = C_{BS}$$

With convergence rate O(1/N).

---

## 📁 Project Structure

```
Quant-Option-Portfolio/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
├── notebooks/
│   ├── Stochastic_Volatility_Models.ipynb    # Heston/SABR research
│   └── Modèle_SABR_Compréhension_et_simulation.ipynb
└── data/
    ├── spx.csv           # S&P 500 historical data
    └── vix_daily.csv     # VIX historical data
```

---

## 👥 Contributors

| Name | Role |
|------|------|
| Alexis Hanna Gerguis | Lead Developer |
| Adrien Bayre | Developer |
| Jack Liu | Developer |
| Marcellin Milcent | Developer |
| Sinthia Vanelle Jouonang Kapnang | Developer |
| **Vincent Marc Lambert** | Supervisor (ESILV) |

---

## 📚 References

1. Cox, J. C., Ross, S. A., & Rubinstein, M. (1979). *Option pricing: A simplified approach*. Journal of Financial Economics.
2. Black, F., & Scholes, M. (1973). *The pricing of options and corporate liabilities*. Journal of Political Economy.
3. Hull, J. C. (2018). *Options, Futures, and Other Derivatives*. Pearson.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**ESILV - Projet d'Innovation Industrielle • 2025**

*Built with ❤️ using Python and Streamlit*

</div>
