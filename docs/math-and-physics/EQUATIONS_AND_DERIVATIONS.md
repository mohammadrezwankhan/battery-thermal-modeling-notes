# Implemented equations and explanatory derivations

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

The preserved [lumped model guide](../../models/README.md) is canonical for feature examples. This page traces the implemented balance, then derives its discrete and exact forms. Equations below are a transcription or algebraic consequence of the cited implementation; they are not a new solver or measured-cell model.

## One temperature state

Let $T$ be cell temperature in °C, $T_K=T+273.15$ in K, $C=m c_p$ in J/K, $G$ the effective convection conductance in W/K, and $\beta=dU_{oc}/dT$ in V/K. Current $I>0$ means discharge. Each input is constant within its supplied interval.

$$
R(T)=R_0[1+\alpha_R(T-T_{ref})],\qquad
Q_{irr}=I^2R(T),\qquad Q_{rev}=-I(T+273.15)\beta.
$$

$$
Q_{gen}=Q_{irr}+Q_{rev}+Q_{ext},\quad
Q_{conv}=G(T-T_a),\quad
Q_{rad}=\epsilon\sigma A[(T+273.15)^4-(T_s+273.15)^4].
$$

$$
C\frac{dT}{dt}=Q_{gen}-Q_{conv}-Q_{rad}=Q_{net}(T).
$$

Positive external heat enters the node; negative external heat is a prescribed sink. Positive rejection leaves it. Consequently a warmer ambient or radiative enclosure can produce negative rejection. Reversing current reverses reversible heat but leaves $I^2R$ unchanged. The surroundings schedule $T_s$ is independent of $T_a$ when supplied, otherwise it follows ambient. Source: [models/lumped_cell_thermal.py:13–52](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L13-L52); [models/lumped_cell_thermal.py:130–185](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L130-L185); [models/lumped_cell_thermal.py:468–504](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L468-L504); [models/lumped_cell_thermal.py:783–823](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L783-L823).

The implemented Stefan–Boltzmann literal is `5.670374419e-8` W/(m²·K⁴). [NIST's 2022 CODATA table](https://physics.nist.gov/cuu/pdf/wallet_2022.pdf) prints the exact derived constant with trailing digits indicated by an ellipsis. The finite Python literal is its implemented numerical approximation; do not interpret the guide's word “exact” as unlimited floating-point precision. The [NREL reading note](../../references/reading-log-nrel-li-ion-thermal-characterization.md) supplies research context, not fitted parameters for this model.

## Euler and the affine exact update

Euler uses the interval-start rate:

$$T_{n+1}=T_n+\frac{Q_{net}(T_n)}{C}\Delta t_n.$$

With radiation disabled, resistance and reversible heat make the within-interval equation affine. Its constant temperature-feedback slope is

$$b=I^2R_0\alpha_R-I\beta-G\quad [\mathrm{W/K}].$$

Writing $q_n=Q_{net}(T_n)$, integration of $C\,d(T-T_n)/dt=q_n+b(T-T_n)$ gives

$$
T_{n+1}-T_n=
\begin{cases}
q_n\Delta t_n/C,&b=0,\\
(q_n/b)\operatorname{expm1}(b\Delta t_n/C),&b\ne0.
\end{cases}
$$

The implementation uses the exact equality `b == 0.0` and `math.expm1`; it rejects enabled radiation for exact-linear and Euler. Exact-linear removes discretization error for this affine equation up to floating-point effects; it does not validate interval averaging, material parameters or the one-node approximation. [models/lumped_cell_thermal.py:112–119](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L112-L119); [models/lumped_cell_thermal.py:903–945](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L903-L945).

For a stable linear interval ($b<0$), the derived equilibrium is $T_*=T_n-q_n/b$ and time constant $\tau=-C/b$. Euler's perturbation multiplier is $1+b\Delta t/C$: asymptotic stability requires $0<\Delta t<2C/|b|$, with a nonoscillatory approach when $0<\Delta t\le C/|b|$. These are explanatory linear conditions, not enforced runtime guards. If $b>0$, the affine model has positive feedback; this is not a chemical thermal-runaway mechanism. [models/lumped_cell_thermal.py:903–933](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L903-L933).

## Bounded-step RK4

RK4 chooses $N=\max(1,\lceil\Delta t/\Delta t_{max}\rceil)$ equal internal steps $h=\Delta t/N$, evaluates four classical Runge–Kutta derivative stages, and validates finite/above-absolute-zero temperatures. It supports the nonlinear radiation term. The bound is a maximum step, not an adaptive tolerance or error estimate. Only the outer interval endpoint is returned; internal stage/substep states are not output samples. [models/lumped_cell_thermal.py:507–547](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L507-L547); [models/lumped_cell_thermal.py:947–993](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L947-L993).

## Energy and limit reporting

For every method, the stored interval energy is $E_n=C(T_{n+1}-T_n)$, and the bookkeeping residual is

$$r_E=\left|C(T_N-T_0)-\sum_n E_n\right|.$$

It is a telescoping identity apart from floating-point accumulation, not independent heat-rate quadrature. `energy_balance_error_j` is the compatibility alias for the same value. CSV heat rates remain start samples even for exact-linear/RK4; multiplying them by the interval duration generally does not reproduce the integrated state change. [models/lumped_cell_thermal.py:247–277](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L247-L277); [models/lumped_cell_thermal.py:953–962](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L953-L962); [tests/test_lumped_cell_thermal.py:406–441](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L406-L441).

Upper-limit crossings use the chord fraction $(T_L-T_n)/(T_{n+1}-T_n)$ between reported states. Exposure sums only the portions strictly above $T_L$; lower limits analogously count strictly below. Upper margin is $T_L-\max T_n$, lower margin is $\min T_n-T_{min}$. These postprocessing approximations do not solve a continuous event root. [models/lumped_cell_thermal.py:283–394](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L283-L394).

## Browser subset

The active browser assumes $T_0=T_a$, constant positive heat $Q$, constant $G>0$, constant $C$, and no other heat terms. At browser time $t$ in minutes,

$$\Delta T=\frac{Q}{G}(1-e^{-60Gt/C}),\quad T=T_a+\Delta T,\quad E_{stored}=C\Delta T/1000\;\mathrm{kJ}.$$

It reports $G\Delta T$ as heat removed and $Q-G\Delta T$ as `residualW` (net heating in W). That quantity is distinct from the native bookkeeping residual in J. [docs/index.html:167–172](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L167-L172); [docs/index.html:257–259](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L257-L259).
