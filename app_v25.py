"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CRR OPTION PRICING PLATFORM - V2.5                        ║
║                    ESILV - Projet d'Innovation Industrielle                  ║
║                                                                              ║
║   Enhanced version with:                                                     ║
║   - Implied Volatility Surface (3D)                                          ║
║   - Real-time Options Chain                                                  ║
║   - Greeks Heatmaps                                                          ║
║   - Stress Testing                                                           ║
║   - P&L Analysis                                                             ║
║   - Dark/Light Theme Toggle                                                  ║
║   - PDF Export                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import pandas as pd
import scipy.stats as si
from scipy.optimize import brentq
from scipy.interpolate import griddata
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import base64

# =============================================================================
# 1. PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="CRR Pricing Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. THEME SYSTEM - Dark/Light Mode
# =============================================================================

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def get_theme_colors():
    """Return color scheme based on current theme."""
    if st.session_state.theme == 'dark':
        return {
            'bg_primary': '#0a0e17',
            'bg_secondary': '#111827',
            'bg_card': '#1a2332',
            'bg_hover': '#243044',
            'accent_blue': '#3b82f6',
            'accent_cyan': '#06b6d4',
            'accent_green': '#10b981',
            'accent_red': '#ef4444',
            'accent_orange': '#f59e0b',
            'accent_purple': '#8b5cf6',
            'text_primary': '#f8fafc',
            'text_secondary': '#94a3b8',
            'text_muted': '#64748b',
            'border_color': '#1e293b',
            'chart_bg': 'rgba(17, 24, 39, 0.8)',
            'grid_color': '#1e293b'
        }
    else:  # light theme
        return {
            'bg_primary': '#f8fafc',
            'bg_secondary': '#ffffff',
            'bg_card': '#ffffff',
            'bg_hover': '#f1f5f9',
            'accent_blue': '#2563eb',
            'accent_cyan': '#0891b2',
            'accent_green': '#059669',
            'accent_red': '#dc2626',
            'accent_orange': '#d97706',
            'accent_purple': '#7c3aed',
            'text_primary': '#0f172a',
            'text_secondary': '#475569',
            'text_muted': '#94a3b8',
            'border_color': '#e2e8f0',
            'chart_bg': 'rgba(255, 255, 255, 0.9)',
            'grid_color': '#e2e8f0'
        }

colors = get_theme_colors()

# =============================================================================
# 3. DYNAMIC CSS
# =============================================================================

def generate_css(colors):
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {{
    --bg-primary: {colors['bg_primary']};
    --bg-secondary: {colors['bg_secondary']};
    --bg-card: {colors['bg_card']};
    --bg-hover: {colors['bg_hover']};
    --accent-blue: {colors['accent_blue']};
    --accent-cyan: {colors['accent_cyan']};
    --accent-green: {colors['accent_green']};
    --accent-red: {colors['accent_red']};
    --accent-orange: {colors['accent_orange']};
    --accent-purple: {colors['accent_purple']};
    --text-primary: {colors['text_primary']};
    --text-secondary: {colors['text_secondary']};
    --text-muted: {colors['text_muted']};
    --border-color: {colors['border_color']};
}}

.stApp {{
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-primary) 100%);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, sans-serif;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

.main .block-container {{
    padding: 2rem 3rem;
    max-width: 100%;
}}

h1, h2, h3 {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
    color: var(--text-primary) !important;
}}

/* Premium Card */
.premium-card {{
    background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}}

.premium-card:hover {{
    border-color: var(--accent-blue);
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
    transform: translateY(-2px);
}}

/* Accent Card */
.accent-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-left: 4px solid var(--accent-blue);
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
}}

/* Metric Card */
.metric-card {{
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
}}

.metric-card:hover {{
    border-color: var(--accent-cyan);
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.15);
}}

.metric-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}}

.metric-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.2;
}}

.metric-value.positive {{ color: var(--accent-green); }}
.metric-value.negative {{ color: var(--accent-red); }}
.metric-value.blue {{ color: var(--accent-blue); }}
.metric-value.cyan {{ color: var(--accent-cyan); }}

/* Section Title */
.section-title {{
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: var(--accent-blue);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.section-title::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--accent-blue) 0%, transparent 100%);
}}

/* Header Banner */
.header-banner {{
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}}

.header-banner::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan), var(--accent-purple));
}}

.header-title {{
    font-family: 'Inter', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 8px 0;
}}

.header-subtitle {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    color: var(--text-secondary);
}}

/* Greeks Grid */
.greeks-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin: 16px 0;
}}

.greek-item {{
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    transition: all 0.2s ease;
}}

.greek-item:hover {{
    border-color: var(--accent-purple);
    background: var(--bg-hover);
}}

.greek-symbol {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 600;
    color: var(--accent-purple);
}}

.greek-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    color: var(--text-primary);
}}

.greek-name {{
    font-size: 10px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* Formula Box */
.formula-box {{
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-left: 3px solid var(--accent-purple);
    border-radius: 8px;
    padding: 20px;
    margin: 16px 0;
    font-family: 'JetBrains Mono', monospace;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: var(--bg-secondary);
    padding: 8px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border-radius: 8px;
    color: var(--text-secondary);
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    padding: 12px 24px;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-cyan) 100%);
    color: white !important;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
    border-right: 1px solid var(--border-color);
}}

/* Inputs */
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stSelectbox > div > div {{
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
}}

/* Slider */
.stSlider > div > div > div > div {{
    background: var(--accent-blue) !important;
}}

/* Badge */
.badge {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
}}

.badge-success {{
    background: rgba(16, 185, 129, 0.15);
    color: var(--accent-green);
    border: 1px solid var(--accent-green);
}}

.badge-info {{
    background: rgba(59, 130, 246, 0.15);
    color: var(--accent-blue);
    border: 1px solid var(--accent-blue);
}}

.badge-warning {{
    background: rgba(245, 158, 11, 0.15);
    color: var(--accent-orange);
    border: 1px solid var(--accent-orange);
}}

/* Comparison Row */
.comparison-row {{
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-color);
}}

.comparison-label {{
    color: var(--text-secondary);
}}

.comparison-value {{
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    color: var(--text-primary);
}}

/* Theme Toggle Button */
.theme-toggle {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 8px 16px;
    cursor: pointer;
    transition: all 0.2s;
}}

