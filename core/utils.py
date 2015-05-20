import queue
import collections


def make_inner_paths_for_table(selected_table, tables, relationships):
    q = queue.deque([(selected_table, ())])
    used_tables = set()
    paths = []
    while q:
        table_name, table_tree_path = q.popleft()
        used_tables.add(table_name)

        columns = tables[table_name].columns
        relations = relationships.get(table_name, [])

        for x in columns:
            table_tree_full_path = table_tree_path + (x, )
            paths.append(table_tree_full_path)

        for x in relations:
            relation_table = x.relation_table
            visited = {r.table for r in table_tree_path}
            if relation_table not in visited:
                q.append((relation_table, table_tree_path + (x, )))

    return paths, used_tables
