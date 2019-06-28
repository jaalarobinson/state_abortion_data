# Data Blueprint

### What is this?

This dataset is a compilation of variables from many, many different sources.
This is the blueprint. It allows you (and me) to trace the origin, processing,
and coding of each contained variable.

### Variable List

<ul>
<li>[Abortion Rate Residence](#Abortion-Rate-Residence)</li>
<li>[Abortion Rate Occurrence](#abortion-rate-occurrence)</li>
<li>[Number of Abortions - Residence](#number_abortions_residence)</li>
<li>[Number of Abortions - Occurrence](#number_abortions_occurrence)</li>
<li>[Number of Abortion Providers](#number_providers)</li>
<li>[Percent Counties No Provider](#Percent_Counties_No_Provider)</li>
<li>[Percent Women Without Provider](#Percent_Women_Without_Provider)</li>
<li>[Percent Change Abortion Rate Occurrence](#Percent_Change_Abortion_Rate_Occurence)</li>
<li>[Percent Change Providers](#Percent_Change_Providers)</li>
<li>[Percent Women Medicaid](#Percent_Women_Medicaid)</li>
<li>[Percent Women Private Insurance](#Percent_Women_Uninsured)</li>
<li>[Percent Women Uninsured](#Percent_Women_Uninsured)</li>

</ul>


### Abortion Rate Residence

#### Definition

The number of abortions per 1,000 women aged 15-44, by state of residence

#### Years
1978-1982 1984-1985 1987-1988 1991-1992 1996 1999-2000 2004-2005
2007-2008 2011 2013-2014

#### Source
This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

The 2014 data comes from a report using two sources to compile state-level estimates of pregnancy desires and outcomes. These two sources are the Guttmacher Institute's 2014 U.S. Abortion Patient Survey (APS) and the annual Pregnancy Risk Assessment Monitoring System (PRAMS) conducted by the Centers for Disease Control and Prevention (CDC). The 2014 describes the calculation of the abortion rate in the following quote:

<blockquote>
For abortion counts, most but not all states conduct annual surveillance of abortions provided in the state. However, abortions are almost always underreported to state surveillance systems. In addition, for the calculation of state-specific pregnancy rates, abortion counts need to be according to the individual’s state of residence (not where the abortion occurred).  We therefore used counts of abortions by state of residence for 2014 estimated from a periodic national census of abortion providers and ancillary surveys of clinics conducted by the Guttmacher Institute, in conjunction with data on the state of residence of individuals having abortions in each state from the CDC and state-level health departments
</blockquote>

Guttmacher does not provide its sources for previous years, specifically, though it is possible to make an educated guess that these estimates derive from the same, ongoing, sources. There are additional sources that also provide trend data on abortions using the CDC surveillance of abortion clinics, however, as Guttmacher specifically discounts this data are underestimates (see above blockquote), I do not provide these as sources.

As far as I know, the raw data for the CDC estimates are not readily accessible. At some point in the future, I may compile what I can find of these estimates based on published articles and the tables contained therein. However, a rough comparison between the CDC values and the values based on the Guttmacher survey show small deviations rather than large discrepancies. Additionally, due to different state reporting practices, the CDC data does not include some large states, such as California and Florida. Guttmacher, in this sense, is more complete.

### Coding

This variable is coded as a float64 variable as it is the ratio of abortions performed to population.

### Processing

This variable required no additional processing.

### Missing Data

As this measure was collected intermittently, there is missing data for the years between censuses. (Planned) This data will be forward-filled from the most recent census.

#### References

Jatlaoui TC, Shah J, Mandel MG, et al. Abortion Surveillance — United States, 2014. MMWR Surveill Summ 2018;66(No. SS-25):1–44.

Kost K, Maddow-Zimet I and Kochhar S, Pregnancy Desires and Pregnancies at the State Level: Estimates for 2014, New York: Guttmacher Institute, 2018.

### Abortion Rate Occurrence

#### Definition

The number of abortions per 1,000 women aged 15-44, by state of occurrence

#### Years
1973-1982 1984-1985 1987-1988 1991-1992 1995-1996 1999-2000 2004-2005
2007-2008 2010-2011 2013-2014

#### Source
This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

The data from all years come from an ongoing census of abortion providers carried out by Guttmacher since 1973. Researchers collect data on the number of abortions performed, then combine this with known population data to estimate national and state-level abortion rates.

While Guttmacher Data Center is inconsistent in its citation, I have compiled the original papers describing each wave of this census. I include all below as sources in the interest of full data transparency. The raw census information is not available, to my knowledge.

### Coding

This variable is coded as a float64 variable as it is the ratio of abortions performed to population.

### Processing

This variable required no additional processing.

### Missing Data

As this measure was collected intermittently, there is missing data for the years between censuses. (Planned) This data will be forward-filled from the most recent census.

#### References

Finer LB and Henshaw SK, Abortion incidence and services in the United States in 2000, Perspectives on Sexual and Reproductive Health, 2003, 35(1):6–15.

Finer LB and Henshaw SK, Disparities in rates of unintended pregnancy in the United States, 1994 and 2001, Perspectives on Sexual and Reproductive Health, 2006, 38(2):90–96.

K. Henshaw, Stanley & Van Vort, Jennifer. (1990). Abortion Services in the United States, 1987 and 1988. Family planning perspectives. 22. 102-8, 142. 10.2307/2135639.

Henshaw SK and Van Vort J, Abortion incidence and services in the United States, 1991 and 1992, Family Planning Perspectives, 1994, 26(3):100–106 & 112.

Henshaw SK, Abortion incidence and services in the United States, 1995–1996, Family Planning Perspectives, 1998, 30(6):263–270 & 287.

Jones RK et al., Abortion in the United States: incidence and access to services, 2005, Perspectives on Sexual and Reproductive Health, 2008, 40(1):6–16.

Jones RK and Kooistra K, Abortion incidence and access to services in the United States, 2008, Perspectives on Sexual and Reproductive Health, 2011, 43(1):41–50.

Jones RK and Jerman J, Abortion incidence and service availability in the United States, 2011, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.

### Number of Abortions - Residence

#### Definition

Number of women in state who have had legal abortions (excludes nonresidents of the United States who obtained abortions in the United States)

#### Years
1978-1982 1984-1985 1987-1988 1991-1992 1996 1999-2000 2004-2005
2007-2008 2011 2013-2014

#### Source
This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Residence](#abortion-rate-residence)).

### Coding

This variable is coded as an int64 variable.

### Processing

This variable required no additional processing.

### Missing Data

As this measure was collected intermittently, there is missing data for the years between censuses. (Planned) This data will be forward-filled from the most recent census.

#### References

Henshaw, Stanley K., and Kathryn Lyle Kost. Trends in the characteristics of women obtaining abortions, 1974 to 2004. New York: Guttmacher Institute, 2008.

Kost K, Maddow-Zimet I and Kochhar S, Pregnancy Desires and Pregnancies at the State Level: Estimates for 2014, New York: Guttmacher Institute, 2018.

### Number of Abortions - Occurrence

#### Definition

Number of abortions legally performed in state (excludes nonresidents of the United States who obtained abortions in the United States)

#### Years
1973-1982 1984-1985 1987-1988 1991-1992 1995-1996 1999-2000 2004-2005
2007-2008 2010-2011 2013-2014

#### Source
This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)).

### Coding

This variable is coded as an int64 variable.

### Processing

This variable required no additional processing.

### Missing Data

As this measure was collected intermittently, there is missing data for the years between censuses. (Planned) This data will be forward-filled from the most recent census.

#### References

Finer LB and Henshaw SK, Abortion incidence and services in the United States in 2000, Perspectives on Sexual and Reproductive Health, 2003, 35(1):6–15.

Finer LB and Henshaw SK, Disparities in rates of unintended pregnancy in the United States, 1994 and 2001, Perspectives on Sexual and Reproductive Health, 2006, 38(2):90–96.

K. Henshaw, Stanley & Van Vort, Jennifer. (1990). Abortion Services in the United States, 1987 and 1988. Family planning perspectives. 22. 102-8, 142. 10.2307/2135639.

Henshaw SK and Van Vort J, Abortion incidence and services in the United States, 1991 and 1992, Family Planning Perspectives, 1994, 26(3):100–106 & 112.

Henshaw SK, Abortion incidence and services in the United States, 1995–1996, Family Planning Perspectives, 1998, 30(6):263–270 & 287.

Jones RK et al., Abortion in the United States: incidence and access to services, 2005, Perspectives on Sexual and Reproductive Health, 2008, 40(1):6–16.

Jones RK and Kooistra K, Abortion incidence and access to services in the United States, 2008, Perspectives on Sexual and Reproductive Health, 2011, 43(1):41–50.

Jones RK and Jerman J, Abortion incidence and service availability in the United States, 2011, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.

### Number of Abortion Providers

#### Definition

A provider is a hospital, clinic, or physician's office where abortions are performed. This is distinct from, though includes, an abortion clinic, which is a non-hospital facility that reported 400 or more abortions a year, including abortion clinics and non-specialized clinics.

#### Years
1973-1982 1984-1985 1987-1988 1991-1992 1995-1996 1999-2000 2005 2008 2011 2014

#### Source
This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)).

### Coding

This variable is coded as an int64 variable.

### Processing

This variable required no additional processing.

### Missing Data

As this measure was collected intermittently, there is missing data for the years between censuses. (Planned) This data will be forward-filled from the most recent census.

#### References

Finer LB and Henshaw SK, Abortion incidence and services in the United States in 2000, Perspectives on Sexual and Reproductive Health, 2003, 35(1):6–15.

Finer LB and Henshaw SK, Disparities in rates of unintended pregnancy in the United States, 1994 and 2001, Perspectives on Sexual and Reproductive Health, 2006, 38(2):90–96.

K. Henshaw, Stanley & Van Vort, Jennifer. (1990). Abortion Services in the United States, 1987 and 1988. Family planning perspectives. 22. 102-8, 142. 10.2307/2135639.

Henshaw SK and Van Vort J, Abortion incidence and services in the United States, 1991 and 1992, Family Planning Perspectives, 1994, 26(3):100–106 & 112.

Henshaw SK, Abortion incidence and services in the United States, 1995–1996, Family Planning Perspectives, 1998, 30(6):263–270 & 287.

Jones RK et al., Abortion in the United States: incidence and access to services, Perspectives on Sexual and Reproductive Health, 2008, 40(1):6–16.

Jones RK and Kooistra K, Abortion incidence and access to services in the United States, Perspectives on Sexual and Reproductive Health, 2011, 43(1):41–50.

Jones RK and Jerman J, Abortion incidence and service availability in the United States, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.


### Percent Counties No Provider

#### Definition

Percent of counties in the state in that year that had no abortion provider.

A provider is a hospital, clinic, or physician's office where abortions are performed. This is distinct from, though includes, an abortion clinic, which is a non-hospital facility that reported 400 or more abortions a year, including abortion clinics and non-specialized clinics.

#### Years
1976 1988 1992 1996 2000 2005 2008 2011 2014

#### Source

This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)).


### Coding

This variable is coded as an int64 as the percents are provided by Guttmacher rounded to the nearest whole number.

### Processing

This variable required no additional processing.

### Missing Data

As this measure was collected intermittently, there is missing data for the years between censuses. (Planned) This data will be forward-filled from the most recent census.

#### References

Frost JJ et al., Contraceptive Needs and Services, 2014 Update, New York: Guttmacher Institute, 2016, https://www.guttmacher.org/sites/default/files/report_pdf/contraceptive-needs-and-services-2014_1.pdf

Henshaw, Stanley K., and Kathryn Lyle Kost. Trends in the characteristics of women obtaining abortions, 1974 to 2004. New York: Guttmacher Institute, 2008.

Jones RK and Kooistra K, Abortion incidence and access to services in the United States, Perspectives on Sexual and Reproductive Health, 2011, 43(1):41–50.

Jones RK and Jerman J, Abortion incidence and service availability in the United States, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.



### Percent Women No Provider

#### Definition

Percent of women aged 15-44 living in a county without an abortion provider.

A provider is a hospital, clinic, or physician's office where abortions are performed. This is distinct from, though includes, an abortion clinic, which is a non-hospital facility that reported 400 or more abortions a year, including abortion clinics and non-specialized clinics.

#### Years
1988 1992 1996 2000 2005 2008 2011 2014

#### Source

This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)). They then compare this information with population estimates from the CDC.

### Coding

This variable is coded as an int64 as the percents are provided by Guttmacher rounded to the nearest whole number.

### Processing

This variable required no additional processing.

### Missing Data

As this measure was collected intermittently, there is missing data for the years between censuses. (Planned) This data will be forward-filled from the most recent census.

#### References

National Center for Health Statistics, Vintage 2014 Post Censal Estimates of the Resident Population of the United States (April 1, 2010, July 1, 2010 - July 1, 2014), by Year, County, Single-Year of Age (0, 1, 2, .., 85 Years and Over), Bridged Race, Hispanic Origin, and Sex. Prepared Under a Collaborative Arrangement With the U.S.Census Bureau, 2015. <http://www.cdc.gov/nchs/nvss/bridged_race/data_documentation.htm>

Special tabulations of data from Frost JJ, Frohwirth L and Zolna MR, Contraceptive Needs and Services, 2014 Update, New York: Guttmacher Institute, 2016

Special tabulations of data from the Guttmacher Institute's 2012 Abortion Provider Census, Guttmacher Institute

Henshaw, Stanley K., and Kathryn Lyle Kost. Trends in the characteristics of women obtaining abortions, 1974 to 2004. New York: Guttmacher Institute, 2008.


### Percent Change Abortion Rate Occurrence

#### Definition

Percent change in abortion rate (number of abortions per 1,000 women aged 15-44) between 2011 and 2014

#### Years
2011 2014

#### Source

This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)).

This measure takes the difference in abortion rate between 2011 and 2014 and then divides by 100.

### Coding

This variable is coded as an int64 as the percents are provided by Guttmacher rounded to the nearest whole number.

### Processing

This variable required no additional processing.

### Missing Data

Thus far I only have data for 2014. In the future I may add trend data.

#### References

Jones RK and Jerman J, Abortion incidence and service availability in the United States, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.


### Percent Change Providers

#### Definition

Percent change in the number of abortion providers between 2011 and 2014

A provider is a hospital, clinic, or physician's office where abortions are performed. This is distinct from, though includes, an abortion clinic, which is a non-hospital facility that reported 400 or more abortions a year, including abortion clinics and non-specialized clinics.

#### Years
2011 2014

#### Source

This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)).

