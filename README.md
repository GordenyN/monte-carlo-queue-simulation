# Monte Carlo Queue Simulation

##  Overview

This project is a **Monte Carlo simulation** of a multi-channel service system with a finite-length queue, designed to model real-world inspection or service processes — such as vehicle inspections, customer service centers, or technical support systems.

It captures the behavior of:

* random arrival of requests (e.g., vehicles),
* parallel service channels (e.g., inspectors),
* queue buildup when all channels are busy,
* queue overflows (request loss),
* and state changes over time (visualized).

---

##  Objectives

* Simulate a **queuing system** with finite channels and queue capacity.
* Visualize the **state of each service channel** and **queue slot** over time.
* Evaluate system load, waiting, and potential refusals.
* Apply **Monte Carlo methods** to model randomness in arrival and service processes.

---



## Parameters

| Parameter                | Description                                  | Example |
| ------------------------ | -------------------------------------------- | ------- |
| `lambda_rate`            | Arrival rate (e.g., 36 vehicles/day)         | 36 / 24 |
| `mu_rate`                | Service rate (e.g., 1 vehicle per 0.5 hours) | 1 / 0.5 |
| `num_channels`           | Number of parallel service channels          | 2       |
| `max_queue_length`       | Maximum allowed queue length                 | 3       |
| `total_time`             | Simulation time span (in hours)              | 24      |
| `max_wait_time_in_queue` | Optional: max wait before rejection          | 2       |



---

##  Methodology

This simulation uses the **Monte Carlo method** — relying on randomly generated interarrival and service times (exponentially distributed) to imitate real-world stochastic behavior.

---


## Requirements

NumPy
Matplotlib
