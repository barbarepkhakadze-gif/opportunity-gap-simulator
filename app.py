import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🌍 Opportunity Gap Simulator (Stable Scientific Model)")
st.markdown("""
**Created by Barbare Pkhakadze**

Computational model exploring how structural factors such as education, income,
mentorship, internet access, and social inequality influence long-term outcomes.

- **Average Opportunity Gap Index (OGI):** {avg_ogi:.2f}
- **Opportunity Inequality:** {std_ogi:.2f}

#### Interpretation

The Opportunity Gap Index measures the difference between an individual's
potential outcome (in a perfectly equal-opportunity society) and their actual
outcome under the simulated social conditions.

A higher OGI indicates that structural barriers prevented individuals from
fully realizing their potential.

The inequality measure indicates how unevenly opportunity is distributed across
the simulated population.
""")



# ---------------- UI ----------------
n = st.slider("Population size", 50, 1000, 300)
years = st.slider("Years simulated", 5, 40, 20)

edu_mean = st.slider("Education Level", 0.0, 1.0, 0.6)
income_mean = st.slider("Income Level", 0.0, 1.0, 0.5)
mentorship_mean = st.slider("Mentorship", 0.0, 1.0, 0.4)
internet_mean = st.slider("Internet Access", 0.0, 1.0, 0.7)
tax_pressure = st.slider("Tax Pressure", 0.0, 1.0, 0.3)
inequality = st.slider("Inequality Level", 0.0, 1.0, 0.4)


# ---------------- INIT POPULATION (SAFE) ----------------
def init_population(n):
    return {
        "talent": np.random.normal(0.5, 0.15, n).clip(0, 1),
        "education": np.clip(np.random.normal(edu_mean, 0.15, n), 0, 1),
        "income": np.clip(np.random.normal(income_mean, 0.2, n), 0, 1),
        "mentorship": np.clip(np.random.normal(mentorship_mean, 0.2, n), 0, 1),
        "internet": np.clip(np.random.normal(internet_mean, 0.15, n), 0, 1),
        "status": np.random.beta(2, 2, n)  # ALWAYS ARRAY, NEVER SCALAR
    }


# ---------------- OPPORTUNITY (VECTOR SAFE) ----------------
def opportunity(p):
    return (
        0.30 * p["education"] +
        0.25 * p["income"] +
        0.20 * p["mentorship"] +
        0.15 * p["internet"] +
        0.10 * (1 - tax_pressure) +
        inequality * p["status"]
    )


# ---------------- SIMULATION (NO LOOPS OVER i) ----------------
def run_simulation(n, years):
    p = init_population(n)

    real = np.zeros(n)
    ideal = np.zeros(n)

    for _ in range(years):

        opp = opportunity(p)

        growth = p["talent"] * np.log1p(1 + opp)
        shock = np.random.normal(0, 0.02, n)

        real += growth + shock
        ideal += p["talent"] * np.log1p(2.0)

        # feedback loop (SAFE normalization)
        norm = real / (np.max(real) + 1e-9)
        p["income"] = np.clip((p["income"] + norm) / 2, 0, 1)

    return real, ideal


# ---------------- RUN ----------------
if st.button("Run Simulation"):

    real, ideal = run_simulation(n, years)

    ogi = ideal - real


    st.subheader("📊 Results")
    st.write("Average OGI:", np.mean(ogi))
    st.write("Inequality (Std Dev):", np.std(ogi))

    fig1, ax1 = plt.subplots()
    ax1.hist(ogi, bins=30)
    ax1.set_title("Opportunity Gap Distribution")
    st.pyplot(fig1)

    st.caption("""
Histogram of Opportunity Gap Index values.

Each bar represents the number of individuals whose opportunity gap falls
within a particular range.

A wider distribution suggests greater variation in opportunity access.
A distribution concentrated near zero indicates a more equitable society.
""")

    fig2, ax2 = plt.subplots()
    ax2.scatter(real, ideal, alpha=0.5)
    ax2.set_title("Real vs Ideal Outcomes")
    st.pyplot(fig2)

    st.caption("""
Actual outcomes compared with potential outcomes.

Each point represents one individual.

Points closer to the diagonal line indicate individuals who achieved outcomes
closer to their theoretical potential.

Large deviations suggest structural barriers limiting opportunity.
""")

    fig3, ax3 = plt.subplots()
    ax3.plot(np.sort(ogi))
    ax3.set_title("Inequality Curve")
    st.pyplot(fig3)
    st.caption("""
Sorted Opportunity Gap Index values.

This curve visualizes how opportunity gaps are distributed throughout the
population.

A steeper curve indicates that some individuals experience substantially larger
opportunity deficits than others.
""")
    st.subheader("🏛️ Policy Insights")

if avg_ogi > 3:
    st.warning("""
The simulation suggests substantial opportunity inequality.

Potential interventions:
- Improve educational access
- Expand mentorship programs
- Increase internet connectivity
- Reduce structural barriers to advancement
""")
else:
    st.success("""
The simulation suggests relatively equitable opportunity distribution.

Most individuals are able to achieve outcomes reasonably close to their
potential under current assumptions.
""")

    st.markdown("---")

st.markdown("""
### Methodology

This simulator models opportunity as a function of:

- Education
- Income
- Mentorship
- Internet Access
- Social Status
- Tax Environment

Individual outcomes evolve over time through a stochastic agent-based model
with feedback effects, where success can influence future opportunity.

The Opportunity Gap Index (OGI) is defined as:

OGI = Potential Outcome − Actual Outcome

Higher values indicate greater unrealized potential due to structural
constraints.
""")


  
