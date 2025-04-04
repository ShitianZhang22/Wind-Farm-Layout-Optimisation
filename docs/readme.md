# Open-Source Web-Based Planning Support Application for Wind Farm Layout

Shitian Zhang, Yiyang Chen, and Huanfa Chen

The Bartlett Centre for Advanced Spatial Analysis, University College London, UK

GISRUK 2025

## Summary

This work presents an open-source and web-based application to optimise wind farm layouts. Despite recent progress in wind farm layout optimisation research, a gap remains in translating research into practical and widely accessible tools. In this context, the proposed application offers a comprehensive and user-friendly framework to support wind farm designers in the planning process. By integrating global wind data, the application optimises wind farm layouts with the Genetic Algorithm to maximise annual energy production. Additionally, it presents a detailed summary of energy production and efficiency, facilitating effective planning practices.

**KEYWORDS**: Wind farm layout optimisation, web application, visualisation, sustainable energy 

## 1. Introduction

Wind energy plays a crucial role in sustainable energy development and achieving net-zero carbon emissions. With the rapid expansion of wind farms worldwide, enhancing energy production efficiency has become increasingly urgent.

Wind Farm Layout Optimisation (WFLO) aims to optimise wind turbine placement to minimise wake effects between turbines and maximise energy production. The wake effect refers to the reduction in wind speed after passing through a wind turbine (Wang et al., 2024), resulting in the power deficit of downstream turbines. Optimising wind turbine placement and changing the spatial distribution of wake fields can reduce the mutual effects among wind turbines (Kim, Song and You, 2024). Various algorithms have been applied to WFLO, including mathematical programming (Ulku and Alabas-Uslu, 2019), metaheuristics (Kim, Song and You, 2024), and machine learning (Jaadi et al., 2024).

A gap remains in transforming theoretical development into practical tools in WFLO research. Most WFLO studies concentrate on improving algorithm performance (Sow et al., 2024) or incorporating multiple objectives (Mittal and Mitra, 2020), often testing proposed algorithms in hypothetical case studies (Zhong, Xiao and Gao, 2024). Among the few studies on practical tool development, Reddy (2020) introduced an open-source framework integrating multiple optimisation algorithms and wake models. However, this framework requires extensive programming knowledge, making it more suitable for researchers than practitioners. Marrero and Arzola Ruíz (2021) developed a web-based tool for optimising the site selection and capacity of photovoltaic and wind farms on the national scale, but this tool does not optimise layouts within wind farms. In summary, there is a lack of accessible tools to support wind farm layout planning.

This study aims to develop a web-based tool for wind farm layout optimisation. This tool automatically retrieves wind data, optimises turbine placement, and visualises the optimised results.

## 2. Application framework

The application consists of three main modules: User Interface (UI), Data Integration Module, and Optimiser. The basic workflow is shown in **Figure 1**. First, users select the wind farm site from a predefined list and specify the number of wind turbines. Then, the Data Integration module retrieves wind speed data and sends it to the Optimiser. Finally, the Optimiser generates the optimal layout, which is displayed on the UI.

