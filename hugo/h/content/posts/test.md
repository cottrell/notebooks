---
title: "Mathjax example"
date: 2018-09-20T19:08:42+01:00
draft: true
---

Nothing here, just some mathjax.

<div>$$
\begin{align}
Y &\sim F_{A}(X) + \epsilon \\
Y - F_{A}(X) &\sim G_{B}(X, X') + \eta \\
\end{align}
$$</div>
And then you can naively extract information about the sensativities or importances by perturbing:
<div>$$
g_{X'}(X) = \partial_{X'} G_B(X, X')
$$</div>
