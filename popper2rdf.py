import re
from rdflib import Graph, Literal, RDF, URIRef, Namespace

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def popper2rdf(dataset_name,
               input_path='',
               output_path='',
               universal_predicate_1='has_property',
               subject_prefix='http://vseILPconvertor/',
               predicate_suffix='_p%d',
               remove_spaces=True,
               negation_prefix='not_',
               subject_true=True,
               subject_false=False):
    """
    Method for converting Popper Prolog files to N-Triples.
    :param dataset_name: name of the folder, where BK and examples are located
    :param input_path: path to the input files
    :param output_path: destination for the output file
    :param universal_predicate_1: universal predicate for atoms with arity = 1
    :param subject_prefix: prefix for artificial subject for atoms where arity > 2
    :param predicate_suffix: prefix for predicates for atoms where arity > 2
    :param remove_spaces: optional removal of spaces in text
    :param negation_prefix: prefix for predicates of negative examples with arity = 2
    :param subject_true: value that should be assigned to positive examples with arity = 1
    :param subject_false: value that should be assigned to negative examples with arity = 1
    :return: N-Triples file
    """

    if input_path is None:
        input_path = ''
    if len(input_path) > 0 and not input_path.endswith('/'):
        input_path += '/'

    if output_path is None:
        output_path = ''
    if len(output_path) > 0 and not output_path.endswith('/'):
        output_path += '/'

    bias_file = f'{input_path}{dataset_name}/bias.pl'
    bk_file = f'{input_path}{dataset_name}/bk.pl'
    exs_file = f'{input_path}{dataset_name}/exs.pl'

    graph_bk = Graph()

    bk_pattern = re.compile(r'^(\w+)\((.+)\)\.$')

    with open(bk_file, 'r') as f:
        for line in f:
            match = bk_pattern.match(line)
            if match:
                predicate = match.group(1)
                reduced_triple = match.group(2).split(',')
                reduced_triple = [s.strip() for s in reduced_triple]

                if len(reduced_triple) == 1:
                    graph_bk.add((URIRef(reduced_triple[0]), URIRef(universal_predicate_1), URIRef(predicate)))

                elif len(reduced_triple) == 2:
                    if is_integer(reduced_triple[1]):
                        graph_bk.add((URIRef(reduced_triple[0]), URIRef(predicate), Literal(int(reduced_triple[1]))))
                    elif is_float(reduced_triple[1]):
                        graph_bk.add((URIRef(reduced_triple[0]), URIRef(predicate), Literal(float(reduced_triple[1]))))
                    else:
                        graph_bk.add((URIRef(reduced_triple[0]), URIRef(predicate), URIRef(reduced_triple[1])))

                else:
                    subj = subject_prefix + match.group(0)
                    if remove_spaces: subj = subj.replace(' ', '')
                    pred = predicate + predicate_suffix
                    # TODO: for now predicates are numbered from 1 (later will be configurable)
                    for i in range(len(reduced_triple)):
                        if is_integer(reduced_triple[i]):
                            graph_bk.add((URIRef(subj), URIRef(pred % (i + 1)), Literal(int(reduced_triple[i]))))
                        elif is_float(reduced_triple[i]):
                            graph_bk.add((URIRef(subj), URIRef(pred % (i + 1)), Literal(float(reduced_triple[i]))))
                        else:
                            graph_bk.add((URIRef(subj), URIRef(pred % (i + 1)), URIRef(reduced_triple[i])))

    graph_exs = Graph()

    exs_pattern = re.compile('(pos|neg)\((\w+)\((.+)\)\)\.')

    with open(exs_file, 'r') as f:
        for line in f:
            match = exs_pattern.match(line)
            if match:
                positive = match.group(1) == 'pos'
                predicate = match.group(2)
                reduced_triple = match.group(3).split(',')
                reduced_triple = [s.strip() for s in reduced_triple]

                if len(reduced_triple) == 1:
                    if positive:
                        graph_exs.add((URIRef(reduced_triple[0]), URIRef(predicate), Literal(subject_true)))
                    else:
                        graph_exs.add((URIRef(reduced_triple[0]), URIRef(predicate), Literal(subject_false)))

                elif len(reduced_triple) == 2:
                    if is_integer(reduced_triple[1]):
                        obj = Literal(int(reduced_triple[1]))
                    elif is_float(reduced_triple[1]):
                        obj = Literal(float(reduced_triple[1]))
                    else:
                        obj = URIRef(reduced_triple[1])
                    if positive:
                        graph_exs.add((URIRef(reduced_triple[0]), URIRef(predicate), obj))
                    else:
                        graph_exs.add((URIRef(reduced_triple[0]), URIRef(negation_prefix + predicate), obj))

                else:
                    subj = subject_prefix + match.group(0)
                    if remove_spaces: subj = subj.replace(' ', '')
                    if positive:
                        pred = predicate + negation_prefix
                    else:
                        pred = negation_prefix + predicate + negation_prefix
                    # TODO: for now predicates are numbered from 1 (later will be configurable)
                    for i in range(len(reduced_triple)):
                        if is_integer(reduced_triple[i]):
                            graph_exs.add((URIRef(subj), URIRef(pred % (i + 1)), Literal(int(reduced_triple[i]))))
                        elif is_float(reduced_triple[i]):
                            graph_exs.add((URIRef(subj), URIRef(pred % (i + 1)), Literal(float(reduced_triple[i]))))
                        else:
                            graph_exs.add((URIRef(subj), URIRef(pred % (i + 1)), URIRef(reduced_triple[i])))

    result = graph_bk + graph_exs
    result.serialize(format='nt', destination=f'{output_path}{dataset_name}.nt', encoding='utf-8')