This measure takes the difference in abortion rate between 2011 and 2014 and then divides by 100.

### Coding

This variable is coded as an int64 as the percents are provided by Guttmacher rounded to the nearest whole number.

### Processing

This variable required no additional processing.

### Missing Data

Thus far I only have data for 2014. In the future I may add trend data.

#### References

Jones RK and Jerman J, Abortion incidence and service availability in the United States, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.

### Percent Change Clinics

#### Definition

Percent change in the number of abortion clinics between 2011 and 2014

A provider is a hospital, clinic, or physician's office where abortions are performed. This is distinct from, though includes, an abortion clinic, which is a non-hospital facility that reported 400 or more abortions a year, including abortion clinics and non-specialized clinics.

#### Years
2011 2014

#### Source

This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)).

This measure takes the difference in abortion rate between 2011 and 2014 and then divides by 100.

### Coding

This variable is coded as an int64 as the percents are provided by Guttmacher rounded to the nearest whole number.

### Processing

This variable required no additional processing.

### Missing Data

Thus far I only have data for 2014. In the future I may add trend data.

#### References

Jones RK and Jerman J, Abortion incidence and service availability in the United States, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.

### Percent US Abortions Occurence

#### Definition

The percent of all U.S. abortions that occur in the state.

#### Years
2014

