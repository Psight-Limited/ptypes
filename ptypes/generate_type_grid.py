from tabulate import tabulate
from ptypes import \
    ESTJ, ESTP, ENTJ, ENFJ, ESFJ, ESFP, ENTP, ENFP, \
    ISTJ, ISTP, INTJ, INFJ, ISFJ, ISFP, INTP, INFP


def generate_type_grid(table):
    """Input a 2D array of types and generate a type grid.

    ```
    with open("TypeGrid.txt", "w") as f:
        f.write(generate_type_grid([
            [ESTJ, ESTP, ENTJ, ENFJ],
            [ESFJ, ESFP, ENTP, ENFP],
            [ISTJ, ISTP, INTJ, INFJ],
            [ISFJ, ISFP, INTP, INFP],]))
    ```"""
    row_attributes = []
    for row in table:
        row_part = []
        for attribute in row[0].get_attributes():
            if all(attribute in other.get_attributes() for other in row):
                row_part.append(attribute)
        row_attributes.append(row_part)
    column_attributes = []
    for column in zip(*table):
        column_part = []
        for attribute in column[0].get_attributes():
            if all(attribute in other.get_attributes() for other in column):
                column_part.append(attribute)
        column_attributes.append(column_part)
    final_table = []
    for i, row in enumerate(table):
        final_table.append(row + row_attributes[i])
    for i in range(max(len(x) for x in column_attributes)):
        new_row = []
        for column in column_attributes:
            try:
                new_row.append(column[i])
            except IndexError:
                new_row.append("")
        final_table.append(new_row)
    return tabulate(final_table, tablefmt="outline")


def main():
    with open("TypeGrid.txt", "w") as f:
        f.write(generate_type_grid([
            [ESTJ, ESTP, ENTJ, ENFJ],
            [ESFJ, ESFP, ENTP, ENFP],
            [ISTJ, ISTP, INTJ, INFJ],
            [ISFJ, ISFP, INTP, INFP],]))


if __name__ == "__main__":
    main()
