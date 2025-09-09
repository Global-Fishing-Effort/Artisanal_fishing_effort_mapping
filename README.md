# README
## Mapping global artisanal fisheries

This is a repository for spatialising country-level artisanal fishing effort data from
[Rousseau et al. 2019 and 2024](https://metadata.imas.utas.edu.au/geonetwork/srv/eng/catalog.search#/metadata/1241a51d-c8c2-4432-aa68-3d2bae142794)
to grid cells, based on observed, high resolution, satellite imagery from Skylight (provided by Minderoo) and [observed Sentinel 2 Satellite Imagery from Global Fishing Watch
data](https://globalfishingwatch.org/data-download/datasets/public-sentinel2-vessel-detections%3Av1.0)
(a top-down approach). We apply a similar methodology to that of [McDonald et al. 2024](https://www.pnas.org/doi/10.1073/pnas.2400592121)


Please read this file before trying to reproduce the output from this research project. Below you will find information on the model structure and data, contact information for the repository creator, and a description of the repository structure with each section explained.

## Approach

We use two-stage hurdle random forest models to predict fishing effort. The first stage predicts whether any fishing occurs in a pixel (classification), and the second stage predicts the intensity of fishing if it occurred (regression).
This model predicts the spatial distribution of fishing effort globally, using environmental, spatial, and fleet-specific predictors to distribute country-level fishing effort data across a global grid. 

### Model Structure

The models predict the **proportion of fishing effort** in each grid
cell. We fit an individual model for each flag state represented in Rousseau et al. 2019 and 2024:

#### Categorical Predictors

-   Vessel length category (length_category)
-   Mesopelagic zone (33 distinct regions) ([Sutton et al
    2017](<https://www.sciencedirect.com/science/article/pii/S0967063717301437>))
-   Exclusive Economic Zone (EEZ) ([Marine Regions V11](https://www.vliz.be/en/imis?dasid=6316&doiid=386))
-   FAO major fishing area ([FAO Fisheries and Aquaculture 2024 Division](https://www.fao.org/fishery/geonetwork/srv/eng/catalog.search#/metadata/ac02a460-da52-11dc-9d70-0017f293bd28)
- Ocean region (e.g., Pacific, Atlantic, etc) ([Global Oceans and Seas, version 1](https://doi.org/10.14284/542))
- [World Bank Development Indicators regions from R countrycode package](http://joss.theoj.org/papers/10.21105/joss.00848)

#### Continuous Predictors

-   Location (longitude, latitude)
-   Distance measures:
    -   Distance from port (m) ([Global Fishing Watch; Kroodsma et al. 2018](https://globalfishingwatch.org/data-download/datasets/public-distance-from-port-v1))
    -   Distance from shore (m) ([Global Fishing Watch; Kroodsma et al. 2018](https://globalfishingwatch.org/data-download/datasets/public-distance-from-shore-v1))
    - Distance to nearest seamount (m) ([Yesson et al. 2020](https://doi.pangaea.de/10.1594/PANGAEA.921688))
-   Environmental variables:
    -   Chlorophyll-A concentration (mean, sd) in mg/m³ (Present: [Aqua MODIS Chl-a 4km monthly](https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1chlamday.html))
    -   Sea surface temperature (mean, sd) in °C (Present: [NOAA 0.25-deg Daily OI SST V2.1](https://coastwatch.pfeg.noaa.gov/erddap/info/ncdcOisst21Agg_LonPM180/index.html))
    -   Wind speed (mean, sd) in m/s (Present: [CCMP Wind Vector V2.1, 4x daily](https://data.remss.com/ccmp/))
    - El Niño Souther Oscillation index (mean and sd) ([NOAA ENSO 3.4 Index](https://psl.noaa.gov/data/correlation/oni.data))
    - Pacific Decadal Oscillation Index ([NOAA PDO Index](https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/ersst.v5.pdo.dat))
-   Bathymetry (depth in m) ([Global Fishing Watch; Kroodsma et al. 2018](https://globalfishingwatch.org/data-download/datasets/public-bathymetry-v1))
- [Global Fishing Index governance capacity, Spijkers wt al. 2023](https://cdn.minderoo.org/assets/documents/policies/20220505-global-fishing-index-2021-report.pdf)
-   Year (Model trained on 2009-2024)

We estimate the amount of fishing effort in each cell by multplying the
total known amount (per flag, sector (artisnal), and vessel length) (from Rousseau et al. 2019) by the
proportion in each cell (per those same categories).

### **Historical Predictions**

The model can be used to predict historical fishing effort distributions
under the following assumptions:

#### Key Assumptions: 

1.  The relationships between environmental conditions and fishing
    effort distribution are relatively stable over time

2.  The basic responses of fish and fishers to environmental conditions
    are similar across decades

#### **Implementation Details**

-   Model is trained on 2009-2024 data

-   For historical predictions:

    -   Uses environmental data from the target year

    -   Uses Rousseau total fishing effort from the target year

    -   Maintains the learned relationships between predictors and
        effort distribution

    -   The total amount of fishing effort in each flag country is allocated
    to the proportional contribution as modeled. I.e., we estimate the
    amount of fishing effort in each cell by multiplying the total
    amount by the modelled proportion value in each cell.
    
#### **Historical data used**

 - Chorophyll-a: [ISIMIP; Büchner 2024](https://data.isimip.org/datasets/49dc048b-29e5-4cde-a89a-2fe448d86476/)
 - Wind speed: [ISIMIP; Lange & Büchner 2021](https://data.isimip.org/datasets/dbcf73ba-878d-41d4-be7d-e28ce13121bc/ )
 - Sea Surface Temperature: [ISIMIP; Büchner 2024](https://data.isimip.org/datasets/9e8a4b3f-5a56-4f4c-9677-1737a9f952d7/)

####  **Limitations**

Users should be aware that historical predictions may not capture:

-   Technological changes in fishing capabilities

-   Evolution of fishing strategies and practices

-   Changes in management regulations

### Other assumptions

 - We limit artisanal fisheries to "Inshore fishing areas", which are areas <=50km from shore AND <=200m depth AND adjacent to a population (i.e., <=50km from a populated area, Volkholz et al. 2024), as defined by Chuenpagdee et al. (2006) and the Sea Around US Project (Pauly et al. 2020). 
 - We restrict fishing areas to cells which have less than 9 months per year of ice coverage (Liu et al. 2022, Kawaguchi & Press 2009, Hewitt 1997).
 - This is a "top-down" approach, using published and reported fishing effort estimates from Rousseau et al. 2019. Given this, we are not modelling potential effort, we are only creating a new spatial allocation model to distribute reported effort. There may be cases where countries under-report their effort, and we are not estimating any "new" effort, just where the reported effort is placed. 
 
## File structure

### 'prep' folder

The prep folder contains all code necessary to run the models and
generate the spatialised fishing effort data.

All scripts are numbered by the order in which they should be run.
Within the prep folder, there are multiple folders, which have their own
descriptions.

### 'R' folder

Contains reference scripts 'dir.R',
which hold regularly used directory file paths and functions. These are
sourced within markdown scripts when needed.

### 'data' folder

The data folder is divided into a number of subfolders, each with their
own sub directories. The main sub directories within the data folder are
listed below.

| Folder         | Description                                                                                                                                                         |
|:------------------------------|:---------------------------------------|
| vessels       | This folder contains prepped to 0.5 degree vessel detection data from Skylight and Sentinel-2 data |
| int            | This folder contains a number of intermediate data products that are used in the markdown files, and are necessary for reproduction, specifically, the historical climate data |
| model_features | Processed versions of raw data sets we will use for the model. All data stored here are processed to 0.5 by 0.5 degree cell sizes.|


## Contact

Please direct any correspondence to Gage Clawson at `gage.clawson@utas.edu.au`

## Reproducibility

We strongly advocate for open and reproducible science. The code in this repository enables a use to recreate the results outlined in the above publication. There are a few important points to know/adhere to for the code to run smoothly:

 - The code must be run as an R project (unless you would like to recreate it in another language) - the code within relies on relative file paths from the project home folder. 
 - There is large data required throughout, that we do not include in this repository due to GitHub's large file size limits. Please follow any instructions to download this data that is contained in the scripts within the `prep` folder. All data used is freely accessible online, except for the Skylight data provided by Minderoo. 

## Data sources

 - Arel-Bundock, V., Enevoldsen, N., Yetman, C., 2018. countrycode: An R package to convert country names and country codes. JOSS 3, 848. https://doi.org/10.21105/joss.00848
 - Büchner, M., 2024. ISIMIP3b ocean input data. https://doi.org/10.48364/ISIMIP.575744.5
 - Chuenpagdee, R., Liguori, L., Palomares, M.L., Daniel Pauly, 2006. Bottom-up, global estimates of small-scale marine fisheries catches. Fisheries Centre Research Reports 14, 105.
 - FAO Fisheries and Aquaculture Division, 2024. FAO Statistical Areas for Fishery Purposes.
 - Flanders Marine Institute (VLIZ), Belgium, 2021. Global Oceans and Seas, version 1. https://doi.org/10.14284/542
 - Flanders Marine Institute (VLIZ), Belgium, 2019. Maritime Boundaries Geodatabase: Maritime Boundaries and Exclusive Economic Zones (200NM). https://doi.org/10.14284/386
 - Global Fishing Watch, 2025. 2019 (annual data) Vessel detections from Sentinel 2. https://doi.org/10.5281/ZENODO.15978309
 - Hewitt, R.P., 1997. Areal and seasonal extent of sea-ice cover off the Northwestern side of the Antarctic peninsula: 1979 to 1996. CCAMLR Science 4, 65–73.
 - Hu, C., Lee, Z., Franz, B., 2012. Chlorophyll a algorithms for oligotrophic oceans: A novel approach based on three‐band reflectance difference. J. Geophys. Res. 117, 2011JC007395. https://doi.org/10.1029/2011JC007395
 - Huang, B., Liu, C., Banzon, V.F., Freeman, E., Graham, G., Hankins, W., Smith, T.M., Zhang, H.-M., n.d. NOAA 0.25-degree Daily Optimum Interpolation Sea Surface Temperature (OISST), Version 2.1. https://doi.org/10.25921/RE9P-PT57
 - Kawaguchi, S., Nicol, S., Press, A.J., 2009. Direct effects of climate change on the Antarctic krill fishery. Fisheries Management Eco 16, 424–427. https://doi.org/10.1111/j.1365-2400.2009.00686.x
 - Kroodsma, D.A., Mayorga, J., Hochberg, T., Miller, N.A., Boerder, K., Ferretti, F., Wilson, A., Bergman, B., White, T.D., Block, B.A., Woods, P., Sullivan, B., Costello, C., Worm, B., 2018. Tracking the global footprint of fisheries. Science 359, 904–908. https://doi.org/10.1126/science.aao5646
 - Lange, S., Büchner, M., 2021. ISIMIP3b bias-adjusted atmospheric climate input data. https://doi.org/10.48364/ISIMIP.842396.1
 - Liu, X., Stock, C., Dunne, J., Lee, M., Shevliakova, E., Malyshev, S., Milly, P.C.D., Büchner, M., 2022. ISIMIP3a ocean physical and biogeochemical input data [GFDL-MOM6-COBALT2 dataset]. https://doi.org/10.48364/ISIMIP.920945
 - Mantua, N.J., Hare, S.R., 2002. The Pacific Decadal Oscillation. Journal of Oceanography 58, 35–44. https://doi.org/10.1023/A:1015820616384
 - McDonald, G., Bone, J., Costello, C., Englander, G., Raynor, J., 2024. Global expansion of marine protected areas and the redistribution of fishing effort. Proc. Natl. Acad. Sci. U.S.A. 121, e2400592121. https://doi.org/10.1073/pnas.2400592121
 - Mears, C., Lee, T., Ricciardulli, L., Wang, X., Wentz, F., 2022. Improving the Accuracy of the Cross-Calibrated Multi-Platform (CCMP) Ocean Vector Winds. Remote Sensing 14, 4230. https://doi.org/10.3390/rs14174230
 - Oceanic Niño Index (ONI), 2024.
 - Pauly, D., Zeller, D., Palomares, M.L., 2020. Sea Around Us Concepts, Design, and Data.
 - Rousseau, Y., Blanchard, J.L., Novaglio, C., Pinnell, K.A., Tittensor, D.P., Watson, R.A., Ye, Y., 2024. A database of mapped global fishing activity 1950–2017. Sci Data 11, 48. https://doi.org/10.1038/s41597-023-02824-6
 - Rousseau, Y., Watson, R.A., Blanchard, J.L., Fulton, E.A., 2019. Evolution of global marine fishing fleets and the response of fished resources. Proc. Natl. Acad. Sci. U.S.A. 116, 12238–12243. https://doi.org/10.1073/pnas.1820344116
 - Spijkers, J., Mackay, M., Turner, J., McNeill, A., Travaille, K., Wilcox, C., 2023. Diversity of global fisheries governance: Types and contexts. Fish and Fisheries 24, 111–125. https://doi.org/10.1111/faf.12713
 - Sutton, T.T., Clark, M.R., Dunn, D.C., Halpin, P.N., Rogers, A.D., Guinotte, J., Bograd, S.J., Angel, M.V., Perez, J.A.A., Wishner, K., Haedrich, R.L., Lindsay, D.J., Drazen, J.C., Vereshchaka, A., Piatkowski, U., Morato, T., Błachowiak-Samołyk, K., Robison, B.H., Gjerde, K.M., Pierrot-Bults, A., Bernal, P., Reygondeau, G., Heino, M., 2017. A global biogeographic classification of the mesopelagic zone. Deep Sea Research Part I: Oceanographic Research Papers 126, 85–102. https://doi.org/10.1016/j.dsr.2017.05.006
 - Volkholz, J., Lange, S., Sauer, I., Otto, C., 2024. ISIMIP3b population input data. https://doi.org/10.48364/ISIMIP.889136.2
 - Yesson, C., Letessier, T.B., Nimmo-Smith, A., Hosegood, P., Brierley, A.S., Hardouin, M., Proud, R., 2020. List of seamounts in the world oceans - An update. https://doi.org/10.1594/PANGAEA.921688
