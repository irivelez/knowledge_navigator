import sqlite3
from tabulate import tabulate

def view_stored_articles():
    with sqlite3.connect('knowledge.db') as conn:
        cursor = conn.execute('''
            SELECT 
                title,
                substr(summary, 1, 100) as summary_preview,
                key_concepts,
                processed_date
            FROM articles
            ORDER BY processed_date DESC
            LIMIT 5
        ''')
        
        rows = cursor.fetchall()
        headers = ['Title', 'Summary Preview', 'Key Concepts', 'Processed Date']
        
        # Format the output
        formatted_rows = []
        for row in rows:
            formatted_row = list(row)
            formatted_row[1] = formatted_row[1] + "..."  # Add ellipsis to summary preview
            formatted_rows.append(formatted_row)
            
        print(tabulate(formatted_rows, headers=headers, tablefmt='grid'))

if __name__ == "__main__":
    view_stored_articles()
