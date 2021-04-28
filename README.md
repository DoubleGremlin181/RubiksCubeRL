# RubiksCubeRL
### Solving Twisty Puzzles with Reinforcement Learning(Parallel Q-Learning)
____

![Python Version](https://img.shields.io/badge/python->=3.8-blue)
![GitHub](https://img.shields.io/github/license/DoubleGremlin181/RubiksCubeRL)
![OS](https://img.shields.io/badge/platform-linux%20%7C%20windows-lightgrey)

## Instructions
* Install requirements
* Create a Q-Table by running `pql.py` on Linux or `pql-windows.py` on Windows.
* [Download](https://www.worldcubeassociation.org/results/misc/export.html) and unzip the WCA results TSV dataset
* Run `scrambles_extractor.py` to extract the scrambles to a csv
* Run `validator.py` to track the performance of your agent on official WCA scrambles
* (Optional) Solve any scramble via `solver.py`

## Results

### 2x2 Pocket Rubiks Cube

| Size of validation set | Average reward | Success rate | Average number of moves | Method | Training Size |
|------------------------|----------------|--------------|-------------------------|--------|---------------|
| 10000                  | -86.1917       | 49.89        | 136.5806                | lbl    | 2000000       |
| 10000                  | -31.9635       | 66.9         | 99.5325                 | none   | 2000000       |
| 10000                  | -188.8264      | 18.48        | 207.4912                | ortega | 2000000       |
| 10000                  | 32.4786        | 85.26        | 53.634                  | lbl    | 3000000       |
| 10000                  | 79.5309        | 99.8         | 21.2671                 | none   | 3000000       |
| 10000                  | -54.1187       | 53.18        | 127.4008                | ortega | 3000000       |
| 10000                  | 77.5661        | 98.12        | 21.5351                 | lbl    | 5000000       |
| 10000                  | 83.681         | 100          | 17.319                  | none   | 5000000       |
| 10000                  | 31.9869        | 84.53        | 53.3884                 | ortega | 5000000       |
| 10000                  | 84.2557        | 99.77        | 16.512                  | lbl    | 7500000       |
| 10000                  | 85.1919        | 100          | 15.8081                 | none   | 7500000       |
| 10000                  | 81.5391        | 99.09        | 18.5418                 | ortega | 7500000       |
| 10000                  | 85.5475        | 100          | 15.4525                 | lbl    | 10000000      |
| 10000                  | 85.5908        | 100          | 15.4092                 | none   | 10000000      |
| 10000                  | 85.2556        | 99.95        | 15.6939                 | ortega | 10000000      |

### Pyraminx
| Size of validation set | Average reward | Success rate | Average number of moves | Method | Training Size |
|------------------------|----------------|--------------|-------------------------|--------|---------------|
| 10000                  | -221.2995      | 8.54         | 229.9249                | lbl    | 500000        |
| 10000                  | -142.075       | 32.68        | 175.0818                | none   | 500000        |
| 10000                  | -235.6532      | 4.25         | 239.9457                | lbl    | 600000        |
| 10000                  | 15.0487        | 80.6         | 66.3573                 | none   | 600000        |
| 10000                  | -153.2174      | 28.78        | 182.2852                | lbl    | 700000        |
| 10000                  | 73.6991        | 97.52        | 24.7961                 | none   | 700000        |
| 10000                  | -182.2324      | 20.06        | 202.493                 | lbl    | 800000        |
| 10000                  | 82.0213        | 99.62        | 18.5949                 | none   | 800000        |
| 10000                  | -240.883       | 2.68         | 243.5898                | lbl    | 900000        |
| 10000                  | 84.6026        | 99.97        | 16.3671                 | none   | 900000        |
| 10000                  | -122.8171      | 37.63        | 160.8234                | lbl    | 1000000       |
| 10000                  | 85.615         | 100          | 15.385                  | none   | 1000000       |
| 10000                  | -39.7088       | 62.08        | 102.4096                | lbl    | 1500000       |
| 10000                  | 87.6315        | 100          | 13.3685                 | none   | 1500000       |
| 10000                  | 51.072         | 88.77        | 38.5857                 | lbl    | 2500000       |
| 10000                  | 89.3179        | 100          | 11.6821                 | none   | 2500000       |

### Skewb
| Size of validation set | Average reward | Success rate | Average number of moves | Method | Training Size |
|------------------------|----------------|--------------|-------------------------|--------|---------------|
| 10000                  | -72.3876       | 54.91        | 127.8467                | none   | 2000000       |
| 10000                  | -222.4332      | 8.25         | 230.7657                | sarah  | 2000000       |
| 10000                  | 81.9239        | 99.88        | 18.9549                 | none   | 3000000       |
| 10000                  | -125.7149      | 37.21        | 163.297                 | sarah  | 3000000       |
| 10000                  | 86.4634        | 100          | 14.5366                 | none   | 5000000       |
| 10000                  | 83.4465        | 99.18        | 16.7253                 | sarah  | 5000000       |
| 10000                  | 88.1116        | 100          | 12.8884                 | none   | 7500000       |
| 10000                  | 87.7215        | 99.89        | 13.1674                 | sarah  | 7500000       |
| 10000                  | 88.7571        | 100          | 12.2429                 | none   | 10000000      |
| 10000                  | 88.712         | 100          | 12.288                  | sarah  | 10000000      |