![](https://github.com/ShitianZhang22/Wind-Farm-Layout-Optimisation/blob/main/docs/fig1.png?raw=true "Application Framework")

**Figure 1** Application Framework

### 2.1. Data Integration Module

The Data Integration Module acquires historical wind data, including speed and direction, from the *ERA5-Land data from 1950 to present dataset* (European Centre for Medium-Range Weather Forecasts, 2025). ERA5-Land is derived from ERA5 and provides a consistent view of land variables, including temperature, lakes, snow, soil water, heat, evaporation, wind, and vegetation. It has a spatial resolution of 9 km and an hourly temporal frequency.

### 2.2. Optimiser

The Optimiser executes the optimisation algorithm based on user-defined settings and returns the results to the UI. The optimisation objective is to maximise Annual Energy Production (AEP), with wind turbine locations as design variables.

The Optimiser employs a Genetic Algorithm (GA) to determine the optimal wind farm layout. GA is a metaheuristic algorithm widely used for various optimisation problems. It imitates natural selection and iteratively maintains and refines a population of wind farm layouts.

## 3. Preliminary results

The application can be accessed at https://wind-farm-layout-optimisation.streamlit.app/. Currently, it includes a case study of Whitelee Wind Farm, which is located on the Eaglesham Moor in Scotland and is the largest on-shore wind farm in the United Kingdom. Whitelee Wind Farm has 215 wind turbines with an installed generation capacity of 539 MW, enough to supply more than 350,000 homes (Whitelee Windfarm, 2025).

The results include wind turbine placement and the performance of both the wind farm as a whole and individual turbines (**Figure 2**). Wind farm performance is assessed using AEP and energy production efficiency ($\eta$), which quantifies the energy transfer ratio under wake effects (Ju and Liu, 2019):

```
$\eta=\frac{AEP}{AEP_0}\times100\%$
```
	
Here, $\eta$ represents the energy production efficiency, and $AEP_0$ denotes the theoretical maximum energy production without considering wake effects between turbines.

![](https://github.com/ShitianZhang22/Wind-Farm-Layout-Optimisation/blob/main/docs/fig2.png?raw=true "Application Framework")

**Figure 2** Result of Wind Farm Layout Optimisation

## 4. Discussion and future directions

This research develops an open-source and web-based application to support wind farm planning. By integrating optimisation, data acquisition, and map-based visualisation, the application provides an accessible tool for generating optimal wind farm layouts. In the context of sustainable energy, it facilitates the connection between academic research and real-world practice.

This application will be improved in several ways. First, remote sensing data for land cover will be integrated to automatically identify infeasible areas, such as water bodies and cropland, ensuring that wind turbines are not placed in infeasible locations. In addition, the user interface will be redesigned to improve data visualisation and overall usability.

## References

European Centre for Medium-Range Weather Forecasts (2025) ‘ERA5-Land hourly data from 1950 to present’. Available at: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=‌overview (Accessed: 27 January 2025).

Jaadi, M.E. et al. (2024) ‘Optimizing wind farm layout for enhanced electricity extraction using a new hybrid PSO-ANN method’, Global Energy Interconnection, 7(3), pp. 254–269. Available at: https://doi.org/10.1016/j.gloei.2024.06.006.

Ju, X. and Liu, F. (2019) ‘Wind farm layout optimization using self-informed genetic algorithm with information guided exploitation’, Applied Energy, 248, pp. 429–445. Available at: https://doi.org/‌10.1016/j.apenergy.2019.04.084.

Kim, T., Song, J. and You, D. (2024) ‘Optimization of a wind farm layout to mitigate the wind power intermittency’, Applied Energy, 367, p. 123383. Available at: https://doi.org/10.1016/j.apenergy.‌2024.123383.

Marrero, L.E.G. and Arzola Ruíz, J. (2021) ‘Web-based tool for the decision making in photovoltaic/wind farms planning with multiple objectives’, Renewable Energy, 179, pp. 2224–2234. Available at: https://doi.org/10.1016/j.renene.2021.08.022.

Mittal, P. and Mitra, K. (2020) ‘Micrositing under practical constraints addressing the energy-noise-cost trade-off’, Wind Energy, 23(10), pp. 1905–1918. Available at: https://doi.org/10.1002/we.2525.

Reddy, S.R. (2020) ‘Wind Farm Layout Optimization (WindFLO) : An advanced framework for fast wind farm analysis and optimization’, Applied Energy, 269, p. 115090. Available at: https://‌doi.org/10.1016/j.apenergy.2020.115090.

Sow, B. et al. (2024) ‘Wasserstein-Based Evolutionary Operators for Optimizing Sets of Points: Application to Wind-Farm Layout Design’, Applied Sciences, 14(17), p. 7916. Available at: https://doi.org/10.3390/app14177916.

Ulku, I. and Alabas-Uslu, C. (2019) ‘A new mathematical programming approach to wind farm layout problem under multiple wake effects’, Renewable Energy, 136, pp. 1190–1201. Available at: https://doi.org/10.1016/j.renene.2018.09.085.

Wang, Li et al. (2024) ‘Wind turbine wakes modeling and applications: Past, present, and future’, Ocean Engineering, 309, p. 118508. Available at: https://doi.org/10.1016/j.oceaneng.2024.118508.

Whitelee Windfarm (2025) About Whitelee Windfarm, ScottishPower Renewables. Available at: https://www.whiteleewindfarm.co.uk/pages/whitelee_windfarm_about_us.aspx (Accessed: 29 January 2025).

Zhong, K., Xiao, F. and Gao, X. (2024) ‘Wind farm layout optimization using adaptive equilibrium optimizer’, The Journal of Supercomputing, 80(11), pp. 15245–15291. Available at: https://‌doi.org/10.1007/s11227-024-05986-1.

## Biographies

**Shitian Zhang** is a PhD candidate at the Bartlett Centre for Advanced Spatial Analysis (CASA), University College London. His research focuses on spatial layout optimisation for wind farms and healthcare spaces.

**Yiyang Chen** is a data analyst with expertise in data science and spatial optimisation. He previously studied at the Bartlett Centre for Advanced Spatial Analysis (CASA), University College London. His research focuses on wind farm layout optimisation using genetic algorithms, integrating geospatial analysis and meteorological data.
  
**Huanfa Chen** is an Associate Professor in Spatial Data Science, at the Bartlett Centre for Advanced Spatial Analysis (CASA), University College London. His research draws on GIScience, machine learning, and spatial optimisation to address contemporary challenges in the planning and operations of urban services, incl. policing, fire services, public health, and transport.
