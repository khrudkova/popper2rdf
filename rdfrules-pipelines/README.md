# popper2rdf evaluation experiments
# 1. numeric-zendo1
- dataset [source](https://github.com/celinehocquette/numsynth-aaai23/tree/main/numsynth/examples/numeric-zendo1)
- dataset contains 60 examples, 30 positive and 30 negative

Zendo is a game of inductive logic, where one player invents a rule that the rest of the players try to figure out by creating configurations of the game pieces. The winning condition is to correctly induce the rule. The pieces are of several colors, and shapes and can be in various positions, have various sizes, can be in contact or not, and so on. 

An example of Prolog atoms in dataset:
```
piece(0, p0_0).
position(p0_0, 9.05, 5.6).
size(p0_0, 3.14).
color(p0_0, red).
orientation(p0_0, lhs).
rotation(p0_0, 0.89).
```
The same data as RDF triples:
```
<0> <piece> <p0_0> .
<http://vseILPconvertor/position(p0_0,9.05,5.6).> <position_p1> <p0_0> .
<http://vseILPconvertor/position(p0_0,9.05,5.6).> <position_p2> "9.05"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://vseILPconvertor/position(p0_0,9.05,5.6).> <position_p3> "5.6"^^<http://www.w3.org/2001/XMLSchema#double> .
<p0_0> <size> "3.14"^^<http://www.w3.org/2001/XMLSchema#double> .
<p0_0> <color> <red> .
<p0_0> <orientation> <lhs> .
<p0_0> <rotation> "0.89"^^<http://www.w3.org/2001/XMLSchema#double> .
```
To obtain KG from the Prolog atoms, run `popper2rdf` or load the pipeline - the transformed dataset should be loaded into pipeline. To load pipeline, download the `task-numeric-zendo1-rules.json` pipeline to mine rules and `task-numeric-zendo1-eval.json` pipeline, to get the evaluation results, go to [RDFRules GUI](https://rdfrules.vse.cz/index.html), select _create a new pipeline_ and _load pipeline from a local file_ in the right upper corner. Load the downloaded `.json` files.
## 1.1. Mining rules
### 1.1.1. Load `-rules` pipeline
Download the `task-numeric-zendo1-rules.json` pipeline and load it to RDFRules. When loaded, the pipeline should look like this:

<img src="https://github.com/user-attachments/assets/47524c05-319b-4985-8cd8-505d487f604e" width="400" height="800"></img>

By clicking the arrows between nodes, it is possible to add new nodes. It is also possible to remove existing nodes.
### 1.1.2. Setting the parameters
By clicking on the individual nodes, it is possible to set the parameters for rule mining.

For this pipeline, following settings are used:
| Parameter             | Setting                                         |
|-----------------------|-------------------------------------------------|
| Discretize            | Settings in Table \ref{tab:zendo1-rdfrules-disc} |
| Maximun rule length   | 5                                               |
| Minimum head size     | 2                                               |
| Minimum head coverage | 0.35                                            |
| Timeout               | 5                                               |
| Patterns              | \* => (? <zendo> true) |
| CWA confidence        | 0.5                                             |
| Sort                  | CWA confidence                                  |
| Pruning               | Data coverage pruning                           |

Since dataset **numeric-zendo1** contains numerical values, we need to discretize the numerical values first to create intervals. RDFRules provides an option for discretization. The settings used to discretize the dataset in this example are as follows:
| Parameter             | Setting |
|-----------------------|---------|
| Minimum head size     | 2       |
| Minimum head coverage | 0.01    |
| Maximum rule length   | 5       |

Under these settings, RDFRules returns three rules.
### 1.1.3. Mined rules
**Rule 1** produced by RDFRules on **numeric-zendo1** dataset states that _winning condition for a zendo game A is when there is a piece B in a game A, piece B is in contact with piece C and piece C has size between 4,945 and 9,94_.
```
( ?c <size#discretized_level_1> [ 4.945 ; 9.94 ] ) ∧ ( ?c <contact> ?b ) ∧ ( ?a <piece> ?b ) ⇒ ( ?a <zendo> true )
```
**Rule 2** produced by RDFRules on **numeric-zendo1** dataset states that _winning condition for a zendo game A is when there is a piece B in a game A, piece B is in contact with piece C where piece C has position\_p1 D with first coordinate value position\_p2 between 0.04 and 5.055_.
```
( ?d <position_p2#discretized_level_1> [ 0.04 ; 5.055 ) ) ∧ ( ?d <position_p1> ?c ) ∧ ( ?c <contact> ?b ) ∧ ( ?a <piece> ?b ) ⇒ ( ?a <zendo> true )
```
**Rule 3** produced by RDFRules on **numeric-zendo1** dataset states that _winning condition for a zendo game A is when there is a piece B in a game A, piece B is in contact with piece C where piece C has an angle of rotation between 3,2199 and 6,24 and the color of piece C is red_.
```
( ?c <color> <red> ) ∧ ( ?c <rotation#discretized_level_1> [ 3.2199999999999998 ; 6.24 ] ) ∧ ( ?b <contact> ?c ) ∧ ( ?a <piece> ?b ) ⇒ ( ?a <zendo> true )
```
## 1.2. Evaluation
Download the `task-numeric-zendo1-eval.json` pipeline and load it to RDFRules. When loaded, the pipeline should look like this:

<img src="https://github.com/user-attachments/assets/f45e44ab-f114-4cac-8b78-6b179f8e0d8e" width="380" height="800"></img>

By clicking the arrows between nodes, it is possible to add new nodes. It is also possible to remove existing nodes.
The result of the run of this pipeline is table containing following confusion matrix:

|                 | In KG     | Not in KG |
|-----------------|-----------|-----------|
| Predicted       | 58        | 2         |
| Not predicted   | 2        |           |

Included in the output are also calculations of the following metrics:
| |          |
|--------------------|----------|
| Total entities (E) | 60       |
| TP                 | 58       |
| Precision          | 96.67%   |
| Recall             | 96.67%   |
| F-Measure          | 96.67%   |

The ruleset produced by RDFRules successfully covers all 30 positive examples.
### 1.2.1. Qualitative evaluation of solution similarity
The Popper solution, which is the information we want to extract from RDFRules have been produced by [numsynth-aaai23 branch of Popper](https://github.com/celinehocquette/numsynth-aaai23/tree/main). The solution was produced on unchanged dataset and is as follows:
```
********** SOLUTION **********
Precision:1.00 Recall:1.00 TP:30 FN:0 TN:30 FP:0 Size:5
zendo(A):- piece(A,B),contact(B,C),size(C,D),geq(D,4.12).
******************************
```
RDFRules produced three rules, where **Rule 1** is almost identical to Popper results with only small differences in numerical values caused by discretization. Based on Principle 1 and 2, the solutions are therefore considered as _similar_.
