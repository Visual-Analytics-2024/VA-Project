# VA-Project

## Description

Mistford, a mid-sized city near a nature preserve, faces a decline in the population of a local bird species. Mitch Vogel, an ornithology student, seeks to understand the cause. He notices unusual vehicle behaviors in the nearby nature preserve and wants help analyzing vehicle data to aid his investigation.

## Ground Truth 

There is a truck that visits a Ranger Station in a fairly remote part of the Preserve periodically throughout the dataset 
timeline that is illicitly dumping factory waste. It is registering in the data as a non-Ranger vehicle, visiting a Ranger-Stop. The dumping has a slight effect on the visits to the campground nearby

## Data

Download the data [here](https://drive.google.com/file/d/1NEEWqkvGjYIHV9OP1xp2IZi9CAcg5HEC/view?usp=sharing)

The provided dataset consists of traffic data collected from sensors placed around the Boonsong Lekagul Nature Preserve. These sensors track vehicles entering and exiting the preserve through official entrances, as well as their movements within the preserve.

When vehicles enter the Preserve, they must proceed through a gate and obtain a pass.  The gate categorizes vehicles as follows:
1.	2 axle car (or motorcycle)
2.	2 axle truck
3.	3 axle truck
4.	4 axle (and above) truck
5.	2 axle bus
6.	3 axle bus

Vehicles receiving a pass with a “P” appended to their category are park service vehicles that have access to all parts of the Preserve.  Currently, the Preserve vehicles are only 2 axle trucks, so they are designated as “2P” vehicle type.
There are five types of sensors recording data.  
1.	Entrances.  All vehicles pass through an Entrance when entering or leaving the Preserve. 
2.	General-gates.  All vehicles may pass through these gates.  These sensors provide valuable information for the Preserve Rangers trying to understand the flow of traffic through the Preserve. 
3.	Gates.  These are gates that prevent general traffic from passing.  Preserve Ranger vehicles have tags that allow them to pass through these gates to inspect or perform work on the roadway beyond.  
4.	Ranger-stops.  These sensors represent working areas for the Rangers, so you will often see a Ranger-stop sensor at the end of a road managed by a Gate.  Some Ranger-stops are in other locations however, so these sensors record all traffic passing by. 
5.	Camping.  These sensors record visitors to the Preserve camping areas.  Visitors pass by these entering and exiting a campground. 
The Preserve Map

The contractors working with the Nature Preserve rangers have provided a map that presents the Preserve in terms of a 200x200 gridded area. The grid is oriented with north at the top of the map. Grid location (0,0) is at the lower left corner of the map (the SW corner). They have superimposed both the roadways and the sensor locations on this grid.  The map shows an area 12 miles x 12 miles.  
Roadways are indicated by white colored pixels on the map.  Each sensor type has its own unique color: Entrances (green), General-gates (blue), Gates (red), Ranger-stops (yellow), and Camping (orange).
Other information about the dataset:
1.	Traffic either passes through the Preserve, stay as day campers, or stay as extended campers.
2.	Preserve Rangers stay at the ranger-base toward the southeast of the Preserve when they are not working in the Preserve.
3.	The speed limit through the Preserve is 25 mph.
4.	The Preserve area does not observe “Daylight Savings Time”.
5.	The roadways traveling southward from Entrances 3 and 4 do continue to other roadways outside of the Preserve area, but these are not shown on the map.  Vehicle data will not reflect travel beyond the Preserve in this direction.  

Map 

![alt text](<data/Lekagul Roadways labeled v2.jpg>)

Data Snippet  (.csv format)

![alt text](data/data_snipet.JPG)


Data Fields:

Timestamp: the date and time the sensor reading was taken

Car-id: the assigned car ID from the entry gate

Car-type: Vehicle type as enumerated above.  “P” is appended when it is a park vehicle.

Gate-name: name of the sensors taking the reading. 
## Distribution Analysis 

### Mean and Std of Total Traffic Flux at each Gate

![alt text](data/fig/mean_std_traffic_flux_gates.png) 

**Insights**

* General Gates typically exhibit the highest average traffic flow, with the exception of Gates 0 and 3. These gates, located at the park boundaries and directly connected to only two other sites, are expected to experience lower traffic.
* Gates and ranger stops experience the lowest average traffic. This aligns with expectations, as only ranger vehicles are permitted to pass through gates and are more likely to visit ranger stops.

**TODO:** 
1. Add mean STD graph of cartypes.
2. Analyze traffic at each gate or of each cartype or selfloop traffic to see if they follow any standard distribution.
3. Add box plots of the said distributions


## Time Analysis of Traffic Flux


### Traffic Flux by Car Type

#### Aggregated over a day

![alt text](data/fig/traffic_flux_gate_over_day_for_each_cartype.png)

#### Aggregated over a week

![alt text](data/fig/traffic_flux_gate_over_week_for_each_cartype.png)

**Insights**

* Car types 1, 2, and 3 primarily visit during the period from 05-2015 to 10-2015, covering summer through mid-fall. As winter begins, traffic flux decreases, gradually picking up again in summer 2016.
* Car types 4, 5, and 6 follow a similar pattern with slightly less variation.
* The traffic movement of Ranger Car 2P remains relatively consistent throughout the year.

* The park encounters days where there is no recorded traffic for car types 4, 5, and 6. 

### Traffic Flux at each Gate

#### Aggregated over a day

![alt text](data/fig/traffic_flux_at_each_gate_over_day_for_each_gate.png)


#### Aggregated over a week

![alt text](data/fig/traffic_flux_at_each_gate_over_week.png)

**Insights**

* Traffic tends to increase between 5-15 and 10-15 (summer and fall) for all gate names except "gate" and "ranger-stop," but decreases from 10-15 to 5-16 (winter and spring), and then begins to rise again from 6-2016
* Traffic at "gate" and "ranger-stops" is more or less the same throughout the year.
* Gate 1 and 2, General gate 0, and all camping gates except Gate 8 experience days with no recorded traffic.
## Network Analysis

### Car Type 1

* Edge width shows number of cars passing
* Blue nodes are stop were car just passed 
* Green nodes are nodes were car have two consecutive readings 
* Intensity of green color represents average time between two consecutive readings.

![alt text](data/fig/DirectionalGraph.png)

**Insights**

* The busiest routes are typically between nodes General Gates 1, 2, 4, 7, and Ranger Stop 0, 2.
* Vehicles primarily stop at camping stops, with most popular sites 2,4,5, and 8.

## Route Analysis (Tree)

### Car Type 1


![alt text](data/fig/cartype1.png)

Found 3 paths that are longer the usual paths taken.

Below graph shows the car type 1 routes excludes the 3 paths mentioned above.

![alt text](data/fig/cartype1_without_analomy.png)

After analyzing the data we saw the those paths are only taken by 3 cars. (data stored in data/stayed_to_long folder.)

#### Anomaly

Three cars of type 1 have unusual behavior

| S.No|  Car id  |  Entry Time  | Exit Time  |  N Gates | N Entrance Gates  | Total Time | Notes |
|---|---|---|---|---|---|---|---|
|1| 20154112014114-381  | 2015-06-12 13:41:14  | 2015-07-26 23:00:51 | 98  | 14 | 44 days 09:19:37 | Entered and exited from entrance-0 seven times, but each time the car-id is same  |
|2| 20155705025759-63  | 2015-06-05 14:57:59  |  2016-05-20 14:43:07 |  70 | 1 | 349 days 23:45:08 | Entered from entrance-0 and never left |
|3|  20162904122951-717 | 2016-03-04 12:29:51  |  2016-04-10 22:14:22 | 36 | 12 | 37 days 09:44:31 |Entered and exited from entrance-3 six time, but each time the car-id is same |


Check the below graph for repeated behavior for (1) and (2) 

![alt text](<data/fig/cartype 1 _two analomy repeated behavoir  .png>)

### Car Type 2 

![alt text](data/fig/cartype2.png)

Found 1 path that is longer than usual paths.

Below graph shows the car type 2 routes excludes the 1 path mentioned above.

![alt text](data/fig/cartype2_without_analomy.png)

After analyzing the data we saw the that path is only taken by 1 car. (data stored in data/stayed_to_long folder.)

#### Anomaly

One car of type 2 have unusual behavior

|  Car id  |  Entry Time  | Exit Time  |  N Gates | N Entrance Gates  | Total Time | Notes |
|---|---|---|---|---|---|---|
| 20154519024544-322  | 2015-06-19 14:45:44  | 2015-10-05 00:36:54 | 281 | 32 | 107 days 09:51:10 | First Entered from Entrance-1 and exited from entrance-4.then Entered and exited from entrance-4 fifteen times, but each time the car-id is same  |

Please check the repeated behavior in below tree

![alt text](<data/fig/cartype 2 _ analomy_repeated behavoir.png>)

### Car Type 2P

![alt text](data/fig/cartype2P.png)

### Car Type 3

![alt text](data/fig/cartype3.png)

### Car Type 4

![alt text](data/fig/cartype4.png)

### Car Type 5

![alt text](data/fig/cartype5.png)

### Car Type 6

![alt text](data/fig/cartype6.png)

**Insights**

* Car types 5 and 6 traverse identical routes within the park. They have a total of 20 distinct paths. Paths have minimum of 2 gates and a maximum of 9 gates.


## Self Loop Analysis

Here, self loop means if any car has two consecutive entries at a same gate. The aim here is to see if cars spent time at a specific gate. If so, how much time. 

The Assumption: If the car has two consecutive readings at the same gate it will be considered to have spent time at that gate.

### Time spent at a site

#### Camping site

![alt text](data/fig/camping_distribution.png)

**Insights**

* Camping Site 1 is the least preferable for camping.
* Camping Sites 5, 8, and 2 are the most preferable options for camping.

#### Non Camping sites

![alt text](data/fig/non_camping_distribution.png)

### Heat Map 

#### Camping sites aggregated over a month

The value in each entry is 
$$\frac{\text{Total time spent by cars at that site in that month}}{\text{Total cars who stayed at that site on that month}}$$
The color of each entry represent Total cars who stayed at that gate on that month.

* Note: Total cars recorded at a site is different from total cars that stayed at the site.

![alt text](data/fig/heatmap.png)

**Insights**

* Typically, car types 1, 2, and 3 make stops at camping sites.
* Car types 4, 5, and 6 never halt at camping sites.
* Few cars visit camping site 1.
* During June, July, August, and September, the highest number of cars visit camping sites.
* From November to February, there are almost no cars visiting the camping sites.
* The average time spent at camping sites generally mirrors this pattern. Therefore, there is plenty of space available for camping visitors at each site.

## Analysing Ground Truth

**Car type 4 passes ranger gates 3, 5 and 6. see below graph for traffic flux over time.**

![alt text](data/fig/analomy_of_cartype_4_for_ranger_gates.png)

**This Car always follows the same route. See below graph**

![alt text](data/fig/analomy_route.png)



## A Time of Day and Day of Week  Analysis of Traffic.

The day is segmented into six equal parts based on the specified times below.

Morning $\implies (6,10]$

Midday $\implies (10,14] $

Evening $\implies (14,18] $

Night $\implies (18,22]$

Midday $\implies (22,2]$

Dawn $\implies (2,6]$

Week is diveded into 2 parts as shown below

Weekend $\implies$ Sat, Sun.

Weekdays $\implies$ Mon, Tue, Wed, Thu, Fri.


## Percenage analysis 

### Time of Day

![alt text](data/fig/pie_chart_time_of_day.png)

**Insights**

* Car Types 1, 2, 2P, and 3 experience peak traffic during the morning, midday, and evening hours.

* In contrast, Car Types 4, 5, and 6 exhibit a relatively even distribution of traffic across both day and night, with a slight increase in vehicles during nighttime

### Day of Week

![alt text](data/fig/pie_chart_day_of_week.png)

**Insights**
* For all car types, weekend traffic accounts for approximately 30% of the total.


## Animation

**In progress**

## Barchart

An animated display featuring cars at various entrances, progressing with each timestamp to visualize data on an hourly basis.

click [here](https://github.com/Visual-Analytics-2024/VA-Project/blob/wajid/Python/Notebooks/bar_animation.html) to see the animation

## Network Animation

Animation showing traffic at each gate and on each route, progressing with each timestamp to visualize data on an hourly basis.

click [here](https://drive.google.com/file/d/1SzFCRIM_3UDFgFW9gq8X9iDZruyGLkE8/view?usp=sharing) to see the animation.


## TODO
1. Treat traffic a each gate for a particular car a time series (time aggregated over hour, count of cars at that gate as value) and apply ETS-Decomposition to check for trend and seasonality. 












