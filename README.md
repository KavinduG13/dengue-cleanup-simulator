# Dengue Clean-Up Campaign Simulator: Timing versus Intensity in Colombo

A host–vector dengue model, calibrated to 2026 weekly case data for Colombo District with Bayesian MCMC, that asks how early and how large a breeding-site clean-up campaign must be to halve the peak weekly case count.

**[Live demo](https://kavindug13.github.io/dengue-cleanup-simulator/)** · [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KavinduG13/dengue-cleanup-simulator/blob/main/notebook/dengue-cleanup-simulator.ipynb)

![Screenshot of the web demo](figures/demo-screenshot.png)

## The problem

Dengue is endemic in Sri Lanka, and Colombo District is consistently among the most affected districts. In 2026, weekly reported cases in Colombo rose from about 240 in mid-April to a peak of 1,625 in early July, after the south-west monsoon. The main community response is breeding-site clean-up, which reduces the number of new adult *Aedes* mosquitoes.

Health authorities have to decide when to start a campaign and how intensive to make it, and it is not obvious which matters more. This project asks: **how early and how large must a clean-up campaign be to halve the peak weekly case count?** Every answer comes with an uncertainty band from the calibrated model, not a single run.

## Quick start

**Notebook:** click the *Open in Colab* badge above, then *Runtime → Run all*. It uses only NumPy, SciPy, pandas and Matplotlib, which Colab already has, and runs in under 10 minutes on a free runtime. <!-- TODO (Day 3): replace with the measured Run-all time. -->

**Web demo:** open the [live demo](https://kavindug13.github.io/dengue-cleanup-simulator/), or download this repository and double-click `docs/index.html`.

**Run locally (optional):**

```bash
pip install -r requirements.txt
jupyter notebook notebook/dengue-cleanup-simulator.ipynb
```

To rebuild the dataset from its source: `python data/make_dataset.py`.

## Using the demo

<!-- TODO (Day 4): check this matches the finished demo. -->
Sliders set the campaign intensity (the share of new mosquitoes removed), how many weeks before the expected peak the campaign starts, the basic reproduction number R0, the reporting fraction and the susceptible fraction. Press **Start** to watch the weekly case curve unfold against the no-campaign baseline. The panel shows the peak weekly cases, the total cases, the percentage reduction in the peak and the critical clean-up fraction. Full guide: [USER_GUIDE.md](USER_GUIDE.md).

## Model and mathematics

Humans follow an SEIR model and mosquitoes an SEI model. Humans are tracked as fractions of the effective susceptible population and mosquitoes per human:

$$
\frac{ds}{dt} = -\beta V_i s, \quad
\frac{de}{dt} = \beta V_i s - \sigma_h e, \quad
\frac{di}{dt} = \sigma_h e - \gamma i, \quad
\frac{dr}{dt} = \gamma i
$$

$$
\frac{dV_s}{dt} = \lambda(t) - \beta i V_s - \mu_v V_s, \quad
\frac{dV_e}{dt} = \beta i V_s - (\sigma_v + \mu_v) V_e, \quad
\frac{dV_i}{dt} = \sigma_v V_e - \mu_v V_i
$$

A campaign starting on day $t_c$ cuts mosquito recruitment by a fraction $p$: $\lambda(t) = m_0 \mu_v \left(1 - p\,\mathbf{1}[t \ge t_c]\right)$. The basic reproduction number is

$$
R_0^2 = \frac{\beta^2 m_0 \sigma_v}{\gamma\, \mu_v (\sigma_v + \mu_v)},
$$

so a campaign applied from the start stops the outbreak exactly when $p > p_c = 1 - 1/R_0^2$.

The equations are solved with hand-written explicit Euler and fourth-order Runge–Kutta (RK4) integrators at a time step of 0.5 days. The transmission rate, reporting fraction and initial infections are fitted to weekly reported cases with a hand-written random-walk Metropolis sampler and a negative-binomial observation model. Full derivations, assumptions and parameters: [THEORY.md](THEORY.md).

## Verification

Every check runs inside the notebook and ends in an `assert`, so a failure stops *Run all*.

| Check | Expected | Result |
|---|---|---|
| Human population conserved (s + e + i + r) | stays at 1 | maximum error 8.9 × 10⁻¹⁶ |
| Mosquito total after a campaign starts | follows the analytic exponential decline | maximum error 4.1 × 10⁻⁹ |
| No transmission (β = 0) | no new infections; i(t) decays as i₀e^(−γt) | passes |
| R0 formula vs next-generation matrix | equal | agree to 6 decimal places for four values of β |
| Outbreak threshold | grows just below p_c, dies out just above | growth rate +0.009/day at p_c − 0.03, −0.011/day at p_c + 0.03 |
| Time-step convergence | Euler order 1, RK4 order 4 | measured 0.98 and 4.03 |

<!-- TODO (Day 2): add the parameter-recovery check for the MCMC sampler. -->

![Time-step convergence of Euler and RK4](figures/convergence.png)

## Concepts applied

This project applies a host–vector compartmental epidemic model (SEIR humans, SEI mosquitoes), integrated with hand-written explicit Euler and fourth-order Runge–Kutta schemes whose error orders are measured. It uses Bayesian calibration with a random-walk Metropolis Markov chain Monte Carlo sampler and a negative-binomial observation model, and Monte Carlo propagation of posterior uncertainty into intervention scenarios with 95% intervals. The simulator is verified with conservation laws, the analytic R0 threshold, a next-generation-matrix check, a time-step convergence study and recovery of known parameters from synthetic data.

## Results

<!-- TODO (Day 3): replace this paragraph with the answer, the heat-map figure and the key numbers with 95% intervals. -->
Calibration to the 2026 Colombo data and the campaign scenario study (campaign intensity × start week) are in progress. This section will give the smallest campaign, and the latest start week, that halves the peak, with 95% intervals.

## Limitations and future work

- One wave, one serotype and homogeneous mixing across the whole district; real transmission varies between neighbourhoods.
- The susceptible fraction is fixed because, within a single wave, it cannot be separated from the reporting fraction. It is varied in the sensitivity analysis instead.
- A special dengue control week ran in Colombo on 15–21 June 2026, inside the fitted period. Its effect is absorbed into the baseline.
- Five of the 37 weeks in the source extraction are unusable and are left out of the fit (see [data/README.md](data/README.md)).
- With more time: a stochastic version to estimate the chance that an early campaign stops the outbreak completely, and rainfall-driven mosquito numbers.

## Key references

1. W. O. Kermack and A. G. McKendrick, "A contribution to the mathematical theory of epidemics," *Proc. R. Soc. Lond. A*, vol. 115, no. 772, pp. 700–721, 1927. doi: 10.1098/rspa.1927.0118
2. N. Metropolis, A. W. Rosenbluth, M. N. Rosenbluth, A. H. Teller and E. Teller, "Equation of state calculations by fast computing machines," *J. Chem. Phys.*, vol. 21, no. 6, pp. 1087–1092, 1953. doi: 10.1063/1.1699114
3. Epidemiology Unit, Ministry of Health, Sri Lanka, *Weekly Epidemiological Report*, vol. 53, 2026. https://www.epid.gov.lk
4. T. S. Talagala, *denguedatahub: A tidy format datasets of dengue by country*, R package v4.1.2. https://github.com/thiyangt/denguedatahub
5. Department of Census and Statistics, Sri Lanka, *Census of Population and Housing 2024: Final Report*, 2026. https://www.statistics.gov.lk

Full list: [REFERENCES.md](REFERENCES.md).

## AI assistance

Developed with the help of AI coding and writing assistants. All code was reviewed, run and verified by the author.

## Licence and credits

Code: [MIT](LICENSE). Data: weekly notified dengue cases from the *Weekly Epidemiological Report*, Epidemiology Unit, Ministry of Health, Sri Lanka, as extracted in the [denguedatahub](https://github.com/thiyangt/denguedatahub) R package by T. S. Talagala (GPL-3). Population: Census of Population and Housing 2024, Department of Census and Statistics, Sri Lanka.
