---
title: "Sample 3: More Advanced Topics"
id: "20240728195936"
---

This would be a mermaid graph. But this is also not rendered in either the implemented export or print…

# The Diagram

```mermaid
graph LR;
	dist(Disturbances)
    out(Performance Output)
    plt[Plant]
    ctr[Controller]
    dist  --> plt
    ctr == "sensing/measuremet" ==> plt
    plt == "actuation/input" ==> ctr
    ctr --> out
```

# Zettelkasten References

Reference to [[20240728173317]] Sample 1 and [[20240728223001]] Sample 4: Math Test.

This Reference points outside! [[20240315122442]] Secrets

## What about $\lambda > 0$?

- [ ] Check if Latex in title works
- [ ] Check if To Do list work
    - [ ] even if indented
    - [x] and checked

# Emojis!🎉

What was missing?🕵️

Yes! Emojis!🐳 So professional!💥

# To Dos and Questions

You know what happens a lot?

Yes! You have something todo! Ie. a #todo[Add a more convicing example.]

Somethines, there is also questions. #question[aren't those todos with an extra step?]

-   And there is also further tags like #random #whatever[with text]
-   ... some crazy notes might even contain math #todo[is $\sum_{i=1}^n x_i$ really what is meant here?]