#### Source

This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)).

### Coding

This variable is coded as a float64 as the percentages provided but Guttmacher are rounded to the first decimal.

### Processing

This variable required no additional processing.

### Missing Data

Thus far I only have data for 2014. In the future I may add trend data.

#### References

Jones RK and Jerman J, Abortion incidence and service availability in the United States, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.


### Percent Women Medicaid

#### Definition

Percent of women aged 15-44 covered by Medicaid

#### Years
2015

#### Source

This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)). They then compare this information with population estimates from the CDC.

### Coding

This variable is coded as an int64 as the percents are provided by Guttmacher rounded to the nearest whole number.

### Processing

This variable required no additional processing.

### Missing Data

Thus far I only have data for 2015. In the future I may add trend data.

#### References

Jones RK and Jerman J, Abortion incidence and service availability in the United States, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.

### Percent Women Private Insurance

#### Definition

Percent of women aged 15-44 covered by private insurance

#### Years
2015

#### Source

This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)). They then compare this information with population estimates from the CDC.

### Coding

This variable is coded as an int64 as the percents are provided by Guttmacher rounded to the nearest whole number.

### Processing

This variable required no additional processing.

### Missing Data

Thus far I only have data for 2015. In the future I may add trend data.

#### References

Jones RK and Jerman J, Abortion incidence and service availability in the United States, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.

### Percent Women Uninsured

#### Definition

Percent of women aged 15-44 who are uninsured

#### Years
2015

#### Source

This data was downloaded using the [Guttmacher Data Center](https://data.guttmacher.org/regions)

Guttmacher specifies that these estimates derive from their own census of abortion providers along with the CDC abortion surveillance information (See the [Abortion Rate Occurrence](#abortion-rate-occurrence)). They then compare this information with population estimates from the CDC.

### Coding

This variable is coded as an int64 as the percents are provided by Guttmacher rounded to the nearest whole number.

### Processing

This variable required no additional processing.

### Missing Data

Thus far I only have data for 2015. In the future I may add trend data.

#### References

Jones RK and Jerman J, Abortion incidence and service availability in the United States, Perspectives on Sexual and Reproductive Health, 2014, 46(1):3–14, doi:10.1363/46e0414.
