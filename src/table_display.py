def _print_border(left_corner, middle_sep, right_corner, col_widths):
    """Print a table border with specified corners and separators"""
    separator = middle_sep.join("═" * (w + 2) for w in col_widths)
    print(f"{left_corner}═════{middle_sep}{separator}{right_corner}")


def _print_cells(cell_texts, col_widths, is_last_column_check):
    """Print a row of cells with proper formatting and separators"""
    for i, (text, width) in enumerate(zip(cell_texts, col_widths)):
        truncated_text = text[:width] if text else ""
        print(f" {truncated_text:<{width}} ", end="")
        if not is_last_column_check(i):
            print("║", end="")
    print("║")


def print_table(headers, rows, max_rows=2, max_col_width=40):
    """
    Print a formatted table similar to Google Sheets view

    Args:
        headers: List of column headers
        rows: List of rows (each row is a list of values)
        max_rows: Maximum number of data rows to display
        max_col_width: Maximum width for each column
    """
    # Input validation
    if not headers:
        return

    # Limit to max_rows
    display_rows = rows[:max_rows] if rows else []

    # Process all cells once and cache - single pass for efficiency
    processed_rows = []
    col_widths = [len(str(h)) for h in headers]

    for row in display_rows:
        processed_row = []
        for i in range(len(headers)):
            if i < len(row):
                cell_lines = str(row[i]).split('\n')
            else:
                cell_lines = ['']

            processed_row.append(cell_lines)

            # Update column width based on content
            if cell_lines:
                max_line_len = max(len(line) for line in cell_lines)
                col_widths[i] = max(col_widths[i], max_line_len)

        processed_rows.append(processed_row)

    # Cap column widths at maximum
    col_widths = [min(w, max_col_width) for w in col_widths]

    # Helper for checking last column
    is_last_col = lambda i: i >= len(headers) - 1

    # Print top border
    _print_border("╔", "╦", "╗", col_widths)

    # Print header row
    print("║ Row ║", end="")
    header_texts = [str(h) for h in headers]
    _print_cells(header_texts, col_widths, is_last_col)

    # Print header separator
    _print_border("╠", "╬", "╣", col_widths)

    # Print data rows
    for row_idx, processed_row in enumerate(processed_rows, 1):
        # Determine max lines in this row
        max_lines = max((len(cell_lines) for cell_lines in processed_row), default=1)

        # Print each line of the row
        for line_idx in range(max_lines):
            # Print row number on first line, blank on subsequent lines
            if line_idx == 0:
                print(f"║ {row_idx:3} ║", end="")
            else:
                print("║     ║", end="")

            # Extract text for this line from each cell
            cell_texts = []
            for cell_lines in processed_row:
                if line_idx < len(cell_lines):
                    cell_texts.append(cell_lines[line_idx])
                else:
                    cell_texts.append('')

            _print_cells(cell_texts, col_widths, is_last_col)

        # Print row separator (except after last row)
        if row_idx < len(processed_rows):
            _print_border("╠", "╬", "╣", col_widths)

    # Print bottom border
    _print_border("╚", "╩", "╝", col_widths)
