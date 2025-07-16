---
title: "Sample 4: Math Test"
id: "20240728223001"
---

- Equations in a list! This happens often.
    - $e^{\pi i}-1=0$
    - $\boxed{x^+ = Ax+Bu}$ … higlighted with `$\boxed{}$`

Centered equations. Looks OK in LaTex, but aweful in Zettlr…
$$\underbrace{\begin{bmatrix}        x-\hat{x}^+ \\ d-\hat{d}^+    \end{bmatrix}}_{e^+} = \Big(\begin{bmatrix}        A & B_d \\ 0 & I    \end{bmatrix}     + \begin{bmatrix}        L_x \\ L_y    \end{bmatrix}\begin{bmatrix}C &C_d\end{bmatrix}\Big)\underbrace{\begin{bmatrix}    x-\hat{x} \\ d-\hat{d}\end{bmatrix}}_e$$
We can also just put `aligned` blocks into inline equations to look pretty.

$\begin{aligned}        Z^\ast, V^\ast = \argmin_{Z,V} \ \ &I_f(z_N) + \sum_{i=0}^{N-1}I(z_i,v_i)\\        \text{subject to} \quad        &z_{i+1} =Az_i+Bv_i, \quad i\in\{0,\ldots,N-1\}\\        &z_i\in\mathcal{X}\ominus\mathcal{F}_i, \quad i\in\{0,\ldots,N-1\}\\        &v_i\in\mathcal{U}\ominus K\mathcal{F}_i, \quad i\in\{0,\ldots,N-1\}\\        &z_0 = x[0]\\        &z_N\in \mathcal{X}_f^\text{ct}\ominus\mathcal{F}_N \\    \end{aligned}$

- Same with `cases`:
    - $\begin{cases} x(k+1)= Ax(k)\\ x(0) = x_0 \end{cases}$

- `$\displaystyle$` vs. bare inline `$$`
    - $\displaystyle \lim_{t\to\infty} x(t) = 0$
    - $\lim_{t\to\infty} x(t) = 0$

- Nonstandard Support
    - $\argmax$ … `$\argmax$`
    - $\argmin$ … `$\argmin$`