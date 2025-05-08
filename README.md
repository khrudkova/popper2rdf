# popper2rdf
## Package overview
This package contains method for converting the datasets used by the ILP system [Popper](https://github.com/logic-and-learning-lab/Popper) to RDF. The serialization format currently supported is N-Triples.
To create an RDF graph and to serialize it into the file we use the `rdflib` package. The library handles the automatic annotation of literals in the output.
## Dependencies
- rdflib
## Input
- `bk.pl`
- `exs.pl`
## Output
- `.nt` file containing converted triples from BK and examples
## Conversion
The table displays converting strategy used by `popper2rdf` converter. The data from the example are from the [numeric-zendo2](https://github.com/celinehocquette/numsynth-aaai23/tree/main/numsynth/examples/numeric-zendo2) dataset.
Converter can process atom with any arity. For arity >= 3 the reification is used, as shown in the third row.

| Popper atom               | popper2rdf conversion                                                                                                                                                                                                                                              |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pos(zendo(0)).            | \<0\> \<zendo\> "true" .                                                                                                                                                                                                                                           |
| piece(0,p0_0).            | \<0\> \<piece\> \<p0_0\> .                                                                                                                                                                                                                                         |
| position(p0_0,4.11,3.77). | \<http\:\/\/vseILPconvertor\/position\(p0_0,4.11,3.77\).\> \<position_p1\> \<p0_0\> .  \<http\:\/\/vseILPconvertor\/position\(p0_0,4.11,3.77\).\> \<position_p2\> "4.11"\> .  \<http:\/\/vseILPconvertor\/position\(p0_0,4.11,3.77\).\> \<position_p3\> "3.77"\> . |

## Example
This example is also covered in `popper2rdf_usage.ipynb`.
**popper2rdf** has some input parameters, which can are configurable to customize the output. Most of them have default values.
- dataset_name
    - name of the folder, where BK and examples are located, the same name is used for the output file
- input_path: current directory
    - path, to where the input files are located ! minus the folder = dataset name
- output_path: current directory
    - destination for the output file
- universal_predicate_1: has_property
    - universal predicate for atoms with arity = 1
- subject_prefix: http://vseILPconvertor/
    - prefix for artificial subject for atoms where arity > 2 (reification)
- predicate_suffix: _p%d
    - prefix for predicates for atoms where arity > 2
- remove_spaces: True
    - optional removal of spaces in text
- negation_prefix: not_
    - prefix for predicates of negative examples for atoms with arity = 2
- subject_true: True
    - value that should be assigned to positive examples with arity = 1
    - by default boolean literals 
- subject_false: False
    - value that should be assigned to negative examples with arity = 1
    - by default boolean literals

The converter only needs user to pass the path to the **folder**, in which the `bk.pl` and `exs.pl` are located, and the **name** of the folder in which the `bk.pl` and `exs.pl` are located.
This code converts the data, which folder is in the current directory, and creates the output KG in the current directory.
```  
input_files_path = ''
dataset_name = 'data'
popper2rdf(dataset_name, input_files_path)
```