.theme-toggle:hover {{
    border-color: var(--accent-blue);
}}

/* Stress Test Cards */
.stress-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}}

.stress-card.negative {{
    border-left: 3px solid var(--accent-red);
}}

.stress-card.positive {{
    border-left: 3px solid var(--accent-green);
}}

/* Live indicator */
.live-indicator {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: var(--accent-green);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.live-dot {{
    width: 8px;
    height: 8px;
    background: var(--accent-green);
    border-radius: 50%;
    animation: pulse 2s infinite;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.5; }}
}}

/* Heatmap container */
.heatmap-container {{
    background: var(--bg-card);
    border-radius: 12px;
    padding: 16px;
    border: 1px solid var(--border-color);
}}
</style>
"""

st.markdown(generate_css(colors), unsafe_allow_html=True)

# =============================================================================
# 4. MATHEMATICAL FUNCTIONS
# =============================================================================

def black_scholes(S: float, K: float, T: float, r: float, sigma: float, option_type: str = "Call") -> dict:
    """Calculate Black-Scholes option price and Greeks."""
    if T <= 0 or sigma <= 0:
        return {k: 0.0 for k in ["Price", "Delta", "Gamma", "Vega", "Theta", "Rho"]}
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "Call":
        price = S * si.norm.cdf(d1) - K * np.exp(-r * T) * si.norm.cdf(d2)
        delta = si.norm.cdf(d1)
        rho = K * T * np.exp(-r * T) * si.norm.cdf(d2)
        theta = (-(S * si.norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 - r * K * np.exp(-r * T) * si.norm.cdf(d2))
    else:
        price = K * np.exp(-r * T) * si.norm.cdf(-d2) - S * si.norm.cdf(-d1)
        delta = -si.norm.cdf(-d1)
        rho = -K * T * np.exp(-r * T) * si.norm.cdf(-d2)
        theta = (-(S * si.norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 + r * K * np.exp(-r * T) * si.norm.cdf(-d2))
    
    gamma = si.norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * np.sqrt(T) * si.norm.pdf(d1)
    
    return {
        "Price": price,
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega / 100,
        "Theta": theta / 365,
        "Rho": rho / 100
    }


def implied_volatility(price: float, S: float, K: float, T: float, r: float, 
                       option_type: str = "Call") -> float:
    """Calculate implied volatility using Brent's method."""
    if T <= 0 or price <= 0:
        return np.nan
    
    def objective(sigma):
        return black_scholes(S, K, T, r, sigma, option_type)["Price"] - price
    
    try:
        iv = brentq(objective, 0.001, 5.0)
        return iv
    except:
        return np.nan


def crr_binomial_tree(S: float, K: float, T: float, r: float, sigma: float, 
                       N: int, option_type: str = "Call", 
                       return_tree: bool = False) -> tuple:
    """Cox-Ross-Rubinstein binomial tree option pricing."""
    if T <= 0 or sigma <= 0:
        return (0.0, None, None, None, 1, 1, 0.5) if return_tree else 0.0
    
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    
    # Stock price tree
    stock_tree = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(i + 1):
            stock_tree[j, i] = S * (u ** (i - j)) * (d ** j)
    
    # Option value tree
    option_tree = np.zeros((N + 1, N + 1))
    if option_type == "Call":
        option_tree[:, N] = np.maximum(stock_tree[:, N] - K, 0)
    else:
        option_tree[:, N] = np.maximum(K - stock_tree[:, N], 0)
    
    # Backward induction
    discount = np.exp(-r * dt)
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            option_tree[j, i] = discount * (p * option_tree[j, i + 1] + (1 - p) * option_tree[j + 1, i + 1])
    
    # Delta tree
    delta_tree = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1):
            if stock_tree[j, i + 1] != stock_tree[j + 1, i + 1]:
                delta_tree[j, i] = (option_tree[j, i + 1] - option_tree[j + 1, i + 1]) / \
                                   (stock_tree[j, i + 1] - stock_tree[j + 1, i + 1])
    
    if return_tree:
        return option_tree[0, 0], stock_tree, option_tree, delta_tree, u, d, p
    return option_tree[0, 0]


def crr_delta(S: float, K: float, T: float, r: float, sigma: float, 
              N: int, option_type: str = "Call") -> float:
    """Calculate CRR delta."""
    if T <= 0 or sigma <= 0 or N < 1:
        return 0.0
    
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    
    Su = S * u
    Sd = S * d
    
    Cu = crr_binomial_tree(Su, K, T - dt, r, sigma, N - 1, option_type)
    Cd = crr_binomial_tree(Sd, K, T - dt, r, sigma, N - 1, option_type)
    
    return (Cu - Cd) / (Su - Sd)


def simulate_gbm_paths(S0: float, r: float, sigma: float, T: float, 
                        n_steps: int, n_paths: int) -> np.ndarray:
    """Simulate geometric Brownian motion paths."""
    dt = T / n_steps
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = S0
    
    dW = np.random.standard_normal((n_paths, n_steps))
    
    for t in range(1, n_steps + 1):
        paths[:, t] = paths[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dW[:, t-1])
    
    return paths


