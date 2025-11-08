def print_table(headers, rows, max_rows=2, max_col_width=40):
    """
    Print a formatted table similar to Google Sheets view

    Args:
        headers: List of column headers
        rows: List of rows (each row is a list of values)
        max_rows: Maximum number of data rows to display
        max_col_width: Maximum width for each column
    """
    # Limit to max_rows
    display_rows = rows[:max_rows]

    # Calculate column widths
    col_widths = []
    for i, header in enumerate(headers):
        max_width = len(str(header))
        for row in display_rows:
            if i < len(row):
                # Handle multi-line cells
                cell_value = str(row[i])
                lines = cell_value.split('\n')
                max_line_length = max(len(line) for line in lines) if lines else 0
                max_width = max(max_width, max_line_length)
        # Cap at max_col_width
        col_widths.append(min(max_width, max_col_width))

    # Print top border
    print("╔═════╦" + "╦".join("═" * (w + 2) for w in col_widths) + "╗")

    # Print header row
    print("║ Row ║", end="")
    for i, (header, width) in enumerate(zip(headers, col_widths)):
        header_text = str(header)[:width]
        print(f" {header_text:<{width}} ", end="")
        if i < len(headers) - 1:
            print("║", end="")
    print("║")

    # Print header separator
    print("╠═════╬" + "╬".join("═" * (w + 2) for w in col_widths) + "╣")

    # Print data rows
    for row_idx, row in enumerate(display_rows, 1):
        # Handle multi-line cells
        cell_lines = []
        max_lines = 1

        for i, width in enumerate(col_widths):
            if i < len(row):
                cell_value = str(row[i])
                lines = cell_value.split('\n')
                cell_lines.append(lines)
                max_lines = max(max_lines, len(lines))
            else:
                cell_lines.append([''])

        # Print each line of the row
        for line_idx in range(max_lines):
            if line_idx == 0:
                print(f"║ {row_idx:3} ║", end="")
            else:
                print("║     ║", end="")

            for i, (lines, width) in enumerate(zip(cell_lines, col_widths)):
                if line_idx < len(lines):
                    line_text = lines[line_idx][:width]
                    print(f" {line_text:<{width}} ", end="")
                else:
                    print(f" {'':<{width}} ", end="")

                if i < len(col_widths) - 1:
                    print("║", end="")
            print("║")

        # Print row separator (except for last row)
        if row_idx < len(display_rows):
            print("╠═════╬" + "╬".join("═" * (w + 2) for w in col_widths) + "╣")

    # Print bottom border
    print("╚═════╩" + "╩".join("═" * (w + 2) for w in col_widths) + "╝")
