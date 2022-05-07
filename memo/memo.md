---
abstract: |
  I explain why a memo should contain sections on Who, Why, How, What,
  and When.
author:
- Carsten Wulff, *2021-06-13*, v0.1.0
title: Writing a Short Memo
documentclass: IEEEtran
papersize: a4
fontsize: 10pt
classoption: technote
---

# Who

The reader is the Who, and I think it's a good idea to explain what
you want from the reader. [@wheat] "I'm writing this memo because I would like
us all to write better memos".

Think of the reader when you write.
Unless you're writing fiction, there is no need to surprise the reader. 
Information should be clear, concise, and brief.

Leveraging lofty adverbs to pontificate your pathosesque, supreme, very
unique retorical skills just makes the reader confused, and me sound
like a pompus ass. [^1] 

# Why

> He who has a why to live can bear almost any how
-- Nietzsche

Too often we jump to the How and What before we explain the Why.

Allow me to borrow an example from circuit design:  "I need you to design a single ended, fast, analog-to-digital converter with 12-bit resolution and rail-to-rail input swing"

Those that work for you might
do as you say without question, but too often, the result is not what
you really need, because you forgot to explain the Why. 

"I need to measure a Wheatstone bridge [@wheat]. I'll measure the voltage on
one side, and then the other, quite fast, so the samples occur at the same
timeish. Then, I can take the difference in digital. The signal between
the two sides is small, 10 mV, but the signal on each side can change
from rail-to-rail, so I need really high-resolution analog-to-digital
converter"

The Why allows the reader to question the How or
What. Solving the Why is the important thing. Explain the Why
(measuring Wheatstone bridge), and then the What (single ended, fast,
high-resolution, analog-to-digital converter). 

Understanding the Why, I could say "  The
proposed solution is stupid. It's much easier to measure differentially
across the Wheatstone bridge with a differential slow analog-to-digital
converter. Also, since the differential signal is small, we don't need
high-resolution analog-to-digital converter, just a decent common mode
range"

Maybe I'd replace "stupid" by a more appropriate term, like "an
interesting idea". Why is important, to get the right How and
What.

# How

The How can be process, money, resources, tools, everything you need
to do the What. In the circuit example the How could be: "I need a
test chip in Q1 next year for the first iteration of the
analog-to-digital converter, then, about x months later, we can do the
product tapeout".

# What

The What can be a proposed solution to fix the Why. The What can give options, or
indeed be a single solution. It is important, however, that the What
flows naturally from the Why. Expect the What to be questioned.
That's the point, we want to find the best What.

# When

Either, "if we start now, when can we complete the What". Or, "we need
the What to be complete by 2021-10-11, what must we do today to get
there"? 

Often, it's hard to see When the What (become a multi
planetary spieces) to a Why (life could end on earth) can happen,
however, one can setup an early milestone (develop vertical landing with
a rocket) that must be completed on the way. Once the first milestone is
complete, then proceed to the next, and continue until complete.

# Writing

A memo is a serious text, it has a purpose. Maybe to reach a decision,
provide common background information, or spark a discussion. I believe
that we should strive to make memos well written. I do not claim to be a
reference on writing well, for that I refer to William Zinsser's book
"On Writing Well" [@oww].

# Conclusion

A memo should contain Who, Why, How, What, and When.

# References


[^1]: "very unique" doesn't exist, it's either unique, or not.
