from django.core.management.base import BaseCommand
import pandas as pd
from quizapp.models import MCQ
import ast

class Command(BaseCommand):
    help = 'Import MCQs from CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = 'results/mcq_data_1.1.csv'  # Adjust if the path is different

        df = pd.read_csv(csv_file_path)

        for _, row in df.iterrows():
            if pd.isna(row['question']).strip()=='' or row['options']=='[]':
                continue       #skips empty and invalid rows

            # Handle the 'options' column which is stored as string like "['A', 'B', 'C', 'D']"
            options = ast.literal_eval(row['options']) if row['options'] != '[]' else []

            MCQ.objects.create(
                question=row['question'],
                options=options,
                answer=row['answer'],
                explanation=row['explanation'],
                topic=row['topic'],
                difficulty=row['difficulty'],
                chapter=row['chapter']
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {len(df)} MCQs"))