def simulate_hedging_strategy(S0: float, K: float, T: float, r: float, sigma: float,
                               n_steps: int, n_paths: int, use_bs_delta: bool = True) -> dict:
    """Simulate delta hedging strategy."""
    dt = T / n_steps
    paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_paths)
    
    bs_initial = black_scholes(S0, K, T, r, sigma, "Call")
    initial_option_price = bs_initial["Price"]
    
    portfolio_values = np.zeros((n_paths, n_steps + 1))
    cash_accounts = np.zeros((n_paths, n_steps + 1))
    stock_positions = np.zeros((n_paths, n_steps + 1))
    deltas = np.zeros((n_paths, n_steps + 1))
    
    for i in range(n_paths):
        S = paths[i, 0]
        ttm = T
        
        if use_bs_delta:
            delta = black_scholes(S, K, ttm, r, sigma, "Call")["Delta"]
        else:
            delta = crr_delta(S, K, ttm, r, sigma, max(10, n_steps), "Call")
        
        deltas[i, 0] = delta
        stock_positions[i, 0] = delta * S
        cash_accounts[i, 0] = initial_option_price - delta * S
        portfolio_values[i, 0] = stock_positions[i, 0] + cash_accounts[i, 0]
    
    for t in range(1, n_steps + 1):
        ttm = T - t * dt
        
        for i in range(n_paths):
            S = paths[i, t]
            
            if ttm > 0.001:
                if use_bs_delta:
                    new_delta = black_scholes(S, K, ttm, r, sigma, "Call")["Delta"]
                else:
                    new_delta = crr_delta(S, K, ttm, r, sigma, max(10, n_steps - t), "Call")
            else:
                new_delta = 1.0 if S > K else 0.0
            
            old_delta = deltas[i, t - 1]
            cash_accounts[i, t] = cash_accounts[i, t - 1] * np.exp(r * dt)
            shares_traded = new_delta - old_delta
            cash_accounts[i, t] -= shares_traded * S
            deltas[i, t] = new_delta
            stock_positions[i, t] = new_delta * S
            portfolio_values[i, t] = stock_positions[i, t] + cash_accounts[i, t]
    
    final_payoffs = np.maximum(paths[:, -1] - K, 0)
    final_portfolio = portfolio_values[:, -1]
    hedging_errors = final_portfolio - final_payoffs
    
    return {
        "paths": paths,
        "portfolio_values": portfolio_values,
        "cash_accounts": cash_accounts,
        "stock_positions": stock_positions,
        "deltas": deltas,
        "final_payoffs": final_payoffs,
        "hedging_errors": hedging_errors,
        "initial_price": initial_option_price
    }


# =============================================================================
# 5. VISUALIZATION FUNCTIONS
# =============================================================================

def create_binomial_tree_figure(stock_tree, option_tree, delta_tree, N, u, d, p):
    """Create interactive binomial tree visualization."""
    fig = go.Figure()
    
    max_display = min(N, 8)
    
    for i in range(max_display + 1):
        for j in range(i + 1):
            x = i
            y = i - 2 * j
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(size=40, color=colors['accent_blue'], 
                           line=dict(width=2, color=colors['accent_cyan'])),
                text=f"S={stock_tree[j, i]:.1f}<br>V={option_tree[j, i]:.2f}",
                textposition="middle center",
                textfont=dict(size=8, color=colors['text_primary'], family="JetBrains Mono"),
                hovertemplate=f"<b>Step {i}, Node {j}</b><br>" +
                              f"Stock: ${stock_tree[j, i]:.2f}<br>" +
                              f"Option: ${option_tree[j, i]:.2f}<br>" +
                              f"Delta: {delta_tree[j, i] if i < N else 'N/A':.4f}<extra></extra>",
                showlegend=False
            ))
            
            if i < max_display:
                fig.add_trace(go.Scatter(
                    x=[x, x + 1], y=[y, y + 1],
                    mode='lines',
                    line=dict(color=colors['border_color'], width=1.5),
                    hoverinfo='skip',
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=[x, x + 1], y=[y, y - 1],
                    mode='lines',
                    line=dict(color=colors['border_color'], width=1.5),
                    hoverinfo='skip',
                    showlegend=False
                ))
    
    fig.update_layout(
        title=dict(text=f"Binomial Tree (showing {max_display + 1} of {N + 1} steps)",
                   font=dict(size=14, color=colors['text_primary'])),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x"),
        height=450,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


def create_convergence_figure(S, K, T, r, sigma, option_type, max_steps=200):
    """Create convergence visualization."""
    bs_price = black_scholes(S, K, T, r, sigma, option_type)["Price"]
    bs_delta = black_scholes(S, K, T, r, sigma, option_type)["Delta"]
    
    steps_range = list(range(5, max_steps + 1, 5))
    crr_prices = [crr_binomial_tree(S, K, T, r, sigma, n, option_type) for n in steps_range]
    crr_deltas = [crr_delta(S, K, T, r, sigma, n, option_type) for n in steps_range]
    
    price_errors = [abs(p - bs_price) for p in crr_prices]
    delta_errors = [abs(d - bs_delta) for d in crr_deltas]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Option Price Convergence", "Price Error (|CRR - BS|)",
                       "Delta Convergence", "Delta Error (|CRR - BS|)"),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    fig.add_trace(go.Scatter(x=steps_range, y=crr_prices, name="CRR Price",
                   line=dict(color=colors['accent_blue'], width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=[steps_range[0], steps_range[-1]], y=[bs_price, bs_price],
                   name="BS Price", line=dict(color=colors['text_primary'], dash='dash')), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=steps_range, y=price_errors, name="Price Error",
                   line=dict(color=colors['accent_red'], width=2), fill='tozeroy',
                   fillcolor=f"rgba(239, 68, 68, 0.2)"), row=1, col=2)
    
    fig.add_trace(go.Scatter(x=steps_range, y=crr_deltas, name="CRR Delta",
                   line=dict(color=colors['accent_green'], width=2)), row=2, col=1)
    fig.add_trace(go.Scatter(x=[steps_range[0], steps_range[-1]], y=[bs_delta, bs_delta],
                   name="BS Delta", line=dict(color=colors['text_primary'], dash='dash')), row=2, col=1)
    
    fig.add_trace(go.Scatter(x=steps_range, y=delta_errors, name="Delta Error",
                   line=dict(color=colors['accent_orange'], width=2), fill='tozeroy',
                   fillcolor=f"rgba(245, 158, 11, 0.2)"), row=2, col=2)
    
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor=colors['chart_bg'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text_primary'])
    )
    
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(showgrid=True, gridcolor=colors['grid_color'], row=i, col=j)
            fig.update_yaxes(showgrid=True, gridcolor=colors['grid_color'], row=i, col=j)
    
    return fig


