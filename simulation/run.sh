################## YAHOO TRACES ###########################
# Hawk
pypy simulation_main.py YH.tr yes yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 8000 no 0 2 no Hawk
# Sparrow
pypy simulation_main.py YH.tr no no 90.5811 90.5811 100 100 1 2 5 MEAN 0 0 ATC 10000 10 8000 no 0 2 no Hawk
# Eagle
pypy simulation_main.py YH.tr no yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 8000 yes 0 20 yes Eagle
# Ideal Eagle
pypy simulation_main.py YH.tr no yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 8000 no 0 20 yes IdealEagle
# LWL with Partitioning
pypy simulation_main.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 8000 no 0 2 no CLWL
# DLWL with Partitioning and SRPT
pypy simulation_main.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 8000 yes 8 2 no DLWL
# Murmuration with resource heartbeats generated as required, and all jobs
# considered long, and scheduled in a centralized way 
pypy simulation_main.py YH.tr no yes -1 90.5811 100 100 1 2 5 MEAN 0 0 ATC 10000 10 8000 yes 0 2 no Murmuration
