# coding: utf-8
from __future__ import unicode_literals
import sys
import tempfile
import webbrowser

import pygraphviz as pgv


def chese(frame=None, slient=False):

    if frame is None:
        frame = sys._getframe().f_back

    G = pgv.AGraph(strict=False, directed=True)

    stack = []

    node_set = set()
    subgraph_set = {}

    while frame:
        filename = frame.f_code.co_filename
        firstlineno = frame.f_code.co_firstlineno
        function = frame.f_code.co_name

        node = '{}:{}:{}'.format(filename, firstlineno, function)
        if node not in node_set:
            node_set.add(node)
            if filename not in subgraph_set:
                subgraph_set[filename] = G.add_subgraph(
                    name='cluster' + filename,
                    label=filename
                )

            subgraph = subgraph_set[filename]
            subgraph.add_node(
                node,
                label='{}:{}'.format(firstlineno, function)
            )
        stack.append(frame)
        frame = frame.f_back

    stack.reverse()

    stack_size = len(stack)
    for index, start in enumerate(stack):
        if index + 1 < stack_size:
            start_filename = start.f_code.co_filename
            start_firstlineno = start.f_code.co_firstlineno
            start_function = start.f_code.co_name
            start_lineno = start.f_lineno
            start_subgraph = subgraph_set[start_filename]

            end = stack[index+1]
            end_filename = end.f_code.co_filename
            end_firstlineno = end.f_code.co_firstlineno
            end_function = end.f_code.co_name
            end_subgraph = subgraph_set[end_filename]

            if index == 0:
                color = 'green'
            elif index == stack_size - 2:
                color = 'red'
            else:
                color = 'black'

            G.add_edge(
                '{}:{}:{}'.format(start_filename,
                                  start_firstlineno,
                                  start_function),
                '{}:{}:{}'.format(end_filename,
                                  end_firstlineno,
                                  end_function),
                color=color,
                ltail=start_subgraph.name,
                lhead=end_subgraph.name,
                label='#{} at {}'.format(index+1, start_lineno)
            )

    fd, name = tempfile.mkstemp('.png')
    G.draw(name, prog='dot')
    G.close()

    if not slient:
        webbrowser.open('file://' + name)

    return name