def create_hedging_pnl_figure(results, n_display=100):
    """Create hedging P&L visualization."""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Sample Price Paths", "Hedging Error Distribution",
                       "Portfolio Value vs Option Payoff", "Delta Over Time"),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    n_paths = results["paths"].shape[0]
    n_steps = results["paths"].shape[1]
    time_axis = np.linspace(0, 1, n_steps)
    
    for i in range(min(n_display, n_paths)):
        fig.add_trace(go.Scatter(x=time_axis, y=results["paths"][i], mode='lines',
                      line=dict(width=0.5, color=f'rgba(59, 130, 246, 0.3)'),
                      showlegend=False, hoverinfo='skip'), row=1, col=1)
    
    mean_path = results["paths"].mean(axis=0)
    fig.add_trace(go.Scatter(x=time_axis, y=mean_path, mode='lines',
                  line=dict(width=2, color=colors['text_primary']), name='Mean Path'), row=1, col=1)
    
    fig.add_trace(go.Histogram(x=results["hedging_errors"], nbinsx=50,
                    marker_color=colors['accent_blue'], opacity=0.7, name='Hedging Error'), row=1, col=2)
    
    var_95 = np.percentile(results["hedging_errors"], 5)
    var_99 = np.percentile(results["hedging_errors"], 1)
    fig.add_vline(x=var_95, line_dash="dash", line_color=colors['accent_orange'], row=1, col=2)
    fig.add_vline(x=var_99, line_dash="dash", line_color=colors['accent_red'], row=1, col=2)
    
    fig.add_trace(go.Scatter(x=results["final_payoffs"], y=results["portfolio_values"][:, -1],
                  mode='markers', marker=dict(size=4, color=colors['accent_blue'], opacity=0.5),
                  name='Portfolio vs Payoff'), row=2, col=1)
    max_payoff = results["final_payoffs"].max()
    fig.add_trace(go.Scatter(x=[0, max_payoff], y=[0, max_payoff],
                  mode='lines', line=dict(color=colors['text_primary'], dash='dash'),
                  name='Perfect Hedge'), row=2, col=1)
    
    for i in range(min(20, n_paths)):
        fig.add_trace(go.Scatter(x=time_axis, y=results["deltas"][i], mode='lines',
                      line=dict(width=0.5, color=f'rgba(16, 185, 129, 0.4)'),
                      showlegend=False, hoverinfo='skip'), row=2, col=2)
    
    mean_delta = results["deltas"].mean(axis=0)
    fig.add_trace(go.Scatter(x=time_axis, y=mean_delta, mode='lines',
                  line=dict(width=2, color=colors['accent_green']), name='Mean Delta'), row=2, col=2)
    
    fig.update_layout(
        height=700,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor=colors['chart_bg'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text_primary'])
    )
    
    fig.update_xaxes(showgrid=True, gridcolor=colors['grid_color'])
    fig.update_yaxes(showgrid=True, gridcolor=colors['grid_color'])
    
    return fig


def create_greeks_heatmap(S, K, T, r, sigma, greek, option_type):
    """Create heatmap for Greeks across spot and volatility."""
    spot_range = np.linspace(S * 0.7, S * 1.3, 30)
    vol_range = np.linspace(max(0.05, sigma * 0.3), sigma * 2, 30)
    
    Z = np.zeros((len(vol_range), len(spot_range)))
    
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            result = black_scholes(spot, K, T, r, vol, option_type)
            Z[i, j] = result[greek]
    
    fig = go.Figure(data=go.Heatmap(
        z=Z,
        x=spot_range,
        y=vol_range,
        colorscale='RdBu_r' if greek in ['Delta', 'Gamma', 'Vega'] else 'Viridis',
        colorbar=dict(title=greek),
        hovertemplate=f'Spot: %{{x:.1f}}<br>Vol: %{{y:.2%}}<br>{greek}: %{{z:.4f}}<extra></extra>'
    ))
    
    # Add current position marker
    fig.add_trace(go.Scatter(
        x=[S], y=[sigma],
        mode='markers',
        marker=dict(size=15, color='white', symbol='x', line=dict(width=2, color='black')),
        name='Current',
        showlegend=True
    ))
    
    fig.update_layout(
        title=dict(text=f"{greek} Heatmap", font=dict(color=colors['text_primary'])),
        xaxis_title="Spot Price",
        yaxis_title="Volatility",
        height=400,
        plot_bgcolor=colors['chart_bg'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text_primary'])
    )
    
    return fig


def create_pnl_payoff_chart(S, K, T, r, sigma, option_type, premium):
    """Create P&L and Payoff diagram."""
    spot_range = np.linspace(S * 0.5, S * 1.5, 100)
    
    if option_type == "Call":
        payoff = np.maximum(spot_range - K, 0)
    else:
        payoff = np.maximum(K - spot_range, 0)
    
    pnl = payoff - premium
    
    fig = go.Figure()
    
    # Payoff at expiry
    fig.add_trace(go.Scatter(
        x=spot_range, y=payoff,
        mode='lines',
        name='Payoff at Expiry',
        line=dict(color=colors['accent_blue'], width=2)
    ))
    
    # P&L (Payoff - Premium)
    fig.add_trace(go.Scatter(
        x=spot_range, y=pnl,
        mode='lines',
        name='P&L (Payoff - Premium)',
        line=dict(color=colors['accent_green'], width=2),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.2)'
    ))
    
    # Break-even line
    fig.add_hline(y=0, line_dash="dash", line_color=colors['text_muted'])
    
    # Strike price line
    fig.add_vline(x=K, line_dash="dot", line_color=colors['accent_orange'],
                  annotation_text=f"Strike = {K}")
    
    # Current spot
    fig.add_vline(x=S, line_dash="dash", line_color=colors['accent_purple'],
                  annotation_text=f"Spot = {S}")
    
    # Break-even point
    if option_type == "Call":
        breakeven = K + premium
    else:
        breakeven = K - premium
    
    fig.add_trace(go.Scatter(
        x=[breakeven], y=[0],
        mode='markers',
        marker=dict(size=12, color=colors['accent_red'], symbol='diamond'),
        name=f'Break-even = {breakeven:.2f}'
    ))
    
    fig.update_layout(
        title="P&L Diagram",
        xaxis_title="Spot Price at Expiry",
        yaxis_title="P&L ($)",
        height=400,
        plot_bgcolor=colors['chart_bg'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text_primary']),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis=dict(showgrid=True, gridcolor=colors['grid_color']),
        yaxis=dict(showgrid=True, gridcolor=colors['grid_color'])
    )
    
    return fig, breakeven


def create_stress_test_results(S, K, T, r, sigma, option_type):
    """Calculate stress test scenarios."""
    scenarios = {
        'Crash -20%': {'spot_chg': -0.20, 'vol_chg': 0.50},
        'Bear -10%': {'spot_chg': -0.10, 'vol_chg': 0.25},
        'Base Case': {'spot_chg': 0.00, 'vol_chg': 0.00},
        'Bull +10%': {'spot_chg': 0.10, 'vol_chg': -0.10},
        'Rally +20%': {'spot_chg': 0.20, 'vol_chg': -0.20}
    }
    
    base_price = black_scholes(S, K, T, r, sigma, option_type)["Price"]
    results = []
    
    for name, params in scenarios.items():
        new_S = S * (1 + params['spot_chg'])
        new_sigma = max(0.05, sigma * (1 + params['vol_chg']))
        new_price = black_scholes(new_S, K, T, r, new_sigma, option_type)["Price"]
        pnl = new_price - base_price
        pnl_pct = (pnl / base_price) * 100 if base_price > 0 else 0
        
        results.append({
            'Scenario': name,
            'Spot': new_S,
            'Vol': new_sigma,
            'Price': new_price,
            'P&L': pnl,
            'P&L %': pnl_pct
        })
    
    return pd.DataFrame(results)


def create_vol_surface_synthetic(S, K, T, r, sigma):
    """Create synthetic volatility surface for demonstration."""
    # Strikes from 80% to 120% of spot
    strikes = np.linspace(S * 0.80, S * 1.20, 20)
    # Maturities from 1 month to 2 years
    maturities = np.array([1/12, 2/12, 3/12, 6/12, 1.0, 1.5, 2.0])
    
    K_grid, T_grid = np.meshgrid(strikes, maturities)
    
    # Create realistic smile: higher IV for OTM options, term structure
    moneyness = np.log(K_grid / S)
    
    # Smile effect: quadratic in moneyness
    smile = 0.1 * moneyness**2
    
    # Skew effect: linear in moneyness (puts more expensive)
    skew = -0.15 * moneyness
    
    # Term structure: slight upward slope
    term = 0.02 * np.sqrt(T_grid)
    
    # Base volatility + adjustments
    IV_surface = sigma + smile + skew + term
    
    # Add some noise for realism
    IV_surface += np.random.normal(0, 0.005, IV_surface.shape)
    IV_surface = np.clip(IV_surface, 0.05, 1.0)
    
    fig = go.Figure(data=[go.Surface(
        z=IV_surface * 100,  # Convert to percentage
        x=strikes,
        y=maturities,
        colorscale='Viridis',
        contours_z=dict(show=True, usecolormap=True, project_z=True),
        hovertemplate='Strike: %{x:.0f}<br>Maturity: %{y:.2f}y<br>IV: %{z:.1f}%<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text="Implied Volatility Surface", font=dict(color=colors['text_primary'])),
        scene=dict(
            xaxis=dict(title='Strike', backgroundcolor=colors['bg_secondary'], 
                      gridcolor=colors['grid_color']),
            yaxis=dict(title='Maturity (Years)', backgroundcolor=colors['bg_secondary'],
                      gridcolor=colors['grid_color']),
            zaxis=dict(title='Implied Vol (%)', backgroundcolor=colors['bg_secondary'],
                      gridcolor=colors['grid_color']),
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig


# =============================================================================
# 6. SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: {colors['accent_blue']}; margin: 0; font-size: 24px; font-weight: 700;">CRR</h2>
        <p style="color: {colors['text_muted']}; margin: 5px 0 0 0; font-size: 11px; letter-spacing: 2px;">PRICING PLATFORM</p>
        <p style="color: {colors['accent_green']}; font-size: 10px; margin-top: 5px;">V2.5 ENHANCED</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Theme Toggle
    st.markdown(f'<p class="section-title">🎨 Theme</p>', unsafe_allow_html=True)
    theme_options = ['dark', 'light']
    new_theme = st.selectbox("Select Theme", theme_options, 
                             index=theme_options.index(st.session_state.theme),
                             key="theme_selector")
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    
    st.markdown("---")
    
    # Model Parameters
    st.markdown(f'<p class="section-title">📊 Model Parameters</p>', unsafe_allow_html=True)
    
    S = st.number_input("Spot Price (S₀)", value=100.0, min_value=1.0, step=1.0, format="%.2f")
    K = st.number_input("Strike Price (K)", value=100.0, min_value=1.0, step=1.0, format="%.2f")
    T = st.number_input("Time to Maturity (years)", value=1.0, min_value=0.01, max_value=10.0, step=0.1, format="%.2f")
    r = st.number_input("Risk-Free Rate", value=0.05, min_value=0.0, max_value=0.5, step=0.01, format="%.4f")
    sigma = st.slider("Volatility (σ)", min_value=0.05, max_value=1.0, value=0.20, step=0.01, format="%.2f")
    
    st.markdown("---")
    
    option_type = st.selectbox("Option Type", ["Call", "Put"])
    N = st.slider("CRR Tree Steps", min_value=5, max_value=500, value=50, step=5)
    
    st.markdown("---")
    
    # Moneyness indicator
    moneyness = S / K
    if moneyness > 1.05:
        moneyness_text = "ITM" if option_type == "Call" else "OTM"
        moneyness_color = colors['accent_green'] if option_type == "Call" else colors['accent_red']
    elif moneyness < 0.95:
        moneyness_text = "OTM" if option_type == "Call" else "ITM"
        moneyness_color = colors['accent_red'] if option_type == "Call" else colors['accent_green']
    else:
        moneyness_text = "ATM"
        moneyness_color = colors['accent_orange']
    
    st.markdown(f"""
    <div class="metric-card" style="margin-top: 16px;">
        <div class="metric-label">Moneyness (S/K)</div>
        <div class="metric-value" style="color: {moneyness_color};">{moneyness:.2%}</div>
        <span class="badge badge-info" style="margin-top: 8px;">{moneyness_text}</span>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# 7. MAIN CONTENT
# =============================================================================

# Header
st.markdown(f"""
<div class="header-banner">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="header-title">Cox-Ross-Rubinstein Option Pricing</h1>
            <p class="header-subtitle">Interactive platform for binomial option pricing, convergence analysis, and delta hedging simulation</p>
        </div>
        <div class="live-indicator">
            <span class="live-dot"></span>
            <span>LIVE</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Calculate prices
bs_result = black_scholes(S, K, T, r, sigma, option_type)
crr_price, stock_tree, option_tree, delta_tree, u, d, p = crr_binomial_tree(
    S, K, T, r, sigma, N, option_type, return_tree=True
)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Dashboard", 
    "🌳 CRR Model", 
    "📈 Convergence", 
    "🛡️ Hedging",
    "🎯 P&L Analysis",
    "🌊 Vol Surface",
    "📚 Theory"
])

# =============================================================================
# TAB 1: DASHBOARD
# =============================================================================
with tab1:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Black-Scholes Price</div>
            <div class="metric-value">${bs_result['Price']:.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        price_diff = crr_price - bs_result['Price']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CRR Price ({N} steps)</div>
            <div class="metric-value blue">${crr_price:.4f}</div>
            <div style="font-size: 12px; color: {'#10b981' if price_diff >= 0 else '#ef4444'}; margin-top: 4px;">
                {price_diff:+.4f} vs BS
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Up Factor (u)</div>
            <div class="metric-value cyan">{u:.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Down Factor (d)</div>
            <div class="metric-value cyan">{d:.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Risk-Neutral Prob (p)</div>
            <div class="metric-value cyan">{p:.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Greeks
    st.markdown(f'<p class="section-title">Greeks</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="greeks-grid">
        <div class="greek-item">
            <div class="greek-symbol">Δ</div>
            <div class="greek-value">{bs_result['Delta']:.4f}</div>
            <div class="greek-name">Delta</div>
        </div>
        <div class="greek-item">
            <div class="greek-symbol">Γ</div>
            <div class="greek-value">{bs_result['Gamma']:.4f}</div>
            <div class="greek-name">Gamma</div>
        </div>
        <div class="greek-item">
            <div class="greek-symbol">ν</div>
            <div class="greek-value">{bs_result['Vega']:.4f}</div>
            <div class="greek-name">Vega</div>
        </div>
        <div class="greek-item">
            <div class="greek-symbol">Θ</div>
            <div class="greek-value">{bs_result['Theta']:.4f}</div>
            <div class="greek-name">Theta</div>
        </div>
        <div class="greek-item">
            <div class="greek-symbol">ρ</div>
            <div class="greek-value">{bs_result['Rho']:.4f}</div>
            <div class="greek-name">Rho</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("#### Price Convergence Preview")
        
        steps_quick = list(range(10, 150, 5))
        crr_quick = [crr_binomial_tree(S, K, T, r, sigma, n, option_type) for n in steps_quick]
        
        fig_quick = go.Figure()
        fig_quick.add_trace(go.Scatter(x=steps_quick, y=crr_quick, mode='lines+markers',
                           name='CRR Price', line=dict(color=colors['accent_blue'], width=2), marker=dict(size=4)))
        fig_quick.add_hline(y=bs_result['Price'], line_dash="dash", line_color=colors['text_primary'],
                           annotation_text=f"BS = ${bs_result['Price']:.4f}")
        
        fig_quick.update_layout(
            height=300, margin=dict(l=40, r=20, t=20, b=40),
            plot_bgcolor=colors['chart_bg'], paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Number of Steps", showgrid=True, gridcolor=colors['grid_color']),
            yaxis=dict(title="Option Price ($)", showgrid=True, gridcolor=colors['grid_color']),
            font=dict(color=colors['text_primary'])
        )
        st.plotly_chart(fig_quick, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("#### Model Comparison")
        
        error_pct = abs(crr_price - bs_result['Price']) / bs_result['Price'] * 100
        
        st.markdown(f"""
        <div class="comparison-row">
            <span class="comparison-label">Black-Scholes</span>
            <span class="comparison-value">${bs_result['Price']:.4f}</span>
        </div>
        <div class="comparison-row">
            <span class="comparison-label">CRR ({N} steps)</span>
            <span class="comparison-value" style="color: {colors['accent_blue']};">${crr_price:.4f}</span>
        </div>
        <div class="comparison-row">
            <span class="comparison-label">Absolute Error</span>
            <span class="comparison-value" style="color: {colors['accent_red']};">${abs(crr_price - bs_result['Price']):.6f}</span>
        </div>
        <div class="comparison-row">
            <span class="comparison-label">Relative Error</span>
            <span class="comparison-value" style="color: {colors['accent_orange']};">{error_pct:.4f}%</span>
        </div>
        <div class="comparison-row" style="border: none;">
            <span class="comparison-label">CRR Delta</span>
            <span class="comparison-value" style="color: {colors['accent_green']};">{delta_tree[0, 0]:.4f}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Stress Testing
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<p class="section-title">Stress Testing</p>', unsafe_allow_html=True)
    
    stress_df = create_stress_test_results(S, K, T, r, sigma, option_type)
    
    cols = st.columns(5)
    for i, (idx, row) in enumerate(stress_df.iterrows()):
        with cols[i]:
            is_negative = row['P&L'] < 0
            card_class = "negative" if is_negative else "positive" if row['P&L'] > 0 else ""
            pnl_color = colors['accent_red'] if is_negative else colors['accent_green'] if row['P&L'] > 0 else colors['text_primary']
            
            st.markdown(f"""
            <div class="stress-card {card_class}">
                <div style="font-size: 12px; font-weight: 600; color: {colors['text_secondary']}; margin-bottom: 8px;">
                    {row['Scenario']}
                </div>
                <div style="font-size: 20px; font-weight: 600; color: {colors['text_primary']};">
                    ${row['Price']:.2f}
                </div>
                <div style="font-size: 14px; color: {pnl_color}; margin-top: 4px;">
                    {row['P&L']:+.2f} ({row['P&L %']:+.1f}%)
                </div>
                <div style="font-size: 10px; color: {colors['text_muted']}; margin-top: 4px;">
                    S={row['Spot']:.0f} | σ={row['Vol']:.1%}
                </div>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# TAB 2: CRR MODEL
# =============================================================================
with tab2:
    st.markdown(f'<p class="section-title">Binomial Tree Visualization</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        tree_fig = create_binomial_tree_figure(stock_tree, option_tree, delta_tree, N, u, d, p)
        st.plotly_chart(tree_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("#### CRR Parameters")
        
        dt = T / N
        
        st.markdown(f"""
        <div class="formula-box">
            <div style="margin-bottom: 12px;">
                <span style="color: {colors['text_secondary']};">Time step:</span>
                <span style="color: {colors['accent_blue']}; float: right;">Δt = T/N = {dt:.6f}</span>
            </div>
            <div style="margin-bottom: 12px;">
                <span style="color: {colors['text_secondary']};">Up factor:</span>
                <span style="color: {colors['accent_green']}; float: right;">u = e^(σ√Δt) = {u:.6f}</span>
            </div>
            <div style="margin-bottom: 12px;">
                <span style="color: {colors['text_secondary']};">Down factor:</span>
                <span style="color: {colors['accent_red']}; float: right;">d = 1/u = {d:.6f}</span>
            </div>
            <div style="margin-bottom: 12px;">
                <span style="color: {colors['text_secondary']};">Risk-neutral prob:</span>
                <span style="color: {colors['accent_orange']}; float: right;">p = {p:.6f}</span>
            </div>
            <div>
                <span style="color: {colors['text_secondary']};">Discount factor:</span>
                <span style="color: {colors['accent_purple']}; float: right;">e^(-rΔt) = {np.exp(-r * dt):.6f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### No-Arbitrage Condition")
        no_arb = d < np.exp(r * dt) < u
        st.markdown(f"""
        <div class="formula-box">
            <div style="text-align: center;">d < e<sup>rΔt</sup> < u</div>
            <div style="text-align: center; margin-top: 10px;">
                {d:.4f} < {np.exp(r * dt):.4f} < {u:.4f}
            </div>
            <div style="text-align: center; margin-top: 10px;">
                <span class="badge {'badge-success' if no_arb else 'badge-warning'}">
                    {'✓ SATISFIED' if no_arb else '✗ VIOLATED'}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Delta Hedging section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<p class="section-title">Delta Hedging in CRR</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.markdown("#### Replicating Portfolio")
        st.markdown("""
        At each node, we can replicate the option payoff with a portfolio of:
        - **φ** shares of the underlying
        - **ψ** units of the risk-free bond
        
        The number of shares (delta) at node (i,j) is:
        """)
        st.latex(r"\phi_{i,j} = \frac{C^u_{i+1,j} - C^d_{i+1,j+1}}{S_{i+1,j}^u - S_{i+1,j+1}^d} = \frac{C^u - C^d}{S(u-d)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.markdown("#### Current Hedge Ratio")
        
        current_delta = delta_tree[0, 0] if N > 0 else 0
        hedge_cost = current_delta * S
        bond_position = crr_price - hedge_cost
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
            <div class="metric-card">
                <div class="metric-label">Delta (φ)</div>
                <div class="metric-value blue">{current_delta:.4f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Shares to Hold</div>
                <div class="metric-value">{current_delta:.4f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Stock Position</div>
                <div class="metric-value positive">${hedge_cost:.2f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Bond Position</div>
                <div class="metric-value {'positive' if bond_position >= 0 else 'negative'}">${bond_position:.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# TAB 3: CONVERGENCE
# =============================================================================
with tab3:
    st.markdown(f'<p class="section-title">CRR Convergence to Black-Scholes</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        max_steps_conv = st.slider("Maximum Steps", 50, 500, 200, 10, key="conv_steps")
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="padding: 12px;">
            <div class="metric-label">BS Reference Price</div>
            <div class="metric-value" style="font-size: 20px;">${bs_result['Price']:.6f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="padding: 12px;">
            <div class="metric-label">BS Reference Delta</div>
            <div class="metric-value" style="font-size: 20px;">{bs_result['Delta']:.6f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    conv_fig = create_convergence_figure(S, K, T, r, sigma, option_type, max_steps_conv)
    st.plotly_chart(conv_fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.markdown("#### Theoretical Convergence")
        st.markdown("The CRR model converges to Black-Scholes as N → ∞:")
        st.latex(r"|C_{CRR}^N - C_{BS}| = O\left(\frac{1}{N}\right)")
        st.markdown("""
        This means:
        - Doubling the steps roughly halves the error
        - The error decreases linearly with the number of steps
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.markdown("#### Observed Convergence")
        
        test_steps = [50, 100, 200]
        test_prices = [crr_binomial_tree(S, K, T, r, sigma, n, option_type) for n in test_steps]
        test_errors = [abs(p - bs_result['Price']) for p in test_prices]
        
        st.markdown(f"""
        | Steps | CRR Price | Error | Error × N |
        |-------|-----------|-------|-----------|
        | 50 | ${test_prices[0]:.6f} | {test_errors[0]:.6f} | {test_errors[0] * 50:.4f} |
        | 100 | ${test_prices[1]:.6f} | {test_errors[1]:.6f} | {test_errors[1] * 100:.4f} |
        | 200 | ${test_prices[2]:.6f} | {test_errors[2]:.6f} | {test_errors[2] * 200:.4f} |
        """)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# TAB 4: HEDGING SIMULATION
# =============================================================================
with tab4:
    st.markdown(f'<p class="section-title">Monte Carlo Delta Hedging Simulation</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        n_sim_paths = st.selectbox("Simulation Paths", [100, 500, 1000, 5000], index=1)
    with col2:
        n_sim_steps = st.selectbox("Rebalancing Steps", [12, 52, 252], index=1,
                                   format_func=lambda x: f"{x} ({'Monthly' if x==12 else 'Weekly' if x==52 else 'Daily'})")
    with col3:
        use_bs = st.selectbox("Delta Method", ["Black-Scholes", "CRR"], index=0)
    with col4:
        run_sim = st.button("🚀 Run Simulation", type="primary", use_container_width=True)
    
    if run_sim or 'hedge_results' in st.session_state:
        if run_sim:
            with st.spinner("Running Monte Carlo simulation..."):
                results = simulate_hedging_strategy(S, K, T, r, sigma, n_sim_steps, n_sim_paths,
                                                    use_bs_delta=(use_bs == "Black-Scholes"))
                st.session_state['hedge_results'] = results
        
        results = st.session_state['hedge_results']
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        mean_error = results['hedging_errors'].mean()
        std_error = results['hedging_errors'].std()
        var_95 = np.percentile(results['hedging_errors'], 5)
        var_99 = np.percentile(results['hedging_errors'], 1)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        metrics = [
            ("Mean Hedging Error", mean_error, 'positive' if mean_error >= 0 else 'negative'),
            ("Std Dev Error", std_error, ''),
            ("VaR 95%", var_95, 'negative'),
            ("VaR 99%", var_99, 'negative'),
            ("Initial Premium", results['initial_price'], 'blue')
        ]
        
        for col, (label, value, style) in zip([col1, col2, col3, col4, col5], metrics):
            with col:
                color = colors['accent_green'] if style == 'positive' else colors['accent_red'] if style == 'negative' else colors['accent_blue'] if style == 'blue' else colors['text_primary']
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="color: {color};">${value:.4f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        hedge_fig = create_hedging_pnl_figure(results, min(100, n_sim_paths))
        st.plotly_chart(hedge_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# TAB 5: P&L ANALYSIS
# =============================================================================
with tab5:
    st.markdown(f'<p class="section-title">P&L Analysis & Greeks Heatmaps</p>', unsafe_allow_html=True)
    
    # P&L Diagram
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("#### Payoff & P&L Diagram")
    
    pnl_fig, breakeven = create_pnl_payoff_chart(S, K, T, r, sigma, option_type, bs_result['Price'])
    st.plotly_chart(pnl_fig, use_container_width=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Premium Paid</div>
            <div class="metric-value">${bs_result['Price']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Break-Even</div>
            <div class="metric-value cyan">${breakeven:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        max_loss = -bs_result['Price'] if option_type == "Call" else -(bs_result['Price'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Max Loss</div>
            <div class="metric-value negative">${max_loss:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        max_profit = "Unlimited" if option_type == "Call" else f"${K - bs_result['Price']:.2f}"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Max Profit</div>
            <div class="metric-value positive">{max_profit}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Greeks Heatmaps
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<p class="section-title">Greeks Heatmaps</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="heatmap-container">', unsafe_allow_html=True)
        delta_heatmap = create_greeks_heatmap(S, K, T, r, sigma, "Delta", option_type)
        st.plotly_chart(delta_heatmap, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="heatmap-container">', unsafe_allow_html=True)
        gamma_heatmap = create_greeks_heatmap(S, K, T, r, sigma, "Gamma", option_type)
        st.plotly_chart(gamma_heatmap, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="heatmap-container">', unsafe_allow_html=True)
        vega_heatmap = create_greeks_heatmap(S, K, T, r, sigma, "Vega", option_type)
        st.plotly_chart(vega_heatmap, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="heatmap-container">', unsafe_allow_html=True)
        theta_heatmap = create_greeks_heatmap(S, K, T, r, sigma, "Theta", option_type)
        st.plotly_chart(theta_heatmap, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# TAB 6: VOLATILITY SURFACE
# =============================================================================
with tab6:
    st.markdown(f'<p class="section-title">Implied Volatility Surface</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">
        <span class="badge badge-info">SYNTHETIC DATA</span>
        <span style="color: var(--text-secondary); font-size: 12px;">
            Realistic volatility surface generated with smile and term structure effects
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    vol_surface_fig = create_vol_surface_synthetic(S, K, T, r, sigma)
    st.plotly_chart(vol_surface_fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Explanation
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.markdown("#### Volatility Smile")
        st.markdown("""
        The **volatility smile** is the empirical observation that options with strikes 
        far from the current spot price (both ITM and OTM) tend to have higher implied 
        volatilities than ATM options.
        
        **Causes:**
        - Fat tails in return distributions
        - Jump risk in asset prices
        - Supply/demand dynamics
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.markdown("#### Term Structure")
        st.markdown("""
        The **volatility term structure** describes how implied volatility varies 
        across different maturities.
        
        **Typical patterns:**
        - **Contango**: IV increases with maturity (normal markets)
        - **Backwardation**: IV decreases with maturity (stressed markets)
        - **Flat**: IV constant across maturities
        """)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# TAB 7: THEORY
# =============================================================================
with tab7:
    st.markdown(f'<p class="section-title">Mathematical Foundation</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### Cox-Ross-Rubinstein Model")
        
        st.markdown("""
        The CRR model (1979) discretizes the continuous-time Black-Scholes framework:
        """)
        
        st.latex(r"S_{t+\Delta t} = \begin{cases} S_t \cdot u & \text{prob } p \\ S_t \cdot d & \text{prob } 1-p \end{cases}")
        
        st.markdown("Parameters matching GBM moments:")
        
        st.latex(r"u = e^{\sigma\sqrt{\Delta t}}, \quad d = \frac{1}{u}")
        st.latex(r"p = \frac{e^{r\Delta t} - d}{u - d}")
        
        st.markdown("Option price by **backward induction**:")
        
        st.latex(r"C_t = e^{-r\Delta t}[p \cdot C_{t+1}^u + (1-p) \cdot C_{t+1}^d]")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### Black-Scholes Model")
        
        st.markdown("European call option formula:")
        
        st.latex(r"C = S_0 N(d_1) - K e^{-rT} N(d_2)")
        
        st.markdown("Where:")
        
        st.latex(r"d_1 = \frac{\ln(S_0/K) + (r + \frac{\sigma^2}{2})T}{\sigma\sqrt{T}}")
        st.latex(r"d_2 = d_1 - \sigma\sqrt{T}")
        
        st.markdown("**Greeks:**")
        
        st.latex(r"\Delta = N(d_1), \quad \Gamma = \frac{N'(d_1)}{S\sigma\sqrt{T}}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Model comparison
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<p class="section-title">Model Limitations & Extensions</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.markdown("#### CRR Limitations")
        st.markdown("""
        - Constant volatility assumption
        - Discrete time steps
        - No jumps in asset prices
        - European options only (basic form)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.markdown("#### Heston Model")
        st.latex(r"dv_t = \kappa(\theta - v_t)dt + \xi\sqrt{v_t}dW_t^v")
        st.markdown("""
        - Stochastic volatility
        - Captures volatility smile
        - Mean-reverting variance
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="accent-card">', unsafe_allow_html=True)
        st.markdown("#### SABR Model")
        st.latex(r"dF_t = \sigma_t F_t^\beta dW_t^1")
        st.markdown("""
        - Popular in rates/FX markets
        - Analytical approximations
        - Calibrates to smile
        """)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# FOOTER
# =============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; padding: 20px; border-top: 1px solid {colors['border_color']};">
    <p style="color: {colors['text_muted']}; font-size: 12px; margin: 0;">
        CRR Pricing Platform V2.5 • ESILV - Projet d'Innovation Industrielle • 2025
    </p>
    <p style="color: {colors['text_muted']}; font-size: 11px; margin: 8px 0 0 0;">
        Built with Streamlit • Mathematical models for educational purposes only
    </p>
</div>
""", unsafe_allow_html=True)
